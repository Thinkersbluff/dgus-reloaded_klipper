""" Support for DGUS T5UID1 touchscreens"""
#
# NOTE: Design intent was one class per screen type

# Copyright (C) 2020  Desuuuu <contact@desuuuu.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging
import math# math library is not used. Consider removing this import.
import os
import struct
import textwrap
import jinja2
import mcu
from . import var, page, routine, dgus_reloaded
from .. import gcode_macro, heaters

T5UID1_firmware_cfg = {
    'dgus_reloaded': dgus_reloaded.configuration
}

DEFAULT_VOLUME     = 75
DEFAULT_BRIGHTNESS = 100
DEFAULT_INSET      = 30.0

T5UID1_CMD_WRITEVAR = 0x82
T5UID1_CMD_READVAR  = 0x83

T5UID1_ADDR_VERSION    = 0x0f
T5UID1_ADDR_BRIGHTNESS = 0x82
T5UID1_ADDR_PAGE       = 0x84
T5UID1_ADDR_SOUND      = 0xa0
T5UID1_ADDR_VOLUME     = 0xa1
T5UID1_ADDR_CONTROL    = 0xb0

TIMEOUT_SECS = 15
CMD_DELAY = 0.02

# Define the T5L control codes per the DWIN T5L Application Guide
# for inclusion in the applicable messages transmitted to the TFT
CONTROL_TYPES = {
    'variable_data_input': 0x00,
    'popup_window':        0x01,
    'incremental_adjust':  0x02,
    'slider_adjust':       0x03,
    'rtc_settings':        0x04,
    'return_key_code':     0x05,
    'text_input':          0x06,
    'firmware_settings':   0x07
}

def map_value_range(x, in_min, in_max, out_min, out_max):
    """Function to map an input value to an output value"""
    return int(round((x - in_min)
                     * (out_max - out_min)
                     // (in_max - in_min)
                     + out_min))
def get_duration(secs):
    """Build string variable reporting 'printtime so far' in days, hours, minutes, and seconds."""
    if not isinstance(secs, int):
        secs = int(secs)
    if secs < 0:
        secs = 0

    mins, secs = divmod(secs, 60)
    hrs, mins = divmod(mins, 60)
    dys, hrs = divmod(hrs, 24)
    dys %= 365

    parts = []
    if dys:
        parts.append(f"{dys}d")
    if hrs:
        parts.append(f"{hrs}h")
    if mins:
        parts.append(f"{mins}m")
    parts.append(f"{secs}s")
    return " ".join(parts)

def get_remaining(minutes):
    """Express print time remaining, in Days, Hours, and Minutes."""
    if not isinstance(minutes, int):
        minutes = int(minutes)
    if minutes < 0:
        minutes = 0

    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    days %= 365

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)

def bitwise_and(lhs, rhs):
    """Perform bitwise AND"""
    return lhs & rhs

def bitwise_or(lhs, rhs):
    """Perform bitwise OR"""
    return lhs | rhs

class T5UID1GCodeMacro:
    """A Class for wrapping a gcode macro into a jinja2 template?"""
    def __init__(self, config):
        self.printer = config.get_printer()
        self.env = jinja2.Environment('{%', '%}', '{', '}',
                                      trim_blocks=True,
                                      lstrip_blocks=True,
                                      extensions=['jinja2.ext.do'])

    def load_template(self, config, option, default=None):
        """Load applicable jinja2 template"""
        name = f"{config.get_name()}:{option}"
        script = config.get(option, default) if default is not None else config.get(option)
        return gcode_macro.TemplateWrapper(self.printer, self.env, name, script)

