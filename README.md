# Description

The main goal for this workbench is to make simpler the furniture designing process in FreeCAD.

![intro](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/intro.gif)

* **Furniture from scratch & redesign:** [YouTube playlist](https://www.youtube.com/playlist?list=PLSKOS_LK45BBHkWPjdWX49qh-GEsF511v)
* **Cut-list, BOM, dimensions:** [YouTube playlist](https://www.youtube.com/playlist?list=PLSKOS_LK45BCnwvCGt4klfF6uVAxfQQTy)
* **Joinery examples:** [YouTube playlist](https://www.youtube.com/playlist?list=PLSKOS_LK45BBG8kJ2AZvQKBfOSfzhTrLt)
* **Parametrization solutions:** [YouTube playlist](https://www.youtube.com/playlist?list=PLSKOS_LK45BCzvg_B7oSTk1IsQnu5thtZ)
* **Workbench features & development:** [YouTube playlist](https://www.youtube.com/playlist?list=PLSKOS_LK45BDiLCETxbH_PV-uN3RAA0qz)

* **Woodworking workbench YouTube channel:** [all videos](https://www.youtube.com/@dprojects.woodworking/videos)
* **Woodworking workbench documentation:** [Woodworking/Docs](https://github.com/dprojects/Woodworking/tree/master/Docs)

# Release notes

**New significant changes since the last release 0.22 stable:**

* shelf for selected gap by depth, by offsets, custom offsets, automatically adjusted (magicStart)
* front outside or inside for selected gap (magicStart)
* drawer with front outside or inside for selected gap (magicStart)
* foot solutions (magicStart)
* magicDowels improved (GUI redesign, position autodetect, keep settings, menu translation, fixes)
* magicStart tool to create & import furniture, fixture, drawers, ...

# Installation in Xubuntu

**Step 0. Install correct FreeCAD version:**

* Download and install: [FreeCAD 0.21.2](https://github.com/FreeCAD/FreeCAD/releases/tag/0.21.2)

**Step 1. Download Woodworking workbench:** 

* Stable certified versions download at: [Woodworking/releases](https://github.com/dprojects/Woodworking/releases)
* For cutting edge features download: [the master branch](https://github.com/dprojects/Woodworking/archive/refs/heads/master.zip) or run command:
	
		git clone https://github.com/dprojects/Woodworking.git

**Step 2. Get FreeCAD Mod folder localization:**

* From FreeCAD python console run command:

		FreeCAD.ConfigDump()["UserAppData"]

* If there is no `Mod` folder, create it.

**Step 3. Install Woodworking workbench:** 

* Go to FreeCAD `Mod` folder, for example, in Xubuntu operating system:

		cd  ~/.local/share/FreeCAD/Mod/

* Unpack woodworking workbench, if needed, and copy `Woodworking` folder to `Mod` folder. This should be:

		~/.local/share/FreeCAD/Mod/Woodworking/

**Note:**

* You can update this workbench later via [debuginfo](https://github.com/dprojects/Woodworking/tree/master/Docs#debuginfo) tool.
* To get better stability make sure your current Woodworking workbench version has always the same prefix version number as the FreeCAD version. You can also verify this via [debuginfo](https://github.com/dprojects/Woodworking/tree/master/Docs#debuginfo) tool. 

# Installation in other operating systems

* Download and unpack `Woodworking` repository.
* Copy the folder `Woodworking` to the FreeCAD `Mod` folder.

**Note:** I don't have `Windows` or `macOS`, so I am not able to test and certify this workbench for those systems. However, if you use `FreeCAD AppImage` there is a good chance this will be working correctly.

# Extras

This woodworking workbench is delivered with several useful extras:

* [Fully parametric examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Parametric) - this folder inside woodworking workbench contains sample furniture projects. All of the furniture examples are parametric. So, you can quickly adopt it to your current project, without designing e.g. bookcase from scratch. You can also add decoration, if needed, or even merge with other projects.
* [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture) - this is new approach to 3D modeling. For example you can replace any Cylinder with realistic looking detailed screw. This is very powerful feature and gives a lot of flexibility and simplifies the process of making model detailed.
* [Texture samples](https://commons.wikimedia.org/w/index.php?title=Special:ListFiles/Dprojects&ilshowall=1) - sample textures for woodworking projects purposes.

# API for developers

The Woodworking workbench also has an API for developers. This library contains functions that [solve the Topology Naming Problem](https://wiki.freecad.org/Macro_TNP_Solution). You can also leaglly create your own tools and extend the workbench in your private repository in accordance with the MIT license:
	
* **View library API documentation:** [MagicPanelsAPI.md](https://github.com/dprojects/Woodworking/blob/master/Docs/MagicPanelsAPI.md)
* **View library code:** [MagicPanels.py](https://github.com/dprojects/Woodworking/blob/master/Tools/MagicPanels/MagicPanels.py)
* **Download & install library:** [raw version](https://raw.githubusercontent.com/dprojects/Woodworking/master/Tools/MagicPanels/MagicPanels.py)

**Note:**

* If you have Woodworking workbench installed you don't have to install the `MagicPanels` library manaually. Also you can view the library directly from Woodworking workbench via: [scanObjects](https://github.com/dprojects/Woodworking/tree/master/Docs#scanobjects) tool.
* For programming I use simple [Krusader](https://en.wikipedia.org/wiki/Krusader) with `F4` [KWrite](https://en.wikipedia.org/wiki/KWrite) editor. I have set tabulators as indent: `Settings` -> `Configure Editor` -> `Editing` -> `Indentation` -> `Tabulators` -> `Tab width: 4 characters`.

# Translations

Translations are available at [github.com/dprojects/Woodworking-translations](https://github.com/dprojects/Woodworking-translations) repository and are created only for [Woodworking workbench releases](https://github.com/dprojects/Woodworking/releases). This approach allows the translator community to work without time pressure and independently of the development of the main branch, because the code of stable releases will not be changed.

### Woodworking workbench release 0.21

To install translation for [Woodworking workbench release 0.21](https://github.com/dprojects/Woodworking/releases/tag/0.21) you have to download all `.qm` files from [0.21 translations branch](https://github.com/dprojects/Woodworking-translations/tree/0.21), if there such any, and move them to `translations` folder inside Woodworking workbench folder. You can also create your own translations.

### Woodworking workbench release 0.22 and above

You can use `translations update tool` available under drop down menu `Woodworking -> Download and update all translations`. This tool will automatically download all available `.qm` files into `translations` folder for you Woodworking workbench release.

# Support FreeCAD 1.0 and later

Currently there are no plans to support FreeCAD 1.0 and later. 

The main reason for that is that FreeCAD 1.0 no longer allow for direct Sketch move, the [FreeCAD team consider direct Sketch moving as bug](https://forum.freecad.org/viewtopic.php?p=794690#p794690), so they fixed this "bug"... 

Using FreeCAD 1.0 with Woodworking workbench for example you can't use [magicMove](https://github.com/dprojects/Woodworking/tree/master/Docs#magicmove) to move Sketch or Pad. Also you can't move holes after drilling or center holes or Pads. So this "fix" impact many advanced features at Woodworking workbench.

However all these feature works fine with FreeCAD 0.21.2 and personally I don't see any reason to use FreeCAD 1.0. 
Also I am happy with FreeCAD 0.21.2 and I don't see any reason to chase all the FreeCAD team changes and "fixes" and adjust Woodworking workbench code only to have new FreeCAD number...

The Woodworking workbench now has its own [release versioning system](https://github.com/dprojects/Woodworking/releases), the 0.22 release has been published, and will be developed regardless of FreeCAD politics.

# License

[MIT](https://github.com/dprojects/Woodworking/blob/master/LICENSE) for all Woodworking workbench content.

# Contact

* For questions, comments, feature requests, improvements, please open issue at: [issue tracker](https://github.com/dprojects/Woodworking/issues)
* Also we can discuss at: [FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=3&t=8247)

|   |   |
|---|---|
| [![c1r1](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r1.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r1.png) | [![c2r1](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r1.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r1.png) |
| [![c1r2](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r2.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r2.png) | [![c2r2](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r2.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r2.png) |
| [![c1r3](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r3.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r3.png) | [![c2r3](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r3.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r3.png) |
| [![c1r4](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r4.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r4.png) | [![c2r4](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r4.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r4.png) |
