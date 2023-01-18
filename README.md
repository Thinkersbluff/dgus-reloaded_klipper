# DGUS-reloaded-Klipper (modified), CR6Community Edition!
The Klipper in this repo is a fork of Klipper3D Release 0.10.0, which has been modified - [largely by Desuuuu](https://github.com/Desuuuu/klipper), and a little bit more by me - to work with the DGUS-reloaded DWIN_SET for CR6 printers located in [this companion repo.](https://github.com/Thinkersbluff/DGUS-reloadedForKlipper_CR6)

This repo is forked from [the master DGUS-RELOADED project repository](https://github.com/Desuuuu/Klipper) maintained by Desuuuu.
The Desuuuu repo is in-turn forked from [the master Klipper3D.org github repository.](https://github.com/Klipper3d/klipper/)

>>**NOTE:** Desuuuu has also indicated that he intends to stop maintaining his dgus-reloaded-klipper fork, soon, so I am looking for CR6Community help to take over keeping this fork up to date with future releases of Klipper. (See **How to Contribute**, below)

## Who should __NOT__ use this firmware?
If your goal is to run Klipper on your CR6 without using the stock T5L DWIN display hardware, **then you do not need this modified version of Klipper.**
Just install the master Klipper3D.org version and configure it for your CR6 printer per the [Klipper3d.org installation and configuration documentation](https://github.com/Klipper3d/klipper/blob/master/docs/index.md).  

This repository may be very helpful for you: https://github.com/KoenVanduffel/CR-6_Klipper

## Why Not Just Use the Desuuuu/Klipper version?
Some of the functionality implemented in the CR6-specific UI is not present or is organized differently, in the Desuuuu companion display app.
To enable the CR6 UI functionality, it is necessary to edit a few of the Desuuuu/Klipper files, for which I needed to make my own (this) fork.

## How to Install This (Modified) Klipper Instead of the Version at Klipper3D/master

### Recommended Tools:
1. An SSH Client (e.g. PUTtY, for Windows)  
![Untitled-2](https://user-images.githubusercontent.com/36551518/213055863-567e1659-3c46-4944-a5a6-8dd691d03288.png)
2. An SFTP Client (e.g.FileZilla)  
![Untitled-2](https://user-images.githubusercontent.com/36551518/213055590-0c6425ec-da98-4c16-a27d-fe6c14263406.png)
3. Klipper Installation And Update Helper (KIAUH)   
![Untitled-1](https://user-images.githubusercontent.com/36551518/213055141-1b9cad6e-f19e-4cfd-a6a0-a1bf9ef87895.png)


### 'Step-by-Step*' Instructions (*Some steps may be bigger than others...):
1. Install KIAUH on your Klipper host.
   (I recommend you use [KIAUH](https://github.com/th33xitus/kiauh) to manage this installation, so that is the ONLY way I will describe here, to keep this as simple as possible.)
2. In the folder "Related Changes", I have provided a file called, "klipper_repos.txt".  Copy that file into the kiauh folder on your Klipper Host before you launch KIAUH.  That file will allow you to point KIAUH to this eepository to download Klipper.
3. Launch KIAUH
4. Enter '4' to navigate to Advance Settings
5. Enter '0' to select this repo as the source for Klipper
6. KIAUH will ask you to confirm that it should now remove any existing Klipper installation and install this one.  Enter "Y" for "Yeah, man, let's do this"
7. When KIAUH is finished, enter 'B' to go Back to the main menu and 'Q' to Quit KIAUH.

This modfied version of Klipper will now be installed on your Klipper Host.

8. While you are still logged into your Klipper host, let's install STABLE_Z_HOME.py.
9. Navigate to the Klippy/extras folder on the host ($ cd ~/klipper/klippy/extras)
10. Enter this command: $ ln -s ~/Klipper-Stable-Z-Home/stable_z_home.py
11. Verify that you now see stable_z_home.py in the klippy/extras folder on your host.  

12. Also provided in the Related Changes folder is a copy of the Klipper.bin file for the BTT SKR CR6 and Creality ERA 1.1.0.3 or 4.5.3 board. If you have either of those motherboards, copy the appropriate bin file onto an SD card and flash that to your motherboard.
>> If you have a 4.5.2 board, we have not yet captured a Klipper.bin file for you.  Please use _make menuconfig_ to create a Klipper.bin file for the 4.5.2 board and flash that to your motherboard. (When you have confirmed that it works, please upload a copy in a Discussion on this repo, along with a screenshot of the Make Menuconfig screen that worked for configuring it, so that we can share those files in future.)  

13. Now review the Klipper configuration files in the Related Changes folder corresponding to your motherboard (again, apologies to 4.5.2 users; we don't have that info for you, yet...)
    Update your existing Klipper config files as appropriate, to configure your system to work with this version of Klipper and your preferred workflow.
>> Sorry - way too many possible combiations and permutations for me to walk you through this part.  Hoping you can figure it out on your own.  Post questions if you have specific problems you can not work out. Hopefully someone else has a good answer for you.    

## Is This Klipper Fork Using the latest Klipper3D/master version?
No.  
As of Jan 2023: 
- the latest release of Klipper is 0.11.0, available 28 Nov 2022.
- Klipper3D are also signalling there may be a new Klipper release in Feb 2023
- the Desuuuu fork was last updated with Klipper 0.10.0, available 29 Sept 2022.
- this CR6Community Edition is a fork of the Desuuuu fork.

Worst-case, this solution may always be limited to exploiting [the features and capabilities of Klipper at release 0.10.0](https://github.com/Thinkersbluff/dgus-reloaded_klipper/blob/DGUS-ReloadedForCR6/docs/Releases.md).

Because of the customizations in some of the klipper/src/ files, updating this fork is not as simple as using GitHub to merge this repo with the Klipper3D master branch.  If and when Desuuuu updates his fork, I will certainly update this one, but I have neither the expertise nor the time to decipher the conflicts introduced by recent upstream mods to the stm32 serial interface modules. 
 
 ## How to Contribute

CR6Community Firmware features NOT present in this release may be developed in future releases, but no schedule commitment is possible for such extensions.  Users who are able to define and develop such modifications are welcome to fork this repository and to submit Pull Requests or to open Discussions or Issues as appropriate, to propose those changes.

 One "future-proofing" option that comes to mind, for instance, is to pre-compile the Klipper.bin files and package the actual UI interface component (klippy/extras/t5uid1) as a py wheel to be installed into the Klipper3D/master version of Klipper with pip. 

> **If there are CR6Community members who are both capable and willing to take on the challenge of helping to future-proof this fork, please let me know in the Discussions section.  I am certainly open to reviewing PRs.**

## Is There Another Way to Re-Activate My Stock CR6 Display on Klipper, Without Getting Locked-in to Klipper 0.10.10?

If being "locked-in" to Klipper v0.10.0 is not ok for you, but you still want a way to reuse your stock CR6 DWIN display, you may prefer trying [this alternative approach](https://github.com/Thinkersbluff/Klipper-dgus_CR6), which uses a separate serial interface to the display and the Moonraker API.  I only have the bandwidth to focus on this project or that one, but it is in my mind to try to develop a single DWIN_SET app that is compatible with either serial interface solution, if such a thing is possible.    

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
  
