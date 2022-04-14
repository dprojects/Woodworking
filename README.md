# Description

This is Woodworking workbench for FreeCAD.

![000](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/000.png)

# Main features

* `Magic panels` - allow to create woodworking project more quickly. **Note:** They are named `magic` because they are designed for specific situation but they have also `side effect`, you never know how the panel will be created ;-) This depends from selection order and referenced object. Sometimes the effect can be surprisingly good and very useful, sometimes not. So, you have to play with it little bit more to find out how to use it at your project effectively.
* Contains [fully parametric examples](https://github.com/dprojects/Woodworking/tree/master/Examples) - you can adopt it to your current project, without designing e.g. bookcase from scratch. You can also add decoration, if needed.
* Allows to create spreadsheet with dimensions to cut, cutlist, BOM (via [getDimensions](https://github.com/dprojects/getDimensions)).
* Allows to export spreadsheets to chosen file format (via [sheet2export](https://github.com/dprojects/sheet2export)).
* Allows to store, load, repeat and rotate textures from URL (via [setTextures](https://github.com/dprojects/setTextures)).
* Allows to live inspect and debug project, view FreeCAD or any other module API (via [scanObjects](https://github.com/dprojects/scanObjects)).
* Allows to get quick and simple debug info for bug report (via `debugInfo` button).
* Clean toolbar, with sections adjusted for woodworking.

# Install

* Download and unpack `Woodworking` repository.
* Copy the folder `Woodworking` to the FreeCAD module directory.

**Note:** 

* Ubuntu:
	* FreeCAD version < 0.20.27936: `~.FreeCAD/Mod/Woodworking`
	* FreeCAD version >= 0.20.27936: `~.local/share/FreeCAD/Mod/Woodworking`

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
