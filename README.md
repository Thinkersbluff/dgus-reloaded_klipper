# Welcome to the Klipper for CR6Community Printers project!

This repo is forked from [the master DGUS-RELOADED project repository](https://github.com/Desuuuu/Klipper) maintained by Desuuuu.
The Desuuuu repo is in-turn forked from [the master Klipper3D.org github repository.](https://github.com/Klipper3d/klipper/)

The goal of this (Klipper for CR6 Printers) project is to establish and maintain a stable version of the DGUS-RELOADEDForCR6 version of Klipper which works with the DGUS-reloadedForKlipper_CR6 DWIN_SET UI in [this companion repository](https://github.com/Thinkersbluff/DGUS-reloadedForKlipper_CR6). 

The DGUS-reloadedForKlipper_CR6 UI has been specifically customized to run in portrait mode on stock CR6 T5L 272x480 DWIN displays. It has also been programmed to integrate and interact with the modified version of Klipper in this repository, which defines and implements the controls and data displays programmed into the UI.

## Who should __NOT__ use this firmware?
If your goal is to run Klipper on your CR6 without using the stock T5L DWIN display hardware, **then you do not need this modified version of Klipper.**
Just install the master Klipper3D.org version and configure it for your CR6 printer per the [Klipper3d.org installation and configuration documentation](https://github.com/Klipper3d/klipper/blob/master/docs/index.md).

This repository may be very helpful for you: https://github.com/KoenVanduffel/CR-6_Klipper

## Why Not Just Use the Desuuuu/Klipper version?
Some of the functionality implemented in the CR6-specific UI is not present or is organized differently, in the Desuuuu companion display app.
To enable that functionality, it is necessary to edit a few of the Desuuuu/Klipper files, for which I needed to make my own (this) fork.

## Is This Klipper Fork Using the latest Klipper3D/master version?
No.  
As of Jan 2023: 
- the latest release of Klipper is 0.11.0, available 28 Nov 2022.
- the Desuuuu fork was last updated with Klipper 0.10.0, available 29 Sept 2022.
- this CR6Community Edition is a fork of the Desuuuu fork.

Worst-case, this solution may always be limited to exploiting [the features and capabilities of Klipper at release 0.10.0](https://github.com/Thinkersbluff/dgus-reloaded_klipper/blob/DGUS-ReloadedForCR6/docs/Releases.md).

Because of the customizations in some of the klipper/src/ files, updating this fork is not as simple as using GitHub to merge this repo with the Klipper3D master branch.  If and when Desuuuu updates his fork, I will certainly update this one, but I have neither the expertise nor the time to decipher the conflicts introduced by recent upstream mods to the stm32 serial interface modules. (If there are CR6Community members who are both capable and willing to take on that challenge, please let me know in the Discussions section.  I am certainly open to reviewing PRs.)

## Is There Another Way to Re-Activate My Stock CR6 Display on Klipper, Without Getting Locked-in to Klipper 0.10.10?

If being "locked-in" to Klipper v0.10.0 is not ok for you, but you still want a way to reuse your stock CR6 DWIN display, you may prefer trying [this alternative approach](https://github.com/Thinkersbluff/Klipper-dgus_CR6), which uses a separate serial interface to the display and the Moonraker API.  I only have the bandwidth to focus on this project or that one, but it is in my mind to try to develop a single DWIN_SET app that is compatible with either serial interface solution, if such a thing is possible.    

## Recommended References
To learn more about Klipper3d.org and about the DGUS-RELOADED project, you are strongly encouraged to follow these links:

### All about Klipper3D, in their own words
[![Klipper](docs/img/klipper-logo-small.png)](https://www.klipper3d.org/)  https://www.klipper3d.org/

### The DGUS-RELOADED Klipper Project, by Desuuuu
 https://github.com/Desuuuu/Klipper
 
 ### The Klipper-DGUS project, by SEHO85 (BUZZ-T on the CR6Community Discord)
 This project is the "alternative approach" to which I refer, above.
  - His GitHub project is here: https://github.com/seho85/klipper-dgus
  - The CR6-compatible fork of his DWIN_SET UI is here: https://github.com/Thinkersbluff/Klipper-dgus_CR6
  