class T5UID1:
    """Defines one instance of the t5uid1 class as a unique set of parameters/attributes"""
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name()

        self.reactor = self.printer.get_reactor()

        self.gcode = self.printer.lookup_object('gcode')
        self.configfile = self.printer.lookup_object('configfile')
        
        self.toolhead = None
        self.heaters = self.printer.load_object(config, 'heaters')
        self.pause_resume = self.printer.load_object(config, 'pause_resume')
        self.stepper_enable = self.printer.load_object(config, 'stepper_enable')
        self.bed_mesh = None
        self.probe = None

        self.extruders = {}

        self.mcu = mcu.get_printer_mcu(self.printer,
                                       config.get('t5uid1_mcu', 'mcu'))
        self.oid = self.mcu.create_oid()

        self._version = self.printer.get_start_args().get('software_version')

        self.printer.load_object(config, 'gcode_macro')
        self._gcode_macro = T5UID1GCodeMacro(config)

        firmware_cfg = config.getchoice('firmware', T5UID1_firmware_cfg)
        self._firmware = config.get('firmware')

        self._machine_name = config.get('machine_name', 'Generic 3D printer')
        self._baud = config.getint('baud', 115200, minval=1200, maxval=921600)
        self._update_interval = config.getint('update_interval', 2,
                                              minval=1, maxval=10)
        self._volume = config.getint('volume', DEFAULT_VOLUME,
                                     minval=0, maxval=100)
        self._brightness = config.getint('brightness', DEFAULT_BRIGHTNESS,
                                         minval=0, maxval=100)
        self._boot_sound = config.getint('boot_sound',
                                         firmware_cfg['boot_sound'],
                                         minval=-1, maxval=255)
        self._notification_sound = config.getint('notification_sound',
            firmware_cfg['notification_sound'], minval=-1, maxval=255)

        self._x_min_inset = config.getfloat('x_min_inset', DEFAULT_INSET,
                                            minval=0.0)
        self._x_max_inset = config.getfloat('x_max_inset', DEFAULT_INSET,
                                            minval=0.0)
        self._y_min_inset = config.getfloat('y_min_inset', DEFAULT_INSET,
                                            minval=0.0)
        self._y_max_inset = config.getfloat('y_max_inset', DEFAULT_INSET,
                                            minval=0.0)
        self._x_min = config.getfloat('x_min', None)
        self._x_max = config.getfloat('x_max', None)
        self._y_min = config.getfloat('y_min', None)
        self._y_max = config.getfloat('y_max', None)
        self._z_min = config.getfloat('z_min', None)
        self._z_max = config.getfloat('z_max', None)

        self._last_cmd_time = 0
        self._gui_version = 0
        self._os_version = 0
        self._current_page = ""
        self._variable_data = {}
        self._status_data = {}
        self._vars = {}
        self._pages = {}
        self._routines = {}
        self._is_printing = False
        self._print_duration = 0
        self._print_progress = 0
        self._print_start_time = 0
        self._print_pause_time = -1
        self._print_end_time = -1
        self._print_time_remaining = 0
        self._startup_duration = 0
        self._latest_rvalue = 0
        self._slicer_estimated_print_time = 0
        self._boot_page = self._timeout_page = self._shutdown_page = None
        self._t5uid1_ping_cmd = self._t5uid1_write_cmd = None
        self._is_connected = False
        self._files = [None] * 5
        self._sort_index = 0

        self._original_M73 = None
        self._original_M117 = None
        

        global_context = {
            'get_variable': self.get_variable,
            'set_variable': self.set_variable,
            'enable_control': self.enable_control,
            'disable_control': self.disable_control,
            'start_routine': self.start_routine,
            'stop_routine': self.stop_routine,
            'set_message': self.set_message,
            'bitwise_and': bitwise_and,
            'bitwise_or': bitwise_or
        }

        context_input = dict(global_context)
        context_input.update({
            'page_name': self.page_name,
            'switch_page': self.switch_page,
            'play_sound': self.play_sound,
            'set_volume': self.set_volume,
            'set_brightness': self.set_brightness,
            'limit_extrude': self.limit_extrude,
            'heater_min_temp': self.heater_min_temp,
            'heater_max_temp': self.heater_max_temp,
            'heater_min_extrude_temp': self.heater_min_extrude_temp,
            'capture_gcode_files': self.capture_gcode_files,
            'delete_file' : self.delete_file,
            'is_busy': self.is_busy
        })

        context_output = dict(global_context)
        context_output.update({
            'all_steppers_enabled': self.all_steppers_enabled,
            '_files': self._files,
            'heater_min_temp': self.heater_min_temp,
            'heater_max_temp': self.heater_max_temp,
            'probed_matrix': self.probed_matrix,
            'pid_param': self.pid_param,
            'get_duration': get_duration,
            'get_remaining': get_remaining,
            'specific_fpname': self.specific_fpname
        })

        context_routine = dict(global_context)
        context_routine.update({
            'page_name': self.page_name,
            'switch_page': self.switch_page,
            'play_sound': self.play_sound,
            'set_volume': self.set_volume,
            'set_brightness': self.set_brightness,
            'abort_page_switch': self.abort_page_switch,
            'full_update': self.full_update,
            'is_busy': self.is_busy,
            'check_paused': self.check_paused,
            'capture_gcode_files': self.capture_gcode_files
        })

        self._status_data.update({
            'controls': firmware_cfg['controls'],
            'constants': firmware_cfg['constants']
        })

        self._load_config(config,
                          firmware_cfg['config_files'],
                          context_input,
                          context_output,
                          context_routine)

        if self._boot_page is None:
            raise self.printer.config_error("No boot page found")
        if self._timeout_page is None:
            self._timeout_page = self._boot_page
        if self._shutdown_page is None:
            self._shutdown_page = self._boot_page

        self.mcu.register_config_callback(self._build_config)

        self._update_timer = self.reactor.register_timer(self._send_update)
        self._ping_timer = self.reactor.register_timer(self._do_ping)

        self.gcode.register_command(
            'DGUS_ABORT_PAGE_SWITCH', self.cmd_DGUS_ABORT_PAGE_SWITCH)
        self.gcode.register_command(
            'DGUS_PLAY_SOUND', self.cmd_DGUS_PLAY_SOUND)
        self.gcode.register_command(
            'DGUS_PRINT_START', self.cmd_DGUS_PRINT_START)
        self.gcode.register_command(
            'DGUS_PRINT_END', self.cmd_DGUS_PRINT_END)
        self.gcode.register_command('M300', self.cmd_M300)

        self.printer.register_event_handler("klippy:ready",
                                            self._handle_ready)
        self.printer.register_event_handler("klippy:shutdown",
                                            self._handle_shutdown)
        self.printer.register_event_handler("klippy:disconnect",
                                            self._handle_disconnect)

    def _load_config(self, config, fnames, ctx_in, ctx_out, ctx_routine):
        if not isinstance(fnames, list):
            fnames = [fnames]
        v_list = config.get_prefix_sections('t5uid1_var ')
        v_main_names = { c.get_name(): 1 for c in v_list }
        p_list = config.get_prefix_sections('t5uid1_page ')
        p_main_names = { c.get_name(): 1 for c in p_list }
        r_list = config.get_prefix_sections('t5uid1_routine ')
        r_main_names = { c.get_name(): 1 for c in r_list }
        for fname in fnames:
            filepath = os.path.join(os.path.dirname(__file__),
                                    self._firmware,
                                    fname)
            try:
                dconfig = self.configfile.read_config(filepath)
            except Exception as e:
                raise self.printer.config_error(f"Cannot load config '{filepath}'") from e
            v_list += [c for c in dconfig.get_prefix_sections('t5uid1_var ')
                       if c.get_name() not in v_main_names]
            p_list += [c for c in dconfig.get_prefix_sections('t5uid1_page ')
                       if c.get_name() not in p_main_names]
            r_list += [c for c in dconfig.get_prefix_sections('t5uid1_routine ')
                       if c.get_name() not in r_main_names]
        for c in v_list:
            v = var.T5UID1_Var(self._gcode_macro,
                               ctx_in,
                               ctx_out,
                               c)
            if v.name in self._vars:
                raise self.printer.config_error(f"t5uid1_var '{v.name}' already exists")
            self._vars[v.name] = v
        for c in p_list:
            p = page.T5UID1_Page(self._vars.keys(), c)
            if p.name in self._pages:
                raise self.printer.config_error(f"t5uid1_page '{p.name}' already exists")
            self._pages[p.name] = p
            if p.is_boot:
                if self._boot_page is None:
                    self._boot_page = p.name
                else:
                    raise self.printer.config_error("Multiple boot pages found")
            if p.is_timeout:
                if self._timeout_page is None:
                    self._timeout_page = p.name
                else:
                    raise self.printer.config_error("Multiple timeout pages found")
            if p.is_shutdown:
                if self._shutdown_page is None:
                    self._shutdown_page = p.name
                else:
                    raise self.printer.config_error("Multiple shutdown pages found")
        for c in r_list:
            r = routine.T5UID1_Routine(self._gcode_macro,
                                       ctx_routine,
                                       self._pages.keys(),
                                       c)
            if r.name in self._routines:
                raise self.printer.config_error(f"t5uid1_routine '{r.name}' already exists")
            self._routines[r.name] = r

    def _build_config(self):
        timeout_command, timeout_data = self.switch_page(self._timeout_page, send=False)
        timeout_data = "".join(f"{x:02x}" for x in timeout_data)

        self.mcu.add_config_cmd(
            f"config_t5uid1 oid={self.oid} baud={self._baud} timeout={TIMEOUT_SECS}"
            f" timeout_command={timeout_command} timeout_data={timeout_data}"
        )

        curtime = self.reactor.monotonic()
        self._last_cmd_time = self.mcu.estimated_print_time(curtime)

        cmd_queue = self.mcu.alloc_command_queue()
        self._t5uid1_ping_cmd = self.mcu.lookup_command("t5uid1_ping oid=%c", cq=cmd_queue)
        self._t5uid1_write_cmd = self.mcu.lookup_command(
            "t5uid1_write oid=%c command=%c data=%*s", cq=cmd_queue)

        self.mcu.register_response(self._handle_t5uid1_received, "t5uid1_received")

    def _handle_ready(self):
        self.toolhead = self.printer.lookup_object('toolhead')

        self.heaters.lookup_heater('extruder')
        self.heaters.lookup_heater('heater_bed')

        try:
            self.bed_mesh = self.printer.lookup_object('bed_mesh')
        except self.printer.config_error:
            logging.warning("No 'bed_mesh' configuration found")
            self.bed_mesh = None

        try:
            self.probe = self.printer.lookup_object('probe')
        except self.printer.config_error:
            logging.warning("No 'probe' configuration found")
            self.probe = None

        has_bltouch = False
        try:
            self.printer.lookup_object('bltouch')
            has_bltouch = True
        except self.printer.config_error:
            pass

        if self._original_M73 is None:
            original_M73 = self.gcode.register_command('M73', None)
            if original_M73 != self.cmd_M73:
                self._original_M73 = original_M73
            self.gcode.register_command('M73', self.cmd_M73)

        if self._original_M117 is None:
            original_M117 = self.gcode.register_command('M117', None)
            if original_M117 != self.cmd_M117:
                self._original_M117 = original_M117
            self.gcode.register_command('M117', self.cmd_M117)

        self._status_data.update({
            'limits': self.limits(),
            'has_bltouch': has_bltouch
        })

        self._is_connected = True
        self.reactor.register_timer(self._on_ready, self.reactor.NOW)

    def _on_ready(self, eventtime):
        if not self._is_connected:
            return self.reactor.NEVER
        self._last_cmd_time = self.mcu.estimated_print_time(eventtime)
        self.t5uid1_command_read(T5UID1_ADDR_VERSION, 1)
        self.set_brightness(self._brightness)
        self.switch_page(self._boot_page)
        if self._boot_sound >= 0:
            self.play_sound(self._boot_sound, volume=self._volume)
        else:
            self.set_volume(self._volume)
        return self.reactor.NEVER

    def _handle_shutdown(self):
        msg = getattr(self.mcu, "_shutdown_msg", "").strip()
        parts = textwrap.wrap(msg, 32)
        while len(parts) < 4:
            parts.append("")
        self.set_variable("line1", parts[0].strip())
        self.set_variable("line2", parts[1].strip())
        self.set_variable("line3", parts[2].strip())
        self.set_variable("line4", parts[3].strip())
        self.switch_page(self._shutdown_page)
        if self._notification_sound >= 0:
            self.play_sound(self._notification_sound)

    def _handle_disconnect(self):
        self._is_connected = False
        self._current_page = ""
        self.reactor.update_timer(self._update_timer, self.reactor.NEVER)
        self.reactor.update_timer(self._ping_timer, self.reactor.NEVER)

    def _handle_t5uid1_received(self, params):
        if not self._is_connected:
            return
        logging.debug("t5uid1_received %s", params)
        if params['command'] != T5UID1_CMD_READVAR:
            return
        data = bytearray(params['data'])
        if len(data) < 3:
            logging.warning("Received invalid T5UID1 message")
            return
        address = struct.unpack(">H", data[:2])[0]
        data_len = data[2] << 1
        if len(data) < data_len + 3:
            logging.warning("Received invalid T5UID1 message")
            return
        data = data[3:data_len + 3]
        self.reactor.register_async_callback(
            (lambda e, s=self, a=address, d=data: s.handle_received(a, d)))

    def handle_received(self, address, data):
        """A function to parse messages received from DWIN_SET"""
        if not self._is_connected:
            return
        if address == T5UID1_ADDR_VERSION and len(data) == 2:
            self._gui_version = data[0]
            self._os_version = data[1]
            return
        handled = False
        for name in self._vars:
            if (self._vars[name].address != address
                or self._vars[name].type != "input"):
                continue
            handled = True
            try:
                self._vars[name].data_received(data)
            except Exception as e:
                logging.exception("Unhandled exception in '%s' receive"
                                  " handler: %s", name, str(e))
        if not handled:
            logging.warning("Received unhandled T5UID1 message for address %s",
                         hex(address))

    def send_var(self, name):
        """Build and send message to DWIN_SET (but abort and flag unknown messages)"""
        if name not in self._vars:
            raise ValueError(f"T5UID1_Var '{name}' not found")
        var_obj = self._vars[name]
        return self.t5uid1_command_write(var_obj.address, var_obj.prepare_data())

    def page_name(self, page_id):
        """Build string variable 'name' containing name of page corresponding to page number"""
        if not isinstance(page_id, int):
            page_id = int(page_id)
        for name in self._pages:
            if self._pages[name].id == page_id:
                return name
        raise ValueError(f"T5UID1_Page {page_id} not found")

    def send_page_vars(self, page=None, complete=False):
        """Update the applicable variables defined in pages.cfg for the current page"""
        if page is None:
            page = self._current_page
        if page not in self._pages:
            raise ValueError(f"T5UID1_Page '{page}' not found")
        if complete:
            for var_name in self._pages[page].var:
                self.send_var(var_name)
        for var_name in self._pages[page].var_auto:
            self.send_var(var_name)

    def full_update(self):
        """Refresh all data on current page. Reset update_timer."""
        self.send_page_vars(complete=True)
        self.reactor.update_timer(self._update_timer,
                                  self.reactor.monotonic()
                                      + self._update_interval)

    def start_routine(self, routine):
        """Launch called routine. Abort and raise error if cannot"""
        if routine not in self._routines:
            raise ValueError(f"T5UID1_Routine '{routine}' not found")
        if self._routines[routine].trigger != "manual":
            raise ValueError(f"T5UID1_Routine '{routine}' cannot be started manually")
        self._routines[routine].run()

    def stop_routine(self, routine):
        """Abort and flag attempt to process an undefined/deprecated routine"""
        if routine not in self._routines:
            raise ValueError(f"T5UID1_Routine '{routine}' not found")
        self._routines[routine].stop()

    def _start_page_routines(self, page, trigger):
        if page not in self._pages:
            raise ValueError(f"T5UID1_Page '{page}' not found")
        results = []
        results = [
            self._routines[routine].run()
            for routine in self._routines
            if self._routines[routine].page == page
            and self._routines[routine].trigger == trigger
        ]
        return all(result is not None for result in results)

    def _stop_page_routines(self, page):
        if page not in self._pages:
            raise ValueError(f"T5UID1_Page '{page}' not found")
        for routine in self._routines:
            if self._routines[routine].page == page:
                self._routines[routine].stop()


    class sentinel:
        """Defines sentinel as no-op class"""
        pass

    def get_variable(self, name, default=sentinel):
        """Return value of named variable. Raise error if name not recognized"""
        if name not in self._variable_data:
            if default is not self.sentinel:
                return default
            raise ValueError(f"Variable '{name}' not found")

        return self._variable_data[name]

    def set_variable(self, name, value):
        """Read variable values into variables"""
        self._variable_data[name] = value

