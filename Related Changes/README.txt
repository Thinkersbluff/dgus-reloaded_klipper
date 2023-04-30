One of the challenges with installing this distribution on your system is that you will still likely need to make some customizations of your own.

I have used quite verbose folder names, to give you a clue as to what files you will need to put where:

1. Flash this firmware.bin file if...

Part of the normal Klipper installation process involves using a utility called Make Menuconfig, to generate a configuration file, and then to Make (compile) a Klipper.bin based on that configuration file, with which to flash Klipper to your printer's motherboard. 

In this repo, you will find pre-made klipper.bin files for the BTT SKR CR6 and Creality 4.5.2/4.5.3/1.1.0.3 motherboards. If yours is a CR6 printer, just flash the firmware.bin file from the applicable folder & skip the Make Menuconfig/Make steps.

2. Overwrite these Klipper host files\Upload these configuration files to the Machine folder in Mainsail

Klipper, Moonraker and Mainsail each require configuration files to tailor their installation and operation.
I have only one CR6 printer on which to perform my development and testing, so I am not able to verify and validate that the files included with this distribution will operate on all possible CR6 machines.

While I will do my best to recruit other CR6Community members to help "shake-down" this distribution and will try to provide validated tailored configurations in future releases, the pace and extent to which I will be able to achieve that is TBD.

I have included all of my configuration files in this distribution, in the folder "Related Changes\Upload these configuration files to the Machine folder in Mainsail". These files were all verified and validated to work as an integrated set on my CR6-SE which has at least the following modifications on it: 
	- Converted to Direct Drive, with 
		- Orbiter v1.5 extruder and 
		- a pancake Moons extruder motor
	- Y motor converted to 0.8 degree version

When I started this project, I had a BTT SKR CR6 motherboard.  I now use a Creality 1.1.0.3 ERA motherboard.  I have uploaded copies of the configuration files for both motherboards, here, to get you started. 

Be aware that you will likely need to change some settings before these will work on your system. 
	e.g. Printer.cfg and CR6.cfg will both require edits to adjust the extruder & stepper motor and performance settings, at least

If you plan to install this modified Klipper onto an existing Klipper system, you may prefer to keep your existing configuration files and just compare with the ones I have included, to spot and transfer any relevant differences between the two. (A tool like Winmerge is excellent for that type of comparison and harmonization task.)

If you have no existing Klipper installation, you can start by uploading these files as-is, but you will still likely need to modify some of the settings, to be fully compatible with your own system.


NOTE: If you already use Mainsail, make sure that you have updated it on or after Jan 2023.  They have changed the design a little and have corrected a couple of bugs in the CANCEL_PRINT macro used by this firmware.

If you use Fluidd, my apologies, but I do not, so you will likely need to do some additional work to configure your system.  I just don't know what that work will be.  Please share your experience and learning in Discussions, for the benefit of other Fluidd users.

3. Overwrite these Klipper host files\Install into kiauh

I recommend that you use KIAUH to help you make this installation of Klipper, (and Moonraker and Mainsail, if you also need to install those.)

NOTE: IF you are using this firmware on a CR6 printer, you do not need to install klipper-repos.txt and you do NOT need to install the modified Klipper from this repo.  You can, instead, use the pre-made klipper.bin file per step 1, above, and install the current Klipper from Klipper3D.org/master.  Then copy (e.g. by FTP) the T5uid1 folder and contents into ~klipper/klippy/extras.  This will enable Moonraker to maintain klipper for you, without having to keep reinstalling the extras.


NOTE: IF - you are trying to use this DGUS-Reloaded firmware on a printer that is NOT a CR6 (and your screen is 272x480 pixels or you plan to refactor the DWIN_SET component for your display.)
THEN - Once you have KIAUH installed, upload the klipper_repos.txt file into ~/kiauh on the host, so that you are able to select this repository as the one from which KIAUH should install Klipper.  Then use Make Menuconfig and Make, to create your own klipper.bin file and flash that to your motherboard.  After that, you can change KIAUH back to loading Klipper from Klipper3D.org/master.
THEN - Copy (e.g. by FTP) the T5uid1 folder and contents into ~klipper/klippy/extras.  This will enable Moonraker to maintain klipper for you, without having to keep reinstalling the extras.



