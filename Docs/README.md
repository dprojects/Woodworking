# Woodworking workbench documentation

<img align="left" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/Woodworking.png"> FreeCAD is a very cool software and allows to design a lot of interesting things. However, FreeCAD is not dedicated to be software only for furniture designing. For this reason, some tasks when designing furniture can be challenging at the beginning. Despite the fact that I finished math, I have a problem with counting in my memory. For me, constantly calculating wood thickness and adding this to the position was a problem without a calculator. In addition, for me constantly starting from the `10 x 10 x 10` box `Cube` and setting it in the right position is a bit annoying. 

Woodworking workbench has been created because of my woodworking and coding hobby. Everything started from [getDimensions](https://github.com/dprojects/getDimensions/commits/master) project long time ago. I wanted to have [simple cut-list for chipboards order](https://github.com/dprojects/getDimensions/commit/a6f0a2221e90f717be95bd0dc1cc9f1ede95a329) and I found FreeCAD with low hardware requirements and possibility to implement the cut-list. Now it has been transformed into whole Woodworking workbench. The main goal for this workbench is to make the furniture designing process at FreeCAD more simple.

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
  * [Dowels and Screws](#dowels-and-screws)
    * [magicDowels](#magicdowels)
    * [panel2link](#panel2link)
    * [panel2clone](#panel2clone)
    * [sketch2dowel](#sketch2dowel)
    * [edge2dowel](#edge2dowel)
    * [makeTransparent](#maketransparent)
  * [Fixture](#fixture)
    * [magicFixture](#magicfixture)
    * [edge2drillbit](#edge2drillbit)
  * [Drilling holes](#drilling-holes)
    * [magicDriller](#magicdriller)
    * [drillHoles](#drillholes)
    * [drillCountersinks](#drillcountersinks)
    * [drillCounterbores](#drillcounterbores)
    * [drillCounterbores2x](#drillcounterbores2x)
    * [magicCNC](#magiccnc)
  * [Construction](#construction)
    * [panel2profile](#panel2profile)
  * [Joinery](#joinery)
    * [magicCut](#magiccut)
    * [jointTenon](#jointtenon)
    * [jointCustom](#jointcustom)
    * [panel2frame](#panel2frame)
  * [Decoration](#decoration)
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
* [Holes, Countersinks, Counterbores](#holes-countersinks-counterbores)
  * [Drilling serially](#drilling-serially)
  * [Drilling via icons](#drilling-via-icons)
  * [Drilling via magicCNC](#drilling-via-magiccnc)
  * [Pilot holes for angles, hinges](#pilot-holes-for-angles-hinges)
  * [Pocket holes - invisible connections](#pocket-holes---invisible-connections)
    * [Drill pocket holes - manually](#drill-pocket-holes---manually)
    * [Drill pocket holes - with magicDriller](#drill-pocket-holes---with-magicdriller)
* [Realistic parts](#realistic-parts)
  * [Realistic screws and pilot holes](#realistic-screws-and-pilot-holes)
  * [Realistic screws and angles](#realistic-screws-and-angles)
  * [Realistic screws and pocket holes](#realistic-screws-and-pocket-holes)
* [Extras](#extras)
* [Translations](#translations)
* [Contact](#contact)
* [License](#license)

# Main features

## Making panels

### Default panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultZY.png"> There are many types of wood. So there is no chance to cover all possible wood sizes provided by the market. This starting panels, allows for quick start. You do not have to start each time from `10 x 10 x 10` box `Cube` object. This tool creates default panel that can be easily resized. You can clearly see where should be the thickness to keep exact panel `XYZ` axis orientation. All furniture elements should be created according to the `XYZ` axis plane, if possible. Avoid building whole furniture with rotated elements. If you want to rotate panel with dowels, better create panel with dowels without rotation, pack panel with dowels into container like `LinkGroup`, and use [magicAngle](#magicangle) to rotate whole `LinkGroup`. You can rotate whole furniture like this with single click and the dowels will be in the correct place after rotation. If you would like to apply dowels at rotated element it would be pointless complication, almost impossible at FreeCAD.

### Copy panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyZY.png"> This tool copy selected panel into exact `XYZ` axis orientation. By default you can copy any panel based on `Cube` object. If you want to copy `Pad`, you need to have constraints named "SizeX" and "SizeY" at the `Sketch`. For other object types you need to have `Length`, `Width`, `Height` properties at object (Group: "Base", Type: "App::PropertyLength").

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceZY.png"> This tool creates new panel at selected face. The blue panel represents the selected object and the red one represents the new created object. The icon refers to base `XY` model view (0 key position). Click [fitModel](#fitmodel) to set model into referred view, and to be sure the model and face you have selected refers to exact icon. **Note:** If you have problems with unpredicted result, "side effect of Magic Panels", please use [magicManager](#magicmanager) to preview panel before creation and [magicMove](#magicmove) to move panels.

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenXY.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenYX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenXZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenZX.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenYZ.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenZY.png"> This tool creates new panel between two selected faces. Selection faces order is important. To select more than one face, hold left `CTRL` key during second face selection. The blue panels represents the selected objects and the red one represents the new created object. The icon refers to base `XY` model view (0 key position). Click [fitModel](#fitmodel) to set model into referred view. **Note:** If you have problems with unpredicted result, "side effect of Magic Panels", please use [magicManager](#magicmanager) to preview panel before creation and [magicMove](#magicmove) to move panels.

### magicManager

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicManager.png"> This tool allows to preview panel before creation. It allows to see panel at single selected face and also panel between two faces. This tool can be used if you have problems with unpredicted result, "side effect of Magic Panels". However, clicking single icon is sometimes more quicker than opening GUI and choosing right panel.

### Dedicated panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideLeft.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideRight.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideLeftUP.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideRightUP.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBackOut.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCoverXY.png"> Dedicated panels allows you to add specific furniture element. You can add sides, back or top of the furniture with single click. The side panels improves the thickness offset at the face tools. If you would like to add back of the furniture manually, you have to calculate the back dimensions first. Next you have to move the panel exactly to the back of the furniture position. It is not so easy to do it manually because `1 mm` offset might be a problem. Now you can make it with several clicks, without calculating anything manually.

## Resize panels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize1.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize2.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize3.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize4.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize5.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize6.png"> You can resize panel very quickly. The resize step is selected panel thickness, so you can solve the common problem with thickness offset. For example to move top of the furniture and make shelf from it, you have to resize the panel `2 x` with thickness step and once from other side. This may not be so easy calculation, and you may have to calculate something like `534 - 18 - 18 = ?` and `613 - 18 = ?`. Now you can click three times and you have it without thinking. You can also resize Cylinders (drill bits), the long side will be `Height`, the short will be diameter, the thickness will be `Radius`. For Cone objects (drill bits - countersinks, counterbore) the long side will be `Height`, the thickness will be `Radius1` (bottom radius) and the short will be `Radius2` (top radius). [Holes, Countersinks, Counterbores](#holes-countersinks-counterbores).

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

## Dowels and Screws

### magicDowels

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDowels.png"> This tool allows to add mounting points to the furniture, or even any other elements like construction profiles. You can add predefined mounting points e.g. screws, dowels, shelf supporter pins or add custom mounting points. This is very quick way to add mounting points to the furniture, no calculation needed to place dowel exactly in the middle of the edge. If you would like to add e.g. 40 dowels to the whole furniture and align all of them manually, it would probably be big challenge. With this tool you can do it with single click in many cases. Make sure the green faces are visible, because they refers to the head of the screw. If you would like to replace the dowels with detailed screw later, this might be important if the dowel is rotated incorrectly, the screw will be rotated incorrectly as well.

### panel2link

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> This tool allows to replace simple objects with any detailed object, e.g. `Cylinders` with realistic looking screws. First you have to select detailed object and than simple object that will be replaced with `Link`. The first selected detailed object can be `Part`, `LinkGroup` or any other created manually or merged with your project. You can replace more than one simple object at once with `Link`. To select more objects hold left `CTRL` key during selection. The simple objects should imitate the detailed object to replace all of them in-place with realistic looking one. For more details please see: [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture).

### panel2clone

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2clone.png"> This tool allows to replace simple objects with any detailed object, e.g. `Cylinders` with realistic looking screws. First you have to select detailed object and than simple object that will be replaced with `Clones`. The first selected detailed object can be `Part`, `LinkGroup` or any other created manually or merged with your project. You can replace more than one simple object at once with `Clone`. To select more objects hold left `CTRL` key during selection. The simple objects should imitate the detailed object to replace all of them in-place with realistic looking one. This tool works with the same way as [panel2link](#panel2link) but instead of `Link` it creates `Clone` objects. It can be useful if you want to remove the base object and have clean objects Tree. Also if you want to change each copy separately. [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture).

### sketch2dowel

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sketch2dowel.png"> First select face, next Sketches of the holes to create dowels. This tool allows to create dowel from Sketch of the hole. The first selected face refers to the side the dowel will be raised, exact orientation for the dowel. Dowel position will be get from the Sketch. The dowel Radius and Height will be get from hole object. If the hole is throughAll the dowel height will be very big, so make sure you use dimensions for hole. To select more Sketches hold left CTRL key during selection.

### edge2dowel

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/edge2dowel.png"> This tool allows to create dowels above the selected hole edges. To create dowel select edge of the hole. You can select many edges at once but all the holes need to be at the same object. The dowel Height will be 40. The dowel radius will be get from the selected edge hole radius. To select more objects hold left CTRL key during selection.

### makeTransparent

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/makeTransparent.png"> This tool allows to make all parts transparent and back to normal. You can preview all pilot holes, countersinks or any other joints like that, very simply.

## Fixture

### magicFixture

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicFixture.png"> This tool has a little different approach than [magicDowels](#magicdowels) tool, because it allows to apply any type of fixture. Instead of `Cylinders` preview, it creates link to the detailed object and move it to the selected face. You can set exact offset from corner, offset from edge and sink. Also you can select predefined rotations and all edges. If you want you can turn on and off the manually edit mode and move and rotate it by hand. With this tool you can very easily apply detailed aluminum angles.

### edge2drillbit

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/edge2drillbit.png"> This tool allows to create drill bits for making simple hole. The drill bits will be created above the selected hole edges. To create drill bits select edge of the hole. You can select many edges at once but all the holes need to be at the same object. The drill bit Height will be 16. The drill bits radius will be get from the selected edge hole radius but will be little smaller, 1 mm, than the hole to make pilot hole. To select more objects hold left CTRL key during selection. This feature can be used to create drill bits above holes at hinges, angles or other fixture type.

## Drilling holes

### magicDriller

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDriller.png"> This tool is similar to [magicDowels](#magicdowels) but instead of applying dowels this tool allows to drill holes, countersinks or counterbores serially with predefined or custom sets. You can choose the same predefined screws, dowels and pins as at [magicDowels](#magicdowels) but instead of dowels there will be created set of drill bits. The drill bits will be smaller than screws to allow drill pilot holes for screws. For dowels the drill bits will be with the same size. [Drilling serially](#drilling-serially)

### drillHoles

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillHoles.png"> This is drill bit to make simple hole. The hole will be drilled below the bottom part of the drill bit, below the red face of the cylinder. The radius and depth of the hole will be the same as drill bit radius and height. You can resize the drill bit if you want. If you select face only, the drill bit will be created in the corner of the face (0 vertex). So, you will be able to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face to get exact hole depth. If you select face and than any amount of drill bits, the holes will be drilled below each drill bit. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

### drillCountersinks

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCountersinks.png"> This is drill bit to make countersink with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of countersink will be drill bit Radius2. The hole depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

### drillCounterbores

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCounterbores.png"> This is drill bit to make counterbore with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of counterbore will be drill bit Radius2. The hole depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

### drillCounterbores2x

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCounterbores2x.png"> This is drill bit to make counterbore2x with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of counterbore will be drill bit Radius2. The hole depth will be panel thickness. The counterbore depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

### magicCNC

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicCNC.png"> This tool is some kind of CNC drilling machine simulator. It is the same [magicMove](#magicmove) tool but improved for the drilling purposes. The axis which move the drill bit up and down is automatically hidden at this tool. So, you can move the drill bit at the surface and you not move the drill bit up or down by mistake and cause incorrect hole depth. Also this tool has option to drill by button click. It recognize the drill bit type by the label. For the countersink the label need to contains "countersink", and for counterbore need to contains "counterbore". For other label the simple hole will be drilled. This tool also allows for turn on and off the manuall edit mode, transform FreeCAD. So, you can move the drill bit by hand and drill holes by clicking buttons. This option can be useful for artists whom want to make holes in artistic way, not with mathematical precision. For more info see: [Drilling via magicCNC](#drilling-via-magiccnc)

## Construction

### panel2profile

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2profile.png"> This tool allows to replace `Cube` panel with construction profile. You can replace more than one `Cube` panel at once. To select more objects hold `left CTRL key` during selection. The selected `Cube` objects need to have two equal sizes e.g. `20 mm x 20 mm x 300 mm` to replace it with construction profile. The new created construction profile will get the same dimensions, placement and rotation as the selected `Cube` panel. If you have all construction created with simple `Cube` objects that imitating profiles, you can replace all of them with realistic looking construction profiles with single click.

## Joinery

## magicCut

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicCut.png"> This tool make multi bool cut operation at selected objects. First object should be the base object to cut. All other selected objects will cut the base 1st selected object. To select more objects hold left CTRL key during selection. During this process only the copies will be used to cut, so the original objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner.

## jointTenon

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/jointTenon.png"> Select face to create Tenon joint. This is simple Cube object and will be created in the corner of the selected face (0 vertex), allowing you to move the joint precisely to any place at the face. It has predefined size but you can resize and move the joint to fit to your elements and needs. To make more copies you can use [magicFixture](#magicfixture). If you set all Tenons at the element, you can quickly cut all Mortises for the Tenons with [magicCut](#magiccut). 

## jointCustom

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/jointCustom.png"> Select face to create Custom joint. The simple Pad will be created in the corner of the selected face (0 vertex), allowing you to move the joint precisely to any place at the face. It has predefined size but you can resize and move the joint to fit to your elements and needs. Also you can edit the Sketch to create your custom joint shape. To make more copies you can use [magicFixture](#magicfixture). If you set all joints at the element, you can quickly cut all Mortises for the joints with [magicCut](#magiccut).

### panel2frame

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2frame.png"> This tool allows to replace `Cube` panel with frame 45 cut at both sides. You can replace more than one `Cube` panel at once. To replace Cube objects with frames you have to select exact face at each `Cube` object. For example if you want to make picture frame, select all 4 inner faces. To select more faces hold `left CTRL key` during selection. The new created frame will get the same dimensions, placement and rotation as the selected `Cube` panel but will be cut at the selected face. If you have all construction created with simple `Cube` objects that imitating picture frame or window, you can replace all of them with realistic looking frame with single click.

## Decoration

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

# Holes, Countersinks, Counterbores

### Drilling serially

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDriller.png"> To drill holes with countersinks you have to drill through two panels. First select the surface for countersinks and click `refresh selection`, reference for the face should be updated and visible at the tool info screen:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller001.png)

* Next choose `Contersinks` and exact screw type. Also adjust the edge, rotation and sink, if needed:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller002.png)

* If the drill bits are in correct place, click the drill button, this may takes some time, for example if you drill 30 holes for shelf pins at once and you have slow laptop as I have: 
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller003.png)
  
* To drill rest of the hole, hide the first element with countersinks and select edge:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller004.png)

  <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCountersinks.png"> **Note:** To drill rest of the hole, you can also use [Drilling via icons](#drilling-via-icons) feature. Just select edge, next all the countersinks drill bits and click the icon. All the holes will be drilled. But do not exit the tool because the countersinks drill bits will be automatically removed. You can do it if the holes will be drilled. But also you can continue with this tool and drill the rest of holes with this tool directly.

* Now click `refresh selection`, reference for the face should be updated and visible at the tool info screen. Also the drill bits will be moved to the new face, but do not worry, for this tool it is ok, just select `Holes` for hole type and exact screw. For `Hole` type, the depth is adjusted with panel thickness. However, if you have different panel sizes you can adjust it, as well: 
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller005.png)
  
* Now click to drill and the rest of the holes will be drilled at the edge:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller006.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller007.png)

### Drilling via icons

<img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillHoles.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCountersinks.png"> <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCounterbores.png"> Select face you want to drill and click any hole icons. The drill bit for the hole type will be created in the 0 vertex of the face, allowing you to move the drill bit to any place at the face. You can change the drill bit size if you want, manually or with [Resize panels](#resize-panels) icons. Also you can create your own drill bits. But there is rule, for simple holes this need to be `Cylinder` object, but for Countersinks and Counterbores this need to be `Cone` object. This is because at `Cone` you can easily store radius for countersink and other for hole. Also the drill bit need to be exactly rotated, exact face of drill bit need to touch the face for drilling.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillHoles001.png)

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillHoles002.png)
  
* To drill the hole select face and drill bit in this order. The selected drill bit must be at the end. The face to drill should be first.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillHoles003.png)
    
* Now to drill hole click the exact icons for the drill bit and the hole will be drilled below the drill bit.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillHoles004.png)
  
* You can also copy the drill bit and select more at once:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillHoles005.png)
  
* If you click the icon for the hole all holes will be created:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillHoles006.png)
  
* The holes have the same size as the drill bits:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillHoles007.png)
  
### Drilling via magicCNC

* First select exact place to drill:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillCNC001.png)
  
* Create drill bit, in this case countersink, select the face and the drill bit. Next open [magicCNC](#magiccnc) tool. You can also first open the [magicCNC](#magiccnc) tool and then set then refresh selection to set exact objects references. 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillCNC002.png)

* With this tool you can precisely move the drill bit to any place at the surface and drill any type of hole just by single button click. You can also turn on and off the transform edit and move the drill bit by hand. The [magicCNC](#magiccnc) tool recognize the drill bit type by label. For countersink the label need to have "countersink", for counterbore the "counterbore". If nothing will be found the simple hole will be drilled. The tool support only single hole at once but allows you to drill hole very quickly, just by moving and clicking drill. In this example the countersink has been created in the first element:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillCNC003.png)
  
* To drill rest of the hole you have to change the face reference. To do that, hide the first element and select face and drill bit:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillCNC004.png)
  
* Now click `refresh selection` to load new references:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillCNC005.png)

* Now you can click drilling button to create rest of the hole:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillCNC006.png)
  
* Now the hole is created through two elements and the countersink is in the righ place, and also the depth of the hole is equally divided into both elements, like it should be in real-life:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillCNC007.png)

### Pilot holes for angles, hinges

* To create pilot holes for angle, first set the angle into position with [magicFixture](#magicfixture). Remember to set `Clone` option, because if you make a `Link` the drill bits will be created at the base element, and you will not be albe to drill holes.
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillAngles001.png)

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/edge2drillbit.png"> Next select each hole edge inside the fillets and click [edge2drillbit](#edge2drillbit). If the angle do not have fillet it is fine, you can select the hole edge as well. The drill bits will be created above each hole and the drill bits diameter will be a little smaller than the hole. It is OK for pilot hole. Pilot hole should be usually smaller 1 mm than the screw. If you want you can also resize the drill bits. 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillAngles002.png)

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillHoles.png"> Now you can select face of the element to drill and than all the drill bits for the element. If you have this selected you have to click the [drillHoles](#drillholes) icon. All the holes will be created. If the element was Cube it will be automatically changed into Pad, and than all holes will be drilled.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillAngles003.png)
  
* Do the same for second element and you should have all pilot holes drilled precisely and quickly aligned.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillAngles004.png)

**Note:** The same procedure you can use to drill pilot holes for hinges or any other fixture.

### Pocket holes - invisible connections

Personally I do not use this type of connections because I am not convinced to it, and also I do not have such jig. But I know that many woodworkers use pocket invisible connections and they love it. They use it especially for real wood and than put dowels inside the holes so the screws are not visible at all. 

### Drill pocket holes - manually

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDowels.png"> First apply dowels to the surface you want to drill. This is a little trick because I use dowels not tool for holes. Any `Cylinder`, dowel can be drill bit for hole, but [magicDowels](#magicdowels) allows to apply the dowls for further processing. If you use [magicDriller](#magicdriller) you need to keep the tool open or the drill bits will be removed. For the dowels, you have to adjust offset from the edge, size of the dowel and also dowels per side. You can do it at custom settings:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles001.png)

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicAngle.png"> Now use [magicAngle](#magicangle) at each dowel. I set angle 75 degree. As you see the dowels will be below the panel. Make sure you use exact axis for rotation. I use `Y` axis:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles002.png)

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicMove.png"> Now use [magicMove](#magicmove) at each dowel to move all the dowels above the panel. The dowels should touch a little bit the surface to get desired result. If the dowel will be below the surface the hole will be drilled inside the panel and the edge will not be visible at the surface correctly. I set move step to 85 at `Z` axis:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles003.png)

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillHoles.png"> Now select the panel surface you want to drill and all the dowels. If you have it selected click [drillHoles](#drillholes) and all the holes should be created with exact 15 degree angle. 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles004.png)
  
* This is not exactly what should be, because the drill bit for pocket holes in real-life has a little smaller tip at the end. So there should be also smaller hole at the end. But for this manually way it looks not so bad, in my opinion:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles005.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles006.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles007.png)


### Drill pocket holes - with magicDriller

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDriller.png"> To drill pocket holes you can use [magicDriller](#magicdriller). First select exact face you want to drill and run [magicDriller](#magicdriller). Also you can run [magicDriller](#magicdriller) and then select exact face and click `refresh selection`. For hole type choose `Pocket holes` and select predefined screw. You can also change the settings for your custom screw. If you want more rounded hole finish play with increase `Pocket sink` option. 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles008.png)

* Now click button for drilling and you have it:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles009.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles010.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles011.png)


# Realistic parts

### Realistic screws and pilot holes

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCountersinks.png"> If you want to drill pilot holes and apply realistic screws to the holes first you have to drill holes using procedure described at: [Drilling serially](#drilling-serially). For quick way I use the drilling countersinks icon to drill the rest of the holes at the edge of second element.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews001.png)

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDowels.png"> If you have drilled holes with countersinks, apply dowels with [magicDowels](#magicdowels) tool. But remember to apply the dowels to the edge not to the surface. This is because the predefined settings for the screws, I mean sink, are adjusted for the edge not to the surface. However, it also can be done manually with custom settings. If you apply to the surface you need to set exact sink.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews002.png)

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> Now merge realistic screw with your current active document. You can create such screw with PartDesign or even order such realistic part. For this case I use [Screw 45 x 40 mm](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture#screw-45-x-40-mm) from [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture). The dowels applied before is some kind of references points and they can be replaced with realistic screws. To replace the fake screws with realistic screws. Select the realistic screw and next all the fake dowels. Next click [panel2link](#panel2link) icon:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews003.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews004.png)

* As you see the head of the screw is inside the countersink and also the screw is inside the drilled pilot hole.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews005.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews006.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews007.png)
  
* You can also apply textures for the elements to get more realistic preview:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews008.png)

### Realistic screws and angles

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sketch2dowel.png"> First you have to create angles or any other fixture and drill holes according to this procedure: [Pilot holes for angles, hinges](#pilot-holes-for-angles-hinges). If you have it, first select face of the element, and next all `Sketches` of the holes. This allow you to create dowels directly from `Sketches` with exact orientation and size. If you have it selected click [sketch2dowel](#sketch2dowel):

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles001.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles002.png)

* For other element also first select face of the element, and next all `Sketches` of the holes. This allow you to create dowels directly from `Sketches` with exact orientation and size. If you have it selected click [sketch2dowel](#sketch2dowel):
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles003.png)
  
* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> Now merge realistic screw with your current active document. You can create such screw with PartDesign or even order such realistic part. For this case I use [Screw 4 x 16 mm](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture#screw-4-x-16-mm) from [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture). The dowels applied before is some kind of references points and they can be replaced with realistic screws. To replace the fake screws with realistic screws. Select the realistic screw and next all the fake dowels. Next click [panel2link](#panel2link) icon:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles004.png)
  
* As you see the screws are above the holes. To hide them all, select the `Body` container of the base screw, and move it down as much you want, you can use [magicMove](#magicmove) for that with exact step: 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles005.png)

  **Note:** I use a little bigger screws for angles than normally should be, because they hold things a little better than `3 x 20 mm` ones, so the head of the screw is not flat with the surface but you can use any screw size with the same way. For hinges you can use `3 x 20 mm`, without pilot holes.

### Realistic screws and pocket holes

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/edge2dowel.png"> First select edge of the hole inside the pocket hole and click [edge2dowel](#edge2dowel). You can select all edges for the panel to create dowels. The dowels should be created with exact angle, so it will be more easy to adjust the screw later. 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews001.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews002.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews003.png)

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> Now merge with you active document exact screw. In my case I use 19 mm thickness panel. So, according to the pocket holes and screws table I have to merge screw `4 x 30 mm`. If you have merged the screw, replace all the fake dowels with the realistc screw using [panel2link](#panel2link):
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews004.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews005.png)

* <img align="left" width="48" height="48" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicMove.png"> Adjust the screws using [magicMove](#magicmove). Make sure you set `1` at `Move step` to move the screw slower and more precisely. You can also use `Front` view and [makeTransparent](#makeTransparent) tool to see exactly where the screw goes. If you do it right you should get really nice result:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews006.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews007.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews008.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews009.png)

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
