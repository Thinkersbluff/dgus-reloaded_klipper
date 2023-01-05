One of the challenges with installing this distribution on your system is that you will still likely need to make some customizations of your own.

I have used quite verbose folder names, to give you a clue as to what files you will need to put where:

1. Flash this firmware.bin file if...

Part of the Klipper installation process involves using a utility called Make Menuconfig, to generate a configuration file, and then to Make (compile) a Klipper.bin based on that configuration file, with which to flash Klipper to your printer's motherboard. 

If you also happen to have a BTT SKR CR6 motherboard, you can just flash the firmware.bin file in this folder & skip the Make Menuconfig/Make steps.

2. Overwrite these Klipper host files\Upload these configuration files to the Machine folder in Mainsail

Klipper, Moonraker and Mainsail each require configuration files to tailor their installation and operation.
I have only one CR6 printer on which to perform my development and testing, so I am not able to verify and validate that the files included with this distribution will operate on all possible CR6 machines.

While I will do my best to recruit other CR6Community members to help "shake-down" this distribution and will try to provide validated tailored configurations in future releases, the pace and extent to which I will be able to achieve that is TBD.

I have included all of my configuration files in this distribution, in the folder "Related Changes\Upload these configuration files to the Machine folder in Mainsail". These files were all verified and validated to work as an integrated set on my CR6-SE which has at least the following modifications on it: 
	- Converted to Direct Drive, with 
		- Orbiter v1.5 extruder and 
		- a pancake Moons extruder motor
      - Using a BTT SKR CR6 v1.0 motherboard
	- Y motor converted to 0.8 degree version

I have not yet reviewed those files to comment-out or modify settings unique to my system, so be aware that you will likely need to make changes, before these will work on your system.
	e.g. Printer.cfg and CR6.cfg will both require edits to adjust the extruder & stepper motor and performance settings, at least

If you plan to install this modified Klipper onto an existing Klipper system, you may prefer to keep your existing configuration files and just compare with the ones I have included, to spot and transfer any relevant differences between the two. (A tool like Winmerge is excellent for that type of comparison and harmonization task.)

If you have no existing Klipper installation, you can start by uploading these files as-is, but you will still likely need to modify some of the settings, to be fully compatible with your own system.


NOTE: If you already use Mainsail, make sure that you have updated it on or after Jan 2023.  They have changed the design a little and have corrected a couple of bugs in the CANCEL_PRINT macro used by this firmware.

If you use Fluidd, my apologies, but I do not, so you will likely need to do some additional work to configure your system.  I just don't know what that work will be.  Please share your experience and learning in Discussions, for the benefit of other Fluidd users.

3. Overwrite these Klipper host files\Install into kiauh

I recommend that you use KIAUH to help you make this installation of Klipper, (and Moonraker and Mainsail, if you also need to install those.)

Once you have KIAUH installed, upload the klipper_repos.txt file into ~/kiauh on the host, so that you are able to select the correct repository from which Klipper should be installed.

CAUTION: Moonraker does not trust software distributions from forked repositories of forked repositories.  It also does not like it when you edit or overwrite the distributed files.  As a result, you will see a red "Invalid" tag beside the Klipper entry.  We are still investigating options for fixing that.  We may be out of luck.  TBD.  Moonraker does seem to go ahead and update the distribution anyway, so it should not be a "show-stopper" that it is doing this...