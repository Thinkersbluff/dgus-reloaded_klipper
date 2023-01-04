# Welcome to the Klipper for CR6 Printers project!

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
To enable that functionality, it was necessary to edit a few of the Desuuuu/Klipper files.

Unfortunately, when using Moonraker Update Manager to keep all of my system and application files up to date, I could not find a way to configure the Moonraker Update Manager to stop it reverting my modified files back to the Desuuuu versions, nor could I find a way to get it to automatically keep the modified Klipper installation up to date.  I was also not willing to wait and hope for Desuuuu to implement Pull Requests against his master version, to get this CR6 project rolling.  

The best option seemed to be to establish this CR6-specific master repository, from which Moonraker can keep DGUS-Reloaded for CR6 installations of Klipper up to date. 


## Additional Recommended Reading
To learn more about Klipper3d.org and about the DGUS-RELOADED project, you are strongly encouraged to follow these links:

### All about Klipper3D, in their own words
[![Klipper](docs/img/klipper-logo-small.png)](https://www.klipper3d.org/)  https://www.klipper3d.org/

### The DGUS-RELOADED Klipper Project, by Desuuuu

 https://github.com/Desuuuu/Klipper
