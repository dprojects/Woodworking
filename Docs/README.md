# Woodworking workbench documentation

<img align="left" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/Woodworking.png"> FreeCAD is a very cool software and allows to design a lot of interesting things. However, FreeCAD is not dedicated software for furniture designing. For this reason, some tasks when designing furniture can be challenging at the beginning. Despite the fact that I finished math, I have a problem with counting in my memory. For me, constantly calculating wood thickness and adding this to the position was a problem without a calculator. In addition, constantly starting from the `10 x 10 x 10 Cube` and setting it in the right position was a bit challenging at the beginning. 

Woodworking workbench has been created because of my woodworking and coding hobby. Everything started from [getDimensions](https://github.com/dprojects/getDimensions/commits/master) project long time ago. I wanted to have [simple cut-list for chipboards order](https://github.com/dprojects/getDimensions/commit/a6f0a2221e90f717be95bd0dc1cc9f1ede95a329) and I found FreeCAD with low hardware requirements and possibility to implement the cut-list. Now it has been transformed into whole Woodworking workbench.

Currently the Woodworking workbench is one-man project, yes one-man mission to the Moon (LOL), mostly private but I share it with others. There is no huge corporation behind it, so this workbench may not be so advanced like well-paid projects, also there is no 24/7 support plans to buy.

The main goal for this workbench is to make furniture designing process at FreeCAD more simple.

<br><br>

* [Main features](#main-features)
  * [Making panels](#making-panels)
    * [Default panels](#default-panels)
    * [Copy panels](#copy-panels)
    * [magicManager](#magicmanager)
    * [Dedicated panels](#dedicated-panels)
  * [Resize panels](#resize-panels)
  * [Adjust position](#adjust-position)
    * [fitModel](#fitmodel)
    * [arrows](#arrows)
    * [magicMove](#magicmove)
    * [panelMove2Face](#panelmove2face)
    * [magicAngle](#magicangle)
  * [Adding details](#adding-details)
    * [magicDowels](#magicdowels)
    * [magicFixture](#magicfixture)
    * [panel2link](#panel2link)
    * [makeTransparent](#maketransparent)
    * [panel2profile](#panel2profile)
    * [panel2frame](#panel2frame)
    * [panel2pad](#panel2pad)
  * [Colors](#colors)
    * [colorManager](#colormanager)
    * [setTextures](#settextures)
  * [Dimensions](#dimensions)
    * [getDimensions](#getdimensions)
    * [showSpaceModel](#showspacemodel)
    * [showSpaceSelected](#showspaceselected)
    * [sheet2export](#sheet2export)
  * [Debugging](#debugging)
    * [scanObjects](#scanobjects)
    * [debugInfo](#debuginfo)
* [Dowels, Screws, Fixture](#dowels-screws-fixture)
* [Extras](#extras)
* [Translations](#translations)
* [Final notes](#final-notes)
* [Contact](#contact)
* [License](#license)

# Main features

## Making panels

### Default panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultZY.png"> There are many types of wood. So there is no chance to cover all possible wood sizes provided by the market. This starting panels, allows for quick start. You do not have to start each time from `10 x 10 x 10 Cube` object. This tool creates default panel that can be easily resized. You can clearly see where should be the thickness to keep exact panel `XYZ` axis orientation. All furniture elements should be created according to the `XYZ` axis plane, if possible. Avoid building whole furniture with rotated elements. If you want to rotate panel with dowels, better create panel with dowels without rotation, pack panel with dowels into container like `LinkGroup`, and use [magicAngle](#magicangle) to rotate whole `LinkGroup`. You can rotate whole furniture like this with single click and the dowels will be in the correct place after rotation. If you would like to apply dowels at rotated element it would be pointless complication, almost impossible at FreeCAD with the rotation logic and zero-API. 

### Copy panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyZY.png"> This tool copy selected panel into exact `XYZ` axis orientation. By default you can copy any panel based on `Cube` object. If you want to copy `Pad`, you need to have constraints named "SizeX" and "SizeY" at the `Sketch`. For other object types you need to have `Length`, `Width`, `Height` properties at object (Group: "Base", Type: "App::PropertyLength").

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceZY.png"> This tool creates new panel at selected face. The blue panel represents the selected object and the red one represents the new created object. The icon refers to base `XY` model view (0 key position). Click [fitModel](#fitmodel) to set model into referred view, and to be sure the model and face you have selected refers to exact icon. **Note:** If you have problems with unpredicted result, "side effect of Magic Panels", please use [magicManager](#magicmanager) to preview panel before creation and [magicMove](#magicmove) to move panels.

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenZY.png"> This tool creates new panel between two selected faces. Selection faces order is important. To select more than one face, hold left `CTRL` key during second face selection. The blue panels represents the selected objects and the red one represents the new created object. The icon refers to base `XY` model view (0 key position). Click [fitModel](#fitmodel) to set model into referred view. **Note:** If you have problems with unpredicted result, "side effect of Magic Panels", please use [magicManager](#magicmanager) to preview panel before creation and [magicMove](#magicmove) to move panels.

### magicManager

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicManager.png"> This tool allows to preview panel before creation. It allows to see panel at single selected face and also panel between two faces. This tool can be used if you have problems with unpredicted result, "side effect of Magic Panels". However, clicking single icon is sometimes more quicker than opening GUI and choosing right panel.

### Dedicated panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideLeft.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideRight.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideLeftUP.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideRightUP.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBackOut.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCoverXY.png"> Dedicated panels allows you to add specific furniture element. You can add sides, back or top of the furniture with single click. The side panels improves the thickness offset at the face tools. If you would like to add back of the furniture manually, you have to calculate the back dimensions first. Next you have to move the panel exactly to the back of the furniture position. It is not so easy to do it manually because `1 mm` offset might be a problem. Now you can make it with several clicks, without calculating anything manually.

## Resize panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize1.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize2.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize3.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize4.png"> You can resize panel very quickly. The resize step is selected panel thickness, so you can solve the common problem with thickness offset. For example to move top of the furniture and make shelf from it, you have to resize the panel `2 x` with thickness step and once from other side. This may not be so easy calculation, and you may have to calculate something like `534 - 18 - 18 = ?` and `613 - 18 = ?`. Now you can click three times and you have it without thinking.

## Adjust position

### fitModel

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/fitModel.png"> This tool allows to fit model to the 3D screen view and also rotate the model view to the base `XY` position (0 key press). This is very useful, used all the time, during furniture designing process. If you rotate the furniture, you can loose the correct orientation of the furniture. So, it strongly recommended to click this tool very often.

### arrows

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveXp.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveXm.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveYp.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveYm.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveZp.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveZm.png"> With the arrows you can quickly move panels or even any other objects. If the thickness of the selected object can be recognized, the move step will be the thickness. So, you can solve common furniture problem with thickness offset. You do not have to calculate something like `643 - 18 - 18 - 18 = ?`, click three times and you have it. If the thickness will not be recognized the step will be `100`. This approach allows you to move whole furniture segments very quickly. You can select container like `Body` or `LinkGroup` with many element and move it quickly. The arrows recognize the view model rotation. However, all possible rotations are not recognized, sometimes the movement may not be correctly aligned with the arrow icon. So, it strongly recommended to click [fitModel](#fitmodel) tool before using arrows. If you want precisely move object, use [magicMove](#magicmove) tool, instead.

### magicMove

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicMove.png"> This tool allows to move panel with custom step. It automatically show center axes and resize the corner axes. You can also resize the corner axes or turn on and off the center axes. This tool recognize holding button, so you can press once the arrow and hold it, and the selected part will be moving in desired direction with exact step. This approach allows, to precisely move objects and also do it quickly without clicking arrows icons many times.

### panelMove2Face

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMove2Face.png"> This tool allows to align panels or any other objects to face position. First select face and next select objects you want to align with face position. You can select objects at objects `Tree` window holding `left CTRL key`. This tool allows to avoid thickness step problem, if you want to move panel to the other edge but the way is not a multiple of the panel thickness. However, it not cover all possible situations. This will be improved in the future maybe but for now it align object to the first `0 vertex` (beginning of the panel), what may not be always what you want.

### magicAngle

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicAngle.png"> This tool allows to rotate panels and even other more complicated objects, like construction profiles. If you want to rotate many objects together, use this tool directly at `Part` object or pack all objects into `LinkGroup` and use rotation at the `LinkGroup`. You can also choose center point of rotation by browsing vertices.

## Adding details

### magicDowels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDowels.png"> This tool allows to add mounting points to the furniture, or even any other elements like construction profiles. You can add predefined mounting points e.g. screws, dowels, shelf supporter pins or add custom mounting points. This is very quick way to add mounting points to the furniture, no calculation needed to place dowel exactly in the middle of the edge. If you would like to add e.g. 40 dowels to the whole furniture and align all of them manually, it would probably be big challenge. With this tool you can do it with single click in many cases. Make sure the green faces are visible, because they refers to the head of the screw. If you would like to replace the dowels with detailed screw later, this might be important if the dowel is rotated incorrectly, the screw will be rotated incorrectly as well.

### magicFixture

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicFixture.png"> This tool has a little different approach than [magicDowels](#magicdowels) tool, because it allows to apply any type of fixture. Instead of `Cylinders` preview, it creates link to the detailed object and move it to the selected face. You can set exact offset from corner, offset from edge and sink. Also you can select predefined rotations and all edges. If you want you can turn on and off the manually edit mode and move and rotate it by hand. With this tool you can very easily apply detailed aluminum angles.

### panel2link

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> This tool allows to replace simple objects with any detailed object, e.g. `Cylinder` with realistic looking dowel made with `Pad`. First you have to select detailed object and than simple object that will be replaced with `Link`. The first selected detailed object can be `Part`, `LinkGroup` or any other created manually or merged with your project object. You can replace more than one simple objects at once with `Link`. To select more objects hold `left CTRL key` during selection. The simple objects should imitate the detailed object to replace all of them in-place with realistic looking one.

### makeTransparent

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/makeTransparent.png"> This tool allows to make all parts transparent and back to normal. You can preview all pilot holes, countersinks or any other joints like that, very simply.

### panel2profile

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2profile.png"> This tool allows to replace `Cube` panel with construction profile. You can replace more than one `Cube` panel at once. To select more objects hold `left CTRL key` during selection. The selected `Cube` objects need to have two equal sizes e.g. `20 mm x 20 mm x 300 mm` to replace it with construction profile. The new created construction profile will get the same dimensions, placement and rotation as the selected `Cube` panel. If you have all construction created with simple `Cube` objects that imitating profiles, you can replace all of them with realistic looking construction profiles with single click.

### panel2frame

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2frame.png"> This tool allows to replace `Cube` panel with frame 45 cut at both sides. You can replace more than one `Cube` panel at once. To replace Cube objects with frames you have to select exact face at each `Cube` object. For example if you want to make picture frame, select all 4 inner faces. To select more faces hold `left CTRL key` during selection. The new created frame will get the same dimensions, placement and rotation as the selected `Cube` panel but will be cut at the selected face. If you have all construction created with simple `Cube` objects that imitating picture frame or window, you can replace all of them with realistic looking frame with single click.

### panel2pad

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2pad.png"> This tool allows to replace `Cube` panel with `Pad` panel. The new created `Pad` panel will get the same dimensions, placement and rotation as the selected `Cube` panel. You can transform only one `Cube` panel into `Pad` at once. This tool is mostly dedicated to add decoration that is not supported for `Cube` objects by FreeCAD PartDesign workbench. You can also change shape by changing the `Sketch`. This is mostly used for decoration that can be applied only to `Pad`, like `Fillet`.

## Colors

### colorManager

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/colorManager.png"> This tool allows to set face colors for all objects from spreadsheet. Also you can browse colors for manually selected faces or objects and see the effect at 3D model in real-time.

### setTextures

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/setTextures.png"> This tool allows to add textures. For more info see: [setTextures](https://github.com/dprojects/setTextures)

<br>

## Dimensions

### getDimensions

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/getDimensions.png"> This tool allows to create spreadsheet with dimensions to cut, cut-list, BOM. For more info see: [getDimensions](https://github.com/dprojects/getDimensions)

<br>

### showSpaceModel

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showSpaceModel.png"> This tool allows to calculate occupied space in 3D by the model. This approach might be very useful at furniture designing process. For example you can see how much space in your room will take opened front of the furniture. Normally, all the `Pad` or `Cube` elements, should be created according to the `XYZ` plane, so there will be no difference between the real dimensions and occupied space in 3D. 

### showSpaceSelected

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showSpaceSelected.png"> This tool allows to calculate occupied space in 3D by selected elements. This approach might be very useful at furniture designing process. For example you can see how much space take selected parts of the furniture. Normally, all the `Pad` or `Cube` elements, should be created according to the `XYZ` plane, so there will be no difference between the real dimensions and occupied space in 3D.

### sheet2export

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sheet2export.png"> This tool allows to export cut-list, BOM to more flexible file formats. For more info see: [sheet2export](https://github.com/dprojects/sheet2export)

<br>

## Debugging

### scanObjects

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/scanObjects.png"> This tool allows for code debugging, browsing FreeCAD modules, live API. For more info see: [scanObjects](https://github.com/dprojects/scanObjects)

<br>

### debugInfo

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/debugInfo.png"> This tool allows to get platform information used for FreeCAD bug report.

<br><br>

# Dowels, Screws, Fixture

* Use [magicDowels](#magicdowels) for dowels, screws and other mounting points references.
* Use [magicFixture](#magicfixture) for any other type of fixture.
* Examples repository: [Fixture](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture) - you can use this repository, make your own detailed part, or order exact detailed part somewhere and merge with your project and apply with the same rules.

However, if you make your own detailed part or order somewhere, you need to fulfill certain requirements:

* The detailed element should start from `(0, 0, 0)` vector. The bottom of this element and orientation should match the `XYZ` axes as described below. If you want to adjust the detailed element which has been made by someone else, you should rather move it via container (e.g. `Body`). Avoid rotation at the base element.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/fixture001.png)

* If you set reference mounting points with [magicDowels](#magicdowels) that will be replaced later with realistic looking screws. Make sure the green faces refers to the top head of the screw. If not the replaced element will be rotated.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/fixture002.png)

* This furniture from my garage has applied realistic looking screws and dowels. All the screws has been applied with single click via [panel2link](#panel2link) woodworking workbench feature. Also it has angles replaced with [magicFixture](#magicfixture) tool.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/fixture003.png)

# Extras

This woodworking workbench is delivered with several useful extras:

* [Fully parametric examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Parametric) - this folder inside woodworking workbench contains sample furniture projects. All of the furniture examples are parametric. So, you can quickly adopt it to your current project, without designing e.g. bookcase from scratch. You can also add decoration, if needed, or even merge with other projects.
* [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture) - this is new approach to 3D modeling. With [panel2link](#panel2link) feature you can replace any cube object with detailed object created manually. This is very powerful feature and gives a lot of flexibility and simplifies the process of making model detailed. Also if you replace all cube objects with links to detailed object, you will get parametric detailed model. If you change the detailed object all links will be updated.
* [Texture samples](https://commons.wikimedia.org/w/index.php?title=Special:ListFiles/Dprojects&ilshowall=1) - sample textures for woodworking projects purposes. They are totally free to use.

# Translations

For Woodworking workbench translation see dedicated directory: [translations](https://github.com/dprojects/Woodworking/tree/master/translations)

# Contact

Please add all comments and questions to the dedicated [FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=3&t=8247).

# License

MIT
