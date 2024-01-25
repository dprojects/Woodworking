# Description

FreeCAD is great software and this is extension for Woodworking. The main goal for this workbench is to make furniture designing process at FreeCAD more simple.

![intro](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/intro.gif)

* **Furniture from scratch & redesign:** [YouTube playlist](https://www.youtube.com/playlist?list=PLSKOS_LK45BBHkWPjdWX49qh-GEsF511v)
* **Cut-list, BOM, dimensions:** [YouTube playlist](https://www.youtube.com/playlist?list=PLSKOS_LK45BCnwvCGt4klfF6uVAxfQQTy)
* **Joinery examples:** [YouTube playlist](https://www.youtube.com/playlist?list=PLSKOS_LK45BBG8kJ2AZvQKBfOSfzhTrLt)
* **Parametrization solutions:** [YouTube playlist](https://www.youtube.com/playlist?list=PLSKOS_LK45BCzvg_B7oSTk1IsQnu5thtZ)
* **Workbench features & development:** [YouTube playlist](https://www.youtube.com/playlist?list=PLSKOS_LK45BDiLCETxbH_PV-uN3RAA0qz)

* **Woodworking workbench YouTube channel:** [all videos](https://www.youtube.com/@dprojects.woodworking/videos)
* **Woodworking workbench documentation:** [Woodworking/Docs](https://github.com/dprojects/Woodworking/tree/master/Docs)

# Release notes

**New significant changes since the last stable version:**

* nothing yet...

# Installation

**Step 0. Install correct FreeCAD version:**

* Download and install: [FreeCAD 0.21.2](https://github.com/FreeCAD/FreeCAD/releases/tag/0.21.2)

**Step 1. Get FreeCAD Mod folder localization:**

* From FreeCAD python console run command:

		FreeCAD.ConfigDump()["UserAppData"]

* If there is no `Mod` folder, create it.

**Step 2. Install Woodworking workbench:** 

* Go to FreeCAD `Mod` directory, for example, in Xubuntu operating system:

		cd  ~/.local/share/FreeCAD/Mod/

* Get the latest Woodworking workbench repository:

		git clone https://github.com/dprojects/Woodworking.git

**Step 2. Installation in other operating systems:**

* Download and unpack `Woodworking` repository.
* Copy the folder `Woodworking` to the FreeCAD module directory (`Mod` folder).

**Note:** You can update this workbench later via [debuginfo](https://github.com/dprojects/Woodworking/tree/master/Docs#debuginfo) tool.

# Certified platforms

* Stable certified versions download at: [Woodworking/releases](https://github.com/dprojects/Woodworking/releases)
* For cutting edge features download: [the master branch](https://github.com/dprojects/Woodworking/archive/refs/heads/master.zip)

* Current development platform:

		OS: Ubuntu 22.04.3 LTS (XFCE/xubuntu)
		Word size of FreeCAD: 64-bit
		Version: 0.21.2.33771 (Git) AppImage
		Build type: Release
		Branch: (HEAD detached at 0.21.2)
		Hash: b9bfa5c5507506e4515816414cd27f4851d00489
		Python 3.10.13, Qt 5.15.8, Coin 4.0.0, Vtk 9.2.6, OCC 7.6.3
		Locale: English/United States (en_US)
		Installed mods: 
		* Woodworking 0.21.2.33771

**Note:**

* I don't have `Windows` or `macOS`, so I am not able to test and certify this workbench for those systems. However, if you use `FreeCAD AppImage` there is big chance this will be working correctly.
* To get better stability make sure your current Woodworking workbench version has always the same version number as the FreeCAD version. You can also verify this via [debuginfo](https://github.com/dprojects/Woodworking/tree/master/Docs#debuginfo) tool. 

# Known issues

* **Issue**: Cut-list, BOM, report `toPrint` is not in the center of the page. 
	* **Workaround**: FreeCAD 0.21.2 has bug related to the TechDraw template. The TechDraw template size is always zero, so the center of the page cannot be calculated correctly. If this is issue for you, can adjust the report manually or please try higher FreeCAD version with this bug fixed (0.22).

# Extras

This woodworking workbench is delivered with several useful extras:

* [Fully parametric examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Parametric) - this folder inside woodworking workbench contains sample furniture projects. All of the furniture examples are parametric. So, you can quickly adopt it to your current project, without designing e.g. bookcase from scratch. You can also add decoration, if needed, or even merge with other projects.
* [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture) - this is new approach to 3D modeling. For example you can replace any Cylinder with realistic looking detailed screw. This is very powerful feature and gives a lot of flexibility and simplifies the process of making model detailed.
* [Texture samples](https://commons.wikimedia.org/w/index.php?title=Special:ListFiles/Dprojects&ilshowall=1) - sample textures for woodworking projects purposes.

# API for developers

The Woodworking workbench has also API for developers. This library contains functions that solve the Topology Naming Problem. You can also leaglly create your own tools and extend the workbench in your private repository in accordance with the MIT license:
	
* **View library API documentation:** [MagicPanelsAPI.md](https://github.com/dprojects/Woodworking/blob/master/Docs/MagicPanelsAPI.md)
* **View library code:** [MagicPanels.py](https://github.com/dprojects/Woodworking/blob/master/Tools/MagicPanels/MagicPanels.py)
* **Download & install library:** [raw version](https://raw.githubusercontent.com/dprojects/Woodworking/master/Tools/MagicPanels/MagicPanels.py)

**Note:**

* If you have Woodowrking workbench installed you don't have to install the `MagicPanels` library manaually. Also you can view the library directly from Woodworking workbench via: [scanObjects](https://github.com/dprojects/Woodworking/tree/master/Docs#scanobjects) tool.
* For programming I use simple [Krusader](https://en.wikipedia.org/wiki/Krusader) with `F4` [KWrite](https://en.wikipedia.org/wiki/KWrite) editor. I have set tabulators as indent: `Settings` -> `Configure Editor` -> `Editing` -> `Indentation` -> `Tabulators` -> `Tab width: 4 characters`.

# Translations

For Woodworking workbench translation see dedicated directory: [translations](https://github.com/dprojects/Woodworking/tree/master/translations)

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
