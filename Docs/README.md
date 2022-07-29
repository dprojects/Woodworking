# Woodworking workbench documentation

* [Main features](#main-features)
  * [Default panels](#default-panels)
  * [Copy panels](#copy-panels)
  * [Resize panels](#resize-panels)
  * [Move panels](#move-panels)
  * [fitModel](#fitmodel)
  * [panelMove2Face](#panelmove2face)
  * [magicAngle](#magicangle)
  * [magicMove](#magicmove)
  * [magicManager](#magicmanager)
  * [Dedicated panels](#dedicated-panels)
  * [magicDowels](#magicdowels)
  * [magicFixture](#magicfixture)
  * [panel2link](#panel2link)
  * [makeTransparent](#maketransparent)
  * [panel2profile](#panel2profile)
  * [panel2frame](#panel2frame)
  * [panel2pad](#panel2pad)
  * [colorManager](#colormanager)
  * [setTextures](#settextures)
  * [getDimensions](#getdimensions)
  * [showSpaceModel](#showspacemodel)
  * [showSpaceSelected](#showspaceselected)
  * [sheet2export](#sheet2export)
  * [scanObjects](#scanobjects)
  * [debugInfo](#debuginfo)
* [Dowels, Screws, Fixture](#dowels-screws-fixture)
* [External repositories](#external-repositories)
* [Translations](#translations)
* [Final notes](#final-notes)
* [Contact](#contact)
* [License](#license)

# Main features

### Default panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultZY.png"> Default panels options are made to keep exact `XYZ` orientation. You can change the size quickly to adjust to your needs. You see clearly where is the thickness in object's property window, so it can be changed quickly, if needed.

### Copy panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyZY.png"> You can copy any selected panel and map it to the correct `XYZ` orientation. 

<br><br>

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceZY.png"> You can copy panel at selected face very quickly. **Note:** If you have problems with "side effect", please use [magicManager](#magicmanager) to preview panel before creation and [magicMove](#magicmove) to move panels.

<br>

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenZY.png"> You can create panel between two selected faces very quickly. **Note:** If you have problems with "side effect", please use [magicManager](#magicmanager) to preview panel before creation and [magicMove](#magicmove) to move panels.

### Resize panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize1.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize2.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize3.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize4.png"> You can resize panel very quickly. The resize step is selected panel thickness, so you can solve the common problem with thickness offset. You do not have to calculate something like `643 - 18 - 18 - 18 = ?`, click three times and you have it.

### Move panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveXp.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveXm.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveYp.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveYm.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveZp.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveZm.png"> You can move panel very quickly. The move step depends on object type. If the object is recognized the step will be selected panel thickness, so you can solve the common problem with thickness offset. You do not have to calculate something like `643 - 18 - 18 - 18 = ?`, click three times and you have it. If the object is not recognized the step will be 100, so you can move `Body` of the whole furniture very quickly.

### fitModel

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/fitModel.png"> This tool allows to fit model to the screen view and also rotate the model view to the base XY position (0 key press).

<br>

### panelMove2Face

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMove2Face.png"> This tool allows to align panels or any other objects to face position.

<br> 

### magicAngle

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicAngle.png"> This tool allows to rotate panels and even other more complicated objects, like construction profiles. If you want to rotate many objects together, use this tool directly at `Part` object or pack all objects into `LinkGroup` and use rotation at the `LinkGroup`.

### magicMove

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicMove.png"> This tool allows to move panel with custom step.

<br>

### magicManager

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicManager.png"> This tool allows to preview panel before creation. It allows to see panel at single selected face and also panel between two faces. 

<br>

### Dedicated panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideLeft.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideRight.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideLeftUP.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideRightUP.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBackOut.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCoverXY.png"> Dedicated special tools to apply furniture parts more precisely. 

<br>

### magicDowels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDowels.png"> This tool allows to add mounting points to the furniture, or even any other elements like construction profiles. You can add predefined mounting points e.g. screws, dowels, shelf supporter pins or add custom mounting points. This is very quick way to add mounting points to the furniture, no calculation needed to place dowel exactly in the middle of the edge, you can do it with single click in many cases.

### magicFixture

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicFixture.png"> This tool allows to apply any type of fixture. It creates link to the detailed object at selected face and allow to set exact position for the link.

### panel2link

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> This tool allows to replace reference mounting points with detailed object.

<br>

### makeTransparent

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/makeTransparent.png"> This tool allows to make all parts transparent and back to normal. You can preview all pilot holes, countersinks or any other joints like that, very simply.

### panel2profile

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2profile.png"> This tool allows to change panels into construction profiles.

<br>

### panel2frame

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2frame.png"> This tool allows to change panels into frame, 45 angle cut from both side.

<br>

### panel2pad

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2pad.png"> This tool allows to change Cube panel into Pad. This is mostly used for decoration that can be applied only to Pad, like Fillet.

<br>

### colorManager

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/colorManager.png"> This tool allows to set face colors for all objects from spreadsheet. Also you can browse colors for manually selected faces or objects and see the effect at 3D model in real-time.

### setTextures

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/setTextures.png"> This tool allows to add textures. For more info see: [setTextures](https://github.com/dprojects/setTextures)

<br>

### getDimensions

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/getDimensions.png"> This tool allows to create spreadsheet with dimensions to cut, cut-list, BOM. For more info see: [getDimensions](https://github.com/dprojects/getDimensions)

<br>

### showSpaceModel

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showSpaceModel.png"> This tool allows to calculate occupied space in 3D by the model. 

<br>

### showSpaceSelected

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showSpaceSelected.png"> This tool allows to calculate occupied space in 3D by selected elements. 

<br>

### sheet2export

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sheet2export.png"> This tool allows to export cut-list, BOM to more flexible file formats. For more info see: [sheet2export](https://github.com/dprojects/sheet2export)

<br>

### scanObjects

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/scanObjects.png"> This tool allows for code debugging, browing FreeCAD modules, live API. For more info see: [scanObjects](https://github.com/dprojects/scanObjects)

<br>

### debugInfo

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/debugInfo.png"> This tool allows to get platform informations used for FreeCAD bug report.

<br><br>

# Dowels, Screws, Fixture

* For dowels, screws and other mounting points references use [magicDowels](#magicdowels). For other type of fixture use [magicFixture](#magicfixture) tool. The detailed element should start from `(0, 0, 0)` vector. The bottom of this element and orientation should match the `XYZ` axes:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/fixture001.png)

* If you set reference mounting points that will be replaced later with realistic looking screws. Make sure the green faces refers to the top head of the screw.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/fixture002.png)

* This furniture from my garage has applied realistic looking screws and dowels. All the screws has been applied with single click via `panel2link` woodworking workbench feature.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/fixture003.png)

# External repositories

* [Fully parametric examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Parametric) - you can adopt it to your current project, merge them, without designing e.g. bookcase from scratch. You can also add decoration, if needed.
* [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture) - this is new approach to 3D modeling. With `panel2link` feature you can replace any cube object with detailed object created manually. This is very powerful feature and gives a lot of flexibility and simplifies the process of making model detailed. Also if you replace all cube objects with links to detailed object, you will get parametric detailed model. If you change the detailed object all links will be updated.
* [Texture samples](https://commons.wikimedia.org/w/index.php?title=Special:ListFiles/Dprojects&ilshowall=1) - sample textures for woodworking projects purposes. They are totally free to use.

# Translations

For Woodworking workbench translation see dedicated directory: [translations](https://github.com/dprojects/Woodworking/tree/master/translations)

# Final notes

Woodworking workbench has been created because of my woodworking and coding hobby. Everything started from [getDimensions](https://github.com/dprojects/getDimensions/commits/master) project long time ago. I wanted to have [simple cut-list for chipboards order](https://github.com/dprojects/getDimensions/commit/a6f0a2221e90f717be95bd0dc1cc9f1ede95a329) and I found FreeCAD with low hardware requirements and possibility to implement the cut-list. Now it has been transformed into whole Woodworking workbench.

Currently the Woodworking workbench is one-man project, mostly private but I share it with others. There is no huge corporation behind it, so this workbench may not be so advanced like well-paid projects, there is no 24/7 support plans to buy.

Also, for now it is not possible for me to record all the Woodworking workbench features. It would probably takes several hours and I don't want to run special youtube channel for that and record tutorials only. I feel better creating code, making quality improvements, solving problems, inventing new things and prototyping, not making tutorials. Sorry, for that.

# Contact

Please add all comments and questions to the dedicated [FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=3&t=8247).

# License

MIT
