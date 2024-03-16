Last Updated : 15 Mar 2024

These files were built by updating the pin numbers in the ERA/4.5.3 files to be those of the 4.5.2 board.
[Only impacted the Nozzle Heater, Bed and Part Fan pins]

While they are uniquely configured to run on the test system, they also provide you with a reference that should help you figure out how to tailor your own setup to work with DGUS-reloaded_CR6Community_Edition.

NOTE: If you decide to make a new installation of Mainsail/Moonraker/Klipper, then you can upload these files as-is, then proceed to tailor printer.cfg to match your system and to suit your preferences.
There are copious notes throughout the files where they require you to tailor them for your own system.

The Dev_Macros.cfg file adds a couple of macros that help developers research the names/states of available parameters.  It is not needed, for the DGUS-Reloaded app to work. You can comment-out the include statement from printer.cfg if you wish.