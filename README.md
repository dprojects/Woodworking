# Description

The main goal for this workbench is to make simpler the furniture designing process in FreeCAD.

![intro](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/intro.gif)

# Quick start

1. Download FreeCAD 0.21.2 for Xubuntu: [FreeCAD-0.21.2-Linux-x86_64.AppImage](https://github.com/FreeCAD/FreeCAD/releases/download/0.21.2/FreeCAD-0.21.2-Linux-x86_64.AppImage)
2. Download the latest Woodworking workbench version: [the master branch](https://github.com/dprojects/Woodworking/archive/refs/heads/master.zip)
3. Unpack Woodworking workbench to `Mod` folder, the `README.md` file should be: `~/.local/share/FreeCAD/Mod/Woodworking/README.md`
4. Start `FreeCAD-0.21.2-Linux-x86_64.AppImage` file

# Documentation

**Woodworking workbench documentation:** [Woodworking/Docs](https://github.com/dprojects/Woodworking/tree/master/Docs)

**YouTube playlists:**

* [How-to & Tutorials](https://www.youtube.com/playlist?list=PLSKOS_LK45BAP3JmYWzraTHqb0tAeONkf) - explains a little bit how-to use tools
* [Furniture from scratch & redesign](https://www.youtube.com/playlist?list=PLSKOS_LK45BBHkWPjdWX49qh-GEsF511v) - shows how quickly you can design furniture from scratch and redesign, this is not tutorial step by step
* [Cut-list, BOM, dimensions](https://www.youtube.com/playlist?list=PLSKOS_LK45BCnwvCGt4klfF6uVAxfQQTy) - shows how you can create cut-list, BOM and get dimensions
* [Joinery examples](https://www.youtube.com/playlist?list=PLSKOS_LK45BBG8kJ2AZvQKBfOSfzhTrLt) - all videos related to joinery connections, mounting points
* [Parameterization solutions](https://www.youtube.com/playlist?list=PLSKOS_LK45BCzvg_B7oSTk1IsQnu5thtZ) - explains how to approach this problem
* [Workbench features & development](https://www.youtube.com/playlist?list=PLSKOS_LK45BDiLCETxbH_PV-uN3RAA0qz) - all the latest features and development videos

**Woodworking workbench YouTube channel:** [youtube.com/@dprojects.woodworking](https://www.youtube.com/@dprojects.woodworking/videos)

# Extras

This woodworking workbench is delivered with several useful extras:

* [Fully parametric examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Parametric) - this folder inside woodworking workbench contains sample furniture projects. All of the furniture examples are parametric. So, you can quickly adopt it to your current project, without designing e.g. bookcase from scratch. You can also add decoration, if needed, or even merge with other projects.
* [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture) - this is new approach to 3D modeling. For example you can replace any Cylinder with realistic looking detailed screw. This is very powerful feature and gives a lot of flexibility and simplifies the process of making model detailed.
* [Texture samples](https://commons.wikimedia.org/w/index.php?title=Special:ListFiles/Dprojects&ilshowall=1) - sample textures for woodworking projects purposes.

# Support FreeCAD 1.0 and later

Currently there are no plans to support FreeCAD 1.0 and later. The main reason for that is that FreeCAD 1.0 no longer allows for direct Sketch move and the [FreeCAD team consider direct Sketch moving as bug](https://forum.freecad.org/viewtopic.php?p=794690#p794690), so they fixed this "bug"... 

For more information see: [issue about FreeCAD 1.0+ support](https://github.com/dprojects/Woodworking/issues/49)

# Translations

Translations are developed at [github.com/dprojects/Woodworking-translations](https://github.com/dprojects/Woodworking-translations) repository and are created only for [Woodworking workbench releases](https://github.com/dprojects/Woodworking/releases). This approach allows the translator community to work without time pressure and independently of the development of the main branch, because the code of stable releases will not be changed.

### Woodworking workbench release 0.21

To install translation for [Woodworking workbench release 0.21](https://github.com/dprojects/Woodworking/releases/tag/0.21) you have to download all `.qm` files from [0.21 translations branch](https://github.com/dprojects/Woodworking-translations/tree/0.21), if there such any, and move them to `translations` folder inside Woodworking workbench folder. You can also create your own translations.

### Woodworking workbench release 0.22 and above

You can use `translations update tool` available under drop down menu `Woodworking -> Download and update all translations`. This tool will automatically download all available `.qm` files into `translations` folder for you Woodworking workbench release.

# Installation step by step

### Step 0. Install correct FreeCAD version:

* Recommended version for Xubuntu: [FreeCAD-0.21.2-Linux-x86_64.AppImage](https://github.com/FreeCAD/FreeCAD/releases/download/0.21.2/FreeCAD-0.21.2-Linux-x86_64.AppImage)
* For other operating systems download and install: [FreeCAD 0.21.2](https://github.com/FreeCAD/FreeCAD/releases/tag/0.21.2)

**Note:** 

I don't have `Windows` or `macOS`, so I am not able to test and certify this workbench for those systems. However, if you use `FreeCAD AppImage` there is a good chance this will be working correctly.

### Step 1. Download Woodworking workbench:

* Stable certified versions download at: [Woodworking/releases](https://github.com/dprojects/Woodworking/releases)
* For cutting edge features download: [the master branch](https://github.com/dprojects/Woodworking/archive/refs/heads/master.zip) or run command:
	
		git clone https://github.com/dprojects/Woodworking.git

	**New significant changes since the last release 0.22 stable:**

	* Move to Equal feature to set equal space between objects along X, Y or Z (magicMove)
	* panelCopy feature improved to start at face, edge or vertex
	* side fit into the gap, by width, by offsets, X or Y plane (magicStart)
	* table solutions, kitchen or coffee, simple, modern and decorated style (magicStart)
	* shelvesEqual tool to set equal space between existing shelves
	* panelMove2Face improve to adjust position with object size
	* shelf series to create shelves into gap with equal space (magicStart)
	* front with glass, simple and decorated, outside or inside, fit into gap (magicStart)
	* improve magicMeasure (new GUI, descriptions, auto preselection recognize, vertices size)
	* face frame (around, with center bar, with horizontal bar) and predefined furniture (magicStart)
	* tool to quickly add or remove expressions for position and size (magicGlue)
	* drawer series feature to create many drawers at once (magicStart)
	* magicMove improvements (container, auto object type, translation, cross save, fixes)
	* add edge, face, vertex reference to Mirror feature (magicMove)
	* feature Copy by Edge to copy part of the furniture (magicMove)
	* new laveder color for API inspection tool (scanObjects)
	* building complex furniture from modules by selected edge, face, vertex or custom offset (magicStart)
	* center side for selected gap by depth, by offsets, custom offsets, automatically adjusted (magicStart)
	* shelf for selected gap by depth, by offsets, custom offsets, automatically adjusted (magicStart)
	* front outside or inside for selected gap (magicStart)
	* drawer with front outside or inside for selected gap (magicStart)
	* foot solutions (magicStart)
	* magicDowels improved (GUI redesign, position autodetect, keep settings, menu translation, fixes)
	* magicStart tool to create & import furniture, fixture, drawers, ...

### Step 2. Get FreeCAD Mod folder localization:

* From FreeCAD python console run command:

		FreeCAD.ConfigDump()["UserAppData"]

* If there is no `Mod` folder, create it.

### Step 3. Install Woodworking workbench:

* Go to FreeCAD `Mod` folder, for example, in Xubuntu operating system:

		cd  ~/.local/share/FreeCAD/Mod/

* Unpack woodworking workbench, if needed, and copy `Woodworking` folder directly to `Mod` folder. This should be:

		~/.local/share/FreeCAD/Mod/Woodworking/

**Note:**

* You can update this workbench later via [debuginfo](https://github.com/dprojects/Woodworking/tree/master/Docs#debuginfo) tool.
* To get better stability make sure your current Woodworking workbench version has always the same prefix version number as the FreeCAD version. You can also verify this via [debuginfo](https://github.com/dprojects/Woodworking/tree/master/Docs#debuginfo) tool. 

# API for developers

The Woodworking workbench also has an API for developers. This library contains functions that [solve the Topology Naming Problem](https://wiki.freecad.org/Macro_TNP_Solution). You can also leaglly create your own tools and extend the workbench in your private repository in accordance with the MIT license:
	
* **View library API documentation:** [MagicPanelsAPI.md](https://github.com/dprojects/Woodworking/blob/master/Docs/MagicPanelsAPI.md)
* **View library code:** [MagicPanels.py](https://github.com/dprojects/Woodworking/blob/master/Tools/MagicPanels/MagicPanels.py)
* **Download & install library:** [raw version](https://raw.githubusercontent.com/dprojects/Woodworking/master/Tools/MagicPanels/MagicPanels.py)

**Note:**

* If you have Woodworking workbench installed you don't have to install the `MagicPanels` library manaually. Also you can view the library directly from Woodworking workbench via: [scanObjects](https://github.com/dprojects/Woodworking/tree/master/Docs#scanobjects) tool.
* For programming I use simple [Krusader](https://en.wikipedia.org/wiki/Krusader) with `F4` [KWrite](https://en.wikipedia.org/wiki/KWrite) editor. I have set tabulators as indent: `Settings` -> `Configure Editor` -> `Editing` -> `Indentation` -> `Tabulators` -> `Tab width: 4 characters`.

# License

[MIT](https://github.com/dprojects/Woodworking/blob/master/LICENSE) for all Woodworking workbench content.

# Contact

* For questions, feature requests, please open issue at: [github.com/dprojects/Woodworking/issues](https://github.com/dprojects/Woodworking/issues)

|   |   |
|---|---|
| [![c1r1](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r1.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r1.png) | [![c2r1](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r1.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r1.png) |
| [![c1r2](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r2.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r2.png) | [![c2r2](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r2.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r2.png) |
| [![c1r3](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r3.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r3.png) | [![c2r3](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r3.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r3.png) |
| [![c1r4](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r4.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r4.png) | [![c2r4](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r4.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r4.png) |
