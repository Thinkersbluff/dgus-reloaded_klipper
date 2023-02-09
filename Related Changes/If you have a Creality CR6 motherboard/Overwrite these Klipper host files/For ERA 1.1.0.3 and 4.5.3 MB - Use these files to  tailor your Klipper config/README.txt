Last Updated : 8 Feb 2023

These files were downloaded from the Mainsail MACHINE CONFIG FILES tab of the test printer, at release time.

While they are uniquely configured to run on the test system, they also provide you with a reference that should help you figure out how to tailor your own setup to work with DGUS-reloaded_CR6Community_Edition.

NOTE: If you decide to make a new installation of Mainsail/Moonraker/Klipper, then you can upload these files as-is, then proceed to tailor printer.cfg to match your system and to suit your preferences.

New at this release:
At release 1.2.4, the test printer was updated with the MAINSAIL OS build of Raspberry Pi, which included two new add-ins: Sonar and Timelapse.
	- I added considerable new annotation to the Printer.cfg file, to help you tailor it to your own system
	- I also uncommented the superceded setting values and deleted all of the automatically managed settings, so that you can tailor and use this copy of printer.cfg directly on your system. 
	- I have not used the Timelapse add-in, so I can not advise you on how to work with that
	- I have activated sonar, but have no experience or opinion to share, yet
	- I have moved the t5uid1 section from printer.cfg into its own DGUS-Reloaded.cfg file, which is now included into printer.cfg
		- Seemed less confusing to be able to name it DGUS-Reloaded and a better architecture to package it within its own cfg file

