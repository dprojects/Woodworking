# Description

This is Woodworking workbench for FreeCAD. 

![features](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/features.gif)

**Note:**

It has been created because of my woodworking and coding hobby. Everything started from [getDimensions](https://github.com/dprojects/getDimensions/commits/master) project long time ago. I wanted to have [simple cut-list for chipboards order](https://github.com/dprojects/getDimensions/commit/a6f0a2221e90f717be95bd0dc1cc9f1ede95a329) and I found FreeCAD with low hardware requirements and possibility to implement the cut-list. Now it has been transformed into whole Woodworking workbench.

Currently the Woodworking workbench is one-man project, mostly private but I share it with others. There is no huge corporation behind it, so this workbench may not be so advanced like well-paid projects, there is no 24/7 support plans to buy. 

Also, for now it is not possible for me to record all the Woodworking workbench features. It would probably takes several hours and I don't want to run special youtube channel for that and record tutorials only. I feel better creating code, making quality improvements, solving problems, inventing new things and prototyping, not making tutorials. 
Sorry, for that.

# Main features

* **Magic Panels** - allow to create woodworking project more quickly, especially simplifies the positioning process and thickness recognition. You see clearly where is the thickness in object property window, so it can be changed quickly, if needed. If you have problems with "side effect", I mean pure magic of the Magic Panels ;-), please use `magicManager` to preview panel before creation and `magicMove` to move panels.
* [Fully parametric examples](https://github.com/dprojects/Woodworking/tree/master/Examples) - you can adopt it to your current project, merge them, without designing from scratch e.g. bookcase. You can also add decoration, if needed.
* [getDimensions](https://github.com/dprojects/getDimensions) - allows to create spreadsheet with dimensions to cut, cutlist, BOM.
* [sheet2export](https://github.com/dprojects/sheet2export) - allows to export spreadsheets to chosen file format.
* [setTextures](https://github.com/dprojects/setTextures) - allows to store, load, repeat and rotate textures from URL.
* [scanObjects](https://github.com/dprojects/scanObjects) - allows to live inspect and debug project, also view FreeCAD or any other module API.
* [debugInfo](https://github.com/dprojects/Woodworking/blob/master/Tools/debugInfo.py) - allows to get quick and simple debug info for bug report.
* [makeTransparent](https://github.com/dprojects/Woodworking/blob/master/Tools/makeTransparent.py) - allows to make all parts transparent and back to normal. You can preview all pilot holes, countersinks or any other joints like that, very simply.
* [colorManager](https://github.com/dprojects/Woodworking/blob/master/Tools/colorManager.py) - allows to set face colors for all objects from spreadsheet. Also you can browse colors for manually selected face or object and see the effect at 3D model in real-time.
* [magicAngle](https://github.com/dprojects/Woodworking/blob/master/Tools/magicAngle.py) - allows to rotate panels and even other more complicated objects, like construction profiles.
* Also clean toolbar, with sections adjusted for woodworking.

![000](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/000.png)

# How to install

* Download and unpack `Woodworking` repository.
* Copy the folder `Woodworking` to the FreeCAD module directory.

**Note:** 

* Xubuntu:
	* FreeCAD version < 0.20.27936: `~.FreeCAD/Mod/Woodworking`
	* FreeCAD version >= 0.20.27936: `~.local/share/FreeCAD/Mod/Woodworking`

# Certified platforms

**FreeCAD version:** [FreeCAD-0.20.0-Linux-x86_64.AppImage](https://github.com/FreeCAD/FreeCAD/releases/download/0.20/FreeCAD-0.20.0-Linux-x86_64.AppImage)

**Current development platform:**

	OS: Ubuntu 22.04 LTS (XFCE/xubuntu)
	Word size of FreeCAD: 64-bit
	Version: 0.20.29177 (Git) AppImage
	Build type: Release
	Branch: (HEAD detached at 0.20)
	Hash: 68e337670e227889217652ddac593c93b5e8dc94
	Python 3.9.13, Qt 5.12.9, Coin 4.0.0, Vtk 9.1.0, OCC 7.5.3
	Locale: English/United States (en_US)
	Installed mods: 
	* Woodworking 0.20.29177

**Note:** Make sure Your current Woodworking workbench version has the same version number as the FreeCAD version. To get better workbench stability the further Woodworking workbench will be developed according to the specified FreeCAD version, that will never change. Woodworking workbench version will get always the same version number as the approved FreeCAD build, so You will be sure they should work with each other.

I do not have `Windows` or `macOS`, so I am not able to say if this work or not. Should work everywhere with AppImage but... You never know, this is why this section is here, to create stable Woodworking platform.

# Screenshots

![001](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/001.png)

![002](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/002.png)

![003](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/003.png)

# Contact

Please add all comments and questions to the dedicated [FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=3&t=8247).

# License

MIT
