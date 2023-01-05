Klipper, Moonraker and Mainsail each require configuration files to tailor their installation and operation.

The Mainsail Web client provides a virtual folder called MACHINE, with rudimentary file management functions, to help you upload/delete/modify/download those files, between the Klipper Host MCU and your storage system.

The files in the folder "Related Changes\Upload these configuration files to the Machine folder in Mainsail" were used on a CR6-SE, to verify and validate this CR6Community Edition of the DGUS-Reloaded_Klipper solution.

If you plan to install this modified Klipper onto an existing Klipper system, you may prefer to keep your existing configuration files and just compare with these, to spot and transfer any relevant differences between the two. (A tool like Winmerge is excellent for that type of comparison and harmonization task.)

If you have no existing Klipper installation, you can start by uploading these files, but you will still likely need to modify some of the settings here, to be fully compatible with your own system.

These files are configured for the test machine, which is NOT stock.
I have not yet reviewed those files to comment-out or modify settings unique to my system, so be aware that you will likely need to make changes, before these will work on your system.

NOTE: If you already use Mainsail, make sure that you have updated it on or after Jan 2023.  They have changed the design a little and have corrected a couple of bugs in the CANCEL_PRINT macro used by this firmware.

If you use Fluidd, my apologies, but I do not, so you will likely need to do some additional work to configure your system.  I just don't know what that work will be.  Please share your experience and learning in Discussions, for the benefit of other Fluidd users.