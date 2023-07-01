# DGUS-reloaded-Klipper (modified), CR6Community Edition!
The Klipper in this repo is a fork of Klipper3D/Master, which has been modified - [largely by Desuuuu](https://github.com/Desuuuu/klipper), and a little bit more by me - to work with the DGUS-reloaded DWIN_SET for CR6 printers located in [this companion repo.](https://github.com/Thinkersbluff/DGUS-reloadedForKlipper_CR6)

This repo was forked from [the master DGUS-RELOADED project repository](https://github.com/Desuuuu/Klipper).
The Desuuuu repo is in-turn forked from [the master Klipper3D.org github repository.](https://github.com/Klipper3d/klipper/)

>>**NOTE:** Desuuuu has also indicated that he intends to stop maintaining his dgus-reloaded-klipper fork, soon, so I am looking for CR6Community help to maintain and extend this fork. (See **How to Contribute to This Project**, below)

## Who should __NOT__ use this firmware?
If your goal is to run Klipper on your CR6 without using the stock T5L DWIN display hardware, **then you do not need this modified version of Klipper.**
Just install the master Klipper3D.org version and configure it for your CR6 printer per the [Klipper3d.org installation and configuration documentation](https://github.com/Klipper3d/klipper/blob/master/docs/index.md).

This repository may also be very helpful to get you started with Klipper on the CR6: https://github.com/KoenVanduffel/CR-6_Klipper

## Why Not Just Use the Desuuuu version of the Modified DGUS-Reloaded Klipper?

1. Perhaps most importantly, Desuuuu has indicated that he intends to stop maintaining his dgus-reloaded-klipper fork. 

2. To enable the CR6 UI functionality, it is necessary to edit a few of the Desuuuu/Klipper files, for which I needed to make my own (this) fork of the t5uid1 application files.

Given both points 1 and 2 above, negotiating a common standard interface in both versions of DGUS-Reloaded was not a practical option.

## Is This Klipper Fork Using the latest Klipper3D/master version?
Sort of...
As of Jan 2023: 
- the latest release of Klipper is 0.11.0, available 28 Nov 2022.
- the Desuuuu fork was last updated with Klipper 0.10.0, available 29 Sept 2022.
- On 25 Jan 2023, Thinkersbluff was able to update the Klipper in this fork to 0.11.0, by merging this repo with [another fork of Klipper3D/Master maintained by gbkwiatt](https://github.com/gbkwiatt/klipper)

Worst-case, however, this solution may someday be limited to exploiting [the features and capabilities of Klipper at the last release with which we were able to merge without conflict](https://github.com/Thinkersbluff/dgus-reloaded_klipper/blob/DGUS-ReloadedForCR6/docs/Releases.md). 
e.g. At some future release of Klipper, changes to the klipper.bin or Make Menuconfig functionality may render non-functional the pre-built klipper.bin files available here.

Unfortunately, Moonraker flags installations of this repo (e.g. by configuring KIAUH to install Klipper from this repo instead of from the Klipper3D/Master github) as being "Invalid". That means that either:  
1. We have to keep merging this version with the Klipper3D/master repo and manually updating our systems, 
OR 
2. We need to be able to install DGUS-Reloaded (t5uid1) into the ~/klipper/klippy/extras folder and let Moonraker maintain our Klipper installation from the Klipper3D/master github.

## Can I Install the Latest Klipper from Klipper3D/master and STILL Use DGUS-Reloaded for CR6?
Yes, you can!

It is NOT actually necessary to use ALL of this modified Klipper, to make the DGUS-Reloaded display function work on your system.

There are basically TWO modifications made to Klipper, in this repo:  

1. **The T5UID1 folder adds the DGUS-Reloaded Python scripts to the ~/klipper/klippy/extras folder of Klipper.**  
 The DGUS_Reloaded DWIN_SET application is programmed to interact with those scripts, to provide a User Interface (UI) on the stock DWIN TFT. You can just copy that folder to the ~/klipper/klippy/extras folder of ANY Klipper installation, you do  NOT need to clone this entire modified Klipper to your system.

2. **Some of the Make Menuconfig files have also been modified, to enable you to build your own klipper.bin file.**  
When Desuuu created his fork, he set it up as a complete modified fork of Klipper, to enable a wide range of users  to build their own klipper.bin file. 
I, on the other hand, am ONLY providing a working DGUS-Reloaded setup for ONE Creality printer family (CR6-MAX and SE.)  I have therefore already built, tested, and uploaded the klipper.bin files (One for each of the four motherboards designed to work with the CR6 printer). You do NOT need to build your own.  

## Guidelines for How to Install DGUS-Reloaded with the Latest Klipper
Rather than install the full modified Klipper from this repository, with DGUS-Reloaded already installed, you can instead follow these instructions to first install the latest Klipper and then add the DGUS-Reloaded functionality.  That way, Moonraker will automatically maintain your Klipper installation.

1. Download and unzip the Source.zip file for the latest release on this repository. (NOTE: The file and folder names in Sources.zip are quite verbose, so you will first need to significantly shorten the top-level folder name in the zipfile ((e.g. to DGUS-Reloaded), to successfully "extract all" the contents.)
2. If you have not already done so, now create a Linux computer host for Klipper.  (NOTE: If you already have the Klipper/Mainsail host configured and are now updating it to use DGUS-Reloaded, then skip to step 6.)

There are many options for the Klipper host computer and it would greatly complicate these instructions if I tried to try to cover them all.  
For simplicity's sake, I will assume you are using a single Raspberry Pi Single Board Computer as your host.

3. There are two particularly easy ways to install Klipper with a Mainsail front-end, on a Raspberry Pi.  
   Both methods are supported by the Raspberry Pi Imager software. Download and install the appropriate version from here: [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

4. To install MainsailOS (recommended), navigate to [https://docs-os.mainsail.xyz/](https://docs-os.mainsail.xyz/) and follow their instructions.
  OR  
   To use KIAUH (which may be easier if using a laptop or desktop computer as the Klipper host), navigate to [https://github.com/th33xitus/kiauh](https://github.com/th33xitus/kiauh) and follow those instructions.

Once you have installed Klipper and Mainsail, you should be able to browse to your Klipper host in the Mainsail front-end, to finish the installation and configuration:   

5. In the "Related Changes" folder from the unzipped Source.zip archive, in the "Overwrite these Klipper host files" sub-folder of the motherboard sub-folder applicable to your printer,  find and unzip the applicable MACHINE_Configs....zip file.  
6. First read the ReadMe.txt file in the MACHINE_Configs....zip file, to familiarize yourself with the purpose of each file and note any changes made since the last release.  
7. Then copy the applicable files into ~/printer_data/config on your host processor **and configure them for your specific printer/preferences.**  
   **NOTES:**  
          a)  You can upload files to ~/printer_data/config via the Mainsail MACHINE tab, rather than messing about with SFTP and nano, if you prefer.  
          b)  You can use a utility like [Winmerge](https://winmerge.org/downloads/?lang=en) to compare the new files with existing files, if you prefer to selectively modify the existing files, rather than replacing them.  
          c) **You can completely ignore the KIAUH repos.txt file**    
8. Copy the t5uid1 folder and contents into the ~/klipper/klippy/extras directory on your host (e.g. by using an SFTP program logged into your host, to transfer those files from the folder DGUS-Reloaded_for_CR6-Klipper_Component-..../klippy/extras that you extracted from the downloaded release zip file on your system.)
9. Follow the instructions on [https://github.com/matthewlloyd/Klipper-Stable-Z-Home](https://github.com/matthewlloyd/Klipper-Stable-Z-Home), to also install stable_z_home.py.  
10. In the "Related Changes" folder from the unzipped Source.zip archive, in the "Flash this to the motherboard" sub-folder of the motherboard sub-folder applicable to your printer,  find the  klipper.bin file and flash that file to your printer.
11. Restart your printer.
12. Restart Klipper.

Klipper should now connect with your mcu and Mainsail should support printing.  Until you have the matching DWIN_SET installed on your stock display, however, the display will still not function correctly.  

If instead you see error messages in Mainsail, you will need to resolve whatever problems are reported, until Klipper connects and reports "Ready".

## A Word Of Warning About Klipper Documentation
Please note that Klipper3D are very good about keeping [their online documentation](https://www.klipper3d.org/) up to date with their latest firmware.
This repo, however, is NOT up-to-the-minute with every change they release.  That latency can mean that some of their online instructions do not work with this version of Klipper.  The documentation in this repo is, however, "frozen" at the most recent version of Klipper with which we have merged.  

IF you elect to install this modified Klipper INSTEAD of the Klipper3D version, THEN I recommend that you ALWAYS:
 - use [this local copy of their documentation](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/blob/DGUS-ReloadedForCR6/docs/Overview.md), when seeking guidance on how this particular version of modified Klipper is used, if you have decided to install from here and not from Klipper3D/master.
 - use [the online Klipper documentation](https://www.klipper3d.org/), if you have installed Klipper from Klipper3D/master.
 
 ## How to Contribute To This Project

Please feel free to contribute ideas and feedback in the Discussions section.

Since some of the behaviour of the DGUS-Reloaded UI is controlled by the DWIN_SET app and some by this Klipper back-end, it will be "cleaner" to keep all Issues together on one repo.  If you believe you have found a bug in the way the DGUS-Reloaded UI works on your CR6 printer, please therefore navigate to [the Issues folder on the DWIN_SET repo](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues).  If there is no existing open or closed Issue that describes the same issue, then please raise a new Issue there.  

CR6Community Firmware features NOT present in this release may be developed in future releases, but no schedule commitment is possible for such extensions.  Users who are able to define and develop such modifications are welcome to fork this repository and to submit Pull Requests or to open Discussions or Issues as appropriate, to propose those changes.

 One "future-proofing" option that comes to mind, for instance, is to pre-compile the Klipper.bin files and package the actual UI interface component (klippy/extras/t5uid1) as a py wheel to be installed into the Klipper3D/master version of Klipper with pip. 

> **If there are CR6Community members who are both capable and willing to take on the challenge of helping to future-proof this fork, please let me know in the Discussions section of this repo.  I am certainly open to reviewing PRs.**


## Is There Another Way to Re-Activate My Stock CR6 Display on Klipper?

If figuring out how to install and configure your system to work with this firmware is too difficult for you, but you still want a way to reuse your stock CR6 DWIN display, you may prefer trying [this alternative approach](https://github.com/Thinkersbluff/Klipper-dgus_CR6), which uses a separate serial interface to the display and the Moonraker API.  I only have the bandwidth to focus on this project or that one, but it is in my mind to try to someday develop a single DWIN_SET app that is compatible with either serial interface solution, if such a thing is desireable and possible.    

## Recommended References
To learn more about Klipper3d.org and about the DGUS-RELOADED project, you are strongly encouraged to follow these links:

### All about Klipper3D, in their own words  
[![Klipper](docs/img/klipper-logo-small.png)](https://www.klipper3d.org/)  https://www.klipper3d.org/

### The DGUS-RELOADED Klipper Project, by Desuuuu  
 https://github.com/Desuuuu/Klipper
 
#### Additional useful info is available in the Desuuuu/DGUS-reloaded-Klipper-config Wiki
* [Flashing the firmware](https://github.com/Desuuuu/DGUS-reloaded-Klipper/wiki/Flashing-the-firmware)
* [Print status](https://github.com/Desuuuu/DGUS-reloaded-Klipper/wiki/Print-status)
* [Print progress display](https://github.com/Desuuuu/DGUS-reloaded-Klipper/wiki/Print-progress-display)

 ### The Klipper-DGUS project, by SEHO85 (BUZZ-T on the CR6Community Discord)
 This project is the "alternative approach" to which I refer, above.
  - His GitHub project is here: https://github.com/seho85/klipper-dgus
  - The CR6-compatible fork of his DWIN_SET UI is here: https://github.com/Thinkersbluff/Klipper-dgus_CR6
  
