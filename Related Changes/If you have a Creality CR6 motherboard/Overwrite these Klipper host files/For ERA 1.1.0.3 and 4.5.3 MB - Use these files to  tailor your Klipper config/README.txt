Last Updated : 30 Apr 2023

These files were downloaded from the Mainsail MACHINE CONFIG FILES tab of the test printer, at release time.

While they are uniquely configured to run on the test system, they also provide you with a reference that should help you figure out how to tailor your own setup to work with DGUS-reloaded_CR6Community_Edition.

NOTE: If you decide to make a new installation of Mainsail/Moonraker/Klipper, then you can upload these files as-is, then proceed to tailor printer.cfg to match your system and to suit your preferences.

New at this release:
 - Modified in CR6.cfg:
   - [stable_z_home]
      - Increased # of retries to 20 , from 10
      - Increased tolerance from 0.015 to 0.02
   - [gcode_macro M600]
      - Modified the sound parameters to fit within limitations of the DGUS-Reloaded Custom M300 macro
   - [gcode_macro RUN_ABL_BED_60]
	- Removed "<>" from profile name
   - [gcode_macro RUN_ABL_BED_80]
	- Removed "<>" from profile name
   - [gcode_macro START_PRINT]
	- Removed "<>" from BED_MESH_PROFILE names
	- Removed line: 	SET_VELOCITY_LIMIT VELOCITY=200 ACCEL=3000 ACCEL_TO_DECEL=750 SQUARE_CORNER_VELOCITY=5
	- Modified code to skip "TEMPERATURE WAIT" if printing to an unheated bed, as follows:
	      #If mean to print without heating bed, need to prevent software waiting for bed to cool to zero!
            {% if bedTemp >0 %}
               SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET={bedTemp}
               TEMPERATURE_WAIT SENSOR=heater_bed MINIMUM={bedTemp-2} MAXIMUM={bedTemp+2}
           {% endif %}
   - [gcode_macro END_PRINT]
	- Removed these disabled instructions: 
		- #TEMPERATURE_WAIT SENSOR=extruder MAXIMUM=50  ##Use part cooling fan to help cool nozzle after print
		- ##################################################################################################
		  # Button State Detection Macro (e.g. Optical Switch?)  NOTE: This macro is not used at the moment. 
		  # It was too slow to meet my needs to configure the Optical Switch to TARE the nozzle probe.
		  # Keeping it here purely to save me having to find it again, in case I think of a use for it.
		  #################################################################################################

		  # Execute gcode when a button is pressed or released (or when a pin changes state).
		  # Example: You can check the state of the button "my_gcode_button" by using:
		  #    QUERY_BUTTON button=my_gcode_button

		  #[gcode_button my_gcode_button]
		  #pin: !PC2
		  #   The pin on which the button my_gcode_button is connected. This parameter must be
		  #   provided.
		  #press_gcode:
		  #   A list of G-Code commands to execute when the button is pressed.
		  #   G-Code templates are supported.
  		  # TARE_PROBE
		  #release_gcode:
		  #   A list of G-Code commands to execute when the button is released.
		  #   G-Code templates are supported.

		  [print_stats]

		  #[gcode_macro _CURA_SET_PRINT_STATS_INFO]
		  # Found this trick by Pedro Lamas on Klipper Discord, cura channel, pinned posts.
		  # RESEARCH THE MACRO IT CALLS:  SET_PRINT_STATS_INFO
		  # Also requires this Search & Replace "trick" in Cura post-processing scripts:
		  # - Open Cura
		  # - Open the "Extensions" menu, then "Post processing", and click on "Modify G-Code"
		  # - Click the "Add Script" button, and select "Search and Replace" from the options
		  # - On the "Search" textbox, enter this: ;(LAYER|LAYER_COUNT)\:(\d+)
		  # - On the "Replace" textbox, enter this: ;\1:\2\n_CURA_SET_PRINT_STATS_INFO \1=\2
		  # - Tick the "Use Regular Expressions" checkbox
		  # - Click Close
		  #gcode:
		  # {% if params.LAYER_COUNT is defined %}
		  #    SET_PRINT_STATS_INFO TOTAL_LAYER={params.LAYER_COUNT}
		  #  {% endif %}
		  #  {% if params.LAYER is defined %}
		  #    SET_PRINT_STATS_INFO CURRENT_LAYER={(params.LAYER | int) + 1}
		  #  {% endif %}

 - printer.cfg
    - Added: # IF you do not have moonraker timelapse installed, comment out this optional cfg:
	       #[include timelapse.cfg]
    - [extruder]
	- increased samples_tolerance to 0.02 from 0.015
	- increased samples_tolerance retries to 3 from 2
    - [filament_switch_sensor filament_sensor]
	- changed "False" to "True" (i.e. I have reactivated my runout sensor)
    - [printer]
	- Changed max_accel to 3000 from 3300
	- Changed max_accel_to_decel to 1500 from 1900
    - [gcode_arcs]
	- Added resolution: 1.0


 - crowsnest.cfg
	- Configured for Brio500 Webcam.
	- You will need to modify this config for your own camera

 - DGUS_Reloaded.cfg
	- no changes

 - InputShaper.cfg
	- Added pointer to instructions, for installing rpi_mcu: # as documented here: https://www.klipper3d.org/RPi_microcontroller.html
 - Mainsail.cfg
	- UPDATED BY MAINSAIL TEAM (Moonraker manages all changes to this file.)
 - 