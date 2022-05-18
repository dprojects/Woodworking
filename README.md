# Description

This is Woodworking workbench for FreeCAD.

# Main features

![MagicPanels](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/MagicPanels.gif)

* [Magic Panels](#magic-panels) - allow to create woodworking project more quickly, especially simplifies the positioning process and thickness recognition. You see clearly where is the thickness in object property window, so it can be changed quickly, if needed.
* [Fully parametric examples](https://github.com/dprojects/Woodworking/tree/master/Examples) - you can adopt it to your current project, merge them, without designing from scratch e.g. bookcase. You can also add decoration, if needed.
* [getDimensions](https://github.com/dprojects/getDimensions) - allows to create spreadsheet with dimensions to cut, cutlist, BOM.
* [sheet2export](https://github.com/dprojects/sheet2export) - allows to export spreadsheets to chosen file format.
* [setTextures](https://github.com/dprojects/setTextures) - allows to store, load, repeat and rotate textures from URL.
* [scanObjects](https://github.com/dprojects/scanObjects) - allows to live inspect and debug project, also view FreeCAD or any other module API.
* [debugInfo](https://github.com/dprojects/Woodworking/blob/master/Tools/debugInfo.py) - allows to get quick and simple debug info for bug report.
* [makeTransparent](https://github.com/dprojects/Woodworking/blob/master/Tools/makeTransparent.py) - allows to make all parts at transparent and back to normal. You can preview all pilot holes, countersinks or any other joints like that, very simply.
* [colorManager](https://github.com/dprojects/Woodworking/blob/master/Tools/colorManager.py) - allows to set face colors for all objects from spreadsheet. Also you can browse colors for manually selected face or object and see the effect at 3D model in real-time.
* Also clean toolbar, with sections adjusted for woodworking.

![000](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/000.png)

# Install

* Download and unpack `Woodworking` repository.
* Copy the folder `Woodworking` to the FreeCAD module directory.

**Note:** 

* Ubuntu:
	* FreeCAD version < 0.20.27936: `~.FreeCAD/Mod/Woodworking`
	* FreeCAD version >= 0.20.27936: `~.local/share/FreeCAD/Mod/Woodworking`

# Magic Panels

Currently the `Magic Panels` allow to:
* Create default panel `600 mm x 300 mm x 18 mm`.
* Copy any panel based on `Cube` or `Pad`. If you want copy any other object, select base object.
* Move any panel based on `Cube` or `Pad`.
* Resize any panel based on `Cube` or `Pad`.
* Add special parts of the furniture: Side, Back, Top, Shelf. Mostly for `Cube`.
* Apply panel at face in any direction. Mostly for `Cube`, for `Pad` may not be positioned well, because of different vertex handling ;-)
* Apply panel between 2 faces in any direction. Mostly for `Cube`, for `Pad` may not be positioned well, because of different vertex handling ;-)
* Change any panel based on `Cube` into `Pad`. 

**Note:** The `Magic Panels` are named `magic` because they are designed for specific situation but they have also side effect, You never know how the panel will be created ;-) This depends on selection order and referenced object. Sometimes the effect can be surprisingly good and very useful, sometimes not. So, you have to play with the `Magic Panels` little bit more to use it at your project effectively.

# Macro tools - how to update

Macro tools included in this workbench may not be up-to-date. All the macro tools will be developed separately because You may not want to use whole woodworking workbench to use only one macro tool.

To update macro tools You can:
* Use `update` option from `Woodworking` menu.
* Do it manually just by overwrite exact macro tool with new version directly in exact folder.

# Screenshots

![001](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/001.png)

![002](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/002.png)

![003](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/003.png)

# Contact

Please add all comments and questions to the dedicated [FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=3&t=8247).

# License

MIT
