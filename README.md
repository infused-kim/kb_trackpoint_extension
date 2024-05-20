# TrackPoint Extensions

OpenSCAD scripts that generate TrackPoint extensions that can be used in DIY keyboards.

## Table Of Contents <!-- omit from toc -->

- [1. Photos](#1-photos)
- [2. Print Instructions](#2-print-instructions)
    - [2.1. Printing it yourself](#21-printing-it-yourself)
    - [2.2. Printing using JLC 3DP](#22-printing-using-jlc-3dp)
- [3. How to generate customized Extensions](#3-how-to-generate-customized-extensions)
- [4. How to add new TrackPoint models](#4-how-to-add-new-trackpoint-models)
- [5. Related Resources](#5-related-resources)
- [6. License](#6-license)

## 1. Photos

![TrackPoint Extensions Printed](img/tp_extensions_printed.jpg)

![TP Extension STL](img/tp_extension_3d.png)

## 2. Print Instructions

> [!NOTE]
> I am a complete beginner with 3D printing. So, take my advice below with caution. If you have suggestions on how to do this better, please let me know.

### 2.1. Printing it yourself

In my experience, resin 3D printers do a much better job than FDM.

At first, I tried two local companies that offered 3D printing services using FDM printers. However, they were not accurate enough to make the extension hole fit the TrackPoints without cutting the hole bigger.

Next, I tried a company that used a resin printer with ABSLike material. This one was much more precise and the adapter hole fit well on the TP, but the material was too soft and cracked under pressure because the wall thickness at the corners was too small.

So, I increased the diameter of the adapter at the bottom of the extension and it worked much better. The current default for the diameter is 5mm, which means the wall thickness at the corners of the adapter hole is approximately 0.8mm.

I would prefer a thicker wall thickness, but my keyboard PCB's TrackPoint hole is only 5.5mm and I can't go bigger. So, if you design your own keyboard I recommend using a bigger hole.

You also have to consider how much space is between your switches, above the PCB. I am using choc switches with the corne stagger and 4mm is working well.

### 2.2. Printing using JLC 3DP

I have not tried this, but would probably use the resin SLA 8228 or 9000R materials due to the low tolerances and relatively high strength.

With JLC you can combine multiple parts into one file with sprues to get around their minimum cost. This way you can order 10 different versions with slightly different hole sizes and heights for approximately $1.30.

You can generate various stls with different options and then run `make combined` to generate one file with multiple designs like in the screenshot below.

But keep in mind that JLC will charge you an extra $1 per combined STL [as per their connected parts printing policy](https://jlc3dp.com/help/article/213-Connected-Parts-Printing-Guide).

![TrackPoint Extensions Sprued for JLC 3DP](img/tp_extensions_sprued.png)

## 3. How to generate customized Extensions

The OpenSCAD scripts have parameters that allow you to customize many aspects of the generated 3D files.

* Install OpenSCAD
  * The [snapshot version](https://openscad.org/downloads.html#snapshots) is recommended for performance reasons
  * If it crashes, [try an older version of the snapshot](https://files.openscad.org/snapshots/)
* Set up the dev environment
  * Adjust the Makefile with the path to your OpenSCAD installation
* Run the keycap generator
  * Run `make help` to see all available parameters
  * You can, for example, run `make tp_red_t460s ADAPTER_WIDTH_BOTTOM=6 ADAPTER_WIDTH_TOP=4 MOUNTING_DISTANCE=0.5 HOLE_INCR=0.3`.
  * Or run `make all <OPTIONS>` to build extensions for all defined TrackPoints

You can also open the individual files in the OpenSCAD GUI if you prefer to see a preview in the GUI instead of generating using make.

Here are all available options:

```shell
❯ make help

Help:

  You can customize the output using the following parameters with any of the targets below...

  To see the available targets run:
    make targets

  And then to run a target:
    make tp_red_t460s HOLE_INCR=0.2 HEIGHT=10.5

  You can also run multiple targets with the same parameters at once:
    make tp_red_t460s tp_green_t430 HOLE_INCR=0.2 HEIGHT=10.5

  Or you can build all targets with:
    make all HOLE_INCR=0.2 HEIGHT=10.5

Parameters:

  HOLE_INCR=0.2
    By how much you want to increase the adapter hole compared to the actual TP stem width.

  ADAPTER_WIDTH_BOTTOM=5 ADAPTER_WIDTH_TOP=4
    The width of the stem adapter below and above the PCB.

  HEIGHT=10.5
    The height from the pcb to where you want the cap to end.

  MOUNTING_DISTANCE=1.0
    How far the TP is mounted BELOW the PCB. This should include the thickness of any plastic or electrical tape you use to isolate the TP mount.

  PCB_HEIGHT=1.6
    Thickness of the pcb.

  TIP_INCR=0.3
    By how much you want to increase the tip for a tighter cap fit.

Available targets:
  tp_green_t430
  tp_green_t430_with_t460s_cap
  tp_red_t460s
  tp_red_t460s_with_dell_cap

  combined
    Combines all .stl files in stl/output into one stl with sprues for printing at JLC3DP.

  all
    Runs all targets (including combined)

  clean
    Removes all .stl and .log files from stl/output.
```

## 4. How to add new TrackPoint models

You can just duplicate an existing TrackPoint file, such as `src/export_tp_red_t460s.scad`, measure your TrackPoints dimensions, and adjust the variables in the file.

As long as your file starts with the prefix `export_`, it will automatically show up in omake as a target.

## 5. Related Resources

* [My TrackPoint Driver for DIY keyboards using the zmk firmware](https://github.com/infused-kim/kb_zmk_ps2_mouse_trackpoint_driver)
* [My TrackPoint Keycap Cutter](https://github.com/infused-kim/kb_keycaps_trackpoint)

## 6. License

**TLDR:**

* Personal use with attribution
* Commercial use not allowed

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
