# Woodworking workbench documentation

<img align="right" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/Woodworking.png"> FreeCAD is a very cool software and allows to design a lot of interesting things. However, FreeCAD is not dedicated to be software only for furniture designing. For this reason, some tasks when designing furniture can be challenging at the beginning. Despite the fact that I finished math, I have a problem with counting in my memory. For me, constantly calculating wood thickness and adding this to the position was a problem without a calculator. In addition, for me constantly starting from the `10 x 10 x 10` box `Cube` and setting it in the right position is a bit annoying. 

Woodworking workbench has been created because of my woodworking and coding hobby. Everything started from [getDimensions](https://github.com/dprojects/getDimensions/commits/master) project long time ago. I wanted to have [simple cut-list for chipboards order](https://github.com/dprojects/getDimensions/commit/a6f0a2221e90f717be95bd0dc1cc9f1ede95a329) and I found FreeCAD with low hardware requirements and possibility to implement the cut-list. Now it has been transformed into whole Woodworking workbench. The main goal for this workbench is to make the furniture designing process at FreeCAD more simple.

* [Main features](#main-features)
	* [Making panels](#making-panels)
		* [magicStart](#magicstart)
		* [Default panels](#default-panels)
		* [Copy panels](#copy-panels)
		* [Dedicated panels](#dedicated-panels)
		* [magicManager](#magicmanager)
	* [Resize panels](#resize-panels)
		* [magicResizer](#magicresizer)
		* [showConstraints](#showconstraints)
		* [quick resize icons](#quick-resize-icons)
	* [Move panels](#move-panels)
		* [magicMove](#magicmove)
		* [magicAngle](#magicangle)
		* [mapPosition](#mapposition)
		* [panelMove2Face](#panelmove2face)
		* [panelMove2Anchor](#panelmove2anchor)
		* [panelMove2Center](#panelmove2center)
		* [shelvesEqual](#shelvesequal)
		* [align2Curve](#align2curve)
		* [arrows](#arrows)
	* [Dowels and Screws](#dowels-and-screws)
		* [magicDowels](#magicdowels)
		* [panel2link](#panel2link)
		* [panel2clone](#panel2clone)
		* [sketch2dowel](#sketch2dowel)
		* [edge2dowel](#edge2dowel)
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
		* [cutDowels](#cutdowels)
	* [Construction](#construction)
		* [panel2profile](#panel2profile)
		* [panel2angle](#panel2angle)
		* [panel2angle45cut](#panel2angle45cut)
		* [cornerBlock](#cornerblock)
		* [cornerBrace](#cornerbrace)
	* [Joinery](#joinery)
		* [magicJoints](#magicjoints)
		* [magicCut](#magiccut)
		* [magicCutLinks](#magiccutlinks)
		* [magicKnife](#magicknife)
		* [magicKnifeLinks](#magicknifelinks)
		* [jointTenon](#jointtenon)
		* [cutTenons](#cuttenons)
		* [jointCustom](#jointcustom)
		* [panel2frame](#panel2frame)
		* [grainH](#grainh)
		* [grainV](#grainv)
		* [grainX](#grainx)
		* [magicCorner](#magiccorner)
	* [Preview](#preview)
		* [fitModel](#fitmodel)
		* [makeTransparent](#maketransparent)
		* [showVertex](#showvertex)
		* [selectVertex](#selectvertex)
		* [roundCurve](#roundcurve)
	* [Router](#router)
		* [Router bit - Cove](#router-bit---cove)
		* [Router bit - Round Over](#router-bit---round-over)
		* [Router bit - Straight](#router-bit---straight)
		* [Router bit - Chamfer](#router-bit---chamfer)
		* [multiPocket](#multipocket)
	* [Decoration](#decoration)
		* [colorManager](#colormanager)
		* [setTextures](#settextures)
	* [Dimensions](#dimensions)
		* [getDimensions](#getdimensions)
		* [sheet2export](#sheet2export)
		* [showSpaceModel](#showspacemodel)
		* [showSpaceSelected](#showspaceselected)
		* [magicMeasure](#magicmeasure)
	* [Parameterization](#parameterization)
		* [magicGlue](#magicglue)
		* [sketch2clone](#sketch2clone)
		* [showAlias](#showalias)
	* [Advanced](#advanced)
		* [panel2pad](#panel2pad)
	* [Code and Debug](#code-and-debug)
		* [scanObjects](#scanobjects)
		* [debugInfo](#debuginfo)
	* [Project manage](#project-manage)
		* [selected2LinkGroup](#selected2linkgroup)
		* [selected2Link](#selected2link)
		* [selected2Group](#selected2group)
		* [selected2Outside](#selected2outside)
* [How to use containers](#how-to-use-containers)
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
	* [Counterbore 2x with bolt](#counterbore-2x-with-bolt)
* [Raw wood, Lumber](#raw-wood-lumber)
	* [Glued table top](#glued-table-top)

# Main features

## Making panels

### magicStart

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicStart.png">This tool was created to make it easier to start designing furniture. It contains some structures that I often use personally, as well as other carpentry solutions suggested by users. However, this tool does not contain a complete list of solutions, because there are too many of them in the world of carpentry, practically every carpenter and manufacturer of furniture or accessories has their own standards. I try to adjust the contents of this tool in such a way that it gives the greatest possible possibilities for later processing and adapting the initial structure to your own needs. If you have any interesting woodworking idea or solution, worth to be added, please let me know.

* **calculate** button is intended to pre-calculate the remaining dimensions based on those given above this button, although in some cases you can skip this button and create an object or furniture with default settings
* **create** button is intended to create a given object, furniture

**Currently available solutions:**

* Simple storage ( front outside, back full )
* Simple bookcase ( no front, back HDF )
* Bookcase ( import parametric )
* Simple drawer ( import parametric )
* Simple chair ( import parametric )
* Picture frame ( import parametric )
* Simple table ( import parametric )
* Storage box ( import parametric )
* Dowel 8x35 mm ( import parametric )
* Screw 4x40 mm ( import parametric )
* Modular storage ( front outside, 3 modules )
* Screw 3x20 mm for HDF ( import parametric )
* Screw 5x50 mm ( import parametric )
* Counterbore 2x 5x60 mm ( import parametric )
* Shelf Pin 5x16 mm ( import parametric )
* Angle 40x40x100 mm ( import parametric )
* Foot ( good for cleaning )
* Foot ( standard )
* Foot ( more stable )
* Foot ( decorated )
* Foot ( chair style )
* Drawer with front outside ( fit into the shelf gap )
* Drawer with front inside ( fit into the shelf gap )
* Front outside ( fit into gap )
* Front inside ( fit into gap )
* Shelf ( fit into gap )
* Center side ( fit into gap )
* Simple storage ( front outside, back HDF )
* Simple storage ( front inside, back full )
* Simple storage ( front inside, back HDF )
* Drawer series with front outside ( fit into the shelf gap )
* Drawer series with front inside ( fit into the shelf gap )
* Face Frame outside ( frame around, fit into gap )
* Face Frame outside ( frame with center, fit into gap )
* Face Frame outside ( frame for custom changes, fit into gap )
* Simple bookcase ( face frame, no front, back HDF )
* Simple storage ( face frame, no front, back HDF )
* Front outside with glass ( simple frame, fit into gap )
* Front outside with glass ( frame with decoration, fit into gap )
* Front inside with glass ( simple frame, fit into gap )
* Front inside with glass ( frame with decoration, fit into gap )
* Shelf series with equal space ( fit into gap )
* Table ( kitchen simple style )
* Table ( coffee simple style )
* Table ( kitchen modern style )
* Table ( coffee modern style )
* Table ( kitchen decorated style )
* Table ( coffee decorated style )

**Video tutorials:** 
* [Furniture creation tool](https://www.youtube.com/watch?v=lHQ1J9Nahcs)

### Default panels

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultZY.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultYZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultZX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultXZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultYX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultXY.png"> There are many types of wood. So there is no chance to cover all possible wood sizes provided by the market. This starting panels allow you for quick start. You do not have to start each time from `10 x 10 x 10` box `Cube` object and think where should be the thickenss. This tool creates default panel that can be easily resized. You can clearly see where should be the thickness to keep exact panel `XYZ` axis orientation. **Note:** All furniture elements should be created according to the `XYZ` axis plane, if possible. Avoid building whole furniture with rotated elements. If you want to rotate panel with dowels, better create panel with dowels without rotation, pack panel with dowels into container like `LinkGroup`, and use [magicAngle](#magicangle) to rotate whole `LinkGroup`. You can rotate whole furniture like this with single click and the dowels will be in the correct place after rotation. If you would like to apply dowels at rotated element it would be pointless complication, almost impossible at FreeCAD.

### Copy panels

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyZY.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyYZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyZX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyXZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyYX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyXY.png"> This icons copy selected panel into exact `XYZ` axis orientation. By default you can copy any panel based on `Cube` object. If you want to copy `Pad`, you need to have constraints named `SizeX` and `SizeY` at the `Sketch`. For other object types you need to have `Length`, `Width`, `Height` properties at object (Group: `Base`, Type: `App::PropertyLength`). The new panel will be created at `(0, 0, 0) Vector` coordinate `XYZ` axis position. You can use [mapPosition](#mapposition) tool to move the new panel to the original panel position. To copy panel in-place without changing orientation, you can use [magicMove](#magicmove) tool or `CTRL-C` and `CTRL-V` keys with [arrows](#arrows) to move the copy.

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceZY.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceYZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceZX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceXZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceYX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceXY.png"> This icons creates new panel at selected face. The blue panel represents the selected object and the red one represents the new created object. The icon refers to base `XY` model view (0 key position). Click [fitModel](#fitmodel) to set model into referred view, and to be sure the model and face you have selected refers to exact icon. The new created panel will get the same dimensions as panel of the selected face. **Note:** If you have problems with unpredicted result, "side effect of Magic Panels", please use [magicManager](#magicmanager) to preview panel before creation and [magicMove](#magicmove) to move or copy panels.

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenZY.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenYZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenZX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenXZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenYX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenXY.png"> This icons creates new panel between two selected faces. Selection faces order is important. To select more than one face, hold left `CTRL` key during second face selection. The blue panels represents the selected objects and the red one represents the new created object. The icon refers to base `XY` model view (0 key position). Click [fitModel](#fitmodel) to set model into referred view. If the two selected panels will be matching the icon, the new created panel should fill the gap between the selected faces. You can experiment with selection faces outside to resize the new panel. **Note:** If you have problems with unpredicted result, "side effect of Magic Panels", please use [magicManager](#magicmanager) to preview panel before creation and [magicMove](#magicmove) to move or copy panels.

### Dedicated panels

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCoverXY.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBackOut.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideRightUP.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideLeftUP.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideRight.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideLeft.png"> Dedicated panels allows you to add specific furniture element. You can add sides, back or top of the furniture with single click. The side panels improves the thickness offset at the face tools. If you would like to add back of the furniture manually, you have to calculate the back dimensions first. Next you have to move the panel exactly to the back of the furniture position. It is not so easy to do it manually because `1 mm` offset might be a problem. Now you can make it with several clicks, without calculating anything manually. **Note:** If you have problems with unpredicted result, "side effect of Magic Panels", please use [magicManager](#magicmanager) to preview panel before creation and [magicMove](#magicmove) to move or copy panels.

### magicManager

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicManager.png">
This tool allows to preview panel before creation. It allows to see panel at single selected face and also panel between two faces. This tool can be used if you have problems with unpredicted result, "side effect of Magic Panels". However, clicking single icon is sometimes more quicker than opening GUI and choosing right panel. Sice `0.21 version` this tool is able to create panel from selected vertices. This functionality uses observer for reading and helping select vertices. You do not have to hit the vertex directly. If you select edge or face, the nearest vertex will be selected for you. Also you can remove last selected vertex from list if you make mistake. The selected vertices should create wire, shape, but you do not have to select last vertex to close the wire. The first selected vertex will be automatically added at the end to close the wire. If the panel thickness is not set by the user, the thickness for the new panel from vertices will be set from first selected object. Custom thickenss works only for vertices.

* **Panel at face:** To create panel at face select single face and click `refresh selection`.
* **Panel between faces:** To create panel between two faces select two faces and click `refresh selection`. To select more faces hold `CTRL` key. The selection order is important. If the panel is created outside change selection order.
* **Panel from vertices:** To create panel from vertices, you have to activate observer. The `first` means the thickness will be get from first selected object. You can set custom thickness if you want.

**Options:**
  
* **Plane:** You can select panel orientation according to the `XYZ` coordinate axes. The panel can be created at planes: `XY`, `YX`, `XZ`, `ZX`, `YZ`, `ZY`, if you select single face. If you select two faces this tool automatically recognize plane of selected faces and adjust possible panels to create, there will be two panels for valid planes only.
* **Anchor:** You can select position for the new panel. The anchors are the face vertices. If the object is for example `Cut` there might be more than four anchors to choose.
* **Size:** Custom size is taken from edges. For example, if you have `Cut` object you can set panel with the same size as the cut edge. All edges should be available, search for the right one.
* **Offset:** The first selected offset means `no offset` from currently selected `Anchor`. All next are offset with current selected `Size` for `X-`, `X+`, `Y-`, `Y+`, `Z-`, `Z+` coordinate axis. This can be helpful if you want to make frame but the frame is for example `20 mm x 40 mm x 600 mm` and need to be offset with `40 mm`, different size than thickenss `20 mm`.

**Video tutorials:** 
* [Panel from vertices](https://www.youtube.com/watch?v=6s0fbagPeZA)
* [Making panels improvement](https://www.youtube.com/watch?v=sunE2rLThZI)

## Resize panels

### magicResizer

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicResizer.png"> This tool allows to resize `Cube` or `Pad` panel and also other objects based on `Pad` e.g. construction profiles. Make sure your `Pad` object has defined constraints, you can use [showConstraints](#showConstraints) tool for that. If the object has no constraint at the selected edge the object will not be resized. The constraints do not have to be named but must be defined. 

**Options:**

* **Selected edge only:** If you select edge only you can resize the edge with `Resize step` via `resize -` and `resize +` buttons. This is simple resize with current `Resize step` and edge selection. In this mode the tool search for all sizes with selected edge size and resize each one with `Resize step`. Use `resize -` and `resize +` buttons in this mode.

* **Selected edge and face:** This mode allows to resize object to the nearest face of other object. To use this mode, first select edge to resize and next select nearest face of any other object. If the face is at the right side this tool will calculate space needed to resize and will change the exact size. If the face is before the selected edge the object will be resized and moved to the left. So, the result will be resized object from the left side. Use `resize to nearest` button in this mode. If you have selected face the `Resize step` should be automatically calculated. You can also undo this operation via `resize -` button.

* **Selected edge and edge:** This mode allows to resize the object more precisely. If the container is rotated the face may not be good choice. So, you can select edge. In this case the CenterOfMass of the edge will be used as reference point. To use this mode, first select edge to resize and next select nearest edge of any other object. Use `resize to nearest` button in this mode.

* **Selected edge and vertex:** This mode allows to resize the object more precisely. You can select vertex to resize the object exactly to the selected point. To use this mode, first select edge to resize and next select nearest vertex of any other object. Use `resize to nearest` button in this mode.

**Video tutorials:** 
* [Smart resizer tool](https://www.youtube.com/watch?v=t1G7qnRfAgY)
* [How to handle dimension changes](https://www.youtube.com/watch?v=HED1-BH66BU)

### showConstraints

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showConstraints.png"> To use this tool first select objects to see edges with the same size as defined constraints. **Note:** This tool search all constraints for selected objects. If the constraints is non-zero this tool search for all edges with the same size. It allows for quick preview if all the edges are defined by the Sketch. However, in some cases, if the constraints is offset and it is equal edge size this will give false result. To select more objects hold left CTRL key during selection. 

<br><br><br>

### quick resize icons

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize6.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize5.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize3.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize2.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize1.png"> You can resize panel, or even many panels at once, very quickly. The resize step is selected panel thickness, so you can solve the common problem with thickness offset. For example to move top of the furniture and make shelf from it, you have to resize the panel `2 x` with thickness step and once from other side. This may not be so easy calculation, and you may have to calculate something like `534 - 18 - 18 = ?` and `613 - 18 = ?`. Now you can click three times and you have it without thinking. You can also resize Cylinders (drill bits), the long side will be `Height`, the short will be diameter, the thickness will be `Radius`. For Cone objects (drill bits - countersinks, counterbore) the long side will be `Height`, the thickness will be `Radius1` (bottom radius) and the short will be `Radius2` (top radius). [Holes, Countersinks, Counterbores](#holes-countersinks-counterbores).

## Move panels

### magicMove

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicMove.png"> This tool allows you to move and copy objects more easily. This tool supports multi-selection, hold left-CTRL key during selection to select more objects, so you can move or copy many objects at once. 

**Options:**

* **refresh selection:** loads new objects.

* **Move:** In this mode you can move any object with custom step. You can also move containers, for example panel with dowels inside `LinkGroup`.
  * buttons: `X-`, `X+`, `Y-`, `Y+`, `Z-`, `Z+` move object into the chosen axis direction, there is auto-repeat so you can hold the button to move objects more quickly.
  * `Move step` if the object is recognized the `Move step` will be set by default with selected object thickness. The offset is calculated from objects anchors, usually left bottom corner (vertex).

* **Copy:** In this mode you can copy any object with custom offset. For example you can quickly create shelves with equal space or garden floor from small panels.
  * `auto` by default, if the object is `Cube` the `copyObject` will be used, otherwise `Clone` will be created.
  * `copyObject` good for simple objects like `Cube`.
  * `Clone` is useful if you want to make copy of `Body` or `Part` with many Bodies.
  * `Link` if you want to copy `LinkGroup` and generate cut-list, it is better to set this copy option, not `copyObject`. 
  * `copy to new container` next element will be copied to new `LinkGroup` container. If you click the button this will turn into disabled and will be waiting for new copy created to avoid double clicks.
  * `Copy offset` this is offset between objects but calculated from objects sides. If this is set to `0` the next element will be created without space in relation to the last element.
  * buttons: `X-`, `X+`, `Y-`, `Y+`, `Z-`, `Z+` copy object into the chosen axis direction, there is auto-repeat so you can hold the button to copy objects more quickly.

* **Copy by Edge:** In this mode you can copy any object but using selected edge as position reference. This feature allows you, for example, to copy part of the furniture without further positioning each element one by one.
  * `auto` by default, if the object is `Cube` the `copyObject` will be used, otherwise `Clone` will be created.
  * `copyObject` good for simple objects like `Cube`.
  * `Clone` is useful if you want to make copy of `Body` or `Part` with many Bodies.
  * `Link` if you want to copy `LinkGroup` and generate cut-list, it is better to set this copy option, not `copyObject`. 
  * `set` allows to set edge as copy reference point.
  * `Additional offset` this offset will be added to the object offset. For example, if the objects distance from the selected edge on the `X` axis is `18`, i.e. the shelves are touching the right side of the furniture inside, but the selected edge is the right outer edge of the furniture, and the additional offset is set to `-18`, then the shelves will be created `18 (distance) - 18 (additional offset) = 0` from the edge, touching the right outer side of the furniture. So for example you can copy shelves from left to right and ignore the thickness of the right side board of the furniture and quickly extend the furniture to the right.
  * `create`creates a panel in the selected axis direction. In the film, the button responsible for the case in which the plane of the object to be copied is the same as the plane of the selected edge is disabled. This was to avoid copying the object "in place". However, this can be used, for example, to copy the top shelf to the bottom. If the shelf is on the top of the furniture and you want to create a copy along the Z edge, i.e. relative to the edge of the right side of the furniture, the copy point will be the center of the edge, which means that the top shelf will be copied as the bottom shelf.
  
* **Copy by Path:** This mode allows you to create panels along the path. If the panel is already at the path, next panel will be created with the offset from selected panel. With this approach you can remove some panels and fill the gap in a different way, for example with different rotation. If the panel is outside the path, the first panel will be created at the 0 point of the path. This feature allows you, for example, to create irregular shpes like garden sunbed.
  * `auto` by default, if the object is `Cube` the `copyObject` will be used, otherwise `Clone` will be created.
  * `copyObject` good for simple objects like `Cube`.
  * `Clone` is useful if you want to make copy of `Body` or `Part` with many Bodies.
  * `Link` if you want to copy `LinkGroup` and generate cut-list, it is better to set this copy option, not `copyObject`. 
  * `copy to new container` next element will be copied to new `LinkGroup` container. If you click the button this will turn into disabled and will be waiting for new copy created to avoid double clicks.
  * `Rotation X, Y, Z` allows to apply rotation angle for the new object before it will be created. The rotation is added to the last panel rotation, so to stop rotate you have to set 0 again. This approach allows to add rotation during panel creation, so you can adjust each panel during creation to fit the curve, see also [align2Curve](#align2curve).
  * `Next point step` is offset for new panel. This is related to the point at the path. By default it is set to second size of the panel.
  * `set` allows to load the path or reset start position. You can refresh only path here without changing objects to copy. The path can be Wire, Sketch, Helix, or any edge, also edge of the hole.
  * `copy along path` creates new panel along the path. This button has auto-repeat mode, if you hold it this will be creating panels without clicking many times.

* **Mirror:** This option create mirror with reference as edge, face or vertex, also you can add additinal offset. You can select single element like `Cube` or container like `LinkGroup` with more elements inside. This option recognize if the selected object is `LinkGroup` container and if not, it will create `LinkGroup` for the object, so you will be able to extend, build on this object later.
  * `set` allows to load the reference point for mirror as edge, face or vertex.
  * `Mirror XYZ:` is base position for mirror, the object will be in the middle between object and new created mirror if there is no additinal offset.
  * `Additional offset` this offset will be added to the mirror position.
  * `create` creates mirror in the chosen axis direction.

* **Cross:**
  * `Corner cross:` buttons `-`, `+` resize the cross in the right bottom of the screen, it has auto-repeat.
  * `Center cross:` buttons `on`, `off` turn on and off the center cross at the screen.
  * `keep custom cross settings` allows to store the custom cross setting after this tool exit.

**Video tutorials:** 
* [How to use magicMove](https://www.youtube.com/watch?v=DpU2zlckv88)
* [How to copy part of the furniture](https://www.youtube.com/watch?v=oxNiwtZV-Uc)
* [How to handle dimension changes](https://www.youtube.com/watch?v=HED1-BH66BU)

### magicAngle

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicAngle.png"> This tool allows to rotate panels and even other more complicated objects, like construction profiles or containers. It allows for multi-selection, so you can rotate many elements with the same rotation point at once.

**Options:**

* **Sphere radius** Allows you to resize rotation indicator sphere. This tool checks reference for the object, content of containers and get size to set the default size of the sphere. by default the sphere radius is set to object thickness. You can increase or decrease the value or set your custom one.
* **Rotation point** Allows you to switch between several predefined rotation points. If the predefined points not allows you to rotate the object as you wish, you can add your custom point. You can select vertex, face or edge and click `add selected vertex`. If the selected sub-object is face the vertex will be set to its CenterOfMass. If the sub-object is edge the first vertex for the edge will be set. There is also ration, that show you how many rotation points you have to choose and which one is currently chosen.

* **X, Y, Z** Allows to rotate object according to the axis. There is also screen with current rotation status so you can quickly rotate back the object. You can also choose your custom `Angle step` for rotation. 

**Video tutorials:** 
* [Quick parametric fence](https://www.youtube.com/watch?v=egmC-uR4aa4)

### mapPosition

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/mapPosition.png"> First select object to copy position, next select objects to move. **Note:** This tool allows to move objects to the same position as first selected object. The objects will be moved without rotation. Only the placement will change. If the first selected object is rotated the objects may not match exactly the starting point. This tool is very useful if you want to redesign furniture and you want to create new element. Using this tool you can quickly move the new element to the same position of old element and remove the old element. To select more objects hold left CTRL key during selection. With this tool you can also move Cylinders and Sketches more precisely. If first you select Edge or Face the Cylinders or Sketches will be moved to the CenterOfMass. If first you select Vertex the Cylinders or Sketches will be moved to the selected Vertex position.

**Video tutorials:** 
* [Mapping position](https://www.youtube.com/watch?v=841xzb_uRpc)
* [mapPosition little improved](https://www.youtube.com/watch?v=pMKLXvwmGSI)

### panelMove2Face

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMove2Face.png">To adjust panel to face please select: 

1. selection: **face**
2. selection: **objects to align**

**Note:** This tool allows to align panels to face position. You can select more objects holding left CTRL key. This tool allows you to avoid thickness step problem, if you want to move panel to the other edge but the way is not a multiple of the panel thickness. For rotated containers use [panelMove2Anchor](#panelmove2anchor).

**Video tutorials:** 
* [How to create shelves with equal space](https://www.youtube.com/watch?v=2odJa0baGqw)
* [Simple table](https://www.youtube.com/watch?v=Xru52f8uyBk)
* [Move to face](https://www.youtube.com/watch?v=i9pXqdEhahU)

<br><br><br>

### panelMove2Anchor

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMove2Anchor.png"> This tool allows to align panels more precisely, with anchor. To align panels with anchors first select anchor at base object, next select anchor at each object to move. Hold left CTRL key to select anchors.

Available anchors to select: 

* **vertex** - selected vertex will be set as anchor,
* **edge** - CenterOfMass of the selected face will be set as anchor,
* **face** - CenterOfMass of the selected face will be set as anchor,
* **object** - default object anchor, of the Placement, will be set as anchor.

**Video tutorials:** 
* [Align to anchor](https://www.youtube.com/watch?v=IfVJVXVc9r8)

<br><br><br>

### panelMove2Center

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMove2Center.png"> This tool allows to move objects to the center of two holes or two vertices. The edge holes or vertices should lie on one of the coordinate axes `XYZ`. The object can be `Cylinder`, `Cone` (dril bit), `Cube` (panel), `Pad` or `LinkGroup` with as many objects you want. If you want to move `Pad`, select `Body`. If you want to move many Pads, select Body or pack all `Part` into `LinkGroup` and select `LinkGroup` to move. Make sure you do not have `Sketch` position set. This tool use `.Shape.CenterOfMass` but if it is not available for object like it is for `LinkGroup` the center will be calculated from vertices. You can move to the center many objects at once. Hold left CTRL key during selection. 

**Video tutorials:** 
* [Move to center](https://www.youtube.com/watch?v=zKttrKdahg8)

<br><br><br>

### shelvesEqual

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/shelvesEqual.png">To set equal space between shelves please select: 

1. selection: **X axis edge**
2. selection: **X axis edge**
3. selection: **shelves to set equal space**

**Note:** This tool allows you to set equal space for selected shelves. It works only at Z axis. To select more objects hold left CTRL key during selection.

**Video tutorials:** 
* [How to create shelves with equal space](https://www.youtube.com/watch?v=2odJa0baGqw)

<br><br><br><br><br>

### align2Curve

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/align2Curve.png"> This tool allows to align panels to the curve. It has been created for magicMove Copy Path option, to align panels to the curve. To select more objects hold left CTRL key during selection. To use this tool the panel need to have only single axis rotation offset. For example if you rotate panel 35 degrees around Y axis the vertex will touch the curve. This tool not works if you need to rotate the panel additionally, for example 15 degrees around X axis. For more details see description at documentation page. 

Selection modes:

* **Curve and Edges** In this mode you can select curve and next edge at each object you want to align to the curve. This mode is automatic and this tool will try to calculate the angle between the curve and the selected edge. The selected edge need to be this one with object anchor and the object anchor should be already at the curve. If this tool will be able to determine the angle, it will align the panel. Otherwise the panel will be skipped.

* **Curve and Vertex** In this mode you can select curve and next vertex at each object you want to align to the curve. This mode is more precised and slower. It allow to align panel backwards, so the selected vertex will be before he anchor. In this mode the tool will try to search the curve from the nearest side of the vertex. If the curve will be found the panel will be aligned, otherwise the panel will be skipped.

**Video tutorials:** 
* [Align to curve](https://www.youtube.com/watch?v=fbJV_SEuNLg)

<br><br><br>

### arrows

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveXp.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveXm.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveYp.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveYm.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveZp.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveZm.png"> With the arrows you can quickly move panels. The move step is the selected panel thickness, if reference for the selected object can be recognized. You can also use the arrows for quick copy. Select object at objects Tree, click `CTRL-C` and `CTRL-V` to copy in-place the selected object and use arrows to move the object. The thickness step solves common furniture problem with thickness offset. You do not have to calculate something like `643 - 18 - 18 - 18 = ?`, click three times and you have it. If the thickness will not be recognized the step will be `100`. This approach allows you to move whole furniture segments very quickly. You can select container like `Body` or `LinkGroup` with many elements and move it quickly. The arrows recognize the view model rotation. However, all possible rotations are not recognized, sometimes the movement may not be correctly aligned with the arrow icon. So, it strongly recommended to click [fitModel](#fitmodel) tool before using arrows. If you want precisely move object, use [magicMove](#magicmove) tool, instead.

## Dowels and Screws

### magicDowels

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDowels.png"> This tool allows to add mounting points to panels. You can add predefined mounting points e.g. screws, dowels, shelf supporter pins or add custom mounting points. This is very quick way to add mounting points to the furniture, no calculation needed to place dowel exactly in the middle of the edge. If you would like to add e.g. 40 dowels to the whole furniture and align all of them manually, it would probably be big challenge. With this tool you can do it with single click in many cases. Make sure the green faces are visible, because they refers to the head of the screw. If you would like to replace the dowels with detailed screw later, this might be important if the dowel is rotated incorrectly, the screw will be rotated incorrectly as well. 

**Options:**

* **+:** You have to select face and click `+` to start using this tool. Also you can change face with this button. However you can also first select face and next open this tool, so this tool will open GUI with the face loaded.
* **1 / 4:** For example it means you have selected `1` edge from `4` edges available. The same for other selections.
* **Select edge:** You can choose the edge for the dowels. Normally, for surface there are 4 edges but if the object is for example `boolean Cut` there might be much more edges or only 2 edges if this is edge of the board.
* **position autodetect:** this checkbox is checked by default and allows for searching correct edge offset, sink and rotation. The edge selection might be slower but no further adjustment will be needed, I hope.
* **create:** This store the dowels permanently.

For manual adjust you can use:

* **Adjust edge:** Allows to adjust offset from the edge. This option is useful if by default the dowels not sink to the surface, so there is problem with correct positioning by default. 
* **Adjust sink:** With this option you can change the sign for the sink. Sometimes it solves the problem with correct positioning and further adjust is not needed.
* **Adjust rotation:** You can rotate the dowels. There are some predefined rotations according to the current face plane  to speed up this process.
* **Select sides:** You can choose the side for the dowels, left side only, right side only or both sides.
* **Text inputs:** You can set your custom values here and click `show custom values` to see if the dowels fits your needs. 
* **keep custom settings:** This checkbox allows you to keep custom values, for example custom dowels size or dowels per side, while you changing the faces.
* **show custom values:** Allows you to preview the custom settings but you need to click `create` button to store dowels.

**Video tutorials:** 
* [Adding dowels improved](https://www.youtube.com/watch?v=6qixKpVKA-0)
* [Adding dowels](https://www.youtube.com/watch?v=q7tJffBBUGY)
* [Make quickly 168 dowels](https://www.youtube.com/watch?v=_a_Q7BjEHLA)
* [Tenons with magicDowels](https://www.youtube.com/watch?v=xXfy9KaYJC4)

### panel2link

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> This tool allows to replace simple objects with any detailed object, e.g. `Cylinders` with realistic looking screws made using `PartDesign`. First you have to select detailed object, next select simple objects to replace with `Links`. The first selected detailed object can be `Part`, `LinkGroup` or any other created manually or merged with your project. You can replace more than one simple object at once with `Link`. To select more objects hold left `CTRL` key during selection. The simple objects should imitate the detailed object to replace all of them in-place with realistic looking one. For more details please see: [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture).

**Video tutorials:** 
* [Dowels and Screws are fully parametric](https://www.youtube.com/watch?v=hWaM19edjFE)

### panel2clone

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2clone.png"> This tool allows to replace simple objects with any detailed object, e.g. `Cylinders` with realistic looking screws made using `PartDesign`. First you have to select detailed object, next simple objects to replace with `Clones`. The first selected detailed object can be `Part`, `LinkGroup` or any other created manually or merged with your project. You can replace more than one simple object at once with `Clone`. To select more objects hold left `CTRL` key during selection. The simple objects should imitate the detailed object to replace all of them in-place with realistic looking one. This tool works with the same way as [panel2link](#panel2link) but instead of `Links` it creates `Clones` objects. It can be useful if you want to remove the base object and have clean objects Tree. Also if you want to change each copy separately. [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture).

**Video tutorials:** 
* [Dowels and Screws are fully parametric](https://www.youtube.com/watch?v=hWaM19edjFE)

### sketch2dowel

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sketch2dowel.png"> First select face, next Sketches of the holes to create dowels. This tool allows to create dowel from Sketch of the hole. The first selected face refers to the side the dowel will be raised, exact orientation for the dowel. Dowel position will be get from the Sketch. The dowel Radius and Height will be get from hole object. If the hole is throughAll the dowel height will be very big, so make sure you use dimensions for hole. To select more Sketches hold left CTRL key during selection. 

**Video tutorials:** 
* [Dowels from Sketch](https://www.youtube.com/watch?v=CI4M5_DDWSg)

### edge2dowel

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/edge2dowel.png"> This tool allows to create dowels above the selected hole edges. To create dowel select edge of the hole. You can select many edges at once but all the holes need to be at the same object. The dowel Height will be 40. The dowel radius will be get from the selected edge hole radius. To select more objects hold left CTRL key during selection. 

**Video tutorials:** 
* [Dowels from holes](https://www.youtube.com/watch?v=l8-Jven6VTQ)

<br><br><br>

## Fixture

### magicFixture

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicFixture.png"> This tool has a little different approach than [magicDowels](#magicdowels) tool, because it allows to apply any type of fixture. Instead of `Cylinders` preview, it creates link to the detailed object and move it to the selected face. You can set exact offset from corner, offset from edge and sink. Also you can select predefined rotations and all edges. If you want you can turn on and off the manually edit mode and move and rotate it by hand. With this tool you can very easily apply detailed aluminum angles. For more details please see: [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture).

<br><br><br>

### edge2drillbit

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/edge2drillbit.png"> This tool allows to create drill bits for making simple hole. The drill bits will be created above the selected hole edges. To create drill bits select edge of the hole. You can select many edges at once but all the holes need to be at the same object. The drill bit Height will be 16. The drill bits radius will be get from the selected edge hole radius but will be little smaller, 1 mm, than the hole to make pilot hole. To select more objects hold left CTRL key during selection. This feature can be used to create drill bits above holes at hinges, angles or other fixture type.

<br><br><br>

## Drilling holes

### magicDriller

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDriller.png"> This tool is similar to [magicDowels](#magicdowels) but instead of applying dowels this tool allows to drill holes, countersinks or counterbores serially with predefined or custom sets. You can choose the same predefined screws, dowels and pins as at [magicDowels](#magicdowels) but instead of dowels there will be created set of drill bits. The drill bits will be smaller than screws to allow drill pilot holes for screws. For dowels the drill bits will be with the same size. [Drilling serially](#drilling-serially)

<br><br>

### drillHoles

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillHoles.png"> This is drill bit to make simple hole. The hole will be drilled below the bottom part of the drill bit, below the red face of the cylinder. The radius and depth of the hole will be the same as drill bit radius and height. You can resize the drill bit if you want. If you select face only, the drill bit will be created in the corner of the face (0 vertex). So, you will be able to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face to get exact hole depth. If you select face and than any amount of drill bits, the holes will be drilled below each drill bit. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

<br>

### drillCountersinks

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCountersinks.png"> This is drill bit to make countersink with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of countersink will be drill bit Radius2. The hole depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

<br>

### drillCounterbores

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCounterbores.png"> This is drill bit to make counterbore with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of counterbore will be drill bit Radius2. The hole depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

<br>

### drillCounterbores2x

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCounterbores2x.png"> This is drill bit to make counterbore2x with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of counterbore will be drill bit Radius2. The hole depth will be panel thickness. The counterbore depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

<br>

### magicCNC

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicCNC.png"> This tool is some kind of CNC drilling machine simulator. It is the same [magicMove](#magicmove) tool but improved for the drilling purposes. The axis which move the drill bit up and down is automatically hidden at this tool. So, you can move the drill bit at the surface and you not move the drill bit up or down by mistake and cause incorrect hole depth. Also this tool has option to drill by button click. It recognize the drill bit type by the label. For the countersink the label need to contains "countersink", and for counterbore need to contains "counterbore". For other label the simple hole will be drilled. This tool also allows for turn on and off the manuall edit mode, transform FreeCAD. So, you can move the drill bit by hand and drill holes by clicking buttons. This option can be useful for artists whom want to make holes in artistic way, not with mathematical precision. For more info see: [Drilling via magicCNC](#drilling-via-magiccnc)

### cutDowels

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/cutDowels.png"> This tool is designed to allow drilling for designing approach based on Cut holes using Cylinders without creating PartDesign objects. This tool allows you to automatically cut all dowels from selected panel. You do not have to select and search exact dowels that belongs to the selected panel. If you select panel, this tool search for all dowels that belongs to the selected panel and apply Boolean Cut on the panel. You can select many panels at once to cut dowels. To select more panels hold left CTRL key during selection. During this process only the copies will be used to cut, so the original Cylinders will not be moved at the objects Tree and will be visible at cut-list report. This feature is sensitive for visibility of Cylinders. So, you can hide Cylinders you do not want to be cut out from the panel.

**Video tutorials:** 
* [Search and cut dowels](https://www.youtube.com/watch?v=Oogs8LqkReQ)

## Construction

### panel2profile

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2profile.png"> Please select valid `Cube` or `Pad` object imitating profile. The selected `Cube` or `Pad` objects need to have two equal sizes e.g. `20 mm x 20 mm x 300 mm` to replace it with construction profile. **Note:** This tool allows to replace panel with construction profile. You can replace more than one panel at once. To select more panels hold left `CTRL` key during selection. The new created construction profile will get the same dimensions, placement and rotation as the selected panel. If you have all construction created with simple panel objects that imitating profiles, you can replace all of them with realistic looking construction profiles with single click.

**Video tutorials:** 
* [Construction profiles](https://www.youtube.com/watch?v=5hXMFAxXQag)

### panel2angle

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2angle.png"> Please select valid faces at any amount of `Cubes` or `Pads` to cut the faces and create construction angle profiles. **Note:** This tool allows to replace panel with construction angle. You can replace more than one panel at once. To select more faces hold left `CTRL` key during faces selection. The new created construction angle will get the same dimensions, placement and rotation as the selected panel. You can cut any faces at panel. However, if the panel has two equal sizes e.g. `20 mm x 20 mm x 600 mm`, the ends will be cut as well, so you do not have to select them. If you do not have same sizes you have have to select ends too, if you want to cut them. If the selected faces are not valid, e.g. opposite faces, the final object may disappear and be broken. You can remove last operation and try again. If you have all construction created with simple panels that imitating angles, you can replace all of them with realistic looking construction angles with single click and they will be rotated according to the selected faces.

**Video tutorials:** 
* [Construction profiles](https://www.youtube.com/watch?v=5hXMFAxXQag)

### panel2angle45cut

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2angle45cut.png"> Please select valid face at construction angle to create 45 cut at edges. **Note:** This tool allows to cut construction angle with 45 cut. You can select many construction angles at once but only single face can be selected for each construction angle. If the construction angle is C-shape you can select face inside profile and two sides will be cut. If the construction angle is L-shape you select single face inside profile and only single side will be cut. Because to create frame with L-shape profiles you have to cut only single side. To create frame with C-shape profiles you have to cut both sides. The face should be selected inside profile to set exact cut size without profile thickness. To select more faces hold left `CTRL` key during faces selection. You can remove last operation and try again. If you have all construction created with construction angles you can cut all of them at once.

**Video tutorials:** 
* [Construction profiles](https://www.youtube.com/watch?v=5hXMFAxXQag)

### cornerBlock

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/cornerBlock.png"> Please select single edge at each panel you want to change into corner block. **Note:** This tool allows to create corner block from selected edge. The cut size will be the panel thickness. For example you can create Cube 100 mm x 100 mm x 100 mm in the corner of the table to support table leg, and you can change it into corner block, quickly with single click. You can replace more than one panel at once. Hold left CTRL key during edges selection.

**Video tutorials:** 
* [Table corner block](https://www.youtube.com/watch?v=Fyss9sZ4AgE)

<br><br><br>

### cornerBrace

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/cornerBrace.png"> Please select single edge at each panel you want to change into corner brace. **Note:** This tool allows to create corner brace from selected edge (the single visible edge). The cut size will be the panel thickness for the first edge and for the second edge half of the thickness. So, you get nice looking corner brace with single click. For example you can create Cube 100 mm x 100 mm x 100 mm in the corner of the table to support table leg, and you can change it into corner brace, quickly with single click. You can replace more than one panel at once. Hold left CTRL key during edges selection.

**Video tutorials:** 
* [Table corner brace](https://www.youtube.com/watch?v=Y9Wa4o9N1mM)

<br><br><br>

## Joinery

### magicJoints

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicJoints.png"> This tool is to create Mortises and Tenons. It allows to create any joint shape using Sketch. First you have to create joint pattern with Sketch. The Sketch do not have to be assigned to the face of object, the `Support` can be empty. The joint pattern should be created in the corner of coordinate axes cross. This will be better for rotation and positioning. However, you can add any offset, if you want. If you have joint pattern created, select the Sketch and Face to create Mortise or Tenon. First `Anchor` position is the Sketch position, all others are the vertices of selected face, so you can move the Sketch to any point at the selected face. If you want to map the Sketch to the another object, you may need use rotation selector. If the selected object is `Cube` it will be automatically converted to `Pad` during Mortise or Tenon creation. The Mortise and Tenons are `PartDesign :: Pocket` and `PartDesign :: Pad` objects, so they can be easily managed by FreeCAD. If you want to select more objects hold left `CTRL` key during selection. You can also refresh only face. It is useful, if you want to map quickly the Sketch to the another object in the same line. To refresh face only, select face and click `refresh all selections` button or use `set` button for exact face.

**Options:**

* **set** The buttons allow to refresh single selection. You can quickly change Sketch or faces.
* **refresh all selections** read all selections and set objects, if you have only single face selected, the 2nd selection will be updated.
* **Anchor:** First selection is the actual `Sketch` global position. Next are vertices from selected face. You can switch between the available positions to adjust the position more precisely.
* **Rotation:** This is `Sketch` pattern rotation. It is useful if you change the face and the face is not at the same line. For example if you want to create Tenon at the other side of the table supporter.
* **X axis:** Offset for the `X` coordinate axis.
* **Y axis:** Offset for the `Y` coordinate axis.
* **Z axis:** Offset for the `Z` coordinate axis.
* **Step:** Is the step for the `XYZ` offset. The step is automatically get during `- +` changes.
* **set custom values** This button should be clicked if you write manually values for `X`, `Y` or `Z` axis offset.
* **set manually** Allows to set `Sketch` pattern into transform mode and move the `Sketch` pattern manually by hand. You can create Mortise and Tenon in this mode.
* **finish manually** Close transform mode.
* **create Mortise** Create `PartDesign :: Pocket` object below the current `Sketch` pattern position at the selected face. However, in practise you can create only Tenons and use boolean [magicCut](#magiccut) to create Mortises.
* **create Tenon** Create `PartDesign :: Pad` above the current `Sketch` pattern position at the selected face.
* **create Tenon and Mortise** If you have selected 3rd selection, face for Mortise, you can create Tenon and Mortise with single click.

**Video tutorials:** 
* [Playlist for Joinery](https://www.youtube.com/playlist?list=PLSKOS_LK45BBG8kJ2AZvQKBfOSfzhTrLt)

### magicCut

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicCut.png"> This tool make multi boolean cut operation at selected objects. First object should be the base object to cut. All other selected objects will cut the base 1st selected object. To select more objects hold left CTRL key during selection. During this process only the copies will be used to cut, so the original objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. If you are looking for parametric Boolean Cut operation you may consider [magicCutLinks](#magiccutlinks) instead.

**Video tutorials:** 
* [Skip copies in cut-list](https://www.youtube.com/watch?v=rFEDLaD8lxM)
* [Boolean cut with containers](https://www.youtube.com/watch?v=OVwazL8MQwI)

<br><br><br>

### magicCutLinks

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicCutLinks.png"> This tool make multi boolean cut operation at selected objects. First object should be the base object to cut. All other selected objects will cut the base 1st selected object. To select more objects hold left CTRL key during selection. During this process only the links will be used to cut, so the original objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. This tool works with the same way as [magicCut](#magiccut) tool but creates LinkGroup container for cut panels, knives, and uses container links for cut operation. Thanks to this approach you can change Cube to Pad or even add new element to the LinkGroup container and the cut will be updated with new content. So, if you are looking for parametric cut, you should rather use this version.

**Video tutorials:** 
* [Boolean cut with links](https://www.youtube.com/watch?v=EE-A6CMgb-4)

<br><br><br>

### magicKnife

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicKnife.png"> This tool is opposite for [magicCut](#magiccut) tool. This tool allows to use single knife to cut many panels. First selected object should be knife, and all other selected objects will be cut with the knife. The knife can be any object. So, you can create your own shape of the knife and cut many panels at once. Also you can cut all legs of the table using floor or top of the table as knife. To select more objects hold left CTRL key during selection. During this process the copies of knife are used, so the original knife objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. If you are looking for parametric Boolean Cut operation you may consider [magicKnifeLinks](#magicknifelinks) instead.

**Video tutorials:** 
* [Skip copies in cut-list](https://www.youtube.com/watch?v=rFEDLaD8lxM)
* [Boolean cut with containers](https://www.youtube.com/watch?v=OVwazL8MQwI)

### magicKnifeLinks

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicKnifeLinks.png"> This tool allows to use single knife to cut many panels. First selected object should be knife, and all other selected objects will be cut with the knife. The knife can be any object. So, you can create your own shape of the knife and cut many panels at once. Also you can cut all legs of the table using floor or top of the table as knife. To select more objects hold left CTRL key during selection. During this process the links of knife are used, so the original knife objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. This tool works with the same way as [magicKnife](#magicknife) tool but creates LinkGroup container for Knife and uses container links for cut operation. Thanks to this approach you can change Knife Cube to Pad or even add new Knife to the LinkGroup container and the cut will be updated with new Knife content. So, if you are looking for parametric cut, you should rather use this version.

**Video tutorials:** 
* [Boolean cut with links](https://www.youtube.com/watch?v=EE-A6CMgb-4)

### jointTenon

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/jointTenon.png"> This tool allows to create quick tenon joint at selected face. You can select multiple faces at single object or multiple faces at multiple objects. The tenon joint offset is 1/4 of the object thickness. The tenon joint is hidden inside the object equally to the visible part. So, you can cut the tenon also at the object and create removable joint similar to the dowels. Tenons have special attribute, so they are not listed at cut-list report. 

**Video tutorials:** 
* [Quick Tenon and Mortise](https://www.youtube.com/watch?v=fHUjW8-37Pk)

<br><br>

### cutTenons

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/cutTenons.png"> This tool allows to create mortises using tenons. This tool cut all tenons automatically for selected panel. You do not have to select and search exact tenons that belongs to the selected panel. If you select panel, this tool search for all tenons that belongs to the selected panel and apply Boolean Cut on the panel. You can select multiply panels at once to cut tenons. To select more panels hold left CTRL key during selection. During this process only the copies will be used to cut, so the original tenon will not be moved at the objects Tree. This feature is sensitive for visibility of tenons. So, you can hide tenons you do not want to be cut out from the panel. 

**Video tutorials:** 
* [Quick Tenon and Mortise](https://www.youtube.com/watch?v=fHUjW8-37Pk)

<br><br>

### jointCustom

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/jointCustom.png"> Select face to create Custom joint. The simple Pad will be created in the corner of the selected face (0 vertex), allowing you to move the joint precisely to any place at the face. It has predefined size but you can resize and move the joint to fit to your elements and needs. Also you can edit the Sketch to create your custom joint shape. To make more copies you can use [magicFixture](#magicfixture). If you set all joints at the element, you can quickly cut all Mortises for the joints with [magicCut](#magiccut).

<br><br><br>

### panel2frame

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2frame.png"> This tool allows to replace `Cube` panel with frame 45 cut at both sides. You can replace more than one `Cube` panel at once. To replace Cube objects with frames you have to select exact face at each `Cube` object. For example if you want to make picture frame, select all 4 inner faces. To select more faces hold `left CTRL key` during selection. The new created frame will get the same dimensions, placement and rotation as the selected `Cube` panel but will be cut at the selected face. If you have all construction created with simple `Cube` objects that imitating picture frame or window, you can replace all of them with realistic looking frame with single click. 

**Video tutorials:** 
* [Quick 45 cut joint](https://www.youtube.com/watch?v=aFe9p4At41c)

<br><br><br>

### grainH

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/grainH.png"> This tool creates horizontal grain direction description at selected face. You can select multiple faces and multiple objects. Hold left CTRL key during selection. The Grain attribute will be added to the object. After adding grain direction description the object can be moved and the grain description will be moved together with the object.

**Video tutorials:** 
* [Grain Direction Marker](https://www.youtube.com/watch?v=PXXKBrtAtzQ)
* [Grain Direction Report](https://www.youtube.com/watch?v=4W6Lnkh3DRs)

<br><br><br>

### grainV

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/grainV.png"> This tool creates horizontal grain direction description at selected face. You can select multiple faces and multiple objects. Hold left CTRL key during selection. The Grain attribute will be added to the object. After adding grain direction description the object can be moved and the grain description will be moved together with the object.

**Video tutorials:** 
* [Grain Direction Marker](https://www.youtube.com/watch?v=PXXKBrtAtzQ)
* [Grain Direction Report](https://www.youtube.com/watch?v=4W6Lnkh3DRs)

<br><br><br>

### grainX

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/grainX.png"> This tool creates horizontal grain direction description at selected face. You can select multiple faces and multiple objects. Hold left CTRL key during selection. The Grain attribute will be added to the object. After adding grain direction description the object can be moved and the grain description will be moved together with the object.

**Video tutorials:** 
* [Grain Direction Marker](https://www.youtube.com/watch?v=PXXKBrtAtzQ)
* [Grain Direction Report](https://www.youtube.com/watch?v=4W6Lnkh3DRs)

<br><br><br>

### magicCorner

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicCorner.png"> This tool allows to create corner connection via Part :: Embed object FreeCAD feature. To fit corners, first select base object that will be cut, next panels that should be fited to the base object. To select multiple panels hold left CTRL key during selection.

**Video tutorials:** 
* [Corner connection](https://www.youtube.com/watch?v=lIZFvDqgWdQ)

<br><br><br>

## Preview

### fitModel

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/fitModel.png"> This tool allows to fit model to the 3D screen view and also rotate the model view to the base `XY` position (0 key press). This is very useful, used all the time, during furniture designing process. If you rotate the furniture, you can loose the correct orientation of the furniture. So, it strongly recommended to click this tool very often.

<br><br><br>

### makeTransparent

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/makeTransparent.png"> This tool allows to make all parts transparent and back to normal. You can preview all pilot holes, countersinks or any other joints like that, very simply.

<br><br><br><br><br>

### showVertex

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showVertex.png"> This tool allows you to resize all vertices for selected objects or for all objects if there is no selected objects. Resized vertices are easier to select. This tool also change vertices color to red for better visibility. If the object have already resized or red vertices it will be changed back to normal. So, you can keep the model good looking with small vertices and if you have problem with vertices selection, you can quickly resize vertices for selection purposes only and back to normal later.

**Video tutorials:** 
* [Helping Vertex selection](https://www.youtube.com/watch?v=qSsua04AKg8)

<br><br><br>

### selectVertex

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/selectVertex.png"> This tool helps vertex selection. If you click this tool icon the tool activates observer and listen for your selection. If you select Face or Edge the nearest Vertex will be selected instead. If you select Vertex the Vertex will stay selected. The observer is closed after selection so this help works only once to not disturb face or edge selection later. If you want select more vertices with help of this tool, you have to hold left CTRL key during Edge or Face selection, you can also hold it during icon click. 

**Video tutorials:** 
* [Helping Vertex selection](https://www.youtube.com/watch?v=qSsua04AKg8)

<br><br><br>

### roundCurve

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/roundCurve.png"> This tool allows to improve curve visibility. It makes the curve to look more rounded. Normally, circle Sketch is rendering from straight line segments. If you want to align panel to the curve manually this might be problem to hit exactly the point you want at curve. This tool may help for more precised alignment. If you select the curve and click this tool again the curve will back to default settings. To select more object hold left CTRL key during selection. 

**Video tutorials:** 
* [Align to curve](https://www.youtube.com/watch?v=fbJV_SEuNLg)

<br><br><br>

## Router

### Router bit - Cove

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerCove4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerCove2.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerCove.png"> **Note:** This tool allows to create decoration router bits effect. You can select many edges or faces. The selected edges or faces do not have to be at the same object. You can select edges or faces at any object. But each edge or face need to be according to the XYZ coordinate axis to get correct plane of the edge or face. For face the routing path is the CenterOfMass of the face and also along the longest edge. Hold left CTRL key during edges or faces selection. The router bits get size from object thickness. If the router bit is for example Cove2, it means the size of the Cove will be 1/2 of the object thickness.

**Video tutorials:** 
* [Router Cove](https://www.youtube.com/watch?v=MQYaZ4NEiBI)
* [Decoration testing with router bits](https://www.youtube.com/watch?v=K229hhMt8Vc)

### Router bit - Round Over

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerRoundOver4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerRoundOver2.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerRoundOver.png"> **Note:** This tool allows to create decoration router bits effect. You can select many edges or faces. The selected edges or faces do not have to be at the same object. You can select edges or faces at any object. But each edge or face need to be according to the XYZ coordinate axis to get correct plane of the edge or face. For face the routing path is the CenterOfMass of the face and also along the longest edge. Hold left CTRL key during edges or faces selection. The router bits get size from object thickness. If the router bit is for example Cove2, it means the size of the Cove will be 1/2 of the object thickness.

**Video tutorials:** 
* [Router Round Over](https://www.youtube.com/watch?v=RErYZpqbqAY)
* [Decoration testing with router bits](https://www.youtube.com/watch?v=K229hhMt8Vc)

### Router bit - Straight

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerStraight4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerStraight3.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerStraight2.png"> **Note:** This tool allows to create decoration router bits effect. You can select many edges or faces. The selected edges or faces do not have to be at the same object. You can select edges or faces at any object. But each edge or face need to be according to the XYZ coordinate axis to get correct plane of the edge or face. For face the routing path is the CenterOfMass of the face and also along the longest edge. Hold left CTRL key during edges or faces selection. The router bits get size from object thickness. If the router bit is for example Cove2, it means the size of the Cove will be 1/2 of the object thickness.

**Video tutorials:** 
* [Router Straight](https://www.youtube.com/watch?v=NDBLmh2SwwI)
* [Decoration testing with router bits](https://www.youtube.com/watch?v=K229hhMt8Vc)

### Router bit - Chamfer

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerChamfer4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerChamfer2.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerChamfer.png"> **Note:** This tool allows to create decoration router bits effect. You can select many edges or faces. The selected edges or faces do not have to be at the same object. You can select edges or faces at any object. But each edge or face need to be according to the XYZ coordinate axis to get correct plane of the edge or face. For face the routing path is the CenterOfMass of the face and also along the longest edge. Hold left CTRL key during edges or faces selection. The router bits get size from object thickness. If the router bit is for example Cove2, it means the size of the Cove will be 1/2 of the object thickness.

**Video tutorials:** 
* [Router Chamfer](https://www.youtube.com/watch?v=Z45TDosmb-U)
* [Decoration testing with router bits](https://www.youtube.com/watch?v=K229hhMt8Vc)

### multiPocket

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/multiPocket4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/multiPocket2.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/multiPocket.png"> **Note:** This tool allows to create custom decoration from Sketches. You can select many Sketches at once. The selected Sketches will make Pockets at the first selected object. The Sketches need to be correctly aligned at the object. Hold left CTRL key during Sketches selection. For 2 and 4 variant this tool gets first selected object size and create Pocket with 1/2 thickness or 1/4 thickness.

**Video tutorials:** 
* [multiPocket custom decoration](https://www.youtube.com/watch?v=FHups7Zvl5E)
* [Future of parametric modeling](https://www.youtube.com/watch?v=0M9EW0I9iwg)

<br><br><br>

## Decoration

### colorManager

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/colorManager.png"> This tool allows to set face colors for all objects from spreadsheet. Also you can browse colors for manually selected faces or objects and see the effect at 3D model in real-time.

<br><br><br><br>

### setTextures

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/setTextures.png"> This is FreeCAD macro for woodworking to apply and store textures.

Main features:

* Store texture URL or local HDD path, repeat factor, rotation and fit mode in object's property.
* Download and show textures from stored URL or local HDD path.
* Set and refresh texture for all objects or selected object only.
* Auto fit mode to object shape type.
* Small GUI interface in corner to see 3D model refresh.

Tool repository: [github.com/dprojects/setTextures](https://github.com/dprojects/setTextures)

## Dimensions

### getDimensions

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/getDimensions.png"> This tool allows to create spreadsheet with dimensions to cut, cut-list, BOM.

Main features:

* Languages: Polish, English.
* Units: millimeters, meters, inches.
* Report types:
    * quick, quantity first (q - report type),
    * names, objects listing (n - report type),
    * group, grandparent or parent folder name first (g - report type),
    * edgeband, extended edge (e - report type),
    * detailed, edgeband, drill holes, countersinks (d - report type),
    * constraints names, totally custom report (c - report type),
    * pads, all constraints (p - report type),
    * approximation of needed material (a - report type), it can be imported at [cutlistoptimizer.com](https://www.cutlistoptimizer.com/).
* Additional reports:
    * custom measurements,
    * dowels and screws,
    * construction profiles,
* Other:
    * wood properties - grain direction, type of wood, color of wood,
    * edgeband (quick way, described, detailed by selection),

Tool repository: [github.com/dprojects/getDimensions](https://github.com/dprojects/getDimensions)
  
**Video tutorials:** 
* [Cut-list, BOM](https://www.youtube.com/watch?v=lYssiliONVo)
* [Custom measurements & BOM](https://www.youtube.com/watch?v=-Mmwvw_Bue4)
* [Preview furniture & cut-list](https://www.youtube.com/watch?v=xEMQUH665Vw)

### sheet2export

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sheet2export.png"> This tool allows to export cut-list, BOM to more flexible file formats. Useful if you want to print multi-page report. 

Main features:

* Supported file types:
    * .csv - Comma-separated values,
    * .html - HyperText Markup Language,
    * .json - JavaScript Object Notation,
    * .md - MarkDown.

* Additional features:
    * export selected spreadsheet or all spreadsheets,
    * custom CSV separator,
    * custom empty cell content,
    * custom CSS decoration for each cell.

Tool repository: [github.com/dprojects/sheet2export](https://github.com/dprojects/sheet2export)

### showSpaceModel

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showSpaceModel.png"> This tool allows to calculate occupied space in 3D by the model. This approach might be very useful at furniture designing process. For example you can see how much space in your room will take opened front of the furniture. Normally, all the `Pad` or `Cube` elements, should be created according to the `XYZ` plane, so there will be no difference between the real dimensions and occupied space in 3D. 

<br><br><br>

### showSpaceSelected

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showSpaceSelected.png"> This tool allows to calculate occupied space in 3D by selected elements. This approach might be very useful at furniture designing process. For example you can see how much space take selected parts of the furniture. Normally, all the `Pad` or `Cube` elements, should be created according to the `XYZ` plane, so there will be no difference between the real dimensions and occupied space in 3D.

<br><br><br>

### magicMeasure

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicMeasure.png"> 
This tool allows you to quickly measure objects. All measurements are recognized by the getDimensions tool and can be listed in the cut-list report with a reference to the object. This tool works in two modes:

* **Preselection mode** - this mode allows you to quickly measure objects by just moving the mouse cursor over the object. In this mode you can measure: edge, surface (all edges), hole diameter and hole depth. If you left-click, the current visible measurements will be saved.
    
* **Selection mode** - this mode allows you to measure objects by selecting vertices, surfaces or holes. In this mode you have the following choices:
  * select `Edge`: to measure edge size, 
  * select `Vertex` and next `Face`: to measure distance between vertex and face, for example shelf space,
  * select `Vertex` and next `Edge`: to measure distance between vertex and edge, for example space between front and side of the furniture, 
  * select `Vertex` and next `Hole`: to measure distance between vertex and hole center point, for example drill point, 
  * select `Vertex` and next `Vertex`: to measure distance between two vertices, for any purposes, 
  * select `Hole` and next `Hole`: to measure distance between holes center points, for example to verify 32 mm system, 
  * select `Hole` and next `Edge`: to measure distance between hole and edge, for example to verify pilot hole offset,
  * select `Hole` and next `Face`: to measure distance between hole and face, for example to measure angle mounting point, 
  * select `Hole` and next `Vertex`: to measure distance between hole and vertex.

**Note:** This tool automatically recognizes the FreeCAD `Edit->Preferences->Display->Colors->Enable preselection highlighting` settings and if you set this option, it will start in `Preselection` mode, otherwise in `Selection` mode, so you don't have to switch it at the beginning.

* **Measurement observer:**
  * `START` button allows you to start the measurement process,
  * `PAUSE` button allows you to stop the measurement process, without leaving this tool's graphical interface, for example if you want to select or create objects.

* **Preselection mode:**
  * `ON` button allows you to start preselection mode and also exit selection mode,
  * `OFF` button allows you to start selection mode and also exit preselection mode.
  
* **Vertices size:**
  * `-5` button allows you to make smaller all vertices of all objects by `-5` points, 
  * `+5` button allows you to make bigger all vertices of all objects by `+5` points.

**Note:** You can also use [showVertex](#showvertex), but here you can adjust the vertices more precisely and it works for all vertices, so you don't have to unselect the object or select a specific object. 

**Text field** the text box shows the current measurements, so you can easily copy these dimensions for later use.

**Video tutorials:** 
* [How to use magicMeasure](https://www.youtube.com/watch?v=_yGLzNmeK0Q)

## Parameterization

### magicGlue

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicGlue.png"> This tool allows you to add or remove expressions to keep objects position and size.

**Options:**

* **Glue position:** This option allows you to glue position of target objects to the source object position.
  * `set` **for source** allows you to add source object postition. The source can be vertex or face. For vertex the `XYZ` placement will be get as reference point. For face the `CenterOfMass` will be the reference point, so you need to be careful with linking to this face source because the `CenterOfMass` move `1/2` of the object move way. However it can be used to glue object to the center, for example center furniture side.
  * `set` **for target** allows you to add target objects to set expressions. If the object is Cube `Part::Box` the expression will be set at `Placement` of the `Cube`. If the object is Pad `PartDesign::Pad` the expression will be set at `Placement` of its `Body`.
  * `refresh all selection` allows you to add quickly source and targets. First selected vertex or face will be the source and all other objects will be considered as targets to set expressions. Also this is default init option, for example if you select vertex and 2 objects and open the tool this will be ready to set glue position.
  * `add glue` for `X` direction allows you to add expression for moving objects along `X` axis.
  * `add glue` for `Y` direction allows you to add expression for moving objects along `Y` axis.
  * `add glue` for `Z` direction allows you to add expression for moving objects along `Z` axis.

* **Glue size:** 
  * `set` **for source** allows you to add source object postition. The source can be edge. The selected `edge.Length` will be the reference point.
  * `set` **for target** allows you to add target objects to set expressions. The selected objects should be edges. 
    * If the object is Cube `Part::Box` the expression will be set to `Length` or `Width` or `Height` of the `Cube` according to the selected edge plane. 
    * If the object is Pad `PartDesign::Pad` the expression will be set at `Length` property or `Sketch` constraints.
    * If the object is for example Profile `PartDesign::Thickness` the expression will be set at `Value` property or `Sketch` constraints.
    * If the object is for example cornerBlock `PartDesign::Chamfer` the expression will be set at `Size` property or `Sketch` constraints.
  * `refresh all selection` allows you to add quickly source and targets. First selected edge will be the source and all other edges will be considered as targets to set expressions.
  * `add glue size` allows you to add expression for size changes of source edge.
  
* **Clean glue:** 
  * `refresh all selection` allows you to add target objects to clean expressions.
  * `clean glue position` clean all position expressions. Make sure you do not have your private expressions.
  * `clean glue size` clean all size expressions. Make sure you do not have your private expressions.

* **Cross:**
  * `Corner cross:` buttons `-`, `+` resize the cross in the right bottom of the screen, it has auto-repeat.
  * `Center cross:` buttons `on`, `off` turn on and off the center cross at the screen.
  * `keep custom cross settings` allows to store the custom cross setting after this tool exit.

**Video tutorials:** 
* [How to make parametric furniture quickly](https://www.youtube.com/watch?v=z2rpVoLgqWI)

### sketch2clone

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sketch2clone.png"> This tool allows to replace selected Sketches with Clones and thanks to it, convert static model to parametric. First selected Sketch will be changed into `Parametric Pattern` for all other selected Sketches. After this operation, if you change the `Parametric Pattern` all other Sketches will be automatically updated with new pattern. For example if you have Pad, it will change the shape. Make sure the center of coordinate axes XYZ for each selected Sketch is in the middle of the pattern, this will allow for correct positioning of the Sketches. To select more objects hold left CTRL key during selection. For more complicated objects use [panel2link](#panel2link) or [panel2clone](#panel2clone) at the whole `Part`. 

**Video tutorials:** 
* [Playlist for parametrization](https://www.youtube.com/playlist?list=PLSKOS_LK45BCzvg_B7oSTk1IsQnu5thtZ)

### showAlias

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showAlias.png"> To see all objects with alias: 1. First select spreadsheet at objects Tree. 2. Click this tool icon to activate the preview mode. 3. Click any spreadsheet cell with alias. **Note:** This tool needs to be activated to work. To activate this tool you have to select spreadsheet at objects Tree and click this tool icon. If this tool will be activated you can select any cell with alias to see all objects selected. The selected objects at 3D model will be those that uses the selected alias. Also the objects will be selected at objects Tree. To finish the preview mode, click the tool icon without any selection.

**Video tutorials:** 
* [Preview alias](https://www.youtube.com/watch?v=tS9pvkPH5RI)

## Advanced

### panel2pad

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2pad.png"> This tool allows to replace `Cube` panel with `Pad` panel. The new created `Pad` panel will get the same dimensions, placement and rotation as the selected `Cube` panel. You can transform many `Cube` panels into `Pad` at once. To select more `Cubes` hold `left CTRL key` during selection. This tool is mostly dedicated to add decoration that is not supported for `Cube` objects by FreeCAD PartDesign workbench. You can also change shape by changing the `Sketch`. This is mostly used for decoration that can be applied only to `Pad`, like `Fillet`.

<br><br><br>

**Video tutorials:** 
* [Automatic parametrization](https://www.youtube.com/watch?v=JuZsAjrQr6M)

<br><br><br>

## Code and Debug

### scanObjects

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/scanObjects.png"> This is inspection tool for FreeCAD, macro or workbench tools development, live API. It allows for live preview of FreeCAD projects, code debugging, browsing FreeCAD modules, custom libraries or even command results. 

Main features:

* View object properties hidden in XML file (e.g.: Shape, Faces, Edges).
* Object type auto-recognition.
* Auto-resize to active screen size.
* Move, resize, close, any window.
* Quick browse predefined modules.
* Allow to browse custom module, library or even macro.
* Allow to browse custom command result (need to be array).
* Quick windows positioning (layouts).
* Funny color schemas.
* Quick browse via cursors.
* Selection search filter for quick parse long lists.
* Allow to quick copy window content.

Tool repository: [github.com/dprojects/scanObjects](https://github.com/dprojects/scanObjects)

**Video tutorials:** 
* [Debugger, Live API](https://www.youtube.com/watch?v=nFK_o95y6xk)
* [Debugger, Search filter](https://www.youtube.com/watch?v=5h_feMn_lsQ)

### debugInfo

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/debugInfo.png"> This tool allows to get platform information used for FreeCAD bug report.

Main features:

* This tool compares date of your Woodworking workbench with the latest date for you version branch, from github repository. If the date of your Woodworking workbench match the latest master branch date you have information "up-to-date". Otherwise you have link to download the latest version from github master branch. 
* Additionally, `update button` will be visible allowing you to update your workbench with single button click. The latest update for Woodworking workbench will be downloaded and unpacked. After this the FreeCAD will restart with new Woodworking workbench version. The old Woodworking workbench version will remain untouched but only disabled to protect your personal files, if there are such any.
* This tool also run some test cases, mostly import modules used by Woodworking workbench, to find out if the FreeCAD version is safe to use.
* Additionally, this tool will verify if your Woodworking workbench is certified.
* There is also funny worm icon describing current verification status: 
  * The worms are unhappy, if everything works.
  * The worms are happy, if everything is broken.
  * If not everything is broken, the worm will be partially happy, I mean happy and sad at the same time, good joke? ;-)

## Project manage

### selected2LinkGroup

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/selected2LinkGroup.png"> This tool call FreeCAD LinkGroup command and set color for new LinkGroup objects from first selected object. To select more objects hold left CTRL key during selection.

<br><br><br><br><br><br>

### selected2Link

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/selected2Link.png"> This tool call FreeCAD simple Link command and set color for new Link objects from first selected object. To select more objects hold left CTRL key during selection.

<br><br><br><br><br><br>

### selected2Group

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/selected2Group.png"> Normally, the FreeCAD Group command not recognize selection and always creates empty folder. This tool improves this command a little bit, creates new Group and move all selected objects to the new Group folder. The Group folder label is from first selected element. To select more objects hold left CTRL key during selection at Tree or 3D view.

<br><br><br><br><br><br>

### selected2Outside

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/selected2Outside.png"> This tool allows you to get out the selected objects from containers. Normally, if you get out object from the container manually, the object will change place and rotation. This tool allows you to move the objects and keep the same position and rotation. This feature might be very useful if automatic movement to container is not what you want. For example you want single element to no longer be mirrored or further processed with other objects inside the container. To select more objects hold left CTRL key during selection.

* [Boolean cut with containers](https://www.youtube.com/watch?v=OVwazL8MQwI)

<br><br><br>

# How to use containers

* `Body` is container for single Pad object. If you want to move Pad or any other PartDesign object, it is better to move it via Body container not directly via AttachmentOffset. If you move PartDesign object via AttachmentOffset, all the transformations, for example Hole, need to be recalculated. So, this is very slow and also if you drill holes and move object via AttachmentOffset the holes will disappear. So, move PartDesign objects via Body container.
* `Part` is good container for many Bodies, more complicated PartDesign objects. For example if you move Pad directly to Body this will be merged with the current Pad in the Body. So, it will be single object. If you want to keep Pad separated, you can create single Body container for each Pad and keep all Bodies in Part. I rather not recommend to mix Cube with PartDesign object inside Part container. Part should rather be used only for PartDesign objects.
* `LinkGroup` is high level, real container. You can move there many Part containers and also Cube objects. Also you can nesting LinkGroup containers. If you want to move many objects, bigger structures, rotate them, this is good container to do it.
* `Link` is not container but it is mentioned here, because you should rather avoid linking objects directly. You should rather link LinkGroup. This approach allows you to change LinkGroup content and update the Link in real-time. If you link directly object, and the base Cube object will be replaced with Pad, the link will be broken, because the base object no longer exists. This not happen if you link the LinkGroup with Cube inside. You can replace Cube with Pad inside LinkGroup container and the link will be still correct and also the link will be updated in real-time.
* `Group` is normal FreeCAD folder. You can't move it or rotate but it is good container to keep LinkGroup structure. 

**Note:** If you want to use `Part :: Boolean :: Cut` inside `LinkGroup` container, first you have to get out of the container all the elements using [selected2Outside](#selected2outside). See video: [Boolean cut with containers](https://www.youtube.com/watch?v=OVwazL8MQwI)

# Dowels, Screws, Fixture

* Use [magicDowels](#magicdowels) for dowels, screws and other mounting points references.
* Use [magicFixture](#magicfixture) for any other type of fixture (angles, hinges, anything). For drilling templates use `Clone`.
* Examples repository: [Fixture](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture) - you can use this repository, make your own detailed part, or order exact detailed part somewhere and merge with your project and apply with the same rules.

However, if you make your own detailed part or order somewhere, you need to fulfill certain requirements:

* The detailed element should start from `(0, 0, 0)` vector. The bottom of this element and orientation should match the `XYZ` axes as described below. If you want to adjust the detailed element which has been made by someone else, you should rather move it via container (e.g. `Body`). Avoid rotation at the base element.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/fixture001.png)

* If you set reference mounting points with [magicDowels](#magicdowels) that will be replaced later with realistic looking screws. Make sure the green faces refers to the top head of the screw. If not the replaced element will be rotated.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/fixture002.png)

* This furniture from my garage has applied realistic looking screws and dowels. All the screws has been applied with single click via [panel2link](#panel2link) woodworking workbench feature. Also it has angles replaced with [magicFixture](#magicfixture) tool.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/fixture003.png)

**Video tutorials:** 

* [Adding dowels](https://www.youtube.com/watch?v=q7tJffBBUGY)
* [Angles, Pilot holes, Screws](https://www.youtube.com/watch?v=CYaL-sGvIK8)

# Holes, Countersinks, Counterbores

## Drilling serially

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDriller.png"> To drill holes with countersinks you have to drill through two panels. First select the surface for countersinks and click `refresh selection`, reference for the face should be updated and visible at the tool info screen:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller001.png)

* Next choose `Contersinks` and exact screw type. Also adjust the edge, rotation and sink, if needed:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller002.png)

* If the drill bits are in correct place, click the drill button, this may takes some time, for example if you drill 30 holes for shelf pins at once and you have slow laptop as I have: 
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller003.png)
  
* To drill rest of the hole, hide the first element with countersinks and select edge:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller004.png)

  <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCountersinks.png"> **Note:** To drill rest of the hole, you can also use [Drilling via icons](#drilling-via-icons) feature. Just select edge, next all the countersinks drill bits and click the icon. All the holes will be drilled. But do not exit the tool because the countersinks drill bits will be automatically removed. You can do it if the holes will be drilled. But also you can continue with this tool and drill the rest of holes with this tool directly.

* Now click `refresh selection`, reference for the face should be updated and visible at the tool info screen. Also the drill bits will be moved to the new face, but do not worry, for this tool it is ok, just select `Holes` for hole type and exact screw. For `Hole` type, the depth is adjusted with panel thickness. However, if you have different panel sizes you can adjust it, as well: 
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller005.png)
  
* Now click to drill and the rest of the holes will be drilled at the edge:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller006.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller007.png)

**Video tutorials:** 
* [Countersinks & realistic screws](https://www.youtube.com/watch?v=N5SpUCtNMY0)

## Drilling via icons

<img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillHoles.png"> <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCountersinks.png"> <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCounterbores.png"> Select face you want to drill and click any hole icons. The drill bit for the hole type will be created in the 0 vertex of the face, allowing you to move the drill bit to any place at the face. You can change the drill bit size if you want, manually or with [Resize panels](#resize-panels) icons. Also you can create your own drill bits. But there is rule, for simple holes this need to be `Cylinder` object, but for Countersinks and Counterbores this need to be `Cone` object. This is because at `Cone` you can easily store radius for countersink and other for hole. Also the drill bit need to be exactly rotated, exact face of drill bit need to touch the face for drilling.

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
  
## Drilling via magicCNC

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

**Video tutorials:** 

* [Drilling holes](https://www.youtube.com/watch?v=SS-fnr_ud2I)
* [Drilling counterbores](https://www.youtube.com/watch?v=xpEWPRFq-7A)

## Pilot holes for angles, hinges

* To create pilot holes for angle, first set the angle into position with [magicFixture](#magicfixture). Remember to set `Clone` option, because if you make a `Link` the drill bits will be created at the base element, and you will not be albe to drill holes.
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillAngles001.png)

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/edge2drillbit.png"> Next select each hole edge inside the fillets and click [edge2drillbit](#edge2drillbit). If the angle do not have fillet it is fine, you can select the hole edge as well. The drill bits will be created above each hole and the drill bits diameter will be a little smaller than the hole. It is OK for pilot hole. Pilot hole should be usually smaller 1 mm than the screw. If you want you can also resize the drill bits. 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillAngles002.png)

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillHoles.png"> Now you can select face of the element to drill and than all the drill bits for the element. If you have this selected you have to click the [drillHoles](#drillholes) icon. All the holes will be created. If the element was Cube it will be automatically changed into Pad, and than all holes will be drilled.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillAngles003.png)
  
* Do the same for second element and you should have all pilot holes drilled precisely and quickly aligned.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillAngles004.png)

**Note:** The same procedure you can use to drill pilot holes for hinges or any other fixture.

**Video tutorials:** 
* [Angles, Pilot holes, Screws](https://www.youtube.com/watch?v=CYaL-sGvIK8)

# Pocket holes - invisible connections

Personally I do not use this type of connections because I am not convinced to it, and also I do not have such jig. But I know that many woodworkers use pocket invisible connections and they love it. They use it especially for real wood and than put dowels inside the holes so the screws are not visible at all. 

## Drill pocket holes - manually

**Note:** This is deprecated.

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDowels.png"> First apply dowels to the surface you want to drill. This is a little trick because I use dowels not tool for holes. Any `Cylinder`, dowel can be drill bit for hole, but [magicDowels](#magicdowels) allows to apply the dowls for further processing. If you use [magicDriller](#magicdriller) you need to keep the tool open or the drill bits will be removed. For the dowels, you have to adjust offset from the edge, size of the dowel and also dowels per side. You can do it at custom settings:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles001.png)

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicAngle.png"> Now use [magicAngle](#magicangle) at each dowel. I set angle 75 degree. As you see the dowels will be below the panel. Make sure you use exact axis for rotation. I use `Y` axis:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles002.png)

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicMove.png"> Now use [magicMove](#magicmove) at each dowel to move all the dowels above the panel. The dowels should touch a little bit the surface to get desired result. If the dowel will be below the surface the hole will be drilled inside the panel and the edge will not be visible at the surface correctly. I set move step to 85 at `Z` axis:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles003.png)

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillHoles.png"> Now select the panel surface you want to drill and all the dowels. If you have it selected click [drillHoles](#drillholes) and all the holes should be created with exact 15 degree angle. 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles004.png)
  
* This is not exactly what should be, because the drill bit for pocket holes in real-life has a little smaller tip at the end. So there should be also smaller hole at the end. But for this manually way it looks not so bad, in my opinion:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles005.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles006.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles007.png)


## Drill pocket holes - with magicDriller

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDriller.png"> To drill pocket holes you can use [magicDriller](#magicdriller). First select exact face you want to drill and run [magicDriller](#magicdriller). Also you can run [magicDriller](#magicdriller) and then select exact face and click `refresh selection`. For hole type choose `Pocket holes` and select predefined screw. You can also change the settings for your custom screw. If you want more rounded hole finish play with increase `Pocket sink` option. To tilt the drill bit to the other side just change the sign at `Pocket rotation`. The angle is `75` by default because pocket holes are drilled with `15` degree angle, so `90 - 75 = 15`. However, you can play with the `Pocket rotation` option as well.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles008.png)

* Now click button for drilling and you have it:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles009.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles010.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles011.png)

**Video tutorials:** 
* [Pocket holes & realistic screws](https://www.youtube.com/watch?v=eXzYXNbWwqM)

# Realistic parts

## Realistic screws and pilot holes

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCountersinks.png"> If you want to drill pilot holes and apply realistic screws to the holes first you have to drill holes using procedure described at: [Drilling serially](#drilling-serially). For quick way I use the drilling countersinks icon to drill the rest of the holes at the edge of second element.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews001.png)

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDowels.png"> If you have drilled holes with countersinks, apply dowels with [magicDowels](#magicdowels) tool. But remember to apply the dowels to the edge not to the surface. This is because the predefined settings for the screws, I mean sink, are adjusted for the edge not to the surface. However, it also can be done manually with custom settings. If you apply to the surface you need to set exact sink.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews002.png)

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> Now merge realistic screw with your current active document. You can create such screw with PartDesign or even order such realistic part. For this case I use [Screw 45 x 40 mm](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture#screw-45-x-40-mm) from [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture). The dowels applied before is some kind of references points and they can be replaced with realistic screws. To replace the fake screws with realistic screws. Select the realistic screw and next all the fake dowels. Next click [panel2link](#panel2link) icon:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews003.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews004.png)

* As you see the head of the screw is inside the countersink and also the screw is inside the drilled pilot hole.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews005.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews006.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews007.png)
  
* You can also apply textures for the elements to get more realistic preview:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticScrews008.png)

**Video tutorials:** 
* [Pocket holes & realistic screws](https://www.youtube.com/watch?v=eXzYXNbWwqM)

## Realistic screws and angles

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sketch2dowel.png"> First you have to create angles or any other fixture and drill holes according to this procedure: [Pilot holes for angles, hinges](#pilot-holes-for-angles-hinges). If you have it, first select face of the element, and next all `Sketches` of the holes. This allow you to create dowels directly from `Sketches` with exact orientation and size. If you have it selected click [sketch2dowel](#sketch2dowel):

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles001.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles002.png)

* For other element also first select face of the element, and next all `Sketches` of the holes. This allow you to create dowels directly from `Sketches` with exact orientation and size. If you have it selected click [sketch2dowel](#sketch2dowel):
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles003.png)
  
* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> Now merge realistic screw with your current active document. You can create such screw with PartDesign or even order such realistic part. For this case I use [Screw 4 x 16 mm](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture#screw-4-x-16-mm) from [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture). The dowels applied before is some kind of references points and they can be replaced with realistic screws. To replace the fake screws with realistic screws. Select the realistic screw and next all the fake dowels. Next click [panel2link](#panel2link) icon:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles004.png)
  
* As you see the screws are above the holes. To hide them all, select the `Body` container of the base screw, and move it down as much you want, you can use [magicMove](#magicmove) for that with exact step: 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles005.png)

  **Note:** I use a little bigger screws for angles than normally should be, because they hold things a little better than `3 x 20 mm` ones, so the head of the screw is not flat with the surface but you can use any screw size with the same way. For hinges you can use `3 x 20 mm`, without pilot holes.

**Video tutorials:** 
* [Angles, Pilot holes, Screws](https://www.youtube.com/watch?v=CYaL-sGvIK8)

## Realistic screws and pocket holes

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/edge2dowel.png"> First select edge of the hole inside the pocket hole and click [edge2dowel](#edge2dowel). You can select all edges for the panel to create dowels. The dowels should be created with exact angle, so it will be more easy to adjust the screw later. 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews001.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews002.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews003.png)

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> Now merge with you active document exact screw. In my case I use 19 mm thickness panel. According to the [Wolfcraft Guide to Wood Joints](https://www.wolfcraft.com/products/wolfcraft/en/EUR/Products/Wood-Joints/Dowel-Jointers/Undercover-Jig-Set/p/P_4642) I have to merge screw `4 x 30 mm`. If you have merged the screw, replace all the fake dowels with the realistc screw using [panel2link](#panel2link):
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews004.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews005.png)

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicMove.png"> Adjust the screws using [magicMove](#magicmove). Make sure you set `1` at `Move step` to move the screw slower and more precisely. You can also use `Front` view and [makeTransparent](#makeTransparent) tool to see exactly where the screw goes. If you do it right you should get really nice result:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews006.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews007.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews008.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticPocketScrews009.png)

**Video tutorials:** 
* [Pocket holes & realistic screws](https://www.youtube.com/watch?v=eXzYXNbWwqM)

## Counterbore 2x with bolt

Personally, the two side counterbore I use for screwing things to the table. I use double counterbore for example for screwing the `Parkside PNTS 250` grinder to a piece of chipboard. Thanks to it the grinder gains greater stability and mobility, because it can be attached anywhere to the workbench by simple clamps.

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCounterbores2x.png"> <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicCNC.png"> To make simple table for grinder, first you need to make double counterbores. I use [magicCNC](#magiccnc) for better precision. I do not remember the exact spacing of the holes, so I will make a rectangle, for example.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticCounterbore2x001.png)

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sketch2dowel.png"> Now I use the [sketch2dowel](#sketch2dowel) tool to have the fake dowels aligned correctly. First select the top face of the wood and than all second Sketches. First Sketch is always from the side of drill bit. The next Sketch is from the other side according to the wood thickness. 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticCounterbore2x002.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticCounterbore2x003.png)

<img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2clone.png"> Now merge realistic bolt designed for double counterbore with your current active document. You can create such screw with PartDesign or even order such realistic part. For this case I use [Conterbore2x_5_x_60_mm](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture#conterbore2x-5-x-60-mm) from [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture). The dowels applied before is some kind of references points and they can be replaced with realistic bolts. To replace the fake dowels with realistic bolt, select the realistic bolt and next all the fake dowels. Next click [panel2clone](#panel2clone) icon. If you clone the realistic part you can remove later the original part.
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticCounterbore2x004.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticCounterbore2x005.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticCounterbore2x006.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticCounterbore2x007.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticCounterbore2x008.png)

# Raw wood, Lumber

Working with raw wood is difficult, it requires a lot of knowledge about different types of wood and experience. The wood must be properly seasoned, dried, and the proper grain direction must be maintained during gluing or joining. If not the wood will crack later when it starts working. I remember a bread cutting board bought in a shop that broke. It was made of beech wood and I assume it was made by experienced carpenters, but it cracked.

Wood is a natural product, therefore it is also difficult to predict the exact size. For this reason, raw real wood is a product that is not very practical and difficult to process. Currently, it has been replaced by prefabricated panels. Nowadays, nobody makes furniture entirely from raw real wood for everyday use. Even these expensive furniture, as if made of real raw wood, are built on prefabricated boards, MDF, plywood, and only the front parts are made of raw real oak wood. However, raw real wood is making a comeback as a luxurious, expensive and healthy product.

Working with raw wood is an art of some sort. This is the true form of working with wood, so it deserves to be supported by furniture design programs. However, computers have slightly different rules. Here it starts with the dimensions and not the order of operations. However, with the right approach some real wood operations can be simulated.

## Glued table top

* To simulate the creation of a glued table top. First, you can create an irregular shape from panels of different length. You can also use a different thickness, and then simulate a thickness planer woodworking tool. But for the sake of simplicity, I chose panels of the same thickness.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RawWoodGlued001.png)
  
* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/setTextures.png"> Using [setTextures](#settextures) tool you can simulate grain direction. I use [texture samples](https://commons.wikimedia.org/w/index.php?title=Special:ListFiles/Dprojects&ilshowall=1) but you can also create your own textures, looking much better or even mark the grain direction using colors only. 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RawWoodGlued002.png)
  
* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDowels.png"> Using [magicDowels](#magicdowels) tool you can apply dowels. I use standard predefined dowels but you can use any joints you like. Also you may want to drill holes. It depends how precisely you want to simulate this process. 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RawWoodGlued003.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RawWoodGlued004.png)
  
* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicKnife.png"> Using [magicKnife](#magicknife) tool you can simulatee the cuting edges process. The "knife" should be larger to cut off the irregular protruding part of the panels. Make a note that if the panel will be cut, the texture disappear because it is applied at base object that is hidden after cut. But you can bring it back by applying the texture to the cut object.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RawWoodGlued005.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RawWoodGlued006.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RawWoodGlued007.png)
  
* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showSpaceSelected.png"> <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/getDimensions.png"> You can use [showSpaceSelected](#showspaceselected) to see oaccupied space by any selected panel after cut or even by all the parts. Not use [showSpaceModel](#showspacemodel) because it also calculates the hidden elements, "knives". However you can also create report via [getDimensions](#getdimensions) with the base elements used before cut.
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RawWoodGlued008.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RawWoodGlued009.png)

**Video tutorials:** 
* [Glued table top simulation (force order of operations)](https://www.youtube.com/watch?v=SULl3EmCTsk)