# Before entering Print_Menu page, return path & name of all gcode files on Virtual SD Card into the set _files
    def capture_gcode_files(self, directory):
        self._files=[]
        for root, dirs, filenames in os.walk(os.path.expanduser(directory)):
            for filename in filenames:
               if filename.endswith('.gcode'):
                    self._files.append(os.path.join(root, filename))

        # If fewer than 5 files were found, pad the rest of the _files list with 'None'
        while len(self._files) < 5:
            self._files.append(None)

# Sort the files list by modification time, most recent file first 
        self._files = sorted( 
            [f for f in self._files if f is not None],
            key=lambda x: os.path.getmtime(x),
            reverse=True
            ) + [None] * (5 - len([f for f in self._files if f is not None]))

        return (self._files)

    def specific_fpname(self, i, index): 
        # Allow for scrolling up and down the list in increments of 1 position
        # Manage the value of scroll_index as a variable in a vars_in.cfg script, in response to button-presses
        try: 
            if i + index < len(self._files):
                if self._files[i + index] is not None:
                    return self._files[i + index].split('/')[-1]
                else:
                    return None 
            else: raise IndexError("Index out of range") 
        except Exception as e:
            logging.exception("Unhandled exception in specific_fpname: %s, %s, %s", i, index, str(e)) 
            return None

    def delete_file(self, index):
            self._scroll_index = index
            try: # Find the file path in _files based on the index + _scroll_index 
                file_path = self._files[self._scroll_index] 
                if file_path is not None: 
                    # Delete the file
                    os.remove(file_path)
                    logging.info(f"Deleted file: {file_path}") 
                    # Update the _files list 
                    self._files[self._scroll_index] = None 
                else: logging.warning("No file to delete at the specified index.") 
            except Exception as e: 
                logging.exception("Failed to delete file at index %s: %s", index, str(e))

    def check_paused(self):
        """Manage the printer if and while paused"""
        # If the printer is not printing a model, exit this process
        if not self._is_printing:
            return
        # Next two lines are disabled. They prevent processing resume action
        # if not self.pause_resume.is_paused:
        #    return
        # If the printer has resumed printing but the print_paused page is still displayed:
            # assume the printer has been resumed by a RESUME macro
            # and restore the displayed page to "print_status"
        if self._current_page == "print_paused" and not self.pause_resume.is_paused:
            self.switch_page("print_status")
            self._current_page = "print_status"
        # If the printer is paused but the displayed page is still "print_status":
            # assume the printer has been paused by Klipper (e.g. M600 or PAUSE macros)
            # and change the display page to "print_paused".
        if self._current_page == "print_status" and self.pause_resume.is_paused:
            self.switch_page("print_paused")
            self._current_page = "print_paused"
        # Keep track of the amount of time spent paused (i.e. "time not printing")
        # to be able to subtract that from the total at the end of the job, as follows:
        # Step 1: set the variable curtime to the value of "time now"
        curtime = self.reactor.monotonic()
        # Step 2: If this is the first iteration of check_paused since the printer was paused,
        # set the value of self._print_pause_time to "time now"
        if self._print_pause_time < 0 and self.pause_resume.is_paused:
            self._print_pause_time = curtime
        # Step 4: When the printer is resumed add the total amount of time
        # that the printer was paused to the print start time,
        # so that the total time printed (calculated as "end time" - "start time")
        # will not include that time if pause_duration > 0:
        if self._print_pause_time >= 0 and not self.pause_resume.is_paused:
            pause_duration = curtime - self._print_pause_time
            self._print_start_time += pause_duration
            # Now reset the trigger so that if the current print is paused again,
            # the above process will also  measure the new print paused time.
            self._print_pause_time = -1

    def get_start_countdown_status(self):
        """Check whether to start the Splicer-Estimated Print Time Remaining countdown timer""" 
        variables_file = '/home/pi/klipper/klippy/extras/t5uid1/dgus_reloaded/variables.cfg' 
        start_countdown_timer = None 
        try: 
            with open(variables_file, 'r') as file: 
                for line in file: 
                    if 'start_countdown_timer' in line: 
                        # Strip out unnecessary characters and split the line key, 
                        key, value = line.strip().split(' = ') 
                        if key == 'start_countdown_timer': 
                            start_countdown_timer = value.strip().lower() == 'true' 
                            break 

        except FileNotFoundError: 
            print(f"File not found: {variables_file}") 
        except Exception as e: 
            print(f"Error reading {variables_file}: {e}") 
        
        # If the variable isn't found, handle the case 
        if start_countdown_timer is None: 
            print("Variable 'start_countdown_timer' not found.") 
            start_countdown_timer = False

        return start_countdown_timer

    def get_status(self, eventtime):
        """Update the values of the displayed printer status variables"""
        pages = { p: self._pages[p].id for p in self._pages }
        res = dict(self._status_data)
        # Calculate the current value of print_duration, before performing the update routine
        # If finished printing, print duration = "time at finish" - "time at start"
        if not self._is_printing:
            self._print_duration = self._print_end_time - self._print_start_time
        # If printing is paused, print duration = "time when paused" - "time at start"
        elif self._print_pause_time >= 0:
            self._print_duration = self._print_pause_time - self._print_start_time
        # If printing, print_duration = "current time" - "time at start",
        # iff "eventtime"= "current_time"
        else:
            self._print_duration = eventtime - self._print_start_time
        # Since the slicer estimated print time and the M73 R values are in minutes, not seconds, 
        # compute _print_time_remaining in minutes
 
        start_counting=self.get_start_countdown_status()
        if start_counting==False:
            self._print_time_remaining = self._slicer_estimated_print_time
            self._startup_duration=self._print_duration
        else:
            self._print_time_remaining = self._slicer_estimated_print_time - self._print_duration/60 + self._startup_duration/60 + 1
        # If_ slicer_estimated_print_time proves too low, revert to using the M73 R factor rather than displaying zero or negative times
        if self._print_time_remaining <= 0:
            self._print_time_remaining = self._latest_rvalue
            
        # update() the res dictionary based on the keys and current values declared
        # within the {} braces here:
        res.update({
            'version': self._version,
            'machine_name': self._machine_name,
            'gui_version': self._gui_version,
            'os_version': self._os_version,
            'notification_sound': self._notification_sound,
            'page': self._current_page,
            'volume': self._volume,
            'brightness': self._brightness,
            'pages': pages,
            'control_types': CONTROL_TYPES,
            'is_printing': self._is_printing,
            'print_progress': self._print_progress,
            'print_duration': max(0, self._print_duration),
            'time_remaining': self._print_time_remaining
        })
        return res

    def _send_update(self, eventtime):
        if not self._is_connected or not self._current_page:
            return self.reactor.NEVER
        try:
            # Try updating the var_auto variables on the current page
            self.send_page_vars(self._current_page, complete=False)
        except Exception as e:
            logging.exception("Unhandled exception in update timer: %s", str(e))
        return eventtime + self._update_interval

    def _do_ping(self, eventtime):
        if not self._is_connected or self._t5uid1_ping_cmd is None:
            return self.reactor.NEVER
        print_time = self.mcu.estimated_print_time(eventtime)
        print_time = max(self._last_cmd_time + CMD_DELAY, print_time)
        clock = self.mcu.print_time_to_clock(print_time)
        self._t5uid1_ping_cmd.send([self.oid], minclock=clock)
        self._last_cmd_time = print_time
        return eventtime + TIMEOUT_SECS - 2

    def _t5uid1_write(self, command, data, schedule_ping=True):
        if not self._is_connected or self._t5uid1_write_cmd is None:
            return
        curtime = self.reactor.monotonic()
        print_time = self.mcu.estimated_print_time(curtime)
        print_time = max(self._last_cmd_time + CMD_DELAY, print_time)
        clock = self.mcu.print_time_to_clock(print_time)
        self._t5uid1_write_cmd.send([self.oid, command, list(data)],
                                    minclock=clock)
        self._last_cmd_time = print_time
        if schedule_ping:
            self.reactor.update_timer(self._ping_timer,
                                      curtime + TIMEOUT_SECS - 2)

    def t5uid1_command_write(self, address, data, send=True):
        """Build message to send to DWIN_SET. Flag if invalid address or data"""
        if address < 0 or address > 0xffff:
            raise ValueError("invalid address")
        if not isinstance(data, bytearray):
            raise ValueError("invalid data")
        if len(data) < 1 or len(data) > 64 or len(data) % 2 != 0:
            raise ValueError("invalid data length")
        command = T5UID1_CMD_WRITEVAR
        command_data = bytearray([ (address >> 8), (address & 0xff) ])
        command_data.extend(data)
        if not send:
            return (command, command_data)
        self._t5uid1_write(command, command_data)

    def t5uid1_command_read(self, address, wlen, send=True):
        """Parse message received from DWIN_SET. Flag if not valid content"""
        if address < 0 or address > 0xffff:
            raise ValueError("invalid address")
        if wlen < 1 or wlen > 0x7d:
            raise ValueError("invalid wlen")
        command = T5UID1_CMD_READVAR
        command_data = bytearray([ (address >> 8), (address & 0xff), wlen ])
        if not send:
            return (command, command_data)
        self._t5uid1_write(command, command_data)

    def switch_page(self, name, send=True):
        """Switch to named page. Flag if page name not known"""
        if name not in self._pages:
            raise ValueError("invalid page")
        if not send:
            return self.t5uid1_command_write(T5UID1_ADDR_PAGE,
                                             bytearray([
                                                 0x5a, 0x01,
                                                 0x00, self._pages[name].id
                                             ]),
                                             send)
        if name == self._current_page:
            return
        if not self._start_page_routines(name, "enter_pre"):
            return
        self.send_page_vars(name, complete=True)
        self.t5uid1_command_write(T5UID1_ADDR_PAGE,
                                  bytearray([
                                      0x5a, 0x01,
                                      0x00, self._pages[name].id
                                  ]),
                                  send)
        if self._current_page:
            self._stop_page_routines(self._current_page)
            self._start_page_routines(self._current_page, "leave")
        self._current_page = name
        self._start_page_routines(name, "enter")
        self.reactor.update_timer(self._update_timer,
                                  self.reactor.monotonic()
                                      + self._update_interval)

    def abort_page_switch(self):
        """Send message to calling routine, if abort page switch"""
        return "DGUS_ABORT_PAGE_SWITCH"

    def play_sound(self, start, slen=1, volume=-1, send=True):
        """Play sound defined by the calling function."""
        if start < 0 or start > 255:
            raise ValueError("invalid start")
        if slen < 1 or slen > 255:
            raise ValueError("invalid slen")
        if volume > 100:
            raise ValueError("invalid volume")
        if volume < 0:
            volume = self._volume
        val = map_value_range(volume, 0, 100, 0, 255)
        return self.t5uid1_command_write(T5UID1_ADDR_SOUND,
                                         bytearray([start, slen, val, 0]),
                                         send)

    def enable_control(self, page, ctype, control, send=True):
        """Build and send a message to DWIN_SET to enable a control"""
        if page < 0 or page > 255:
            raise ValueError("invalid page")
        if ctype < 0 or ctype > 255:
            raise ValueError("invalid ctype")
        if control < 0 or control > 255:
            raise ValueError("invalid control")
        return self.t5uid1_command_write(T5UID1_ADDR_CONTROL,
                                         bytearray([
                                             0x5a, 0xa5, 0, page,
                                             control, ctype, 0, 0x01
                                         ]),
                                         send)

    def disable_control(self, page, ctype, control, send=True):
        """Build and send a message to DWIN_SET to disable a control"""
        if page < 0 or page > 255:
            raise ValueError("invalid page")
        if ctype < 0 or ctype > 255:
            raise ValueError("invalid ctype")
        if control < 0 or control > 255:
            raise ValueError("invalid control")
        return self.t5uid1_command_write(T5UID1_ADDR_CONTROL,
                                         bytearray([
                                             0x5a, 0xa5, 0, page,
                                             control, ctype, 0, 0
                                         ]),
                                         send)

    def set_brightness(self, brightness, send=True):
        """Build and send a message to DWIN_SET to set the display brightness"""
        if brightness < 0 or brightness > 100:
            raise ValueError("invalid brightness")
        val = map_value_range(brightness, 0, 100, 5, 100)
        result = self.t5uid1_command_write(T5UID1_ADDR_BRIGHTNESS,
                                           bytearray([val, val]),
                                           send)
        if not send:
            return result
        if self._brightness != brightness:
            self._brightness = brightness
            self.configfile.set(self.name, 'brightness', brightness)

    def set_volume(self, volume, send=True):
        """Build and send a message to DWIN_SET to set the display speaker volume"""
        if volume < 0 or volume > 100:
            raise ValueError("invalid volume")
        val = map_value_range(volume, 0, 100, 0, 255)
        result = self.t5uid1_command_write(T5UID1_ADDR_VOLUME,
                                           bytearray([val, 0]),
                                           send)
        if not send:
            return result
        if self._volume != volume:
            self._volume = volume
            self.configfile.set(self.name, 'volume', volume)

    def all_steppers_enabled(self):
        """Return which of the three steppers is/are enabled"""
        res = True
        for name in ['stepper_x', 'stepper_y', 'stepper_z']:
            res &= self.stepper_enable.lookup_enable(name).is_motor_enabled()
        return res

    def heater_min_temp(self, heater):
        """Read value of min_temp in heaters.py for specified heater"""
        try:
            return self.heaters.lookup_heater(heater).min_temp
        except Exception:
            return 0

    def heater_max_temp(self, heater, margin=0):
        """Read value of max_temp in heaters.py for specified heater"""
        try:
            return max(0, self.heaters.lookup_heater(heater).max_temp - margin)
        except Exception:
            return 0

    def heater_min_extrude_temp(self, heater):
        """Return minimum extrusion temperature"""
        return self.heaters.lookup_heater(heater).min_extrude_temp

    def probed_matrix(self):
        """ Draw a checkmark at each probed point, as the ABL process executes"""
        # In the DWIN_SET app, the total matrix requires two full words to describe the 25 points
        # The first 16 points are stored in the first word (0x3122)
        # The remaining nine points are stored in the second word (0x3123)
        if self.bed_mesh is None:
            return 0
        count = len(self.probe.probe_session.results)
        points_map = [ 0,  1,  2,  3,  4,
                       9,  8,  7,  6,  5,
                      10, 11, 12, 13, 14,
                      19, 18, 17, 16, 15,
                      20, 21, 22, 23, 24]
        res = 0
        # This process re-draws the probed_matrix map,
        # based on how many points have been probed so far
        for i in range(25):
            if count > points_map[i]:
                if i < 16:
                    res |= 1 << (i + 16)
                else:
                    res |= 1 << (i - 16)
        return res

    def pid_param(self, heater, param):
        """Load the PID parameter values"""
        if param not in ['p', 'i', 'd']:
            raise ValueError("Invalid param")
        try:
            return getattr(self.heaters.lookup_heater(heater).control,
                           'K' + param) * heaters.PID_PARAM_BASE
        except Exception as e:
            logging.exception("Unhandled exception in t5uid1.pid_param: %s", str(e))
            return 0

    def limit_extrude(self, extruder, val):
        """ Ensure filament_length value !> max_extrude_only_distance in printer.cfg"""
        logging.exception("Entering t5uid1.limit_extrude with val = : %s", str(val))
        try:
            if extruder in self.extruders:
                res = self.extruders[extruder].max_e_dist
            else:
                ex = self.printer.lookup_object('extruder')
                res = ex.max_e_dist
                self.extruders[extruder] = ex
            # If entered value (val) > max_extrude_only_distance (res),
            # then limit filament_length entry to the value of res
            return min(res, val)
        # NOTE: Started failing when upgraded python on test printer to 3.11.1, from 3.9
        # Now returning zero on test printer. Does not return 140, so assume no exception above...
        except Exception as e:
            logging.exception("Unhandled exception in t5uid1.limit_extrude: %s", str(e))
            return 140

    def limits(self):
        """Load the printer kinematics variable values"""
        kin = self.toolhead.get_kinematics()
        x_min, x_max = kin.rails[0].get_range()
        y_min, y_max = kin.rails[1].get_range()
        z_min, z_max = kin.rails[2].get_range()
        if (self._x_min is not None
            and self._x_min > x_min
            and self._x_min < x_max):
            x_min = self._x_min
        if (self._x_max is not None
            and self._x_max < x_max
            and self._x_max > x_min):
            x_max = self._x_max
        if (self._y_min is not None
            and self._y_min > y_min
            and self._y_min < y_max):
            y_min = self._y_min
        if (self._y_max is not None
            and self._y_max < y_max
            and self._y_max > y_min):
            y_max = self._y_max
        if (self._z_min is not None
            and self._z_min > z_min
            and self._z_min < z_max):
            z_min = self._z_min
        if (self._z_max is not None
            and self._z_max < z_max
            and self._z_max > z_min):
            z_max = self._z_max
        x_min_inset = min(self._x_min_inset, (x_max - x_min) / 2.0)
        x_max_inset = min(self._x_max_inset, (x_max - x_min) / 2.0)
        y_min_inset = min(self._y_min_inset, (y_max - y_min) / 2.0)
        y_max_inset = min(self._y_max_inset, (y_max - y_min) / 2.0)
        return {
            'x_min': x_min,
            'x_max': x_max,
            'y_min': y_min,
            'y_max': y_max,
            'z_min': z_min,
            'z_max': z_max,
            'x_min_inset': x_min_inset,
            'x_max_inset': x_max_inset,
            'y_min_inset': y_min_inset,
            'y_max_inset': y_max_inset
        }

    def set_message(self, message):
        """Set or clear the string value of the message on the display"""
        self.set_variable('message', message.strip())
        if 'message' in self._vars:
            self.send_var('message')
        if len(message) > 0 and 'message_timeout' in self._routines:
            self.start_routine('message_timeout')

    def is_busy(self):
        """Return whether the printer is too busy to process a command"""
        eventtime = self.reactor.monotonic()
        print_time, est_print_time, lookahead_empty = self.toolhead.check_busy(
            eventtime)
        idle_time = est_print_time - print_time
        if (not lookahead_empty
                or idle_time < 1.0
                or self.gcode.get_mutex().test()):
            return True
        # If there is a probe, and if the probe is currently performing multiple probes,
        # return True, else return False
        return (self.probe is not None and self.probe.probe_session.homing_helper.multi_probe_pending)
    def cmd_DGUS_ABORT_PAGE_SWITCH(self, gcmd):
        """define abort_page_switch as a no-op function"""
        pass

    def cmd_DGUS_PLAY_SOUND(self, gcmd):
        """Play Sound gcode handler"""
        if self._notification_sound >= 0:
            start = gcmd.get_int('START', self._notification_sound,
                                 minval=0, maxval=255)
        else:
            start = gcmd.get_int('START', minval=0, maxval=255)
        slen = gcmd.get_int('LEN', 1, minval=0, maxval=255)
        volume = gcmd.get_int('VOLUME', -1, minval=0, maxval=100)
        try:
            self.play_sound(start, slen, volume)
        except Exception as e:
            raise gcmd.error(str(e))
        gcmd.respond_info(f"Playing sound {start} (len={slen}, volume={volume})")

    def cmd_DGUS_PRINT_START(self, gcmd):
        """DGUS_Print_Start gcode handler"""
        self._print_progress = 0
        self._print_start_time = self.reactor.monotonic()
        self._print_pause_time = -1
        self._print_end_time = -1

        # If the gcode includes M73 R messages, then capture the first one as the slicer's estimated total print time
        if self._print_time_remaining > 0:
            self._slicer_estimated_print_time = self._print_time_remaining
        else: self._print_time_remaining = 0

        self._is_printing = True
        self.check_paused()
        if 'print_start' in self._routines:
            self.start_routine('print_start')

    def cmd_DGUS_PRINT_END(self, gcmd):
        """DGUS_Print_End gcode handler"""
        if not self._is_printing:
            return
        self._print_progress = 100
        curtime = self.reactor.monotonic()
        if self._print_pause_time >= 0:
            pause_duration = curtime - self._print_pause_time
            if pause_duration > 0:
                self._print_start_time += pause_duration
            self._print_pause_time = -1
        self._print_end_time = curtime
        self._print_time_remaining = 0
        self._latest_rvalue = 0
        self._slicer_estimated_print_time = 0
        self._is_printing = False
        if 'print_end' in self._routines:
            self.start_routine('print_end')

    def cmd_M73(self, gcmd):
        """Custom M73 function"""
        # The message format may be M73 P_ R_ or M73 P_ or M73 R_
        if gcmd.get_int('P', 0):
            progress = gcmd.get_int('P', 0)
            self._print_progress = min(100, max(0, progress))
        if gcmd.get_int('R', 0):
            self._latest_rvalue = gcmd.get_int('R', 0)
            self._print_time_remaining = max(0, self._latest_rvalue)
        if self._original_M73 is not None:
            self._original_M73(gcmd)

    def cmd_M117(self, gcmd):
        """Custom M117 function"""
        msg = gcmd.get_commandline()
        umsg = msg.upper()
        if not umsg.startswith('M117'):
            start = umsg.find('M117')
            end = msg.rfind('*')
            msg = msg[start:end]
        if len(msg) > 5:
            self.set_message(msg[5:])
        else:
            self.set_message("")
        if self._original_M117 is not None:
            self._original_M117(gcmd)

    def cmd_M300(self, gcmd):
        """Custom M300 function"""
        if self._notification_sound >= 0:
            start = gcmd.get_int('S', self._notification_sound)
        else:
            start = gcmd.get_int('S', minval=0, maxval=255)
        slen = gcmd.get_int('P', 1, minval=1, maxval=255)
        volume = gcmd.get_int('V', -1, minval=0, maxval=100)
        if start < 0 or start > 255:
            start = self._notification_sound
        try:
            self.play_sound(start, slen, volume)
        except Exception as e:
            raise gcmd.error(str(e))

def load_config(config):
    """Load the DGUS-Reloaded.cfg file settings into this instance of T5UID1"""
    return T5UID1(config)
