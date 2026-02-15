# Woodworking workbench documentation

<img align="right" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/Woodworking.png"> FreeCAD is a very cool software and allows to design a lot of interesting things. However, FreeCAD is not dedicated to be software only for furniture designing. For this reason, some tasks when designing furniture can be challenging at the beginning. Despite the fact that I finished math, I have a problem with counting in my memory. For me, constantly calculating wood thickness and adding this to the position was a problem without a calculator. In addition, for me constantly starting from the `10 x 10 x 10` box `Cube` and setting it in the right position is a bit annoying. 

Woodworking workbench has been created because of my woodworking and coding hobby. Everything started from [getDimensions](https://github.com/dprojects/getDimensions/commits/master) project long time ago. I wanted to have [simple cut-list for chipboards order](https://github.com/dprojects/getDimensions/commit/a6f0a2221e90f717be95bd0dc1cc9f1ede95a329) and I found FreeCAD with low hardware requirements and possibility to implement the cut-list. 

In 2014, FreeCAD [did not have any tools to help create even simple cabinets](https://forum.freecad.org/viewtopic.php?t=8247). The work around Woodworking workbench [did not seem advanced even in 2022](https://forum.freecad.org/viewtopic.php?p=572287#p572287), so [I decided](https://forum.freecad.org/viewtopic.php?p=573458#p573458) to create my own workbench for creating simple cabinets. First, [I added my own macros](https://github.com/dprojects/Woodworking/commit/412bb997e338fa66e2dc1c38f68b175ffdfa37a8) that I had written earlier. Then I started creating new features useful for creating simple cabinets.

I added many tools, and now Woodworking workbench has so many features and simplifications that it can be considered as a new CAD program based only on the FreeCAD kernel. It is mainly intended to make cabinet creation more simple, although it has many solutions to speed up and make more simple typical carpentry work and other CAD projects. I hope you will find something for yourself here.

* [Installation](#installation)
	* [Step 0. Install supported kernel](#step-0-install-supported-kernel)
	* [Step 1. Download Woodworking workbench](#step-1-download-woodworking-workbench)
	* [Step 2. Get FreeCAD Mod folder localization](#step-2-get-freecad-mod-folder-localization)
	* [Step 3. Install Woodworking workbench](#step-3-install-woodworking-workbench)
* [Extras](#extras)
* [Translations](#translations)
* [Objects, Workflow, Golden rules](#objects-workflow-golden-rules)
* [How to start](#how-to-start)
	* [magicStart](#magicstart)
		* [Construction geometry](#construction-geometry)
		* [Cabinet structure](#cabinet-structure)
		* [US style](#us-style)
		* [Drawers for cabinets](#drawers-for-cabinets)
		* [Fronts for cabinets](#fronts-for-cabinets)
		* [Shelves and top for cabinets](#shelves-and-top-for-cabinets)
		* [Sides for cabinets](#sides-for-cabinets)
		* [Back](#back)
		* [Foot for cabinets](#foot-for-cabinets)
		* [Table](#table)
		* [Connections](#connections)
		* [Accessories](#accessories)
		* [Other](#other)
	* [Default panels](#default-panels)
* [Move and copy](#move-and-copy)
	* [magicMove](#magicmove)
	* [Arrows](#arrows)
	* [magicAngle](#magicangle)
* [Resize panels](#resize-panels)
	* [magicResizer](#magicresizer)
	* [Quick resize icons](#quick-resize-icons)
* [Panel on face and between](#panel-on-face-and-between)
	* [Create panel on face](#create-panel-on-face)
	* [Create panel between](#create-panel-between)
* [Custom regular and irregular shapes](#custom-regular-and-irregular-shapes)
	* [magicManager](#magicmanager)
	* [addExternal](#addexternal)
	* [sketch2pad](#sketch2pad)
	* [wires2pad](#wires2pad)
* [Panels conversion](#panels-conversion)
	* [panel2pad](#panel2pad)
	* [Backward conversion](#backward-conversion)
* [Position](#position)
	* [panelMove2Anchor](#panelmove2anchor)
	* [showVertex](#showvertex)
	* [selectVertex](#selectvertex)
	* [panelMove2Face](#panelmove2face)
	* [mapPosition](#mapposition)
	* [panelMove2Center](#panelmove2center)
	* [shelvesEqual](#shelvesequal)
* [Preview furniture](#preview-furniture)
	* [fitModel](#fitmodel)
	* [makeTransparent](#maketransparent)
	* [frontsOpenClose](#frontsopenclose)
	* [magicView](#magicview)
* [Project manage](#project-manage)
	* [magicSettings](#magicsettings)
		* [Settings - page 1](#settings---page-1)
		* [Settings - page 2](#settings---page-2)
		* [Settings - page 3](#settings---page-3)
		* [Settings - page 4](#settings---page-4)
		* [Settings - page 5](#settings---page-5)
		* [Settings - page 6](#settings---page-6)
	* [selected2LinkGroup](#selected2linkgroup)
	* [selected2Link](#selected2link)
	* [selected2Group](#selected2group)
	* [selected2Assembly](#selected2assembly)
	* [selected2Outside](#selected2outside)
	* [eyeRa](#eyera)
	* [eyeHorus](#eyehorus)
	* [How to use containers - short tutorial](#how-to-use-containers---short-tutorial)
* [Decoration](#decoration)
	* [magicColors](#magiccolors)
	* [setTextures](#settextures)
	* [makeBeautiful](#makebeautiful)
* [Cut list, Measure, Dimensions, Bill Of Materials](#cut-list-measure-dimensions-bill-of-materials)
	* [getDimensions](#getdimensions)
		* [Report type](#report-type)
			* [Search path](#search-path)
			* [Main report](#main-report)
			* [Additional reports](#additional-reports)
		* [Units](#units)
		* [Precision](#precision)
		* [Visibility](#visibility)
		* [Additional settings](#additional-settings)
		* [Edgeband](#edgeband)
		* [Supported objects](#supported-objects)
		* [Supported transformations](#supported-transformations)
		* [Video tutorials and documentation](#video-tutorials-and-documentation)
	* [sheet2export](#sheet2export)
	* [showMeasurements](#showmeasurements)
	* [magicMeasure](#magicmeasure)
* [Dowels and Screws](#dowels-and-screws)
	* [magicDowels](#magicdowels)
	* [panel2link](#panel2link)
	* [panel2clone](#panel2clone)
	* [sketch2dowel](#sketch2dowel)
	* [edge2dowel](#edge2dowel)
* [Fixture](#fixture)
	* [magicFixture](#magicfixture)
	* [edge2drillbit](#edge2drillbit)
	* [Dowels, Screws, Fixture - short tutorial](#dowels-screws-fixture---short-tutorial)
* [Drilling holes](#drilling-holes)
	* [magicDriller](#magicdriller)
	* [drillHoles](#drillholes)
	* [drillCountersinks](#drillcountersinks)
	* [drillCounterbores](#drillcounterbores)
	* [drillCounterbores2x](#drillcounterbores2x)
	* [magicCNC](#magiccnc)
	* [cutDowels](#cutdowels)
* [Parameterization](#parameterization)
	* [magicGlue](#magicglue)
	* [sketch2clone](#sketch2clone)
	* [showAlias](#showalias)
* [Construction profiles](#construction-profiles)
	* [panel2profile](#panel2profile)
	* [panel2angle](#panel2angle)
	* [panel2angle45cut](#panel2angle45cut)
	* [panel2frame](#panel2frame)
	* [cornerBlock](#cornerblock)
	* [cornerBrace](#cornerbrace)
* [Joinery](#joinery)
	* [magicJoints](#magicjoints)
	* [jointTenonCut](#jointtenoncut)
	* [jointMortiseCut](#jointmortisecut)
	* [grainH](#grainh)
	* [grainV](#grainv)
	* [grainX](#grainx)
	* [magicCut](#magiccut)
	* [magicKnife](#magicknife)
	* [jointTenonDowel](#jointtenondowel)
	* [cutTenonDowels](#cuttenondowels)
	* [magicCorner](#magiccorner)
	* [magicCutLinks](#magiccutlinks)
	* [magicKnifeLinks](#magicknifelinks)
	* [jointTenonDowelP](#jointtenondowelp)
	* [cutTenonDowelsP](#cuttenondowelsp)
* [Router](#router)
	* [Router bit - Cove](#router-bit---cove)
	* [Router bit - Round Over](#router-bit---round-over)
	* [Router bit - Straight](#router-bit---straight)
	* [Router bit - Chamfer](#router-bit---chamfer)
	* [multiPocket](#multipocket)
* [Advanced](#advanced)
	* [addVeneer](#addveneer)
	* [align2Curve](#align2curve)
	* [roundCurve](#roundcurve)
	* [showOccupiedSpace](#showoccupiedspace)
	* [showConstraints](#showconstraints)
* [Code and Debug](#code-and-debug)
	* [scanObjects](#scanobjects)
	* [showPlacement](#showplacement)
	* [debugInfo](#debuginfo)
* [API for developers](#api-for-developers)
* [Short old tutorials](#short-old-tutorials)
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

# Installation

## Step 0. Install supported kernel

**Currently supported kernels:**
* [FreeCAD 0.21.2.33771](https://github.com/FreeCAD/FreeCAD/releases/tag/0.21.2): Personally, I like this version of FreeCAD. It runs very fast on my slow laptop, is stable, and all the bugs are well-known. So, I would like to keep backward compatibility with this version as long as possible. The only thing missing is `VarSet`, which is more handy than spreadsheet in my opinion.
* [FreeCAD 0.21.4.33929](https://codeberg.org/xCAD/FreeCAD21/releases/tag/0.21.4): This is Werner and Zolko xCAD branch. I think the guys are doing the right thing by wanting to maintain support for such a good version of FreeCAD as `0.21.2` version. That is why I decided to test their version and add support for this version as well.
* [FreeCAD 1.0.1.39285](https://github.com/FreeCAD/FreeCAD/releases/tag/1.0.1): The advantage of this version is `VarSet`. Unfortunately, this version has encountered issues with edge, face, vertex selection for `Pad` objects in `LinkGroup` containers, which makes using such objects very uncomfortable. However, there are no noticeable issues with simple `Part::Box` panels. Also, this version is much slower on my slow laptop. Read more about: [FreeCAD 1.0+ Support](https://github.com/dprojects/Woodworking/issues/49).
* [FreeCAD 1.0.2.39319](https://github.com/FreeCAD/FreeCAD/releases/tag/1.0.2): Personally, I do not see any major differences or benefits between versions `1.0.1` and `1.0.2`. Since this is the next official stable release, I decided to add it to the list of supported kernels.
* [FreeCAD weekly 1.1.0.20251104](https://github.com/FreeCAD/FreeCAD/releases/tag/weekly-2025.11.05): This is the last of the weekly development releases before the `1.2` development release. I have been using this version for a while now to develop new features for Woodworking workbench, so I have had the opportunity to test it quite thoroughly with the Woodworking workbench. A major advantage of the `1.1dev` release is that it eliminates the issues with selecting and deleting objects in `LinkGroup` containers, which significantly improves the user experience. An additional advantage is the new version of `PySide6`, which extends the life of this kernel. Therefore, I decided to add this version to the tested kernels and create an installation package [magicCAD_2.0](https://github.com/dprojects/Woodworking-package/releases/tag/2.0) with this kernel version to keep it working forever.
  
> [!NOTE]
> * Whenever possible, I try to use and test the latest development versions so that I do not have to work so long on fixing 
> Woodworking wokbench after the stable kernel version is released. Because of this, backward compatibility for some features 
> can sometimes be lost. However, if you are still using any of the above listed kernels and have noticed such a problem, 
> please open an issue and I will try to fix it if possible. <br>
> * I don't have `Windows` or `macOS`, so I am not able to test and certify this workbench for those systems. <br>

## Step 1. Download Woodworking workbench

* Stable certified versions download at: [Woodworking/releases](https://github.com/dprojects/Woodworking/releases)
* For cutting edge features download: [the master branch](https://github.com/dprojects/Woodworking/archive/refs/heads/master.zip) or run command: `git clone https://github.com/dprojects/Woodworking.git`

> [!NOTE]
> **New significant changes since the last release 2.0 stable:** <br>
> * tools GUI position anchor option (MagicPanels, magicSettings, magicStart) <br>
> * added edgeband price to cut-list (MagicPanels, magicSettings, getDimensions) <br>
> * improve workbench update and add buttons to list and remove disabled workbenches (debugInfo) <br>
> * Ukrainian translation <br>
> * improve layout position and size (MagicPanels, all tools with GUI) <br>
> * new magicStart layout with scroller (magicStart) <br>
> * option to add theme to main window (magicSettings, MagicPanels) <br>
> * support for Draft::PathArray objects at cut-list (getDimensions) <br>
> * options to browse folder with textures and redesign GUI (setTextures) <br>
> * attributes option for drilling via CNC (magicCNC) <br>
> * improve panel at face and panel between (MagicPanels, MagicPanelsController) <br>
> * new global variable and option for shelf sides offset (MagicPanels, magicSettings, magicStart) <br>
> * object anchor option to create panel along path (magicMove) <br>
> * not calculate global position for measurement inside containers (MagicPanels) <br>
> * fix fronts open and close inside containers (frontsOpenClose) <br>
> * improve textures, GUI, add live preview and any axis (setTextures) <br>
> * maximum and minimum edge size in cut-list (getDimensions) <br>
> * improve samples of furniture modules (magicStart) <br>
> * load textures from Woods workbench material texture attribute (setTextures) <br>
> * add Woods workbench material description to cut-list (getDimensions) <br>
> * copy .Label2 description and .ShapeMaterial to new copied objects (MagicPanels) <br>
> * material description in cut-list (getDimensions, MagicPanels, magicSettings, fixes) <br>
> * weight and price as additional column in cut-list (getDimensions) <br>
> * tools to show and hide tree structure (eyeRa, eyeHorus) <br>
> * toolbar fix for FreeCAD 1.2dev (InitGui) <br>
> * map to face for pocket hole object (panelMove2Face) <br>
> * router and pocket backward compatibility fix (MagicPanels) <br>

## Step 2. Get FreeCAD Mod folder localization

* From FreeCAD python console run command:

		FreeCAD.ConfigDump()["UserAppData"]

* If there is no `Mod` folder, create it.

## Step 3. Install Woodworking workbench

* Go to FreeCAD `Mod` folder, for example, in Xubuntu operating system:

		cd  ~/.local/share/FreeCAD/Mod/

* Unpack woodworking workbench, if needed, and copy `Woodworking` folder directly to `Mod` folder. This should be:

		~/.local/share/FreeCAD/Mod/Woodworking/

> [!TIP]
> The `README.md` file should be: `~/.local/share/FreeCAD/Mod/Woodworking/README.md`

# Extras

This woodworking workbench is delivered with several useful extras:

* [Fully parametric examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Parametric) - this folder inside woodworking workbench contains sample furniture projects. All of the furniture examples are parametric. So, you can quickly adopt it to your current project, without designing e.g. bookcase from scratch. You can also add decoration, if needed, or even merge with other projects.
* [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture) - this is new approach to 3D modeling. For example you can replace any Cylinder with realistic looking detailed screw. This is very powerful feature and gives a lot of flexibility and simplifies the process of making model detailed.
* [Texture samples](https://commons.wikimedia.org/w/index.php?title=Special:ListFiles/Dprojects&ilshowall=1) - sample textures for woodworking projects purposes.

# Translations

Currently supported languages: 
  
* **English** - by default development language
* **Polish** - my native language supported since 0.23 release
* **Ukrainian** added by [Andrii Semerun](https://github.com/dprojects/Woodworking-translations/pull/1) since 2.0 release

Of course, if someone is interested in doing a translation, please create pull request at: [github.com/dprojects/Woodworking-translations](https://github.com/dprojects/Woodworking-translations) repository.
  
Since Woodworking workbench release 0.22 there is `translations update tool` available under drop down menu `Woodworking -> Download and update all translations`. This tool will automatically download all available `.qm` files from [github.com/dprojects/Woodworking-translations](https://github.com/dprojects/Woodworking-translations) repository into `translations` folder for you Woodworking workbench version.

# Objects, Workflow, Golden rules

Woodworking workbench does not create any specific objects. Objects created by Woodworking workbench can be further processed using standard FreeCAD tools.

Woodworking workbench does not have a pre-defined workflow. It is just a set of additional tools that you can use to make your work easier.

The general rule of FreeCAD is that you create an object in Sketch and then assemble the objects using Assembly. However, in the case of cabinets where each board is practically the same, it makes no sense to draw each board from scratch in Sketch, save it in a separate file and then assemble it. Of course, if someone wants to do it in this way, they can do this. The Woodworking workbench not disable any workbench or possibilities.

I personally design furniture structures directly, from simple panels. I usually focus only on designing the main structure, possible locations of mounting points, stress distribution and ease of creation in real life. I do not design hinges, handles, mounting elements such as dowels or screws, because this is an obvious stage of assembly in real life. Accessories such as hinges, handles, drawer systems or angle brackets are bought in the store and simply assembled, you do not need to design them in detail to make furniture.

The techniques I show also allow you to avoid problems caused by Sketch or PartDesign objects, and FreeCAD bugs in general. For this reason, I have created golden rules so that new users who are unfamiliar with the issues in FreeCAD do not encounter unsolvable problems that can be easily solved by just changing their approach to design.

**Golden rules:**

* Not rotate objects directly, rotate them via LinkGroup container.
* Not copy Pad directly. Copy, Clone or Link the Part container.
* Not mix Cut with PartDesign too much. Keep clear and simple design line based on simple panels.
* If you want generate cut-list, BOM, dimensions, rather avoid packing objects extremely, for example Array on Array or MultiTransform on MultiTransform.
* Not move objects via AttachmentOffset, move them via Body or LinkGroup container.
* Design furniture from simple panels (Part::Box objects). If you want more detailed model convert desired simple panel into Pad and edit the Sketch. Also for irregular or not rectangle shapes.
* Always make backup of your project. Read documentation, watch videos, learn more or open issue.
* Break all rules, if you know what you are doing.

# How to start

## magicStart

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicStart.png">This tool was created to make it easier to start designing furniture. It contains some structures that I often use personally, as well as other carpentry solutions suggested by users. However, this tool does not contain a complete list of solutions, because there are too many of them in the world of carpentry, practically every carpenter and manufacturer of furniture or accessories has their own standards. I try to adjust the contents of this tool in such a way that it gives the greatest possible possibilities for later processing and adapting the initial structure to your own needs. If you have any interesting woodworking idea or solution, worth to be added, please let me know.

* **calculate** button is intended to pre-calculate the remaining dimensions based on those given above this button, although in some cases you can skip this button and create an object or furniture with default settings.
* **create** button is intended to create a given object, furniture.

**Currently available solutions:**

### Construction geometry

* Workspace platform

### Cabinet structure

**Single module samples:**

* Storage module ( front outside, back inside, veneer )
* Storage module ( front outside, back outside, veneer )
* Storage module ( front inside, back inside, veneer )
* Storage module ( front inside, back outside, veneer )
* Kitchen wall module ( front outside, back outside, veneer )
* Bookcase module ( no front, back outside, veneer )

**Multi-module samples:**

* Storage ( front outside, back inside, heavy duty )
* Wardrobe ( front outside, back outside, 2x clothes width )
* Wardrobe ( front outside, back outside, clothes hangers )
* Bookcase ( no front, back inside, simple )
* Bookcase ( no front, back outside, simple )
* Bookcase ( import parametric )

**Modules for custom construction:**

* Module base ( back inside, veneer )
* Module on top ( back inside, veneer )
* Module base ( back outside, veneer )
* Module on top ( back outside, veneer )

> [!TIP]
> Constructions with `veneer` descriptions support veneer settings in [magicSettings](#magicsettings) tool.

**Video tutorials:** 
* [Furniture creation tool](https://www.youtube.com/watch?v=lHQ1J9Nahcs)
* [New furniture samples in magicStart](https://www.youtube.com/watch?v=o2cw2Z8vQoE)
* [How to build complex furniture from modules](https://www.youtube.com/watch?v=SUm_N2rjXbs)

### US style

* Simple storage ( face frame, no front, back HDF )
* Simple bookcase ( face frame, no front, back HDF )
* Kitchen cabinet ( US style )
* Kitchen wall cabinet ( US style )
* Face Frame ( vertical, for custom changes )
* Face Frame ( horizontal, around )
* Face Frame ( horizontal, with center )
* Face Frame ( horizontal, for custom changes )

**Video tutorials:** 
* [How to create "kick toe" in kitchen cabinet](https://www.youtube.com/watch?v=aLZh3mH-OH8)
* [How to add Face Frame to the furniture](https://www.youtube.com/watch?v=CtWfvxd4UmI)
* [Kitchen cabinet with face frame](https://www.youtube.com/watch?v=WW8du2l_ZuY)

### Drawers for cabinets

* Drawer ( single, X or Y direction, front outside )
* Drawer ( single, X or Y direction, front inside )
* Drawer ( series, front outside )
* Drawer ( series, front inside )
* Drawer ( series, Blum, Hafele, GTV, Amix, front outside )
* Drawer ( series, Blum, Hafele, GTV, Amix, front inside )
* Drawer ( simple, parametric )
* Drawer ( decoration, parametric )
			
**Video tutorials:** 
* [How to set front thickness and overlap](https://www.youtube.com/watch?v=geEolSSB6n0)
* [How to create drawer at each side](https://www.youtube.com/watch?v=4qEbQQhwmns)
* [How to make drawer series](https://www.youtube.com/watch?v=tncytX82NSY)
* [How to connect drawer elements together](https://www.youtube.com/watch?v=FwyzZR5V05c)

### Fronts for cabinets

* Front outside
* Front outside ( decorative )
* Front outside with glass ( simple frame )
* Front outside with glass ( frame with decoration )
* Front inside
* Front inside ( decorative )
* Front inside with glass ( simple frame )
* Front inside with glass ( frame with decoration )
* Front decoration ( simple frame )
* Front left (decoration, import parametric )
* Front right (decoration, import parametric )

**Video tutorials:** 
* [How to create front with glass](https://www.youtube.com/watch?v=csZK_k8GpnQ)
* [How to use decoration features](https://www.youtube.com/watch?v=R9u6ikswO_0)

### Shelves and top for cabinets

* Shelf
* Shelf series with equal space
* Top (decoration, import parametric )

**Video tutorials:** 
* [How to create shelf inside gap](https://www.youtube.com/watch?v=zbhK4dNWQl0)
* [How to create shelves with equal space](https://www.youtube.com/watch?v=2odJa0baGqw)

### Sides for cabinets

* Side
* Center side
* Side decoration ( simple frame )
* Sides with holes ( import parametric )

**Video tutorials:** 
* [How to create side anywhere](https://www.youtube.com/watch?v=IS3MDLzv6Ko)
* [How to create center side](https://www.youtube.com/watch?v=0rSwB46ssEk)
* [How to use decoration features](https://www.youtube.com/watch?v=R9u6ikswO_0)

### Back

* Back outside ( HDF )
* Back inside ( full )

**Video tutorials:** 
* [Simple office bookcase](https://www.youtube.com/watch?v=U_oi3POJmSw)

### Foot for cabinets

* Foot ( good for cleaning )
* Foot ( standard )
* Foot ( more stable )
* Foot ( decorated )
* Foot ( chair style )

**Video tutorials:** 
* [How to add feet](https://www.youtube.com/watch?v=E4yfRFIqops)
* [New furniture samples in magicStart](https://www.youtube.com/watch?v=o2cw2Z8vQoE)

### Table

* Table ( kitchen simple style )
* Table ( kitchen modern style )
* Table ( kitchen decorated style )
* Table ( coffee simple style )
* Table ( coffee modern style )
* Table ( coffee decorated style )
* Table ( school desk, single right side )
* Table ( School desk, single left side )
* Table ( school desk, both sides )
* Table ( simple, import parametric )

**Video tutorials:** 
* [How to create table](https://www.youtube.com/watch?v=-_ePqw0f1NU)
* [Simple table with drawers quickly](https://www.youtube.com/watch?v=0b5DRSQg52U)
* [New furniture samples in magicStart](https://www.youtube.com/watch?v=o2cw2Z8vQoE)

### Connections

* Dowel 8x35 mm ( import parametric )
* Biscuits 4x16x48 mm ( import parametric ) 
* Biscuits 4x21x54 mm ( import parametric ) 
* Biscuits 4x24x57 mm ( import parametric ) 
* Screw 3x20 mm for HDF ( import parametric ) 
* Screw 4x40 mm ( import parametric ) 
* Screw 5x50 mm ( import parametric ) 
* Pocket screw 4x40 mm ( import parametric ) 
* Minifix 15x45 mm ( import parametric ) 
* Counterbore 2x 5x60 mm ( import parametric )

**Video tutorials:** 
* [How to add minifix connection point](https://www.youtube.com/watch?v=ZaEWmqtlj1Y)
* [How to measure minifix and add to cut-list](https://www.youtube.com/watch?v=l7y0HETobIw)
* [How to drill holes for minifix](https://www.youtube.com/watch?v=4A9lsZveXPc)
* [How to add screws, 2 ways](https://www.youtube.com/watch?v=B0kChgAFAJU)
* [How to add screws to HDF back](https://www.youtube.com/watch?v=MvIRFPDGKYQ)
* [Biscuits joints](https://www.youtube.com/watch?v=NCf07IwuRJI)

### Accessories

* Shelf Pin 5x16 mm ( import parametric )
* Handle ( single hole )
* Handle ( single hole, decorated )
* Handle ( double hole )
* Handle ( double hole, decorated )
* Brackets for wall cabinets ( [Camar 807](https://www.camar.it/prodotti_scheda.php?cat_id=31&prod_id=807%2002%20Z1%20IN%20__&id=259) ) 
* Angle 30x30x25 mm ( import parametric )
* Angle 80x80x20 mm ( import parametric )
* Angle 40x40x100 mm ( import parametric )

**Video tutorials:** 
* [How to add brackets to the kitchen wall cabinet](https://www.youtube.com/watch?v=idHDN9KJYis)
* [How to add handle and see soft-close animation](https://www.youtube.com/watch?v=iOseEBGmwAU)
* [How to add feet](https://www.youtube.com/watch?v=E4yfRFIqops)

### Other

* Simple chair ( import parametric )
* Picture frame ( import parametric )
* Storage box ( import parametric )

> [!TIP]
> To set default wood thickenss or wood color you can use [magicSettings](#magicsettings) tool.

## Default panels

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultZY.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultYZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultZX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultXZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultYX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelDefaultXY.png"> There are many types of wood. So there is no chance to cover all possible wood sizes provided by the market. This starting panels allow you for quick start. You do not have to start each time from `10 x 10 x 10` box `Cube` object and think where should be the thickenss. This tool creates default panel that can be easily resized. You can clearly see where should be the thickness to keep exact panel `XYZ` axis orientation. 

> [!TIP]
> All furniture elements should be created according to the `XYZ` axis plane, if possible. Avoid building whole furniture with rotated elements. If you want to rotate panel with dowels, better create panel with dowels without rotation, pack panel with dowels into container like `LinkGroup`, and use [magicAngle](#magicangle) to rotate whole `LinkGroup`. You can rotate whole furniture like this with single click and the dowels will be in the correct place after rotation. If you would like to apply dowels at rotated element it would be pointless complication, almost impossible at FreeCAD. 
> To set default wood sizes or wood color you can use [magicSettings](#magicsettings) tool.

# Move and copy

## magicMove

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicMove.png"> This tool allows you to move and copy objects more easily. This tool supports multi-selection, hold left-CTRL key during selection to select more objects, so you can move or copy many objects at once with desired step. 

**Options:**

* **refresh selection:** loads new objects. To skip this button, please see `Current selection: yes` options at [magicSettings](#magicsettings) tool.

* **Move:** In this mode you can move any object with custom step. You can also move containers, for example panel with dowels inside `LinkGroup`.
  * buttons: `X-`, `X+`, `Y-`, `Y+`, `Z-`, `Z+` move object into the chosen axis direction, there is auto-repeat so you can hold the button to move objects more quickly.
  * `Move step` if the object is recognized the `Move step` will be set by default with selected object thickness. The offset is calculated from objects anchors, usually left bottom corner (vertex).
  * `animate move` if it is checked it will add animation to the move, so you can see a soft-close animation of the cabinet drawer.
  
* **Move to Equal:** In this mode you can set equal space between objects. This feature works in the same way as [shelvesEqual](#shelvesequal) but here you can choose the coordinate axis.
  * `set` allows to set edge as start or end reference point. Sometimes if the access to edge require hide object it can be more useful to set one by one or if you want to update only single edge.
  * `set both edges` allows to set both edge at once as start and end reference point. This is much quicker way.
  * `move` set equal space between all selected objects along X, Y or Z coordinate axis. 

> [!TIP]
> If you want to set equal space for Array object, you have to select and load Array object from Tree window.

* **Copy:** In this mode you can copy any object with custom offset. For example you can quickly create shelves with equal space or garden floor from small panels.
  * `auto` if the object is simple panel `Part::Box` type the `copyObject` will be used, otherwise `Clone` will be created.
  * `copyObject` the same as `CTRL-C` and `CTRL-V` copy method, good only for simple objects.
  * `Clone` if you want to further process such an object, for example you will measure and drill into such an object.
  * `Link` if you only want to generate a cut-list and do no further processing on this object, it will only be a visual representation of the base object, and you will not measure or drill into such an object.
  * `Array` creates parametric array object, it can be useful if you want to have single parametric object instead of many independent objects.
  * `copy to new container` next element will be copied to new `LinkGroup` container. If you click the button this will turn into disabled and will be waiting for new copy created to avoid double clicks.
  * `Object type` allows you to change anchor for rotated objects:
    * `normal` this should be used for regular objects along coordinate axes X, Y, Z. For rotated object please use `rotated` option, `Copy by Edge` or `Copy by Path`.
    * `rotated` if the object is rotated the occupied space calculated from vertices along coordinate axis will be different, so the space between edges will be bigger because the rotated object have bigger size. The `rotated` allows you to force size calculation directly from object.
  * `Copy offset` this is offset between objects but calculated from objects sides. If this is set to 0 the next element will be created without space in relation to the last element.
  * buttons: `X-`, `X+`, `Y-`, `Y+`, `Z-`, `Z+` copy object into the chosen axis direction, there is auto-repeat so you can hold the button to copy objects more quickly.

* **Copy by Edge:** In this mode you can copy any object but using selected edge as position reference. This feature allows you, for example, to copy part of the furniture without further positioning each element one by one.
  * `auto` if the object is simple panel `Part::Box` type the `copyObject` will be used, otherwise `Clone` will be created.
  * `copyObject` the same as `CTRL-C` and `CTRL-V` copy method, good only for simple objects.
  * `Clone` if you want to further process such an object, for example you will measure and drill into such an object.
  * `Link` if you only want to generate a cut-list and do no further processing on this object, it will only be a visual representation of the base object, and you will not measure or drill into such an object.
  * `Array` creates parametric array object, it can be useful if you want to have single parametric object instead of many independent objects.
  * `set` allows to set `edge` or `face` as copy reference point. In case of edge you should add `- wood thickness` offset, for example `-18`, to create mirror copy by edge. In case of face the reference point will be the `CenterOfMass` of the selected face, so the mirror copy can be created without setting any offset, this is more quicker version.
  * `Additional offset` this offset will be added to the object offset. For example, if the objects distance from the selected edge on the `X` axis is `18`, i.e. the shelves are touching the right side of the furniture inside, but the selected edge is the right outer edge of the furniture, and the additional offset is set to `-18`, then the shelves will be created `18 (distance) - 18 (additional offset) = 0` from the edge, touching the right outer side of the furniture. So for example you can copy shelves from left to right and ignore the thickness of the right side board of the furniture and quickly extend the furniture to the right.
  * `create`creates a panel in the selected axis direction. In the film, the button responsible for the case in which the plane of the object to be copied is the same as the plane of the selected edge is disabled. This was to avoid copying the object "in place". However, this can be used, for example, to copy the top shelf to the bottom. If the shelf is on the top of the furniture and you want to create a copy along the Z edge, i.e. relative to the edge of the right side of the furniture, the copy point will be the center of the edge, which means that the top shelf will be copied as the bottom shelf.
  
* **Copy by Path:** This mode allows you to create panels along the path. If the panel is already at the path, next panel will be created with the offset from selected panel. With this approach you can remove some panels and fill the gap in a different way, for example with different rotation. If the panel is outside the path, the first panel will be created at the 0 point of the path. This feature allows you, for example, to create irregular shpes like garden sunbed.
  * `auto` if the object is simple panel `Part::Box` type the `copyObject` will be used, otherwise `Clone` will be created.
  * `copyObject` the same as `CTRL-C` and `CTRL-V` copy method, good only for simple objects.
  * `Clone` if you want to further process such an object, for example you will measure and drill into such an object.
  * `Link` if you only want to generate a cut-list and do no further processing on this object, it will only be a visual representation of the base object, and you will not measure or drill into such an object.
  * `Array` creates parametric array object, it can be useful if you want to have single parametric object instead of many independent objects.
  * `copy to new container` next element will be copied to new `LinkGroup` container. If you click the button this will turn into disabled and will be waiting for new copy created to avoid double clicks.
  * `set` allows to load the path or reset start position. You can refresh only path here without changing objects to copy. The path can be Wire, Sketch, Helix, or any edge, also edge of the hole.
  * `Rotation X, Y, Z` allows to apply rotation angle for the new object before it will be created. The rotation is added to the last panel rotation, so to stop rotate you have to set 0 again. This approach allows to add rotation during panel creation, so you can adjust each panel during creation to fit the curve, see also [align2Curve](#align2curve).
  * `Next point step` is offset for new panel. This is related to the point at the path. By default it is set to second size of the panel.
  * `Anchor` allows to set anchor for new created object:
    * `default` normal object placement.
    * `object center` the object CenterOfMass.
  * `copy along path` creates new panel along the path. This button has auto-repeat mode, if you hold it this will be creating panels without clicking many times.

* **Mirror:** This option create mirror with reference as edge, face or vertex, also you can add additinal offset. 
  * `auto` if the object is simple panel `Part::Box` type the mirror will be created using parametric `LinkGroup` method, otherwise the `Clone` will be used.
  * `LinkGroup` mirror will be created using `LinkGroup` container. In this case you should select `Part::Box` object (simple panel) or `App::Part` container. If you want to create parametric mirror for `PartDesign` object the structure should be `Part -> Body -> PartDesign object` and you should select the `Part` container, this is to avoid `PartDesign` object destroy.
  * `Clone` mirror will be created using `Clone` object, this is good if you want to make a mirror of the `PartDesign` object.
  * `set` allows to load the reference point for mirror as edge, face or vertex.
  * `Mirror XYZ:` is base position for mirror, the base position will be in the middle between object and new created mirror if there is no additinal offset.
  * `Additional offset` this offset will be added to the mirror position.
  * `create` creates mirror in the chosen axis direction.

* **Cross:**
  * `Corner cross:` buttons `-`, `+` resize the cross in the right bottom of the screen, it has auto-repeat.
  * `Center cross:` buttons `on`, `off` turn on and off the center cross at the screen.
  * `keep custom cross settings` allows to store the custom cross setting after this tool exit.

**Video tutorials:** 
* [How to use magicMove](https://www.youtube.com/watch?v=DpU2zlckv88)
* [Draft & BIM Array improved](https://www.youtube.com/watch?v=mpjZCGqLbPU)
* [How to set equal space between objects](https://www.youtube.com/watch?v=4EfNV-ur6Rw)
* [How to copy part of the furniture](https://www.youtube.com/watch?v=oxNiwtZV-Uc)
* [How to handle dimension changes](https://www.youtube.com/watch?v=HED1-BH66BU)
* [How to add handle and see soft-close animation](https://www.youtube.com/watch?v=iOseEBGmwAU)
* [Simple office bookcase](https://www.youtube.com/watch?v=U_oi3POJmSw)

## Arrows

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveXp.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveXm.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveYp.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveYm.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveZp.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMoveZm.png"> With the arrows you can quickly move panel with thickness step to solve common furniture problem with thickness offset. If you select PartDesign object, it will be moved with thickness step via Body container. If you select containers `App :: Part`, `PartDesign :: Body`, `App :: LinkGroup` and object `App :: Link`, the move step will be 100, to allow move whole furniture modules or drawers inside container more quickly. Also if the thickness will not be recognized the step will be 100. You can also use the arrows for quick copy. Select object at objects Tree, click `CTRL-C` and `CTRL-V` to copy in-place the selected object and use arrows to move the object.

> [!WARNING]
> You can move many objects at once, but make sure the objects have the same thickness to avoid moving objects with different step. If you want precisely move many objects with given step, please use [magicMove](#magicmove) tool, instead. <br>
> The arrows recognize the view model rotation. However, all possible rotations are not recognized, sometimes the movement may not be correctly aligned with the arrow icon. So, it is strongly recommended to click [fitModel](#fitmodel) tool before using arrows.

## magicAngle

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicAngle.png"> This tool allows to rotate panels and even other more complicated objects, like construction profiles or containers. It allows for multi-selection, so you can rotate many elements with the same rotation point at once. You can use this tool to open or close cabinet door with soft close animation.

**Options:**

* **refresh selection** this button loads objects for which rotation is to be performed.
* **Sphere radius** Allows you to resize rotation indicator sphere. This tool checks reference for the object, content of containers and get size to set the default size of the sphere. by default the sphere radius is set to object thickness. You can increase or decrease the value or set your custom one.
* **Rotation point** Allows you to switch between several predefined rotation points. If the predefined points not allows you to rotate the object as you wish, you can add your custom point. You can select:
  * `vertex` in this case this vertex will be added to the end of the `Rotation point` list.
  * `edge` in this case first and end point of the edge will be added to the end of the `Rotation point` list and also CenterOfMass of the edge.
  * `face` in this case all face vertices and CenterOfMass of the face will be added to the end of the `Rotation point` list.
* **add selected vertex** this button loads selected rotation points at the end of the `Rotation point` list.
* **X-**, **X+**, **Y-**, **Y+**, **Z-**, **Z+** allows to rotate loaded objects according to the XYZ coordinate axes. 
* **value between** shows current rotation status so you can quickly rotate back the object, if you still have opened the tool interface. If you close it you have to use CTRL-Z to undo rotation. Because of screen size issue, shows only float precision rounded to two digits but the rotation value set to object is without rounding.
* **Angle step** is step for rotation, float precision is allowed.
* **animate rotation** if it is checked it will add animation to the rotation, so you can see a soft-close animation of the cabinet door.

**Video tutorials:** 
* [How to add handle and see soft-close animation](https://www.youtube.com/watch?v=iOseEBGmwAU)
* [Quick parametric fence](https://www.youtube.com/watch?v=egmC-uR4aa4)

# Resize panels

## magicResizer

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicResizer.png"> This tool allows to resize `Part::Box` or `PartDesign::Pad` objects and also other objects based on `PartDesign::Pad` e.g. [construction profiles](#panel2profile). Make sure your `Pad` object has defined constraints, you can use [showConstraints](#showConstraints) tool for that. If the object has no constraint at the selected edge the object will not be resized. The constraints do not have to be named but must be defined. 

**Possible selection:**

* **set** first button allows you to load selected edge to resize and second one below allows you to load selected face, edge or vertex as destination to resize. The buttons can be used for individual reload but to select destination you have to have loaded edge to resize first.
* **refresh selection** allows you to load selected edge to resize and also selected face, edge or vertex as destination to resize. First selected needs to be edge to resize and next destination.

> [!TIP]
> If you first select edge and next destination and open this tool, the objects will be loaded automatically, 
> so you do not have to press `refresh selection` button.

**Resize options:**

* **Resize step:** if you have loaded destination sub-object this resize step will be automatically recalculated.
* **resize -** button allows you to make smaller loaded edge to resize. The resize size will be `resize step`.
* **resize +** button allows you to make bigger loaded edge to resize. The resize size will be `resize step`.
* **resize to nearest** button allows you to resize object to the nearest face, edge or vertex of other object. This option is able to make panel smaller or bigger automatically to the destination.

**Video tutorials:** 
* [How to use magicResizer](https://www.youtube.com/watch?v=GzC_XoOzeJ8)

## Quick resize icons

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize6.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize5.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize3.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize2.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelResize1.png"> You can resize panel, or even many panels at once, very quickly. The resize step is selected panel thickness, so you can solve the common problem with thickness offset. For example to move top of the furniture and make shelf from it, you have to resize the panel `2 x` with thickness step and once from other side. This may not be so easy calculation, and you may have to calculate something like `534 - 18 - 18 = ?` and `613 - 18 = ?`. Now you can click three times and you have it without thinking. You can also resize Cylinders (drill bits), the long side will be `Height`, the short will be diameter, the thickness will be `Radius`. For Cone objects (drill bits - countersinks, counterbore) the long side will be `Height`, the thickness will be `Radius1` (bottom radius) and the short will be `Radius2` (top radius). [Holes, Countersinks, Counterbores](#holes-countersinks-counterbores---short-tutorial).

# Panel on face and between

## Create panel on face

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceZY.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceYZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceZX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceXZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceYX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelFaceXY.png"> Please select face to create panel at this face. This tool creates new panel at selected face. The blue panel represents the selected face direction and the red one represents the new created panel direction. The icon refers to the base `XY` model view (0 key position), click [fitModel](#fitmodel) tool icon to set model into referred view. The new created panel will get the same dimensions as panel of the selected face. This tool supports veneer thickness from [magicSettings](#magicsettings) and will add addiional offset but not resize the panel. If you have problem with unpredicted result, use [magicManager](#magicmanager) tool to preview panel before creation.

## Create panel between

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenZY.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenYZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenZX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenXZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenYX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBetweenXY.png"> Please select two faces at two different objects, to create panel between them. This tool creates new panel between two selected faces. Selection faces order is not important. To select more than one face, hold left `CTRL` key during second face selection. The blue panels represents the selected faces direction and the red one represents the new created panel direction. The icon refers to base `XY` model view (0 key position), click [fitModel](#fitmodel) to set model into referred view.  If the two selected panels will be matching the icon, the new created panel should fill the gap between the selected faces according to the icon red panel direction. This tool supports veneer thickness from [magicSettings](#magicsettings) tool and will add addiional offset and will resize the panel to fit the gap between. You can experiment with selection faces outside to resize the new panel. If you have problem with unpredicted result, use [magicManager](#magicmanager) tool to preview panel before creation.

# Custom regular and irregular shapes

## magicManager

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicManager.png">
This tool allows to preview panel before creation. It allows to see panel at single selected face and also panel between two faces. This tool can be used if you have problems with unpredicted result, "side effect of Magic Panels". However, clicking single icon is sometimes more quicker than opening GUI and choosing right panel. Sice `0.21 version` this tool is able to create panel from selected vertices. This functionality uses observer for reading and helping select vertices. You do not have to hit the vertex directly. If you select edge or face, the nearest vertex will be selected for you. Also you can remove last selected vertex from list if you make mistake. The selected vertices should create wire, shape, but you do not have to select last vertex to close the wire. The first selected vertex will be automatically added at the end to close the wire. If the panel thickness is not set by the user, the thickness for the new panel from vertices will be set from first selected object. Custom thickenss works only for vertices.

* **Panel at face:** To create panel at face select single face and click `refresh selection`.
* **Panel between faces:** To create panel between two faces select two faces and click `refresh selection`. To select more faces hold `CTRL` key. The selection order is important. If the panel is created outside change selection order.
* **Panel from vertices:** To create panel from vertices, you have to activate observer. The `first` means the thickness will be get from first selected object. You can set custom thickness if you want or you can also use this option to create panel from selected edges in Sketch, see also [wires2pad](#wires2pad) tool. 

**Options:**
  
* **Plane:** You can select panel orientation according to the `XYZ` coordinate axes. The panel can be created at planes: `XY`, `YX`, `XZ`, `ZX`, `YZ`, `ZY`, if you select single face. If you select two faces this tool automatically recognize plane of selected faces and adjust possible panels to create, there will be two panels for valid planes only.
* **Anchor:** You can select position for the new panel. The anchors are the face vertices. If the object is for example `Cut` there might be more than four anchors to choose.
* **Size:** Custom size is taken from edges. For example, if you have `Cut` object you can set panel with the same size as the cut edge. All edges should be available, search for the right one.
* **Offset:** The first selected offset means `no offset` from currently selected `Anchor`. All next are offset with current selected `Size` for `X-`, `X+`, `Y-`, `Y+`, `Z-`, `Z+` coordinate axis. This can be helpful if you want to make frame but the frame is for example `20 mm x 40 mm x 600 mm` and need to be offset with `40 mm`, different size than thickenss `20 mm`.

**Video tutorials:** 
* [How to create panel from wires in Sketch](https://www.youtube.com/watch?v=wV6nlN2z1Ng)
* [Panel from vertices](https://www.youtube.com/watch?v=6s0fbagPeZA)
* [Making panels improvement](https://www.youtube.com/watch?v=sunE2rLThZI)

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCoverXY.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelBackOut.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideRightUP.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideLeftUP.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideRight.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelSideLeft.png"> Dedicated panels allows you to add specific furniture element. You can add sides, back or top of the furniture with single click. The side panels improves the thickness offset at the face tools. If you would like to add back of the furniture manually, you have to calculate the back dimensions first. Next you have to move the panel exactly to the back of the furniture position. It is not so easy to do it manually because `1 mm` offset might be a problem. Now you can make it with several clicks, without calculating anything manually. 

> [!TIP]
> If you have problems with unpredicted result, "side effect of Magic Panels", please use [magicManager](#magicmanager) to preview panel before creation and [magicMove](#magicmove) to move or copy panels.

## addExternal

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/addExternal.png"> This tool allows you to quickly create external geometry visible in a sketch from selected edges and faces. Edges or faces can belong to any objects. If you select face all edges will be added as external geometry, if you select edge only single edge will be added. This tool uses the `PartDesign::SubShapeBinder` function but in a slightly more advanced form. To select more objects, hold down CTRL-left while selecting them. 

**Possible selections methods:**

* **Face as Plane + Edges and Faces** - in this case new Sketch with external geometry will be created. The new sketch plane will be taken from first selected face. I recommend this method, because in this case the sketch will be created in the root directory and all drawn wires can be converted to Pads in-place, using for example tool [wires2pad](#wires2pad) or [magicManager](#magicmanager) `Panel from vertices` option.
* **Sketch + Edges and Faces** - in this case the external geometry will be created inside the selected Sketch. If the Sketch is inside containers with offsets you can adjust position of the converted Pads using for example tool [panelMove2Anchor](#panelmove2anchor) and selecting two edges.

**Video tutorials:** 
* [How to add external geometry quickly](https://www.youtube.com/watch?v=TMcw2JkUeVM)
* [Irregular Shapes: create and measure Part :: Extrusion](https://www.youtube.com/watch?v=l8W5IDqvGgw)

## sketch2pad

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sketch2pad.png"> This tool allows you to create Pad object from selected Sketch. A Pad with the default size of `MagicPanels.gWoodThickness` and color from [magicSettings](#magicsettings) tool will be created for each selected Sketch. To change the default wood size or color use [magicSettings](#magicsettings) tool or change the Pad attributes directly. To select more Sketches hold left CTRL key during selection. This tool has been created to quickly create Pad object from Sketch created via [addExternal](#addexternal) tool to create irregular panels very quickly.

<br><br><br>

## wires2pad

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/wires2pad.png"> You have to select at least one Sketch to create a Pad from wires. This tool allows you to create panels from wires in Sketch. A Pad with the default size of `MagicPanels.gWoodThickness` will be created for each wire. To change the default wood size use [magicSettings](#magicsettings) tool or change the `Pad.Length` option. Also you can use the `Panel from vertices` option in the [magicManager](#magicmanager) tool, selecting the appropriate edges. To create separate Pads from one Sketch, wires must not touch each other. If the Sketch is placed in containers, for example `Part` or `LinkGroup` with set offsets, you need to adjust the panel position, for example using the [panelMove2Anchor](#panelmove2anchor) tool, selecting two edges. You can also consider creating panels from the Sketch in the root directory, see the [addExternal](#addexternal) tool.

**Video tutorials:** 
* [How to create panel from wires in Sketch](https://www.youtube.com/watch?v=wV6nlN2z1Ng)

<br><br><br>

# Panels conversion

## panel2pad

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2pad.png"> This tool allows to replace `Cube` panel with `Pad` panel. The new created `Pad` panel will get the same dimensions, placement and rotation as the selected `Cube` panel. You can transform many `Cube` panels into `Pad` at once. To select more `Cubes` hold `left CTRL key` during selection. This tool is mostly dedicated to add decoration that is not supported for `Cube` objects by FreeCAD PartDesign workbench. You can also change shape by changing the `Sketch`. This is mostly used for decoration that can be applied only to `Pad`, like `Fillet`.

**Video tutorials:** 
* [Automatic parametrization](https://www.youtube.com/watch?v=JuZsAjrQr6M)
* [FreeCAD 1.1 direct assembly](https://www.youtube.com/watch?v=u3Yh2WvdUIk)

<br><br><br>

## Backward conversion

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyZY.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyYZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyZX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyXZ.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyYX.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelCopyXY.png"> This tool creates a new simple panel `Part::Box` object based on a selected object of any type, for example `PartDesign` with holes. The newly created object will be consistent with the selected orientation relative to the `XYZ` coordinate axes visible on the icon. 

**Possible selection:**

* **object**: in this case the new object will be created at position `(0, 0, 0)` on the XYZ axis.
* **object and face**: to start in `CenterOfMass` of the face.
* **object and edge**: to start in `CenterOfMass` of the edge.
* **object and vertex**: to start in `CenterOfMass` of the vertex.

> [!TIP]
> If you want to copy Pad, you need to have Constraints named `SizeX` and `SizeY` at the Sketch. For custom objects types you need to have `Length`, `Width`, `Height` properties at object (Group: `Base`, Type: `App::PropertyLength`).

# Position

## panelMove2Anchor

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMove2Anchor.png"> This tool allows to align panels more precisely, with anchor. To align panels with anchors first select anchor at base object, next select anchor at each object to move. Hold left CTRL key to select anchors.

Available anchors to select: 

* **vertex** - selected vertex will be set as anchor,
* **edge** - CenterOfMass of the selected face will be set as anchor,
* **face** - CenterOfMass of the selected face will be set as anchor,
* **object** - default object anchor, of the Placement, will be set as anchor.

**Video tutorials:** 
* [Align to anchor](https://www.youtube.com/watch?v=IfVJVXVc9r8)

## showVertex

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showVertex.png"> This tool allows you to resize all vertices for selected objects or for all objects if there is no selected objects. Resized vertices are easier to select. This tool also change vertices color to red for better visibility. If the object have already resized or red vertices it will be changed back to normal. So, you can keep the model good looking with small vertices and if you have problem with vertices selection, you can quickly resize vertices for selection purposes only and back to normal later.

**Video tutorials:** 
* [Helping Vertex selection](https://www.youtube.com/watch?v=qSsua04AKg8)

<br><br>

## selectVertex

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/selectVertex.png"> This tool helps vertex selection. If you click this tool icon the tool activates observer and listen for your selection. If you select Face or Edge the nearest Vertex will be selected instead. If you select Vertex the Vertex will stay selected. The observer is closed after selection so this help works only once to not disturb face or edge selection later. If you want select more vertices with help of this tool, you have to hold left CTRL key during Edge or Face selection, you can also hold it during icon click. 

**Video tutorials:** 
* [Helping Vertex selection](https://www.youtube.com/watch?v=qSsua04AKg8)

## panelMove2Face

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMove2Face.png">To adjust panel to face please select: 

1. selection: **face**
2. selection: **objects to align**

> [!NOTE]
> This tool allows to move panels to the selected face position. You can select more objects holding left CTRL key. This tool allows you to avoid thickness step problem, if you want to move panel to the other edge but the way is not a multiple of the panel thickness. Also you can move shelves to the back or to the sides of the furniture. For rotated containers use [panelMove2Anchor](#panelmove2anchor).

**Video tutorials:** 
* [How to create shelves with equal space](https://www.youtube.com/watch?v=2odJa0baGqw)
* [Simple table](https://www.youtube.com/watch?v=Xru52f8uyBk)
* [Move to face](https://www.youtube.com/watch?v=i9pXqdEhahU)

## mapPosition

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/mapPosition.png"> First select object to copy position, next select objects to move. 

> [!NOTE]
> This tool allows to move objects to the same position as first selected object. The objects will be moved without rotation. Only the placement will change. If the first selected object is rotated the objects may not match exactly the starting point. This tool is very useful if you want to redesign furniture and you want to create new element. Using this tool you can quickly move the new element to the same position of old element and remove the old element. To select more objects hold left CTRL key during selection. With this tool you can also move Cylinders and Sketches more precisely. If first you select Edge or Face the Cylinders or Sketches will be moved to the CenterOfMass. If first you select Vertex the Cylinders or Sketches will be moved to the selected Vertex position.

**Video tutorials:** 
* [Mapping position](https://www.youtube.com/watch?v=841xzb_uRpc)
* [mapPosition little improved](https://www.youtube.com/watch?v=pMKLXvwmGSI)

## panelMove2Center

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panelMove2Center.png"> ￼This tool allows you to center objects. Possible selection methods:
* Edge + Edge + Objects
* Face + Face + Objects
* Vertex + Vertex + Objects
* Hole edge + Hole edge + Objects

> [!TIP]
> * **Edge, Face, Vertex or Hole edge** - can be at the same object or at two different objects but both should lie on one of the coordinate axes XYZ. Because if there would be for example offset at X and Y, this tool would not be able to recognize to which direction center objects. 
> * **Objects** - The object can be Cylinder, Cone (dril bit), Cube (panel), Pad or LinkGroup with as many objects you want. If you want to move Pad, select Body. If you want to move many Pads, select Body or pack all Part into LinkGroup and select LinkGroup to move. Make sure you do not have Sketch position set. This tool use .Shape.CenterOfMass but if it is not available for object like it is for LinkGroup the center will be calculated from vertices. You can move to the center many objects at once. Hold left CTRL key during selection. 

**Video tutorials:** 
* [How to center objects](https://www.youtube.com/watch?v=X1Pg-CccwIg)
* [Move to center](https://www.youtube.com/watch?v=zKttrKdahg8)

## shelvesEqual

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/shelvesEqual.png">To set equal space between shelves please select: 

1. selection: **X axis edge**
2. selection: **X axis edge**
3. selection: **shelves to set equal space**

> [!NOTE]
> This tool allows you to set equal space for selected shelves. It works only at Z axis. To select more objects hold left CTRL key during selection.

**Video tutorials:** 
* [How to create shelves with equal space](https://www.youtube.com/watch?v=2odJa0baGqw)

# Preview furniture

## fitModel

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/fitModel.png"> This tool allows to fit model to the 3D screen view and also rotate the model view to the base `XY` position (0 key press). This is very useful, used all the time, during furniture designing process. If you rotate the furniture, you can loose the correct orientation of the furniture. So, it strongly recommended to click this tool very often.

<br><br><br>

## makeTransparent

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/makeTransparent.png"> This tool allows to make all parts transparent and back to normal. You can preview all pilot holes, countersinks or any other joints like that, very simply.

<br><br><br><br><br>

## frontsOpenClose

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/frontsOpenClose.png"> This tool allows you to open and close all cabinet fronts simultaneously. This allows you to quickly view the cabinets internal structure without having to search for each front in the object tree and hide or rotate them individually. The fronts rotate with a default rotation increment of 45 degrees. This allows you to select the front opening angle, from a simple tilt to an open inner front that can open beyond 90 degrees. Rotating the fronts around the Z axis avoids the issue of maximum opening angles for different hinge types. However, the opening of the fronts can be customized by editing the attributes for each front. Opening attributes can also be added to each front using this tool. To select more edges or objects hold left CTRL key during selection.

**Possible selection methods:**

* **no selection** - allows you to open all fronts. If the objects name starts with `front` or `Front` this front will be open by default via Edge1 to the left side.
* **edges** - you have to select single edge for each front to add open front attributes to each front. This allows you to change default left open to right open.
* **LinkGroup + edge of simple front inside** - allows you to set rotation attributes to LinkGroup container with handle and simple front inside, to rotate whole LinkGroup container with handle but via edge of simple front inside. In this case you must also set attributes to simple front inside but turn off open of the simple front inside to not duplicate rotation.

## magicView

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicView.png"> This tool allows you to create views and export view to TechDraw. 

**Options:**

* **menu selection** allows you to browse defined views and your own created ones.
  * `custom` this entry is starting point and do nothing, to allows you to create your custom view.
  * `restore` this view is created the first time you run this tool in an active document. This tool will create a spreadsheet named `magicView - restore view` with the object placement data. This will allow you to return to these settings.
  * `explode` moves all objects relative to the center of the entire model by the distance of the previous object.
  * `along X` aligns all objects along the X coordinate axis.
  * `along Y` aligns all objects along the Y coordinate axis.
  * `along Z` aligns all objects along the Z coordinate axis.
  * `along XYZ` aligns all objects along the X and Y and Z coordinate axis.
  * `Assembly` aligns all objects with the center of all XYZ coordinate axes.
  * `magicView` these are views saved using the `save to spreadsheet` button. For each such view, a spreadsheet will also be created with the placement data for that view so that you can revert to the user-defined placement values ​​for the objects.

* **read from spreadsheet** this button allows you to load a view directly from the selected spreadsheet.
* **save to spreadsheet** allows you to save the current view to a spreadsheet, and also to add this view to the end of the list of views.

* **TechDraw options:**
  * `screenshot` exports the current 3D view of the model as an image to TechDraw. Not visible objects will not be exported.
  * `objects` exports the current `Front` view of the model as objects to TechDraw. This option will try to export only selected objects but if there is no selection, click on screen before to be sure nothing is selected in Tree, all objects will be exported. Also in case of this option the visibility of objects is recognized, i.e. objects hidden by the `space` key will not be exported. 
  * `export to TechDraw` creates a TechDraw page with the exported model.

* **Cross:**
  * `Corner cross:` buttons `-`, `+` resize the cross in the right bottom of the screen, it has auto-repeat.
  * `Center cross:` buttons `on`, `off` turn on and off the center cross at the screen.
  * `keep custom cross settings` allows to store the custom cross setting after this tool exit.

**Video tutorials:** 
* [Simple office bookcase](https://www.youtube.com/watch?v=U_oi3POJmSw)
* [Parametric bookcase with Dado joints](https://www.youtube.com/watch?v=kcP1WmKizDg)
* [How to create view and export to TechDraw](https://www.youtube.com/watch?v=yiZfyMRlE-U)

# Project manage

## magicSettings

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicSettings.png"> This tool allows you to save default settings for Woodworking workbench. 

### Settings - page 1

* **Theme:** allows you to choose a color theme for all Woodworking workbench tools. Switching the theme causes an immediate preview on the tool interface. To save a given theme, press the `save settings` button. The `default` means no theme.
* **Main window theme:** allows you to set theme to FreeCAD main window. The main window theme will be set by this [magicSettings](#magicsettings) tool during theme selection but after FreeCAD restart it disappear and also might be overwritten by FreeCAD during some tasks.
* **Wood thickness:** allows you to set the default thickness of the wood you create. This setting is used by tools such as [magicStart](#magicstart), [wires2pad](#wires2pad), [Default panels](#default-panels) and all others.
* **Wood size X (long):** means the longer size for `XY` default panel, see: [Default panels](#default-panels).
* **Wood size Y (short):** means the shorter size for `XY` default panel, see: [Default panels](#default-panels).
* **Wood description:** this is default material description used by [getDimensions](#getdimensions) cut-list tool if you do not have set Material or `.Label2` attribute.
* **Wood color:** allows you to set the default color of the wood you create in RGBA color schema. This setting is used by tools like [magicStart](#magicstart), [wires2pad](#wires2pad), [Default panels](#default-panels) and all others. If you want to revert to the default wood color which is `RGBA = [ 247, 185, 108, 255 ]` leave all fields empty and press the `save settings` button.
* **Tools GUI anchor:** allows anchor selection for all graphical tool interfaces. Currently supported anchors:
  * `FreeCAD Main Window` the graphical interface of the tools will be positioned according to the size and position of the main FreeCAD window.
  * `Desktop screen` the graphical interface of the tools will be positioned according to the size of the available desktop screen.
* **Window stays on top:**
  * `yes` - Tool windows always stay on top of all other applications. I personally use this feature when creating documentation. I have Krusader (Kwrite Edit) and the new tool window open simultaneously, so I can describe all the options without constantly clicking on the new tool window.
  * `no` - Enables the default window behavior, i.e. when you switch to another application, the window disappears.
* **Current selection:** 
  * `yes` - Allows you to bypass the `refresh selection` button. When enabled, you do not have to constantly press the `refresh selection` button to load objects into memory, you can simply select them. However, this is an experimental option and only works for the [magicMove](#magicmove) tool.
  * `no` - The default behavior of the tools is that moving objects requires loading the objects into memory by pressing the `refresh selection` button.

### Settings - page 2

* **Wood weight:** allows you to set default weight unit for wood. The wood weight value should be set in float in user weight calculation method. By default, the weight of `18 mm` chipboard is set to `12.6`. This value is used by [getDimensions](#getdimensions) cut-list tool to create `w - weight` report type.

Example weights unit of commonly used wood in Poland:

| Wood type | Thickness | kg/m^2 |
| :--- | ---: | ---: |
| HDF board | 3 mm | 2.5 |
| Hardwood plywood | 6 mm | 4.5 |
| Spruce wood | 18 mm | 8.64 |
| Mahogany wood | 18 mm | 11.88 |
| Hardwood plywood | 18 mm | 12.32 |
| Laminated chipboard | 18 mm | 12.6 |
| Oak wood | 18 mm | 12.8 |
| Beech wood | 18 mm | 13.14 |

Example weights unit of commonly used wood in lb/board foot:

| Wood type | lb/board foot |
| :--- | ---: |
| Pine | 2.5 |
| Ponderosa Pine | 2.67 |
| Eastern White Pine | 2.7 |
| Spanish Cedar | 2.75 |
| Cherry | 3.3 |
| Oak | 3.6 |
| Red Oak | 4 |
| White Oak | 4.1 |

* **Wood weight calculation:** this option allows you to choose the weight calculation method. Currently, the following calculation methods are supported:
  * **kg per area in m^2** `kg/m^2`: the `Wood weight` will be considered as kilograms and will be multiplied by the area in meters.
  * **kg per volume in m^3** `kg/m^3`: the `Wood weight` will be considered as kilograms and will be multiplied by the volume in meters.
  * **kg per wood piece** `kg/piece`: the `Wood weight` will be considered as kilograms and will be multiplied by the wood piece.
  * **pounds per area in ft^2** `lb/ft^2`: the `Wood weight` will be considered as pounds and will be multiplied by the area in feet.
  * **pounds per cubic foot** `lb/ft^3`: the `Wood weight` will be considered as pounds and will be multiplied by the volume in feet.
  * **pounds per cubic inch** `lb/in^3`: the `Wood weight` will be considered as pounds and will be multiplied by the volume in inches.
  * **pounds per board foot** `lb/boardfoot`: the `Wood weight` will be considered as pounds and will be multiplied by the board foot.
  * **pounds per wood piece** `lb/piece`: the `Wood weight` will be considered as pounds and will be multiplied by the wood piece.

> [!TIP]
> I personally weighed a `342 mm x 860 mm` shelf and found it weighed exactly `4 kg`, which translates to `13.6 kg/m^2`. 
> The shelf is `18 mm` thick and made of laminated chipboard, but it came from an old wardrobe from many years ago, 
> which suggests that chipboards were much heavier in the past. <br><br>
> The weight of wood depends on many factors. In the case of laminated chipboard, information about density is not always 
> provided, and even the true composition is a trade secret. Typically, stores only provide the weight of the entire board 
> sheet with specific dimensions. In the case of real wood, weight can be influenced not only by the density and type of 
> wood, but also by the degree of drying, the number of voids, knots, and other properties. Furthermore, if you find a piece 
> of old chipboard in the basement, or a piece of real wood, you probably will not be able to determine its density and 
> therefore its weight. <br><br>
> **So it is best to weigh and measure a sample of the wood you are working with. <br>
> The larger the sample, the greater the accuracy.**

* **Wood price:** this should be a float representing the price in your country's currency. By default, it's set to the price of one square meter of typical 18 mm white chipboard in Poland.
* **Wood price symbol:** this should be text representing your country's currency. By default, it's `zł`, representing one `złoty (PLN)`, the base currency in Poland. This symbol will appear in the cut-list generated by the [getDimensions](#getdimensions) tool for a report of type `b - budget`.
* **Wood price calculation:** this option allows you to choose the price calculation method. Currently, the following calculation methods are supported:
  * **price per area in m^2** `m^2`: the `Wood price` will be multiplied by the area in meters. This is the method of displaying prices in stores in Poland, so it is the default option.
  * **price per volume in m^3** `m^3`: the `Wood price` will be multiplied by the volume in meters.
  * **price per wood piece** `piece`: the `Wood price` will be multiplied by the wood piece.
  * **price per area in ft^2** `ft^2`: the `Wood price` will be multiplied by the area in feet.
  * **price per cubic foot** `ft^3`: the `Wood price` will be multiplied by the volume in feet.
  * **price per cubic inch** `in^3`: the `Wood price` will be multiplied by the volume in inches.
  * **price per board foot** `boardfoot`: the `Wood price` will be multiplied by the board foot.

**Video tutorials:** 
* [Furniture weight and price](https://www.youtube.com/watch?v=AY0_f-lJtc8)

### Settings - page 3

* **Front inside thickness:** allows you to set default thickness for fronts inside.
* **Front inside offset left:** allows you to set default left gap for fronts inside.
* **Front inside offset right:** allows you to set default right gap for fronts inside.
* **Front inside offset bottom:** allows you to set default bottom gap for fronts inside.
* **Front inside offset top:** allows you to set default top gap for fronts inside.
* **Front outside thickness:** allows you to set default thickness for fronts outside.
* **Front outside overlap left:** allows you to set default left overlap for fronts outside.
* **Front outside overlap right:** allows you to set default right overlap for fronts outside.
* **Front outside overlap bottom:** allows you to set default bottom overlap for fronts outside.
* **Front outside overlap top:** allows you to set default top overlap for fronts outside.
* **Shelf thickness:** allows you to set default thickness for shelves.
* **Shelf sides offset:** this option allows you for global setting of the gap on both sides for the inner shelf, making it easier to insert the shelf. In practice, cutting inner shelves to within a millimeter is quite risky. A 1-millimeter error in cutting can also occur, causing the shelf to fit too tightly, and hammering the shelf into place can cause unnecessary stress on the joints, screws, dowels, and weaken the structure. Not everyone has a table saw or jigsaw capable of cutting 2 mm of chipboard, or sanding such an oversized wooden shelf can be time-consuming. Additionally, shelf supports pins are approximately 5 mm length outside, with 1 mm being the flange. Therefore, maintaining a 1 mm gap on each side allows the shelf to rest on the entire support rather than just the flange, as can be the case with shelves that are too tight.
* **Back inside thickness:** allows you to set default thickness for back inside, usually 18 mm chipboard in Poland.
* **Back outside thickness:** allows you to set default thickness for back outside, usually 3 mm HDF in Poland.

### Settings - page 4

* **Veneer thickness:** allows you to simulate veneer thickness. Constructions with `veneer` description in [magicStart](#magicstart) supports this option and add additional gap for edgeband.
* **Veneer apply:** allows you to simulate veneer and choose method of veneer applying. Constructions with `veneer` description in [magicStart](#magicstart) supports this option and add additional gap for edgeband.
  * `everywhere` for example you can buy chipboards with `2 mm` PCV veneer. So the veneer will be applied everywhere in this case.
  * `visible` it is more custom way, related mostly only to visible edges.
* **Veneer color:** allows you to set the default RGBA color of the veneer. If you want to revert to the default color which is `white: RGBA = [ 255, 255, 255, 255 ]` leave all fields empty and press the `save settings` button.
* **Edgeband price:** this should be a float representing the price in your country's currency. By default, it's set to the price of one meter edgebanding of typical 18 mm white chipboard in Poland.
* **Edgeband price symbol:** this should be text representing your country's currency. By default, it's `zł`, representing one `złoty (PLN)`, the base currency in Poland. This symbol will appear in the cut-list generated by the [getDimensions](#getdimensions) tool for a report of type `b - budget` and other report type with `price column` option.
* **Edgeband price calculation:** this option allows you to choose the price calculation method. Currently, the following calculation methods are supported:
  * `price per mm - millimeter`,
  * `price per cm - centimeter`,
  * `price per m - meter`,
  * `price per ft - foot`,
  * `price per in - inch`.

### Settings - page 5

* **Prefer magicSettings defaults:**
  * `yes` to open [magicDowels](#magicdowels) and [magicDriller](#magicdriller) with defaults from this magicSettings tool.
  * `no` open with tools predefined defaults. This is default option.
* **Sides:** if the dowels or drill bits should be from both sides or only from one side, possible values:
  * `0` - use both sides
  * `1` - left or right side only
  * `2` - left or right side only
* **Items per side:** means how many dowels or drill bits per side should be created. This should be integer value.
* **Offset from corner:** means offsets from sides, left or right.
* **Offset between items:** space between dowels or drill bits.
* **Offset from edge:** means space to the front where is the currently selected edge. This value should be calculated from board thickness to get drill bit or dowel in the center but here you can define it permanently for all boards. This might be helpful if you plan to create holes for shelves with custom offset.

### Settings - page 6

* **Dowel diameter:** diameter for dowels in [magicDowels](#magicdowels) tool.
* **Dowel size:** the length for the dowels in [magicDowels](#magicdowels) tool.
* **Dowel sink:** initial size inside board for the dowels in [magicDowels](#magicdowels) tool.
* **Hole diameter:** diameter for drill bits in [magicDriller](#magicdriller) tool.
* **Hole countersink diameter:** face hole diameter for countersinks drill bits in [magicDriller](#magicdriller) tool.
* **Hole size:** hole depth in [magicDriller](#magicdriller) tool.
* **Hole spike:** how the spike for hole should be:
  * `Angled` default spike.
  * `Flat` there should be no spike inside the hole at the end. But this works only with normal drill bit holes.
* **Pocket diameter:** diameter for pocket hole drill bits in [magicDriller](#magicdriller) tool.
* **Pocket countersink:** face hole diameter for pocket hole drill bits in [magicDriller](#magicdriller) tool.
* **Pocket size:** hole depth for pocket hole drill bits in [magicDriller](#magicdriller) tool.
* **Pocket offset from edge:** means space to the front where is the currently selected edge. This value should be much bigger in case of pocket hole drill bits in [magicDriller](#magicdriller) tool.
* **Pocket rotation:** pocket hole drill bit angle to the face in [magicDriller](#magicdriller) tool. You can also try value with minus.
* **Pocket sink:** this is space above the face for the pocket hole drill bit spike in [magicDriller](#magicdriller) tool. You can also try value with minus.

**save settings:** button saves the current settings in FreeCAD configuration files, i.e. `User parameter:BaseApp/Preferences/Woodworking`. This data can be checked, fixed or removed using the parameter editor in FreeCAD, i.e. `Tools -> Edit parameters... -> Preferences -> Woodworking`.

> [!TIP]
> If you want to reset settings to defaults, please remove parameters in <br> 
> `User parameter:BaseApp/Preferences/Woodworking` via FreeCAD parameter editor <br> 
> `Tools -> Edit parameters... -> Preferences -> Woodworking`.

**Video tutorials:** 
* [How to use magicSettings tool](https://www.youtube.com/watch?v=kwcO2bRcCrY)

## selected2LinkGroup

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/selected2LinkGroup.png"> This tool call FreeCAD LinkGroup command and set color for new LinkGroup objects from first selected object. To select more objects hold left CTRL key during selection.

<br><br><br><br><br><br>

## selected2Link

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/selected2Link.png"> This tool call FreeCAD simple Link command and set color for new Link objects from first selected object. To select more objects hold left CTRL key during selection.

<br><br><br><br><br><br>

## selected2Group

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/selected2Group.png"> Normally, the FreeCAD Group command not recognize selection and always creates empty folder. This tool improves this command a little bit, creates new Group and move all selected objects to the new Group folder. The Group folder label is from first selected element. To select more objects hold left CTRL key during selection at Tree or 3D view.

<br><br><br><br><br>

## selected2Assembly

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/selected2Assembly.png">To convert a model to an Assembly object, you must first select `FreeCAD Part::Box` objects to convert. This tool allows you to convert a simple model based on simple panels, i.e. `FreeCAD Part::Box` objects, to an Assembly model. Manually, such conversion could be done by converting `Part::Box` objects to `PartDesign::Pad` objects using the [panel2pad](#panel2pad) tool and then extracting `PartDesign::Body` objects using [selected2Outside](#selected2outside) to keep global position and moving them to the `Assembly::AssemblyObject` object. In this tool, these two tools are combined for ease and speed of conversion. However, if you have a problem with converting the model, you can still do such conversion manually.

**Video tutorials:** 
* [FreeCAD 1.1 direct assembly](https://www.youtube.com/watch?v=u3Yh2WvdUIk)

<br><br><br>

## selected2Outside

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/selected2Outside.png"> This tool allows you to get out the selected objects from containers. Normally, if you get out object from the container manually, the object will change place and rotation. This tool allows you to move the objects and keep the same position and rotation. This feature might be very useful if automatic movement to container is not what you want. For example you want single element to no longer be mirrored or further processed with other objects inside the container. To select more objects hold left CTRL key during selection.

**Video tutorials:** 
* [Boolean cut with containers](https://www.youtube.com/watch?v=OVwazL8MQwI)
* [FreeCAD 1.1 direct assembly](https://www.youtube.com/watch?v=u3Yh2WvdUIk)

<br><br>

## eyeRa

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/eyeRa.png"> Please create active document and at least one object inside container to expand tree for container and show its content. This tool allows you to expand all containers in tree view to see quickly full tree structure of your model. Personally I use auto-expand tree after object selection in 3D view option but to exapand full structure you have to select all abject at 3D model or manually expand each container what is time-consuming. This simple tool allows you to make it with single click and together with [eyeHorus](#eyehorus) tool allows you to quickly view and hide full structure. 

> [!NOTE] 
> I did not have any ideas for an icon related to carpentry, and quite by chance I came up with the idea that the Eye of Ra 
> and Horus would be cool in this case. Personally, I love stories about ancient Egyptian gods and the icon represents the 
> eye of the god Ra, who saw everything, so it perfectly fits to the expanding the entire object tree structure and 
> displaying all objects.

<br><br>

## eyeHorus

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/eyeHorus.png"> Please create active document and at least one object inside container to close tree for container. This tool allows you to close all containers in tree view to have cleaner tree structure. Personally I use auto-expand tree after object selection in 3D view option but after modeling and selecting many objects the objects tree look less readable if you have many deeply nested containers. So this simple tool allows you to make it cleaner with single click and together with [eyeRa](#eyera) tool allows you to quickly view and hide full structure. 

> [!NOTE] 
> I did not have any ideas for an icon related to carpentry, and quite by chance I came up with the idea 
> that the Eye of Ra and Horus would be cool in this case. Personally, I love stories about ancient Egyptian gods 
> and the icon represents the eye of the god Horus, whose power was limited. So, in a sense, it is the 
> opposite of the Eye of Ra. 

<br><br>

## How to use containers - short tutorial

* `Body` is container for single Pad object. If you want to move Pad or any other PartDesign object, it is better to move it via Body container not directly via AttachmentOffset. If you move PartDesign object via AttachmentOffset, all the transformations, for example Hole, need to be recalculated. So, this is very slow and also if you drill holes and move object via AttachmentOffset the holes will disappear. So, move PartDesign objects via Body container.
* `Part` is good container for many Bodies, more complicated PartDesign objects. For example if you move Pad directly to Body this will be merged with the current Pad in the Body. So, it will be single object. If you want to keep Pad separated, you can create single Body container for each Pad and keep all Bodies in Part. I rather not recommend to mix Cube with PartDesign object inside Part container. Part should rather be used only for PartDesign objects.
* `LinkGroup` is high level, real container. You can move there many Part containers and also Cube objects. Also you can nesting LinkGroup containers. If you want to move many objects, bigger structures, rotate them, this is good container to do it.
* `Link` is not container but it is mentioned here, because you should rather avoid linking objects directly. You should rather link LinkGroup. This approach allows you to change LinkGroup content and update the Link in real-time. If you link directly object, and the base Cube object will be replaced with Pad, the link will be broken, because the base object no longer exists. This not happen if you link the LinkGroup with Cube inside. You can replace Cube with Pad inside LinkGroup container and the link will be still correct and also the link will be updated in real-time.
* `Group` is normal FreeCAD folder. You can't move it or rotate but it is good container to keep LinkGroup structure. 

> [!IMPORTANT]
> If you want to use `Part :: Boolean :: Cut` inside `LinkGroup` container, first you have to get out of the container all the elements using [selected2Outside](#selected2outside). See video: [Boolean cut with containers](https://www.youtube.com/watch?v=OVwazL8MQwI)

# Decoration

## magicColors

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicColors.png"> This tool allows you to change colors in real time. Color changes can be made for multiple objects, multiple faces, or different objects and faces at the same time.

**Options:**

* **refresh selection:** Loads the objects for which colors are to be changed.
* **Target:** This is the target attribute of the color structure.
  * `DiffuseColor` normal color.
  * `AmbientColor` available since FreeCAD 1.0 new color schema.
  * `EmissiveColor` available since FreeCAD 1.0 new color schema.
  * `SpecularColor` available since FreeCAD 1.0 new color schema.
  * `Shininess` available since FreeCAD 1.0 new color schema.
  * `Transparency` transparency.
  * `let's slide all` sliders to set all target attributes at once.
* **Sample:** These are defined color schemes that can be quickly set.
  * `custom` this is the startup setting mode and does not set any color.
  * `Woodworking - default` this is the default color set in the MagicPanels library for all new objects you create.
  * `reset` this is the FreeCAD default color for objects.
  * `Wood & other` these are sample wood colors chosen by me.
  * `from spreadsheet` allows you to set face colors from a spreadsheet for all objects.

**Setting modes:**

* **simple** color settings can be made using the `-` and `+` buttons or by manually entering values ​​into the text fields. In the case of manually entering values ​​into the text fields, they must be confirmed with the `set custom color` button. In the case of the `-` and `+` buttons, the color value will be changed in real time for all loaded objects.
  * `Red:` changes the proportions of the red color intensity.
  * `Green:` changes the proportions of the green color intensity.
  * `Blue:` changes the proportions of the blue color intensity.
  * `Alpha:` changes the proportions of the red, green and blue color intensity. However, in the case of FreeCAD it works by making a face or object transparent.
  * `RGBA step:` sets the value that will be reduced or added to the current color value when the `-` or `+` button is pressed for red, green, blue and alpha channel text fields.
  * `set custom color` button sets the color based on manually entered color values ​​into text fields.
  
* **extended** allows you to select a color in a way that is typical for graphics programs. When the `Color property` is set to `Shininess` or `Transparency` the vertical slider, or `Val:` field, can be used to change this color attribute. When the `Color property` is of type RGB it works in a standard way affecting the RGB color.

> [!IMPORTANT]
> * The "Sample" color will be set only for currently selected target attribute, i.e. "Target".
> * In FreeCAD 0.21.2 only DiffuseColor and Transparency attributes are available. Transparency works only for objects but you can use alpha channel to make faces transparent.
> * In FreeCAD 1.1 only DiffuseColor and Transparency attributes works for faces and objects, other attributes works only for objects, looks like it is not implemented by FreeCAD yet but this tool is ready for it and set it correctly.
> * In FreeCAD 1.1 alpha channel not works for faces and objects, only the Transparency works for faces and objects, looks like it is not implemented by FreeCAD yet but this tool is ready for it and set it correctly.

**Video tutorials:** 
* [How to use magicColors](https://www.youtube.com/watch?v=7Ly2Ot-kwSM)

## setTextures

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/setTextures.png"> This tool allows to store textures information and load textures. Also solves problem with huge project file size because this tool allows to store only link to texture not texture.

> [!TIP]
> * To load texture from saved attributes: press `load saved` button.
> * To load texture from URL: write URL and press `load from URL` button.
> * To load texture from local disk: press `load from local` button and choose texture, 
> you can browse the folder later via `< local file` and `local file >` buttons.
> * To preview written manually attributes for fit, repeat, rotation: press `preview custom attributes`, 
> however to keep it forever you have to press `save texture` button.
> * To edit texture in real-time: load texture somehow, choose `Live preview target:` and use `-` and `+` buttons, 
> however to keep current texture look forever you have to press `save texture` button.

**Textures can be stored at:**
* `.ShapeMaterial.AppearanceProperties["TextureImage"]` material added to the object, new material approach used by Woods workbench.
* `.Material.Material["TexturePath"]` old material way with setting URL to the texture in material card.
* `.Texture` attribute with URL to the texture.
* `.Label2` attribute, object description, with URL to the texture.
* `.Texture_URL` attribute with URL online or from HDD to the texture added by this [setTextures](#settextures) tool.

> [!TIP]
> Personally, I prefer to add online links to textures. This way, the file size does not increase and there 
> is no need to install additional repositories. However, you need to make sure the server supports external linking. <br>
> Also if you want to use texture from material make sure the `.Texture_URL` attribute for object not exists or is empty, 
> because the `.Texture_URL` is preferred and will be loaded first.

**Setting objects:**
* **chooser:** allows you to choose selection mode. Possible options:
  * `selected objects` allows you to load only selected objects to this tool's memory.
  * `all objects` allows you to set texture for all objects in the `ActiveDocument`. This can be very useful if you want to see if any object has already added texture or just add texture for whole wardrobe elements at once. In this selection mode the button `refresh selection` will be disabled.
* **refresh selection** button allows you to load selected objects into the tool's memory and then perform various texture-related operations on these objects without selecting them.

> [!TIP]
> * You can also select the objects first and then open this tool, then the selected objects will be loaded automatically.
> * This tool supports the `Current selection` setting from [magicSettings](#magicsettings) tool. 
> If you set the `Current selection` option to `Yes` in [magicSettings](#magicsettings) tool, then all operations 
> will be performed on the currently selected objects and the `chooser` and button `refresh selection` will be disabled. 
> If you use this mode try to select face, not whole object, to see texture in real-time.

**Preview texture:**
* **set white color** sets the white color for the object to make the texture look better, shows the real texture color without additional mask.
* **load saved:** loads textures for all objects or for selected objects that have texture information saved. If you have added material to the object via `Right Mouse Click -> Material...` the material texture will be loaded even if the object has no texture attributes, so you can use `Live preview target:` options and save the attributes later via `save texture` button.
* **load from URL** button allows you to load written manually URL to the texture.
* **load from local** button allows you to open local file dialog to choose texture from local disk and automatically preview the texture.
* **< local file** button allows you to load previous texture from the folder you have already loaded texture from disk via button `load from local`.
* **local file >** button allows you to load next texture from the folder you have already loaded texture from disk via button `load from local`.
* **Live preview target:** allows you to choose live preview target and adjust the texture in real-time. For example if you set `rotation Z axis` the `-` and `+` buttons will be rotating the texture around `Z` axis with the `Step` measured with degrees. If you decide to save the current visible texture state, make sure to press `save texture` button and verify if the object's attributes has been stored. To use this feature you need to load texture first.

> [!IMPORTANT]
> Make sure you have the following option disabled:
> `Edit -> Preferences -> Display -> 3D View -> Use OpenGL VBO (Vertex Buffer Object)`
> Especially if you are using the `FreeCAD Dark` or `FreeCAD Light` theme, because they turn on this option and then you may not see the textures.

**Setting texture attributes:**
  
* **First selection:** Allows for better texture matching to the object. Available options:
  * `biggest surface` adjust texture to the biggest surface, but not to edges of the board.
  * `fit to Cube` adjust texture to edges of the board.
  * `fit to Cylinder` adjust texture to cylinder shapes, like dowels or drill bits.
  * `fit to Sphere` adjust texture to sphere shapes.
  * `auto fit` recognize the object type and try to adjust texture.
  * `glass mirror effect` mirror effect.
* **repeat X:** allows you to repeat texture along X axis, to create pattern, `1.0` means visible once but not repeat.
* **repeat Y:** allows you to repeat texture along Y axis, to create pattern, `1.0` means visible once but not repeat.
* **repeat Z:** allows you to repeat texture along Y axis, to create pattern, `1.0` means visible once but not repeat.
* **Rotation X axis:** allows you to store texture rotation coordinate axis value around X coordinate axis. The `1.0` value means rotate around X axis and the `0.0` means not rotate around X axis.
* **Rotation Y axis:** allows you to store texture rotation coordinate axis value around Y coordinate axis. The `1.0` value means rotate around Y axis and the `0.0` means not rotate around Y axis.
* **Rotation Z axis:** allows you to store texture rotation coordinate axis value around Z coordinate axis. The `1.0` value means rotate around Z axis and the `0.0` means not rotate around Z axis.
* **Rotation angle (degrees):** allows you to store texture rotation angle in degrees, more human-readable form than radians.
* **preview custom attributes** button allows you to preview written manually attributes for fit, repeat and rotation.

**Save texture attributes:**
* **save texture** button allows you store current texture attributes and save current texture look forever.

**Video tutorials:** 
* [Furniture from textures](https://www.youtube.com/watch?v=kiD0VqpiTEk)

## makeBeautiful

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/makeBeautiful.png"> This tool change all objects look, make edges and vertices smaller to look better at screenshots. If you click it again all objects will be changed to default values.

<br><br><br><br>

# Cut list, Measure, Dimensions, Bill Of Materials

## getDimensions

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/getDimensions.png"> This tool allows you to create spreadsheet with dimensions to cut (cut-list) or Bill Of Materials (BOM). It has been designed for my private woodworking projects (hobby), especially for chipboards `18 mm` of thickness (they are the most common in Poland). This macro creates a spreadsheet named `toCut` and also a TechDraw page `toPrint` with all needed furniture parts to cut for woodworking project. Also you can export long reports via [sheet2export](#sheet2export).

> [!IMPORTANT]
> The report works automatically mainly for `Part::Box` objects. It also recognizes many other objects and also irregular shapes in Sketch. However, if you are using Sketch-based objects you should rather have constraints with names: `SizeX` and `SizeY` in the Sketch. If you can't add a `SizeX` or `SizeY` constraint name in the Sketch, select the `Reference` checkbox during constraint creation and add exact name. The 3rd dimension will be get from `Pad.Length` attribute. 

### Report type

#### Search path

* **all objects:** default object search path. This path should also be used for the built-in Assembly workbench. This option allows you to search all objects in active document.
* **selected objects:** allows you to search only for selected objects in active document. This might be useful if you have many furniture version in the same active document but you are not able to get it to work the [Visibility](#visibility) feature.
* **Assembly4 structure:** object search path dedicated only to [Assembly4](https://codeberg.org/Zolko/Assembly4) workbench by [Zolko](https://forum.freecad.org/viewtopic.php?t=86110).

#### Main report

* **q - for cut service:** the default report type allows you to quickly create a cutting list needed to order boards from a DIY store in Poland. Objects are grouped by the same dimensions, making cutting easier.
* **n - for verification:** this is a list of all items, grouped by item name (`object.Label`). This report type is necessary to verify that all boards were received from cutting service with correct dimensions.
* **g - wood type:** this type of report groups all items based on their location in folders and containers. This allows you to place all items of a given color, type, or material in a single folder, and this will be reflected in the report. This makes it easier to order boards of different types or thicknesses but with the same dimensions. This type of report can also be used to create groups with edge veneer, left, right, or without veneer.
* **m - material description:** this type of report is the same as `g - wood type` but the group name is created from material description as follows:
  * If you have set Material for object, I mean the `.ShapeMaterial.Name` is not `Default` the `.ShapeMaterial.Name` attribute will be used. In this case if you have `.Label2` attribute the `.ShapeMaterial.Name` will be used.
  * If you not have set Material but you have `.Label2` the `.Label2` attribute will be used.
  * If you not have set Material and also not have set `.Label2` attribute the global variable `MagicPanels.gWoodDescription` will be used. The global variable `MagicPanels.gWoodDescription` can be set via [magicSettings](#magicsettings) tool.
* **e - veneer:** this type of report allows you to precisely describe each face of the object, based on the edge length. Thanks to this you can describe which edge lengths should be covered with veneer. To determine the edge color with veneer, you must set the color of the entire furniture as a color reference. Also you must set the edge symbol, which will appear on the report.
* **d - drilling:** this report type is an extended version of the `e - report` type, but also displays named constraints from the `PartDesign::Hole` object sketch. Additionally, the header comes from the Body object. This allows you to describe all edge distances, diameters, and depths for holes.
* **c - named constraints:** this report type shows the dimensions for all named constraints inside Sketch objects and the `Length` size from `PartDesign` objects.
* **p - all constraints:** this report type shows the dimensions for all constraints on Sketch objects, whether named or unnamed, and the `Length` size from `PartDesign` objects.
* **w - weight:** this report type calculates the weight based on the wood weight unit and calculation method. First, it checks whether the object has a `Woodworking_Weight`attribute of the `App::PropertyFloat` or `App::PropertyString` type, or any other that can be converted to float. If it does, that unit is used to calculate the wood weight. If it doesn't, the wood weight is retrieved from the global variable `MagicPanels.gWoodWeight`, which can be changed using the [magicSettings](#magicsettings) tool and is saved in the user preferences as `wWoodWeight` in the form of a float. The final weight value is calculated according to the calculation method from the `MagicPanels.gWoodWeightCalculation` global variable, which can be changed using the [magicSettings](#magicsettings) tool and is saved in the user preferences as `wWoodWeightCalculation` in the form of a string method key. If the object has a `Woodworking_Weight` weight attribute set, the final weight will be calculated according to the selected weight calculation method. Additionally, the decimal value is rounded according to the precision set for the area.
* **b - budget:** this type of report allows you to estimate the costs associated with purchasing wood or furniture boards. First, it checks whether the object has a `Woodworking_Price` attribute of the `App::PropertyFloat` or `App::PropertyString` type, or any other that can be converted to float. If it does, that unit is used to calculate the wood price. If it doesn't, the wood price is retrieved from the `MagicPanels.gWoodPrice` global variable, which can be changed using the [magicSettings](#magicsettings) tool and is saved in the user preferences as `wWoodPrice` in the form of a float. The final price of a given furniture elements is reported in user currency symbol from `MagicPanels.gWoodPriceSymbol` global variable, which can be changed using the [magicSettings](#magicsettings) tool and is saved in the user preferences as `wWoodPriceSymbol` in the form of a string. The final price value is calculated according to the calculation method from the `MagicPanels.gWoodPriceCalculation` global variable, which can be changed using the [magicSettings](#magicsettings) tool and is saved in the user preferences as `wWoodPriceCalculation` in the form of a string method key. If the object has a `Woodworking_Price` price attribute set, the final price will be calculated according to the selected price calculation method. Additionally, the decimal value is rounded according to the precision set for the area. This approach allows for determining the price of furniture and individual components depending on the currency and wood pricing method. In Poland, chipboard prices are set by cut services per square meter, with additional fees charged for the number of cuts. However, currencies and price calculation methods vary around the world, so this approach seems to cover most wood pricing methods.
* **a - approximation:** this report is some kind of approximation of needed material. It uses different approach to dimensions, because the dimensions are not get here from objects, they are calculated from raw vertices. You have to be careful because the dimensions are occupied space in 3D by the object and you can see the difference for all rotated elements. This type of report can be directly imported at [cutlistoptimizer.com](https://www.cutlistoptimizer.com/) website tool.

> [!TIP]
> Personally, I create two cutting lists. First is `q - for cut service` for the person in the cutting chipboard service. 
> The second one is `n - for verification` so I can verify that all the elements I received from the store and all 
> elements had the correct dimensions, so I can write "OK" on it. <br>
> I usually create furniture for myself from `18 mm white chipboard`, but if, for example, I need to order 
> plywood shelves or boards in a different color, I create `g - wood type` or `m - material description` 
> for the person in the cutting service, where the appropriate board types and colors are grouped.

#### Additional reports

* **thickness summary:** turns off or on the thickenss summary.
* **weight column:** allows you to add additional column with weight to `q - for cut service`, `g - wood type`, `m - material description` report types. In this case the TechDraw page `toPrint` will be horizontal (`Landscape`) to fit to the `A4` page width. Make sure the report is not too long. Use [sheet2export](#sheet2export) tool for longer reports.
* **price column:** allows you to add additional column with price to `q - for cut service`, `g - wood type`, `m - material description` report types. In this case the TechDraw page `toPrint` will be horizontal (`Landscape`) to fit to the `A4` page width. Make sure the report is not too long. Use [sheet2export](#sheet2export) tool for longer reports.
* **edgeband info:** turns off or on information about edge size and needed veneer.
* **custom measurements:** shows custom measurements created via [magicMeasure](#magicmeasure) tool. If you want to create custom measurements you need to have `App::MeasureDistance` or `Measure::MeasureDistanceDetached` object type. To have this custom measurements listed in cut-list generated by [getDimensions](#getdimensions) tool, you need to set object `Label2` attribute. The syntax is "Object name, text you want to have in cut-list", for example "panelXZ, Offset from corner". To show `Label2` attrtibute for object you have to right click on object `Data` window and select `Show hidden`.
* **max and min size:** it also displays information about the longest and shortest edges. Of course the thickness is not calculated here. This allows you to estimate the maximum space you will need in your car trunk to transport all the boards, as well as whether you will exceed the minimum cutting size. In Poland, chipboard cutting services typically require a minimum cutting size of approximately 100 mm, so for safety reasons, they usually do not cut 50 mm pieces.
* **dowels and screws:** shows dowels created via [magicDowels](#magicdowels) tool and also Woodworking workbench screw replaced via [panel2link](#panel2link) or [panel2clone](#panel2clone) tools. If you want to have custom dowels or screws visible at the report you need to have `Part::Cylinder` object inside with measurements.
* **construction profiles:** shows construction profiles created via [panel2profile](#panel2profile) or [panel2angle](#panel2angle) tools. If you want to have custom profiles you need to have `PartDesign::Thickness` object type. This report type supports also [Dodo workbench construction profiles](https://github.com/oddtopus/dodo).
* **decorations:** shows dimensions for objects considered as decoration, i.e. `PartDesign::Fillet`, `PartDesign::Chamfer`, `Part::Sphere`, `Part::Cone`, `Part::Torus` object types.
* **veneer simulation:** create additional report for veneer added via [addVeneer](#addveneer) tool.
* **grain direction:** shows grain direction for object created via [grainH](#grainh), [grainV](#grainv) or [grainX](#grainx) tools.

### Units

* **mm:** all dimensions will be recalculated to `millimeters` or `square millimeters` in case of area, independent of user units settings.
* **cm:** all dimensions will be recalculated to `centimeters` or `square centimeters` in case of area, independent of user units settings.
* **m:** all dimensions will be recalculated to `meters` or `square meters` in case of area, independent of user units settings.
* **inch:** all dimensions will be recalculated to `inches` or `square inches` in case of area, independent of user units settings.
* **fractions:** this is notation `X' Y n/d"`, the fractional part is reduced by the system so you have to set `Building US`. The area will be calculated by the system `sqft` (square foot).
* **fractions minus:** this is notation `X' Y-n/d"`, the fractional part is reduced by the system so you have to set `Building US`. The area will be calculated by the system `sqft` (square foot).
* **fractions equal:** this is notation `X' Y n/d"`, the fractional part is not reduced and is independent of user units settings, can be also `Standard (mm,...)`. The area will be set to `inch2` (square inch).
* **system:** all dimensions will be presented in the user's unit system preferences.

> [!NOTE]
> * The `X'` represents a whole number of feet, the `Y` represents a whole number of inches and the `n/d"`
> represents a fraction of an inch, where `n` is the numerator and `d` is the denominator. 
> The denominator is taken from the user settings from `Edit->Preferences->General->Building US->Minimal fractional inch`.
> * In the case of the `system` option, the spreadsheet has its own shortening unit format, which causes `mm2` to be saved as `cm2`. 
> To force the area to be shown in square meters, set `m` square meter (m2) for `Units for area`.
> * The default units for "Building US" is "fractions", in Poland keep correct metrics, and "system" for others.

### Precision

By default the values at report are rounded to have more clear listing. Rounding values also allows to avoid values at report like e.g. `499.9999999999` instead of `500 mm`. Generally during working with wood material it is rather hard to achieve precision better than `+/-1 mm`. Even professional cutting services are not able to keep always precision `+/-0 mm`, so precision like `+/- 0.1 mm` is rather not possible in real life. So by default precision for `mm` units is `0`, it means the value `500.65 mm` will be rounded to `501 mm` at the report.

### Visibility

* **All objects:**
  * **off:** allows hidden content to be calculated and listed at the report. FreeCAD has many complicated objects with hidden content. For PartDesign objects usually, only the objects of last operation is visible but the first Pad with dimensions is hidden. Similar thing is for Cut objects where the content with dimensions is hidden but the Cut object has no information about dimensions of its parts.
  * **on:** hidden objects will not be listed at the report.
  * **edge:** hidden objects will be listed but not added to the edge size.
  * **parent:** not list object with hidden parent object.
  * **screw:** dedicated mostly to hide the base realistic looking screw.
  * **inherit:** not list elements inside highest hidden container. This is useful to hide whole cabinet inside LinkGroup container. For example you have wardrobe with 5 modules, and each cabinet module inside separate LinkGroup container and you want generate cut-list only for single visible cabinet module and to create it one by one in real-life.
  * **special BOM attribute:** if object has `BOM` attribute set to `False` (`App::PropertyBool`) it will be skipped during parsing and not listed at the report. This special attribute is used by [magicCut](#magiccut) and [magicKnife](#magicknife) tools to skip copies at the report. For more details see video tutorial: [Skip copies in cut-list](https://www.youtube.com/watch?v=rFEDLaD8lxM).

> [!TIP]
> If you are not able to get it to working, for example you have many deep nesting containers and you do not want to parse 
> all objects, please try `selected` option in [Report type](#report-type).

* **Part :: Cut content:**
  * **all:** shows Base and Tool
  * **base:** shows Base only
  * **tool:** shows Tool only

### Additional settings

* **Report Language:**
  * **English:** translation to English.
  * **Polish:** translation to Polish.
  * **system:** translation to from system translation files and user language settings.

* **Report quality:** 
  * **eco:** the colors are removed to keep low ink mode.
  * **hq:** with colors.

### Edgeband

* **set:** first, select any furniture face that will be the reference color for the entire furniture, then press the "set" button to select load the color. If any edge of the board will be in a different color than the loaded furniture reference color, it will be calculated as the edge that should be covered with veneer.
* **Edgeband code:** is only text that will be displayed at the report. It can represent any veneer tape color at shop, even reference code.

### Supported objects

* `Part :: Cube`
* `PartDesign :: Pad`
* `Part :: Extrusion`
* `Assembly :: AssemblyObject`, `Assembly :: AssemblyLink` - tested with Assembly4 and FreeCAD 1.0
* custom objects with `Width`, `Height` and `Length` attribute, for example [Stick Frame Workbench objects](https://gitlab.com/mathcodeprint/stickframe).

### Supported transformations

* `Part :: Mirroring`,
* `Draft :: Array`,
* `Draft :: Array Polar`,
* `Draft :: PathArray`,
* `Draft :: Clone`,
* `PartDesign :: Pocket`,
* `PartDesign :: Hole`,
* `PartDesign :: LinearPattern`,
* `PartDesign :: Mirrored`,
* `PartDesign :: MultiTransform`,
* `App :: Link`,
* `App :: LinkGroup`,
* `Part :: Compound`,
* `Part :: Cut`,
* and probably many more...

### Video tutorials and documentation

* **YouTube playlist:** [Cut-list, BOM, dimensions](https://www.youtube.com/playlist?list=PLSKOS_LK45BCnwvCGt4klfF6uVAxfQQTy)
* **Old documentation:** [getDimensions macro](https://github.com/dprojects/getDimensions/tree/master/Docs)

## sheet2export

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sheet2export.png"> This tool allows to export spreadsheets to more flexible file formats. Useful if you want to print multi-page report. 

**Options:**

* **Export type:** 
  * `a` exports all spreadsheets from active document to the selected file type.
  * `s` exports only selected spreadsheets to the selected file type.

* **Export file path:** allows you to set the directory to which the exported file will be saved. By default, in Linux, this is the `./` directory, i.e. the directory from which the FreeCAD AppImage file was launched.

* **Export file type:** 
  * `csv` - Comma-separated values ( .csv file )
  * `html` - HyperText Markup Language ( .html file )
  * `json` - JavaScript Object Notation ( .json file )
  * `md` - MarkDown ( .md file )

* **Additional options:**
  * `Empty cell content:` allows you to set any value for empty cells in a spreadsheet.
  * `Set CSV separator:` allows you to set any separator for cells in a CSV file.
  * `CSS rules` allows you to set your own HTML file decoration styles.

**Video tutorials:** 
* [How to create cut-list](https://www.youtube.com/watch?v=_n7SUYSGHls)

## showMeasurements

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showMeasurements.png"> This tool allows you to quickly create or remove measurements for all simple objects. The objects that will be dimensioned are `Part :: Box` and `PartDesign :: Pad`. For each such object, the list of edges will be searched and all linear edges of various dimensions will be described with a measurement. The text size depends on the distance, so small dimensions like `18 mm` thick may not be visible from a distance. This tool is a typical **quick shot** that allows you to quickly enable or disable measurements for objects. Because there are so many dimensions, it should be used primarily with [magicView](#magicview) and primarily for `X`, `Y`, `Z`, or `explode` views. For each such measurement object there is special attribute named `Remove` set by default to `True`. So if you click the icon again such measurement will be removed. If you want to keep such measurement, just set this `Remove` attribute to `False`. Also the measurements created via this tool are parametric. So you can change views in [magicView](#magicview) and the measurements will follow the changes.

**Video tutorials:** 
* [New measurement features](https://www.youtube.com/watch?v=9F_fBQYuxvU)

## magicMeasure

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicMeasure.png"> 
This tool allows you to quickly measure objects. All measurements are recognized by the getDimensions tool and can be listed in the cut-list report with a reference to the object. This tool works in two modes:

> [!IMPORTANT]
> To have this custom measurements listed in cut-list generated by [getDimensions](#getdimensions) tool, you need to set 
> object `Label2` attribute. The syntax is "Object name, text you want to have in cut-list", for example "panelXZ, Offset from corner".
> To show `Label2` attrtibute for object you have to right click on object `Data` window and select `Show hidden`.

* **Preselection mode** - this mode allows you to quickly measure objects by just moving the mouse cursor over the object. In this mode you can measure: edge, surface (all edges), hole diameter and hole depth. If you left-click, the current visible measurements will be saved.
    
* **Selection mode** - this mode allows you to measure objects by selecting vertices, surfaces or holes. In this mode you have the following choices:
  * select `Edge`: to measure edge size.
  * select `Vertex` and next `Face`: to measure distance between vertex and face, for example shelf space.
  * select `Vertex` and next `Edge`: to measure distance between vertex and edge, for example space between front and side of the furniture. In this case, two measurements will be created in directions different from the selected edge. For example, if the edge is aligned with the Z coordinate axis, measurements will be created for the X and Y coordinate axes. For example, if the first selected vertex lies on the Y coordinate axis along with the second selected edge, this zero distance will be ignored and only a measurement will be created in the X coordinate axis.
  * select `Vertex` and next `Hole`: to measure distance between vertex and hole center point, for example drill point.
  * select `Vertex` and next `Vertex`: to measure distance between two vertices, for any purposes.
  * select `Hole` and next `Hole`: to measure distance between holes center points, for example to verify 32 mm system.
  * select `Hole` and next `Edge`: to measure distance between hole and edge, for example to verify pilot hole offset. In this case, two measurements will be created in directions different from the selected edge. For example, if the edge is aligned with the Z coordinate axis, measurements will be created for the X and Y coordinate axes. For example, if the first selected hole lies on the Y coordinate axis along with the second selected edge, this zero distance will be ignored and only a measurement will be created in the X coordinate axis.
  * select `Hole` and next `Face`: to measure distance between hole and face, for example to measure angle mounting point.
  * select `Hole` and next `Vertex`: to measure distance between hole and vertex.

> [!NOTE]
> This tool automatically recognizes the FreeCAD `Edit->Preferences->Display->Colors->Enable preselection highlighting` settings and if you set this option, it will start in `Preselection` mode, otherwise in `Selection` mode, so you don't have to switch it at the beginning.

* **Drawing type:** Allows you to choose drawing measurements style:
  * `PartDesign - system` - the same as PartDesign.
  * `Draft - green` - Draft style with auto adjust, green color.
  * `Draft - yellow` - Draft style with auto adjust, yellow color.
  * `Draft - black` - Draft style with auto adjust, black color.
  * `Draft - red` - Draft style with auto adjust, red color.
  * `Draft - handwrite green` - Draft style with auto adjust, handwrite fonts and green color.
  * `Draft - handwrite yellow` - Draft style with auto adjust, handwrite fonts and yellow color.
  * `Draft - handwrite black` - Draft style with auto adjust, handwrite fonts and black color.
  * `Draft - handwrite red` (default) - Draft style with auto adjust, handwrite fonts and red color.

> [!IMPORTANT]
> All the measurements are parametric a little in selection mode. You can move object and the measurement will follow. 
> Also you can resize object and the measurement will update dimension.
> However, if you convert `Part :: Box` into `PartDesign :: Pad` or change objects edges, faces or vertices, 
> the measurement will no longer follow, so you have to remove such measurement and create new one.
> Also the measurements **are not** parametric in preselection mode.
> If you use Draft style some measurements for example for edges inside pocket or holes may not be visible. You can use [makeTransparent](#maketransparent) tool to see it.

* **Measurement observer:**
  * `START` button allows you to start the measurement process,
  * `PAUSE` button allows you to stop the measurement process, without leaving this tool's graphical interface, for example if you want to select or create objects.

* **Preselection mode:**
  * `ON` button allows you to start preselection mode and also exit selection mode. Here the measurements are not parametric.
  * `OFF` button allows you to start selection mode and also exit preselection mode. Here the measurements are parametric.
  
* **Vertices size:**
  * `-5` button allows you to make smaller all vertices of all objects by `-5` points, 
  * `+5` button allows you to make bigger all vertices of all objects by `+5` points.

> [!TIP]
> You can also use [showVertex](#showvertex), but here you can adjust the vertices more precisely and it works for all vertices, so you don't have to unselect the object or select a specific object. 

**Text field** the text box shows the current measurements, so you can easily copy these dimensions for later use.

**Video tutorials:** 
* [New measurement features](https://www.youtube.com/watch?v=9F_fBQYuxvU)
* [How to use magicMeasure](https://www.youtube.com/watch?v=_yGLzNmeK0Q)

# Dowels and Screws

## magicDowels

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDowels.png"> This tool allows to add mounting points to panels. You can add predefined mounting points e.g. screws, dowels, shelf supporter pins or add custom mounting points. This is very quick way to add mounting points to the furniture, no calculation needed to place dowel exactly in the middle of the edge. If you would like to add e.g. 40 dowels to the whole furniture and align all of them manually, it would probably be big challenge. With this tool you can do it with single click in many cases. Make sure the green faces are visible, because they refers to the head of the screw. If you would like to replace the dowels with detailed screw later, this might be important if the dowel is rotated incorrectly, the screw will be rotated incorrectly as well. 

**Options:**

* **refresh face selection:** You have to select face and click `refresh face selection` to start using this tool. Also you can change face with this button. However, you can also first select face and next open this tool, so this tool will open GUI with the face loaded.
* **1 / 4:** For example it means you have selected `1` edge from `4` edges available. The same for other selections.
* **Select edge:** You can choose the edge for the dowels. Normally, for surface there are 4 edges but if the object is for example `boolean Cut` there might be much more edges or only 2 edges if this is edge of the board.
* **position autodetect:** this checkbox is checked by default and allows for searching correct edge offset, sink and rotation. The edge selection might be slower but no further adjustment will be needed, I hope.

> [!TIP]
> This tool can read default settings from [magicSettings](#magicsettings) tool. 
> Select `magicSettings` option from menu to load your custom settings or set `Prefer magicSettings defaults:` option to `yes` in [magicSettings](#magicsettings) tool to open this tool automatically with your custom settings.

For manual adjust you can use:

* **Adjust edge:** Allows to adjust offset from the edge. This option is useful if by default the dowels not sink to the surface, so there is problem with correct positioning by default. 
* **Adjust sink:** With this option you can change the sign for the sink. Sometimes it solves the problem with correct positioning and further adjust is not needed.
* **Adjust rotation:** You can rotate the dowels. There are some predefined rotations according to the current face plane to speed up this process.
* **Select sides:** You can choose the side for the dowels, left side only, right side only or both sides.
* **Text inputs:** You can set your custom values here and click `show custom settings` to see if the dowels fits your needs. 
* **keep custom settings:** This checkbox allows you to keep custom values, for example custom dowels size or dowels per side, while you changing the faces.
* **show custom settings:** Allows you to preview the custom settings but you need to click `create` button to store dowels.
* **create:** This button will store the dowels permanently.

> [!NOTE]
> I personally use a [Wolfcraft dowelling jig](https://www.wolfcraft.com/products/wolfcraft/en/EUR/Products/Attachments-for-Machines/Drill-Guides/Dowelling-jig/p/P_4650) to drill 3 mm pilot holes for 4 x 40 mm screws. On this dowelling jig I have two sleeves I made myself from 16 mm screws (a small improvement). The sleeves are in positions 10 and the stopper in positions 8, so I can drill two holes at once very quickly from each side with high precision with a distance of 50 mm from each edge and with a distance between the holes of 64 mm. That is why the default distance for all screws is set this way.

**Video tutorials:** 
* [Adding dowels improved](https://www.youtube.com/watch?v=6qixKpVKA-0)
* [Adding dowels](https://www.youtube.com/watch?v=q7tJffBBUGY)
* [Make quickly 168 dowels](https://www.youtube.com/watch?v=_a_Q7BjEHLA)
* [Tenons with magicDowels](https://www.youtube.com/watch?v=xXfy9KaYJC4)

## panel2link

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> This tool allows to replace simple objects with any detailed object, e.g. `Cylinders` with realistic looking screws made using `PartDesign`. First you have to select detailed object, next select simple objects to replace with `Links`. The first selected detailed object can be `Part`, `LinkGroup` or any other created manually or merged with your project. You can replace more than one simple object at once with `Link`. To select more objects hold left `CTRL` key during selection. The simple objects should imitate the detailed object to replace all of them in-place with realistic looking one. For more details please see: [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture).

**Video tutorials:** 
* [Dowels and Screws are fully parametric](https://www.youtube.com/watch?v=hWaM19edjFE)

## panel2clone

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2clone.png"> This tool allows to replace simple objects with any detailed object, e.g. `Cylinders` with realistic looking screws made using `PartDesign`. First you have to select detailed object, next simple objects to replace with `Clones`. The first selected detailed object can be `Part`, `LinkGroup` or any other created manually or merged with your project. You can replace more than one simple object at once with `Clone`. To select more objects hold left `CTRL` key during selection. The simple objects should imitate the detailed object to replace all of them in-place with realistic looking one. This tool works with the same way as [panel2link](#panel2link) but instead of `Links` it creates `Clones` objects. It can be useful if you want to remove the base object and have clean objects Tree. Also if you want to change each copy separately. [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture).

**Video tutorials:** 
* [Dowels and Screws are fully parametric](https://www.youtube.com/watch?v=hWaM19edjFE)

## sketch2dowel

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sketch2dowel.png"> First select face, next Sketches of the holes to create dowels. This tool allows to create dowel from Sketch of the hole. The first selected face refers to the side the dowel will be raised, exact orientation for the dowel. Dowel position will be get from the Sketch. The dowel Radius and Height will be get from hole object. If the hole is throughAll the dowel height will be very big, so make sure you use dimensions for hole. To select more Sketches hold left CTRL key during selection. 

**Video tutorials:** 
* [Dowels from Sketch](https://www.youtube.com/watch?v=CI4M5_DDWSg)

## edge2dowel

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/edge2dowel.png"> This tool allows to create dowels above the selected hole edges. To create dowel select edge of the hole. You can select many edges at once but all the holes need to be at the same object. The dowel Height will be 40. The dowel radius will be get from the selected edge hole radius. To select more objects hold left CTRL key during selection. 

**Video tutorials:** 
* [Dowels from holes](https://www.youtube.com/watch?v=l8-Jven6VTQ)

<br><br><br>

# Fixture

## magicFixture

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicFixture.png"> This tool allows you to apply any type of fixture, for example cabinet door handle, hinges or angles. First you have to select fixture, usually LinkGroup container with for example angle inside, and next select face, edge, hole or vertex as reference anchor. Next click `refresh selection` to load objects. After adjust position of the fixture at the surface, you have to click `create` button to store the fixture. For more details please see: [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture).

**Options:**

* **set** button allows you to set the fixture or anchor individually. This option is useful when you need to hide an object to access a specific face, edge, or vertex.
* **refresh selection:** allows you to load the fixture that should be applied and face, edge, hole or vertex as anchor reference point.

* **Anchor:** allows you to select a saved anchor as a reference point (vector).
* **Rotation:** allows you to select the most commonly used rotations to fit an object to a plane.
* **add selected anchor** allows you to add additional anchors as reference points to the end of the list. Before pressing this button, you must select a face, edge, hole edge or vertex. If you select a face and an edge, all vertices for the selected face or edge and the center of the face or edge will be added to the end of the list. If you select a vertex, only the selected vertex will be added to the end of the list.

* **X offset:** The `-` and `+` buttons allows you to move an object along the X coordinate axis.
* **Y offset:** The `-` and `+` buttons allows you to move an object along the Y coordinate axis.
* **Z offset:** The `-` and `+` buttons allows you to move an object along the Z coordinate axis.
* **Step:** Allows you to set the offset step for the `-` and `+` buttons.
* **show custom settings:** allows you to preview the custom settings but you need to click `create` button to store fixture. If you use the `-` and `+` buttons, the object will change its position automatically, but if you enter your own values ​​into the text fields, you must confirm them with this button.

* **set manually:** open manual edit mode.
* **finish manually:** finish manual edit mode.

* **Link:** creates Link object.
* **Clone for drilling:** creates Clone object. For example if you want to measure offsets or drill pilot holes for screws that are to be screwed into the angle holes, it is better to choose this option because Clones have its own position, the Links refers to the base element. For more details see: [Pilot holes for angles, hinges](#pilot-holes-for-angles-hinges)

* **create:** This button will store the fixture permanently.

* **Cross:**
  * `Corner cross:` buttons `-`, `+` resize the cross in the right bottom of the screen, it has auto-repeat.
  * `Center cross:` buttons `on`, `off` turn on and off the center cross at the screen.
  * `keep custom cross settings` allows to store the custom cross setting after this tool exit.

**Video tutorials:** 
* [How to add handle and see soft-close animation](https://www.youtube.com/watch?v=iOseEBGmwAU)

## edge2drillbit

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/edge2drillbit.png"> This tool can be used to create drill bits above holes of the hinges, angles or other fixture type. You to create drill bits precisely above the hole so that you can drill the hole quickly later. The drill bits will be created above the selected hole edges. To create drill bits select edge of the hole. You can select many edges at once but all the holes need to be at the same object. The drill bit Height will be 16. The drill bits radius will be get from the selected edge hole radius but will be little smaller, 1 mm, than the selected hole, to make correct pilot hole for screw. To select more objects hold left CTRL key during selection.

<br><br>

## Dowels, Screws, Fixture - short tutorial

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

<br><br>

# Drilling holes

## magicDriller

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDriller.png"> This tool is similar to [magicDowels](#magicdowels) but instead of applying dowels this tool allows you to drill holes, countersinks or counterbores serially with predefined or custom settings. You can choose the same predefined screws, dowels and pins as [magicDowels](#magicdowels) has but instead of dowels there will be created set of drill bits. The drill bits will be smaller than the screws to allow drill pilot holes for screws. For more details see: [Drilling serially](#drilling-serially)

**Options:**

* **set:** Additional set buttons make it easier to drill pilot holes with a countersink for screws. For example, you can set the drill bit's position relative to the shelf edge and the drilling face to the side of the entire piece of furniture separately. This allows you to quickly drill standard pilot holes in the shelf edges first, and then simply change the drilling face and drill bit type to create a countersink hole in side.
* **refresh all faces selection:** available selections: 
  * `single face` in this case, if you select only one face, it will be set as the face for drill bit positioning and also as the face for drilling.
  * `two faces` in this case, if you select more than one face, the first selected face will be set as the face for drill bit positioning and the second selected face will be set as the face for drilling.

> [!TIP]
> This tool can read default settings from [magicSettings](#magicsettings) tool. 
> Select `magicSettings` option from menu to load your custom settings or set `Prefer magicSettings defaults:` option to `yes` in [magicSettings](#magicsettings) tool to open this tool automatically with your custom settings.

* **Select edge:** You can choose the edge for the drill bits. Normally, for surface there are 4 edges but if the object is for example `boolean Cut` there might be much more edges or only 2 edges if this is edge of the board.
* **Adjust edge:** Allows to adjust offset from the edge. This option is useful if by default the drill bits not touch the surface, so there is problem with correct positioning by default. 
* **Adjust rotation:** You can rotate the drill bits if the red face of the drill bits is at the top of the drill bits. There are some predefined rotations according to the current face plane to speed up this process.
* **Select sides:** You can choose the side for the drill bits, left side only, right side only or both sides.

* **Text inputs:** You can set your custom values here and click `show custom settings` to see if the drill bits fits your needs. 
* **show custom settings:** Allows you to preview the custom settings but you need to click `create` button to drill holes.
* **create:** This button will create holes below the red face of the drill bits. If the object is simple panel (Part::Box) it will be converted to Pad (PartDesign::Pad) object.

> [!NOTE]
> I personally use a [Wolfcraft dowelling jig](https://www.wolfcraft.com/products/wolfcraft/en/EUR/Products/Attachments-for-Machines/Drill-Guides/Dowelling-jig/p/P_4650) to drill 3 mm pilot holes for 4 x 40 mm screws. On this dowelling jig I have two sleeves I made myself from 16 mm screws (a small improvement). The sleeves are in positions 10 and the stopper in positions 8, so I can drill two holes at once very quickly from each side with high precision with a distance of 50 mm from each edge and with a distance between the holes of 64 mm. That is why the default distance for all screws is set this way.

**Video tutorials:** 
* [Drilling countersinks for shelves](https://www.youtube.com/watch?v=rd2W-L6OHuo)
* [Countersinks & realistic screws](https://www.youtube.com/watch?v=N5SpUCtNMY0)
* [How to drill holes for minifix](https://www.youtube.com/watch?v=4A9lsZveXPc)

## drillHoles

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillHoles.png"> This is drill bit to make simple hole. The hole will be drilled below the bottom part of the drill bit, below the red face of the cylinder. The radius and depth of the hole will be the same as drill bit radius and height. You can resize the drill bit if you want. If you select face only, the drill bit will be created in the corner of the face (0 vertex). So, you will be able to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face to get exact hole depth. If you select face and than any amount of drill bits, the holes will be drilled below each drill bit. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

<br>

## drillCountersinks

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCountersinks.png"> This is drill bit to make countersink with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of countersink will be drill bit Radius2. The hole depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

<br>

## drillCounterbores

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCounterbores.png"> This is drill bit to make counterbore with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of counterbore will be drill bit Radius2. The hole depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

<br>

## drillCounterbores2x

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCounterbores2x.png"> This is drill bit to make counterbore2x with hole. The hole will be drilled below the bottom part of the drill bit, below the red face. The radius of the hole will be drill bit Radius1. The radius of counterbore will be drill bit Radius2. The hole depth will be panel thickness. The counterbore depth will be drill bit Height. If you select face only, the drill bit will be created in the corner of the face (0 vertex), allowing you to move the drill bit precisely to any place at the face. Do not move the drill bit up, the drill bit should touch the face. You can select any amount of drill bits, the holes will be drilled below each drill bit but first selected should be face, next drill bits. To select more objects hold left CTRL key during selection. If the selected element is Cube, it will be replaced with Pad. For more info see: [Drilling via icons](#drilling-via-icons)

<br>

## magicCNC

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicCNC.png"> 

**Manual drilling:**

This tool is some kind of CNC drilling machine simulator to drill custom holes. The axis which move the drill bit up and down is automatically hidden at this tool. So, you can move the drill bit at the surface and you not move the drill bit up or down by mistake and cause incorrect hole depth. Also this tool has option to drill by button click. It recognize the drill bit type by the label. For the countersink the label need to contains `countersink`, and for counterbore need to contains `counterbore`. For other label the simple hole will be drilled. This tool also allows for turn on and off the manuall edit mode. So, you can move the drill bit by hand and drill holes by clicking buttons. For more info see: [Drilling via magicCNC](#drilling-via-magiccnc)

* **set** button allows you to set face or drill bit individually. This option is useful when you need to hide an object to access a specific face or drill bit.
* **refresh selection:** allows you to load at once the first selected face and next drill bit.
* **Move along X:** The `-` and `+` buttons allows you to move drill bit along the `X` coordinate axis.
* **Move along Y:** The `-` and `+` buttons allows you to move drill bit along the `Y` coordinate axis.
* **Move along Z:** The `-` and `+` buttons allows you to move drill bit along the `Z` coordinate axis.
* **Move step:** Allows you to set the offset step for the `-` and `+` buttons.
* **set manually:** open manual edit mode.
* **finish manually:** finish manual edit mode.
* **create:** This button will create the hole below the drill bit according to the drill bit type.

**Set attributes for CNC:**

This option was added [to support CNC scripts](https://github.com/dprojects/Woodworking/issues/91). This solution supports PartDesign::Hole objects and allows you to add attributes describing each hole to any object, as well as select an arbitrary starting point from which all hole spacing is calculated.

* **1st set** allows you to select a starting point from which the spacing for each hole will be calculated. If an edge or face is selected, the starting point will be the CenterOfMass.
* **2nd set** allows you to add an object to which all attributes will be saved for easy retrieval by scripts.
* **set CNC attributes to target** this button allows you to save attributes to the target object. Attributes related to holes are in lists, so you can easily retrieve any information for a given hole using a script. Currently supported attributes:
  * `.CNC_Label` a list of labels of `PartDesign::Hole` objects that created the given hole.
  * `.CNC_StartX` starting point (zero position) for CNC along `X` axis.
  * `.CNC_StartY` starting point (zero position) for CNC along `Y` axis.
  * `.CNC_StartZ` starting point (zero position) for CNC along `Z` axis.
  * `.CNC_X` a list of global positions of the hole on the `X` coordinate axis.
  * `.CNC_Y` a list of global positions of the hole on the `Y` coordinate axis.
  * `.CNC_Z` a list of global positions of the hole on the `Z` coordinate axis.
  * `.CNC_OffsetX` a list of the distances the CNC needs to go from the starting point (attribute `.CNC_StartX`) to the center of the hole (attribute `.CNC_X`) along the `X` coordinate axis.
  * `.CNC_OffsetY` a list of distances the CNC needs to go from the starting point (attribute `.CNC_StartY`) to the center of the hole (attribute `.CNC_Y`) along the `Y` coordinate axis.
  * `.CNC_OffsetZ` a list of distances the CNC needs to go from the starting point (attribute `.CNC_StartZ`) to the center of the hole (attribute `.CNC_Z`) along the `Z` coordinate axis.
  * `.CNC_Depth` a list of depths for each hole taken from each `PartDesign::Hole` object that created the hole.
  * `.CNC_Diameter`  a list of diameters for each hole taken from each `PartDesign::Hole` object that created the hole.
			
> [!NOTE]
> The dimensions for each hole are stored in millimeters as the attribute type `App::PropertyFloatList` because FreeCAD does 
> not have any attribute type that can store distances with dynamic user unit settings, for example `App::PropertyLengthList`. 
> For more info see opened issue: [please add App::PropertyLengthList to store dimensions for CNC](https://github.com/FreeCAD/FreeCAD/issues/26897)

**Cross:**

  * `Corner cross:` buttons `-`, `+` resize the cross in the right bottom of the screen, it has auto-repeat.
  * `Center cross:` buttons `on`, `off` turn on and off the center cross at the screen.
  * `keep custom cross settings` allows to store the custom cross setting after this tool exit.

## cutDowels

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/cutDowels.png"> This tool is designed to allow drilling for designing approach based on Cut holes using Cylinders without creating PartDesign objects. This tool allows you to automatically cut all dowels from selected panel. You do not have to select and search exact dowels that belongs to the selected panel. If you select panel, this tool search for all dowels that belongs to the selected panel and apply Boolean Cut on the panel. You can select many panels at once to cut dowels. To select more panels hold left CTRL key during selection. During this process only the copies will be used to cut, so the original Cylinders will not be moved at the objects Tree and will be visible at cut-list report. This feature is sensitive for visibility of Cylinders. So, you can hide Cylinders you do not want to be cut out from the panel.

**Video tutorials:** 
* [Search and cut dowels](https://www.youtube.com/watch?v=Oogs8LqkReQ)

# Parameterization

## magicGlue

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicGlue.png"> This tool allows you to add or remove expressions to keep objects position and size.

**Options:**

* **Glue position:** This option allows you to glue position of target objects to the source object position.
  * `set` **for source** allows you to add source object position. The source can be vertex or face. For vertex the `XYZ` placement will be get as reference point. For face the `CenterOfMass` will be the reference point, so you need to be careful with linking to this face source because the `CenterOfMass` move `1/2` of the object move way. However it can be used to glue object to the center, for example center furniture side.
  * `set` **for target** allows you to add target objects to set expressions. If the object is Cube `Part::Box` the expression will be set at `Placement` of the `Cube`. If the object is Pad `PartDesign::Pad` the expression will be set at `Placement` of its `Body`.
  * `refresh all selection` allows you to add quickly source and targets. First selected vertex or face will be the source and all other objects will be considered as targets to set expressions. Also this is default init option, for example if you select vertex and 2 objects and open the tool this will be ready to set glue position.
  * `add glue` for `X` direction allows you to add expression for moving objects along `X` axis.
  * `add glue` for `Y` direction allows you to add expression for moving objects along `Y` axis.
  * `add glue` for `Z` direction allows you to add expression for moving objects along `Z` axis.
  * `use VarSet` checkbox if this option is checked then a file named `magicGlueVarSet` will be created and the position values ​​will be saved there. However, in this case it is not possible to link the source object to the values ​​in the `magicGlueVarSet` file, due to the limitation of the FreeCAD VarSet object, which throws `cyclic reference` errors. The `magicGlueVarSet` file is recognized by the `.Label` attribute, so you only need to change the file name to use more VarSet files. This option is available only since FreeCAD 1.0 version.

* **Glue size:** 
  * `set` **for source** allows you to add source object position. The source can be edge. The selected `edge.Length` will be the reference point.
  * `set` **for target** allows you to add target objects to set expressions. The selected objects should be edges. 
    * If the object is Cube `Part::Box` the expression will be set to `Length` or `Width` or `Height` of the `Cube` according to the selected edge plane. 
    * If the object is Pad `PartDesign::Pad` the expression will be set at `Length` property or `Sketch` constraints.
    * If the object is for example Profile `PartDesign::Thickness` the expression will be set at `Value` property or `Sketch` constraints.
    * If the object is for example cornerBlock `PartDesign::Chamfer` the expression will be set at `Size` property or `Sketch` constraints.
  * `refresh all selection` allows you to add quickly source and targets. First selected edge will be the source and all other edges will be considered as targets to set expressions.
  * `add glue size` allows you to add expression for size changes of source edge.
  * `use VarSet` checkbox if this option is checked then a file named `magicGlueVarSet` will be created and the size values ​​will be saved there. However, in this case it is not possible to link the source object to the values ​​in the `magicGlueVarSet` file, due to the limitation of the FreeCAD VarSet object, which throws `cyclic reference` errors. The `magicGlueVarSet` file is recognized by the `.Label` attribute, so you only need to change the file name to use more VarSet files. This option is available only since FreeCAD 1.0 version.
  
* **Clean glue:** 
  * `refresh all selection` allows you to add target objects to clean expressions.
  * `clean glue position` clean all position expressions. Make sure you do not have your private expressions.
  * `clean glue size` clean all size expressions. Make sure you do not have your private expressions.

* **Super glue everywhere:** this option is an attempt to quickly automatically parameterize a simple model so that the thickness of the wood used or the dimensions can be changed. The position parameterization is saved directly in the objects, while the VarSet object is used to parameterize the sizes, so that you can conveniently change the sizes in one place.
  * `add super glue everywhere` this option set parameterization for position and sizes at once for all objects.
  * `clean super glue everywhere` this option remove parameterization for position and sizes at once from all objects.
  * `set order from selected` sets the objects to be parameterized in the appropriate order selected by the user. This option is useful in more complex, multi-level structures, where with automatic ordering, the elements from the top level may not be parameterized correctly due to the same position as the lower elements.
  * `glue position` this option sets the parameterization for a position, for all objects, or only for user-selected objects.
  * `glue size` this option creates VarSet object and set the parameterization for a size, for all objects, or only for user-selected objects.
  * `clean position` this option removes the parameterization for a position, for all objects, or only for user-selected objects.
  * `clean size` this option removes the parameterization for a size, for all objects, or only for user-selected objects. But this option not removes the VarSet object.

* **Cross:**
  * `Corner cross:` buttons `-`, `+` resize the cross in the right bottom of the screen, it has auto-repeat.
  * `Center cross:` buttons `on`, `off` turn on and off the center cross at the screen.
  * `keep custom cross settings` allows to store the custom cross setting after this tool exit.

> [!IMPORTANT]
> Sometimes after adding glue it doesn't work, FreeCAD shows a corrupted file in the objects window Tree. However, the expressions set by magicGlue tool are correct but magicGlue skills are too advanced for FreeCAD parser. This is because FreeCAD expression parser works when opening the file and has a very basic parsing solution, the are no reference for Faces and Edges, key thing im my opinion. **To make it work you have to reopen the file and move or resize the source element, the errors should disappear.**

**Video tutorials:** 
* [How to make parametric furniture quickly](https://www.youtube.com/watch?v=z2rpVoLgqWI)
* [FreeCAD 1.1 automatic parameterization](https://www.youtube.com/watch?v=ZAKGnY_0sj8)
* [Table with adjustable height](https://www.youtube.com/watch?v=JhbRkCsrQWg)

## sketch2clone

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sketch2clone.png"> This tool allows to replace selected Sketches with Clones and thanks to it, convert static model to parametric. First selected Sketch will be changed into `Parametric Pattern` for all other selected Sketches. After this operation, if you change the `Parametric Pattern` all other Sketches will be automatically updated with new pattern. For example if you have Pad, it will change the shape. Make sure the center of coordinate axes XYZ for each selected Sketch is in the middle of the pattern, this will allow for correct positioning of the Sketches. To select more objects hold left CTRL key during selection. For more complicated objects use [panel2link](#panel2link) or [panel2clone](#panel2clone) at the whole `Part`. 

**Video tutorials:** 
* [Automatic parametrization](https://www.youtube.com/watch?v=JuZsAjrQr6M)
* [Playlist for parametrization](https://www.youtube.com/playlist?list=PLSKOS_LK45BCzvg_B7oSTk1IsQnu5thtZ)

## showAlias

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showAlias.png"> To see all objects with alias: 1. First select spreadsheet at objects Tree. 2. Click this tool icon to activate the preview mode. 3. Click any spreadsheet cell with alias. 

> [!IMPORTANT]
> This tool needs to be activated to work. To activate this tool you have to select spreadsheet at objects Tree and click this tool icon. If this tool will be activated you can select any cell with alias to see all objects selected. The selected objects at 3D model will be those that uses the selected alias. Also the objects will be selected at objects Tree. To finish the preview mode, click the tool icon without any selection.

**Video tutorials:** 
* [Preview alias](https://www.youtube.com/watch?v=tS9pvkPH5RI)

<br><br><br>

# Construction profiles

## panel2profile

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2profile.png"> Please select valid `Cube` or `Pad` object imitating profile. The selected `Cube` or `Pad` objects need to have two equal sizes e.g. `20 mm x 20 mm x 300 mm` to replace it with construction profile. 

> [!NOTE]
> This tool allows to replace panel with construction profile. You can replace more than one panel at once. To select more panels hold left `CTRL` key during selection. The new created construction profile will get the same dimensions, placement and rotation as the selected panel. If you have all construction created with simple panel objects that imitating profiles, you can replace all of them with realistic looking construction profiles with single click.

**Video tutorials:** 
* [Construction profiles](https://www.youtube.com/watch?v=5hXMFAxXQag)

## panel2angle

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2angle.png"> Please select valid faces at any amount of `Cubes` or `Pads` to cut the faces and create construction angle profiles. 

> [!NOTE]
> This tool allows to replace panel with construction angle. You can replace more than one panel at once. To select more faces hold left `CTRL` key during faces selection. The new created construction angle will get the same dimensions, placement and rotation as the selected panel. You can cut any faces at panel. However, if the panel has two equal sizes e.g. `20 mm x 20 mm x 600 mm`, the ends will be cut as well, so you do not have to select them. If you do not have same sizes you have have to select ends too, if you want to cut them. If the selected faces are not valid, e.g. opposite faces, the final object may disappear and be broken. You can remove last operation and try again. If you have all construction created with simple panels that imitating angles, you can replace all of them with realistic looking construction angles with single click and they will be rotated according to the selected faces.

**Video tutorials:** 
* [Construction profiles](https://www.youtube.com/watch?v=5hXMFAxXQag)

## panel2angle45cut

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2angle45cut.png"> Please select valid face at construction angle to create 45 cut at edges. 

> [!NOTE]
> This tool allows to cut construction angle with 45 cut. You can select many construction angles at once but only single face can be selected for each construction angle. If the construction angle is C-shape you can select face inside profile and two sides will be cut. If the construction angle is L-shape you select single face inside profile and only single side will be cut. Because to create frame with L-shape profiles you have to cut only single side. To create frame with C-shape profiles you have to cut both sides. The face should be selected inside profile to set exact cut size without profile thickness. To select more faces hold left `CTRL` key during faces selection. You can remove last operation and try again. If you have all construction created with construction angles you can cut all of them at once.

**Video tutorials:** 
* [Construction profiles](https://www.youtube.com/watch?v=5hXMFAxXQag)

## panel2frame

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2frame.png"> This tool allows to replace `Cube` panel with frame 45 cut at both sides. You can replace more than one `Cube` panel at once. To replace Cube objects with frames you have to select exact face at each `Cube` object. For example if you want to make picture frame, select all 4 inner faces. To select more faces hold `left CTRL key` during selection. The new created frame will get the same dimensions, placement and rotation as the selected `Cube` panel but will be cut at the selected face. If you have all construction created with simple `Cube` objects that imitating picture frame or window, you can replace all of them with realistic looking frame with single click. 

**Video tutorials:** 
* [Quick 45 cut joint](https://www.youtube.com/watch?v=aFe9p4At41c)

<br><br><br>

## cornerBlock

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/cornerBlock.png"> Please select single edge at each panel you want to change into corner block. 

> [!NOTE]
> This tool allows to create corner block from selected edge. The cut size will be the panel thickness. The cut will be at the other side of selected edge, for better access for example if you create Cube 100 mm x 100 mm x 100 mm in the corner of the table to support table leg, and you want to change it into corner block, quickly with single click. You can replace more than one panel at once. Hold left CTRL key during edges selection.

**Video tutorials:** 
* [Table corner block](https://www.youtube.com/watch?v=Fyss9sZ4AgE)

<br><br><br>

## cornerBrace

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/cornerBrace.png"> Please select single edge at each panel you want to change into corner brace. 

> [!NOTE]
> This tool allows to create corner brace from selected edge (the single visible edge). The cut size will be the panel thickness for the first edge and for the second edge half of the thickness. So, you get nice looking corner brace with single click. For example you can create Cube 100 mm x 100 mm x 100 mm in the corner of the table to support table leg, and you can change it into corner brace, quickly with single click. You can replace more than one panel at once. Hold left CTRL key during edges selection.

**Video tutorials:** 
* [Table corner brace](https://www.youtube.com/watch?v=Y9Wa4o9N1mM)

<br><br><br>

# Joinery

## magicJoints

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicJoints.png"> This tool allows you to quickly create connections based on a sketch. The sketch used to create the connection will be a parametric template that can be modified later, updating all previously created connections. This tool allows you to create connections on `Part :: Box` or `PartDesign` objects. If the object is a `Part :: Box`, it will automatically be converted to a `PartDesign` object and the connection will be created on that object.

**Possible selections:**

* **1. set** the first `set` button allows you to add a sketch as a template for creating connections. This sketch can be drawn on a face where connections can be created, but it can also be completely independent in its own `Part` and `Body` container. The selected sketch will be cloned and become the connection template, which, when modified, will modify all connections created using it.
* **2. set** the second `set` button is used to add a reference face relative to which the pattern's position will be determined. This face is also used to create the pattern's position anchors. Additionally, if no additional face is added, via 3rd `set` button, to create a Mortise, both the Mortise and Tenon will be created on this face using the dedicated `create Mortise` and `create Tenon` buttons.
* **3. set** the third `set` button is used to specify the face for creating a Mortise using the `create Mortise` and `create Tenon and Mortise` buttons. This option is optional and is primarily used for faster and more advanced joint creation. If a face is not added using this `set` button, then a Mortise using the `create Mortise` button will be created on the face added using the second `set` button.

* **refresh all selections** this button loads all elements at once. Before pressing this button, first select Sketch as the connection pattern, then select the face based on which the anchors for positioning the connection pattern will be created, and finally, optionally, select the face that will be the reference for creating a Mortise using the `create Mortise` and `create Tenon and Mortise` buttons. In this case, the second selected element and the third, both faces, should belong to different objects, so that the Mortise and Tenon can be created simultaneously on different objects using the `create Tenon and Mortise` button.

> [!TIP]
> You can also make a selection before opening the tool. In this case, select:
> * **Sketch + Face:** first, select the sketch with the connection pattern, then the face for which you want to define the anchors. 
> * **Sketch + Face + Face:** first, select the sketch with the connection pattern, then the face for which you want to define the anchors, and finally the face on which the Mortises will be created.
> Then open the tool, all selected elements should be automatically loaded and recognized correctly.

**Options:**

* **Anchor:** these are loaded anchors used to set position of the connection pattern. These anchors are determined by the second `set` button and the number of these anchors may vary depending on the complexity of the face and the number of edges:
  * `first position` is the current sketch position loaded via first `set` button.
  * `second position` is the center of the face loaded via the second `set` button.
  * `next positions` are the vertices of the face loaded via the second `set` button.
  * `next positions` are the centers of the edges of the face loaded via the second `set` button.

* **Rotation:** This is `Sketch` pattern rotation. It is useful if you change the face and the face is not at the same line. For example if you want to create Tenon at the other side of the table supporter.

* **X axis:** additional offset for the `X` coordinate axis.
* **Y axis:** additional offset for the `Y` coordinate axis.
* **Z axis:** additional offset for the `Z` coordinate axis.
* **Step:** is the step for the `XYZ` offset. The step is automatically calculated during `-` or `+` changes.
* **set custom values** This button should be clicked if you write manually values for `X`, `Y` or `Z` axis offset.
* **set manually** allows to set pattern into transform mode and move the pattern manually by hand. You can create Mortise and Tenon in this mode as well.
* **finish manually** close transform mode.

* **create Mortise** this button creates a `PartDesign :: Pocket` object on the face loaded with the third `set` button. If no such face has been loaded, a `PartDesign :: Pocket` object will be created on the face loaded with the second `set` button. This allows you to freely select face to create a Mortise, as well as use a joint pattern from tools like [jointTenonCut](#jointtenoncut) and create a Mortise.
* **create Tenon** this button creates a `PartDesign :: Pad` object on the face loaded with the second `set` button. 
* **create Tenon and Mortise** this button creates a `PartDesign :: Pad` object on the face loaded with the second `set` button and also creates a `PartDesign :: Pocket` object on the face loaded with the third `set` button.

**Video tutorials:** 
* [How to create tenon and mortise quickly](https://www.youtube.com/watch?v=vuddlHfAbCc)
* [Playlist for Joinery](https://www.youtube.com/playlist?list=PLSKOS_LK45BBG8kJ2AZvQKBfOSfzhTrLt)

## jointTenonCut

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/jointTenonCut.png"> This tool cut tenon at the selected face in the parametric way. The pocket is created using Clones to the Sketch pattern. The Sketch pattern for pocket operation will be the same for all selected faces and is based from first selected face or Sketch pattern. So if the faces have different sizes it is recommended to use this tool twice with different selection to have two Sketch patterns for pockets. This tool supports multi face selection. To select more faces hold left control button CTRL during faces selection. The objects can be type of `PartDesign :: Pad` or `Part :: Box`. If the object is `Part :: Box` it will be automatically converted into `PartDesign :: Pad` object and the cut will be done on such Pad. The dimensions is taken from not-cut Pad objects, `SizeX` and `SizeY` constraints.

**Possible selections:**

* `Faces` - in this case you need to select all faces on which you want to cut tenon, holding down the left CTRL key.
* `Sketch Tenon pattern + Faces to create Tenons` - this version is the same as the previous one, except that you must first select the Sketch of an existing Tenon connection. This allows you to continue creating a Tenons for the existing connection pattern.

**Video tutorials:** 
* [How to create tenon and mortise quickly](https://www.youtube.com/watch?v=vuddlHfAbCc)
* [Playlist for Joinery](https://www.youtube.com/playlist?list=PLSKOS_LK45BBG8kJ2AZvQKBfOSfzhTrLt)

## jointMortiseCut

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/jointMortiseCut.png"> This tool cut Mortises at the selected face in the parametric way. The pocket is created using Clones to the Sketch pattern. The Sketch pattern for pocket operation will be the same for all selected tenons faces and is based from first selected face or existing Sketch pattern. So if the faces have different sizes it is recommended to use this tool twice with different selection to have two Sketch patterns for pockets. This tool supports multi face selection. To select more faces hold left control button CTRL during faces selection. The objects can be type of `PartDesign :: Pad` or `Part :: Box`. If the object is `Part :: Box` it will be automatically converted into `PartDesign :: Pad` object and the cut will be done on such Pad. The dimensions is taken from not-cut Pad objects, `SizeX` and `SizeY` constraints.

**Possible selections:**
* `Face to create Mortise + Tenons faces` - in this case you need to first select the face of the object on which you want to create the Mortise, then press the spacebar to hide the object on which the Mortise will be created, to get access to the tenons faces inside the Mortise object, then while holding down the left CTRL key, select all the tenons faces for which you want to cut the Mortises. The Mortise object will appear if the Mortises will be created correctly. In this case, a new common Mortise pattern will be created for all selected Tenons faces.
* `Sketch Mortise pattern + Face to create Mortise + Tenons faces` - this version is the same as the previous one, except that you must first select the Sketch of an existing Mortise connection. This allows you to continue creating a Mortise for the existing connection pattern.

**Video tutorials:** 
* [How to create tenon and mortise quickly](https://www.youtube.com/watch?v=vuddlHfAbCc)
* [Playlist for Joinery](https://www.youtube.com/playlist?list=PLSKOS_LK45BBG8kJ2AZvQKBfOSfzhTrLt)

## grainH

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/grainH.png"> This tool creates horizontal grain direction description at selected face. You can select multiple faces and multiple objects. Hold left CTRL key during selection. The Grain attribute will be added to the object. After adding grain direction description the object can be moved and the grain description will be moved together with the object.

**Video tutorials:** 
* [Grain Direction Marker](https://www.youtube.com/watch?v=PXXKBrtAtzQ)
* [Grain Direction Report](https://www.youtube.com/watch?v=4W6Lnkh3DRs)

<br><br><br>

## grainV

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/grainV.png"> This tool creates horizontal grain direction description at selected face. You can select multiple faces and multiple objects. Hold left CTRL key during selection. The Grain attribute will be added to the object. After adding grain direction description the object can be moved and the grain description will be moved together with the object.

**Video tutorials:** 
* [Grain Direction Marker](https://www.youtube.com/watch?v=PXXKBrtAtzQ)
* [Grain Direction Report](https://www.youtube.com/watch?v=4W6Lnkh3DRs)

<br><br><br>

## grainX

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/grainX.png"> This tool creates horizontal grain direction description at selected face. You can select multiple faces and multiple objects. Hold left CTRL key during selection. The Grain attribute will be added to the object. After adding grain direction description the object can be moved and the grain description will be moved together with the object.

**Video tutorials:** 
* [Grain Direction Marker](https://www.youtube.com/watch?v=PXXKBrtAtzQ)
* [Grain Direction Report](https://www.youtube.com/watch?v=4W6Lnkh3DRs)

<br><br><br>

## magicCut

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicCut.png"> This tool make multi boolean cut operation at selected objects. First object should be the base object to cut. All other selected objects will cut the base 1st selected object. To select more objects hold left CTRL key during selection. During this process only the copies will be used to cut, so the original objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. If you are looking for parametric Boolean Cut operation you may consider [magicCutLinks](#magiccutlinks) instead.

**Video tutorials:** 
* [Skip copies in cut-list](https://www.youtube.com/watch?v=rFEDLaD8lxM)
* [Boolean cut with containers](https://www.youtube.com/watch?v=OVwazL8MQwI)

<br><br>

## magicKnife

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicKnife.png"> This tool is opposite for [magicCut](#magiccut) tool. This tool allows to use single knife to cut many panels. First selected object should be knife, and all other selected objects will be cut with the knife. The knife can be any object. So, you can create your own shape of the knife and cut many panels at once. Also you can cut all legs of the table using floor or top of the table as knife. To select more objects hold left CTRL key during selection. During this process the copies of knife are used, so the original knife objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. If you are looking for parametric Boolean Cut operation you may consider [magicKnifeLinks](#magicknifelinks) instead.

**Video tutorials:** 
* [Skip copies in cut-list](https://www.youtube.com/watch?v=rFEDLaD8lxM)
* [Boolean cut with containers](https://www.youtube.com/watch?v=OVwazL8MQwI)

<br><br>

## jointTenonDowel

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/jointTenonDowel.png"> Please select at least one face to create tenon dowel joint at the selected face. This tool allows to create quick tenon as dowel joint at selected face. This tool support any object type because the tenon dowel is additional `Part :: Box` object only positioned at the face. This tool supports multi face selection. To select more faces hold left control button CTRL during faces selection. The tenon as dowel joint offset is `1/4` of the object thickness. The tenon dowel joint is hidden inside the object equally to the visible part, thickness up and thickness down. So, you can cut the tenon dowel also at the object and create removable joint similar to the dowels using [cutTenonDowels](#cuttenondowels) tool. Created tenon dowels have special `BOM` attribute. By default the `BOM` attribute is set to `False`, so all tenon dowels are not listed at cut-list report, but if you set it to `True`, those tenon dowels will be listed. Also the parametric tenon dowels have special `Tenon` attribute, set by default to `True` to notify the [cutTenonDowels](#cuttenondowels) tool to cut such tenon dowel. But if you set it to `False` such tenon dowel will be skipped during cut. 

**Video tutorials:** 
* [How to create tenon and mortise quickly](https://www.youtube.com/watch?v=vuddlHfAbCc)
* [Quick Tenon and Mortise](https://www.youtube.com/watch?v=fHUjW8-37Pk)
* [Playlist for Joinery](https://www.youtube.com/playlist?list=PLSKOS_LK45BBG8kJ2AZvQKBfOSfzhTrLt)

## cutTenonDowels

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/cutTenonDowels.png"> Please select at least one panel to cut all tenon dowels. This tool allows to create mortises using tenon dowels created via [jointTenonDowel](#jointtenondowel) or [jointTenonDowelP](#jointtenondowelp) tool. You do not have to select and search exact tenon dowels that belongs to the selected panel, this tool cut all tenon dowels automatically for selected panel. If you select panel, this tool search for all tenon dowels that belongs to the selected panel and apply `Part Boolean Cut` operation on the panel. The selected panel should rather be `Part :: Box` type to not mix `Part :: Box` objects with `PartDesign :: Pad` design line too much. You can select multiply panels at once to cut tenon dowels. To select more panels hold left control key CTRL during objects selection. During this process only the copies will be used to cut, so the original tenon dowels will not be moved at the objects Tree. This feature is sensitive for visibility of tenon dowels and also for `Tenon` attribute. If the tenon dowel is hidden or `Tenon` attribute is set to `False`, such tenon dowel will be skipped during cut.

**Video tutorials:** 
* [How to create tenon and mortise quickly](https://www.youtube.com/watch?v=vuddlHfAbCc)
* [Quick Tenon and Mortise](https://www.youtube.com/watch?v=fHUjW8-37Pk)
* [Playlist for Joinery](https://www.youtube.com/playlist?list=PLSKOS_LK45BBG8kJ2AZvQKBfOSfzhTrLt)

## magicCorner

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicCorner.png"> This tool allows to create corner connection via Part :: Embed object FreeCAD feature. To fit corners, first select base object that will be cut, next panels that should be fited to the base object. To select multiple panels hold left CTRL key during selection.

**Video tutorials:** 
* [Corner connection](https://www.youtube.com/watch?v=lIZFvDqgWdQ)

<br><br>

## magicCutLinks

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicCutLinks.png"> This tool make multi boolean cut operation at selected objects. First object should be the base object to cut. All other selected objects will cut the base 1st selected object. To select more objects hold left CTRL key during selection. During this process only the links will be used to cut, so the original objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. This tool works with the same way as [magicCut](#magiccut) tool but creates LinkGroup container for cut panels, knives, and uses container links for cut operation. Thanks to this approach you can change Cube to Pad or even add new element to the LinkGroup container and the cut will be updated with new content. So, if you are looking for parametric cut, you should rather use this version.

**Video tutorials:** 
* [Parametric bookcase with Dado joints](https://www.youtube.com/watch?v=kcP1WmKizDg)
* [Boolean cut with links](https://www.youtube.com/watch?v=EE-A6CMgb-4)

<br><br><br>

## magicKnifeLinks

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicKnifeLinks.png"> This tool allows to use single knife to cut many panels. First selected object should be knife, and all other selected objects will be cut with the knife. The knife can be any object. So, you can create your own shape of the knife and cut many panels at once. Also you can cut all legs of the table using floor or top of the table as knife. To select more objects hold left CTRL key during selection. During this process the links of knife are used, so the original knife objects will not be moved at tree. Also there will be auto labeling to keep the cut tree more informative and cleaner. This tool works with the same way as [magicKnife](#magicknife) tool but creates LinkGroup container for Knife and uses container links for cut operation. Thanks to this approach you can change Knife Cube to Pad or even add new Knife to the LinkGroup container and the cut will be updated with new Knife content. So, if you are looking for parametric cut, you should rather use this version.

**Video tutorials:** 
* [Parametric bookcase with Dado joints](https://www.youtube.com/watch?v=kcP1WmKizDg)
* [Boolean cut with links](https://www.youtube.com/watch?v=EE-A6CMgb-4)

## jointTenonDowelP

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/jointTenonDowelP.png"> Please select at least one face to create parametric tenon dowel joint at the selected face. This is parametric version of [jointTenonDowel](#jointtenondowel) tool. In this case all the tenon dowels are linked via `Clones` to the simple `LinkGroup` container. Inside the `LinkGroup` container is the simple `Part :: Box` object as tenon dowel pattern. This approach allows you to add new objects to the `LinkGroup` container or change the tenon dowel pattern inside the container and all tenon dowel clones will be updated. This tool works in the same way as [jointTenonDowel](#jointtenondowel) and allows to create quick tenon as dowel joint at selected face. This tool support any object type because the tenon dowel is additional object only positioned at the face. This tool supports multi face selection. To select more faces hold left control button CTRL during faces selection. The tenon as dowel joint offset is `1/4` of the object thickness but you can change the tenon dowel pattern size and offset here because it is parametric. By default the tenon dowel joint is hidden inside the object equally to the visible part, thickness up and thickness down. So, you can cut all the tenon dowels also at the object and create removable joints similar to the dowels using [cutTenonDowels](#cuttenondowels) tool. Created tenon dowels have special `BOM` attribute. By default the `BOM` attribute is set to `False`, so all tenon dowels are not listed at cut-list report, but if you set it to `True`, those tenon dowels will be listed. Also the parametric tenon dowels have special `Tenon` attribute, set by default to `True` to notify the [cutTenonDowels](#cuttenondowels) tool to cut such tenon dowel. But if you set it to `False` such tenon dowel will be skipped during cut. 

**Video tutorials:** 
* [How to create tenon and mortise quickly](https://www.youtube.com/watch?v=vuddlHfAbCc)
* [Playlist for Joinery](https://www.youtube.com/playlist?list=PLSKOS_LK45BBG8kJ2AZvQKBfOSfzhTrLt)

## cutTenonDowelsP

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/cutTenonDowelsP.png"> Please select at least one panel to cut all tenon dowels. This tool is parametric version of [cutTenonDowels](#cuttenondowels) tool. To cut tenon dowels links will be used here, so the cut mortise will follow the tenon pattern changes. You can add new tenon dowel to the container or change dimensions and the cut mortise will be automatically updated. This tool allows to create mortises using tenon dowels created via [jointTenonDowel](#jointtenondowel) or [jointTenonDowelP](#jointtenondowelp) tool but it is recommended to use parametric tenon dowels created via [jointTenonDowelP](#jointtenondowelp) tool to achieve fully parametric model. In this case you do not have to select and search exact tenon dowels that belongs to the selected panel, this tool cut all tenon dowels automatically for selected panel. If you select panel, this tool search for all tenon dowels that belongs to the selected panel and apply `Part Boolean Cut` with links operation on the panel. The selected panel should rather be `Part :: Box` type to not mix `Part :: Box` objects with `PartDesign :: Pad` design line too much. You can select multiply panels at once to cut tenon dowels. To select more panels hold left control key CTRL during objects selection. This feature is sensitive for visibility of tenon dowels and also for `Tenon` attribute. If the tenon dowel is hidden or `Tenon` attribute is set to `False`, such tenon dowel will be skipped during cut.

**Video tutorials:** 
* [How to create tenon and mortise quickly](https://www.youtube.com/watch?v=vuddlHfAbCc)
* [Playlist for Joinery](https://www.youtube.com/playlist?list=PLSKOS_LK45BBG8kJ2AZvQKBfOSfzhTrLt)

# Router

## Router bit - Cove

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerCove4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerCove2.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerCove.png"> 
> [!NOTE]
> This tool allows to create decoration router bits effect. You can select many edges or faces. The selected edges or faces do not have to be at the same object. You can select edges or faces at any object. But each edge or face need to be according to the XYZ coordinate axis to get correct plane of the edge or face. For face the routing path is the CenterOfMass of the face and also along the longest edge. Hold left CTRL key during edges or faces selection. The router bits get size from object thickness. If the router bit is for example Cove2, it means the size of the Cove will be 1/2 of the object thickness.

**Video tutorials:** 
* [Router Cove](https://www.youtube.com/watch?v=MQYaZ4NEiBI)
* [Decoration testing with router bits](https://www.youtube.com/watch?v=K229hhMt8Vc)
* [How to use decoration features](https://www.youtube.com/watch?v=R9u6ikswO_0)

## Router bit - Round Over

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerRoundOver4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerRoundOver2.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerRoundOver.png"> 
> [!NOTE]
> This tool allows to create decoration router bits effect. You can select many edges or faces. The selected edges or faces do not have to be at the same object. You can select edges or faces at any object. But each edge or face need to be according to the XYZ coordinate axis to get correct plane of the edge or face. For face the routing path is the CenterOfMass of the face and also along the longest edge. Hold left CTRL key during edges or faces selection. The router bits get size from object thickness. If the router bit is for example Cove2, it means the size of the Cove will be 1/2 of the object thickness.

**Video tutorials:** 
* [Router Round Over](https://www.youtube.com/watch?v=RErYZpqbqAY)
* [Decoration testing with router bits](https://www.youtube.com/watch?v=K229hhMt8Vc)
* [How to use decoration features](https://www.youtube.com/watch?v=R9u6ikswO_0)

## Router bit - Straight

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerStraight4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerStraight3.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerStraight2.png"> 
> [!NOTE]
> This tool allows to create decoration router bits effect. You can select many edges or faces. The selected edges or faces do not have to be at the same object. You can select edges or faces at any object. But each edge or face need to be according to the XYZ coordinate axis to get correct plane of the edge or face. For face the routing path is the CenterOfMass of the face and also along the longest edge. Hold left CTRL key during edges or faces selection. The router bits get size from object thickness. If the router bit is for example Cove2, it means the size of the Cove will be 1/2 of the object thickness.

**Video tutorials:** 
* [Router Straight](https://www.youtube.com/watch?v=NDBLmh2SwwI)
* [Decoration testing with router bits](https://www.youtube.com/watch?v=K229hhMt8Vc)

## Router bit - Chamfer

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerChamfer4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerChamfer2.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/routerChamfer.png"> 
> [!NOTE]
> This tool allows to create decoration router bits effect. You can select many edges or faces. The selected edges or faces do not have to be at the same object. You can select edges or faces at any object. But each edge or face need to be according to the XYZ coordinate axis to get correct plane of the edge or face. For face the routing path is the CenterOfMass of the face and also along the longest edge. Hold left CTRL key during edges or faces selection. The router bits get size from object thickness. If the router bit is for example Cove2, it means the size of the Cove will be 1/2 of the object thickness.

**Video tutorials:** 
* [Router Chamfer](https://www.youtube.com/watch?v=Z45TDosmb-U)
* [Decoration testing with router bits](https://www.youtube.com/watch?v=K229hhMt8Vc)

## multiPocket

<img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/multiPocket4.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/multiPocket2.png"> <img align="right" width="100" height="100" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/multiPocket.png">
> [!NOTE]
> This tool allows to create custom decoration from Sketches. You can select many Sketches at once. The selected Sketches will make Pockets at the first selected object. The Sketches need to be correctly aligned at the object. Hold left CTRL key during Sketches selection. For 2 and 4 variant this tool gets first selected object size and create Pocket with 1/2 thickness or 1/4 thickness.

**Video tutorials:** 
* [How to create custom decoration](https://www.youtube.com/watch?v=sZDToy3qCk4)
* [multiPocket custom decoration](https://www.youtube.com/watch?v=FHups7Zvl5E)
* [Future of parametric modeling](https://www.youtube.com/watch?v=0M9EW0I9iwg)

<br><br><br>

# Advanced

## addVeneer

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/addVeneer.png"> Veneer created from `PVC` material can be up to `2 mm` thick. In such a case, you can use this tool, which allows you to simulate the addition of veneer. A `Part::Box` object will be created on the selected face, simulating the added veneer. This approach allows the added veneer to be easily modified. You can modify the length, width, thickness, and other parameters of the applied veneer, which means you can more accurately calculate how much veneer is needed and what spacing should be maintained when calculating board sizes. The default size and other parameters of the applied veneer are taken from the settings in the [magicSettings](#magicsettings) tool. By default, the thickness of the applied veneer is set to `0 mm` to avoid interfering with the modeling process. However, the object cannot be `0 mm` thick, so the default settings set the veneer thickness to `0.01 mm`. The default veneer color is white because the default board color is brown. Personally, I often use white veneer heat-sealing tape on plywood shelves, which makes the shelf look much better in white furniture. I use black veneer on white chipboard furniture. This approach allows you also to add texture only to veneer and get more realistic look. Added venner is also supported by cut-list created via [getDimensions](#getdimensions) tool, so you can create detailed description of added veneer.

**Video tutorials:** 
* [Veneer simulation](https://www.youtube.com/watch?v=VONecUTGSwE)

<br><br><br>

## align2Curve

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/align2Curve.png"> This tool allows to align panels to the curve. It has been created for magicMove Copy Path option, to align panels to the curve. To select more objects hold left CTRL key during selection. To use this tool the panel need to have only single axis rotation offset. For example if you rotate panel 35 degrees around Y axis the and the vertex will touch the curve. This tool not works if you need to rotate the panel additionally, for example 15 degrees around X axis. For more details see description at documentation page. 

Selection modes:

* **Curve and Edges** In this mode you can select curve and next edge at each object you want to align to the curve. This mode is automatic and this tool will try to calculate the angle between the curve and the selected edge. The selected edge need to be this one with object anchor and the object anchor should be already at the curve. If this tool will be able to determine the angle, it will align the panel. Otherwise the panel will be skipped.

* **Curve and Vertex** In this mode you can select curve and next vertex at each object you want to align to the curve. This mode is more precised and slower. It allow to align panel backwards, so the selected vertex will be before he anchor. In this mode the tool will try to search the curve from the nearest side of the vertex. If the curve will be found the panel will be aligned, otherwise the panel will be skipped.

**Video tutorials:** 
* [Align to curve](https://www.youtube.com/watch?v=fbJV_SEuNLg)

## roundCurve

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/roundCurve.png"> This tool allows to improve curve visibility. It makes the curve to look more rounded. Normally, circle Sketch is rendering from straight line segments. If you want to align panel to the curve manually this might be problem to hit exactly the point you want at curve. This tool may help for more precised alignment. If you select the curve and click this tool again the curve will back to default settings. To select more object hold left CTRL key during selection. 

**Video tutorials:** 
* [Align to curve](https://www.youtube.com/watch?v=fbJV_SEuNLg)

<br><br><br>

## showOccupiedSpace

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showOccupiedSpace.png"> This tool allows you to calculate the overall occupied space in 3D by the selected parts or whole model, if nothing is selected. This approach might be very useful at furniture designing process. For example you can see how much space in your room will take opened front of the furniture or how much space take selected parts of the furniture. Normally, all the `Pad` or `Cube` elements, should be created according to the `XYZ` plane, so there will be no difference between the real dimensions and occupied space in 3D.

<br><br><br>

## showConstraints

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showConstraints.png"> To use this tool first select objects to see edges with the same size as defined constraints. 

> [!NOTE] 
> This tool search all constraints for selected objects. If the constraints is non-zero this tool search for all edges with the same size. It allows for quick preview if all the edges are defined by the Sketch. However, in some cases, if the constraints is offset and it is equal edge size this will give false result. To select more objects hold left CTRL key during selection. 

<br><br>

# Code and Debug

## scanObjects

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
* Crash test to test FreeCAD crash during browsing not removed attributes.

Tool repository: [github.com/dprojects/scanObjects](https://github.com/dprojects/scanObjects)

**Video tutorials:** 
* [Debugger, Live API](https://www.youtube.com/watch?v=nFK_o95y6xk)
* [Debugger, Search filter](https://www.youtube.com/watch?v=5h_feMn_lsQ)


## showPlacement

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/showPlacement.png"> This tool allows to see objects anchor placement for selected objects or for all objects, if nothing was selected. To select more objects hold left CTRL key during selection. This tool creates a ball in the default anchor for an object, which corresponds to the X, Y, Z coordinates for the Placement attribute. This allows you to quickly see where the object is anchored and to which vertex it is positioned by default. Additionally, it allows you to quickly check for possible problems with the function of calculating the global position of the object and to further improve it for more complex objects. Unfortunately, FreeCAD has not solved the basic problem with object position for so many years, which means that more complex objects do not know their position and cannot be managed.

<br><br><br>

## debugInfo

<img align="right" width="200" height="200" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/debugInfo.png"> This tool allows to get platform information used for FreeCAD bug report and update Woodworking workbench.

**Main features:**

* Shows your system information which can be used for FreeCAD bug report.
* Run some test cases, mostly import modules used by Woodworking workbench, to find out if the FreeCAD version is safe to use.
* Show information about tested FreeCAD kernel version.
* Checking for Woodworking workbench updates at GitHub.
* Allows you to update Woodworking workbench. If the date of your Woodworking workbench match the latest master branch date you have information `up-to-date`. Otherwise you have link to download the latest version from github master branch and also the button to update will be available. After Woodworking workbench update the FreeCAD will restar with new Woodworking workbench version.
* Allows you to list disabled old Woodworking workbench versions. If you have `up-to-date` Woodworking workbench version, the button to list disabled old Woodworking workbench versions will be visible.
* Allows you to remove old Woodworking workbench versions. If you list disabled old Woodworking workbench versions the button to remove the old Woodworking workbench versions will be visible. After the button press those folder will be removed permanently, so make sure yu want to remove them.

# API for developers

The Woodworking workbench also has an API for developers. This library contains functions that [solve the Topology Naming Problem](https://wiki.freecad.org/Macro_TNP_Solution). You can also leaglly create your own tools and extend the workbench in your private repository in accordance with the MIT license:
	
* **View library API documentation:** [MagicPanelsAPI.md](https://github.com/dprojects/Woodworking/blob/master/Docs/MagicPanelsAPI.md)
* **View library code:** [MagicPanels.py](https://github.com/dprojects/Woodworking/blob/master/Tools/MagicPanels.py)
* **Download & install library:** [raw version](https://raw.githubusercontent.com/dprojects/Woodworking/master/Tools/MagicPanels.py)

> [!TIP]
> If you have Woodworking workbench installed you don't have to install the `MagicPanels` library manaually. Also you can view the library directly from Woodworking workbench via: [scanObjects](https://github.com/dprojects/Woodworking/tree/master/Docs#scanobjects) tool. <br>
> For programming I use simple [Krusader](https://en.wikipedia.org/wiki/Krusader) with `F4` [KWrite](https://en.wikipedia.org/wiki/KWrite) editor. I have set tabulators as indent: `Settings -> Configure Editor -> Editing -> Indentation -> Tabulators -> Tab width: 4 characters`.

<br><br><br>

# Short old tutorials

## Drilling serially

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDriller.png"> To drill holes with countersinks you have to drill through two panels. First select the surface for countersinks and click `refresh all faces selection`, reference for the face should be updated and visible at the tool info screen:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller001.png)

* Next choose `Contersinks` and exact screw type. Also adjust the edge, rotation and sink, if needed:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller002.png)

* If the drill bits are in correct place, click the drill button, this may takes some time, for example if you drill 30 holes for shelf pins at once and you have slow laptop as I have: 
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller003.png)
  
* To drill rest of the hole, hide the first element with countersinks and select edge:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller004.png)

  <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/drillCountersinks.png"> 
  
> [!TIP]
> To drill rest of the hole, you can also use [Drilling via icons](#drilling-via-icons) feature. Just select edge, next all the countersinks drill bits and click the icon. All the holes will be drilled. But do not exit the tool because the countersinks drill bits will be automatically removed. You can do it if the holes will be drilled. But also you can continue with this tool and drill the rest of holes with this tool directly.

* Now click `refresh all faces selection`, reference for the face should be updated and visible at the tool info screen. Also the drill bits will be moved to the new face, but do not worry, for this tool it is ok, just select `Holes` for hole type and exact screw. For `Hole` type, the depth is adjusted with panel thickness. However, if you have different panel sizes you can adjust it, as well: 
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller005.png)
  
* Now click to drill and the rest of the holes will be drilled at the edge:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller006.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillDriller007.png)

> [!TIP]
> If you need to drill a countersink hole for shelves in the center of a side part of the furniture and you do not know exactly where the shelf is from the edge of the side wall to properly position the drill bit, you can use the dedicated set buttons. This allows you to first drill holes in the shelf edge and then update the drilling face for the side wall. In this case, the drill bit will maintain the shelf position and only change the drilling face. For more details see: [magicDriller](#magicdriller)

**Video tutorials:** 
* [Drilling countersinks for shelves](https://www.youtube.com/watch?v=rd2W-L6OHuo)
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

> [!TIP]
> The same procedure you can use to drill pilot holes for hinges or any other fixture.

**Video tutorials:** 
* [Angles, Pilot holes, Screws](https://www.youtube.com/watch?v=CYaL-sGvIK8)

## Pocket holes - invisible connections

Personally I do not use this type of connections because I am not convinced to it, and also I do not have such jig. But I know that many woodworkers use pocket invisible connections and they love it. They use it especially for real wood and than put dowels inside the holes so the screws are not visible at all. 

### Drill pocket holes - manually

> [!WARNING]
> This is deprecated.

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

### Drill pocket holes - with magicDriller

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/magicDriller.png"> To drill pocket holes you can use [magicDriller](#magicdriller). First select exact face you want to drill and run [magicDriller](#magicdriller). Also you can run [magicDriller](#magicdriller) and then select exact face and click `refresh all faces selection`. For hole type choose `Pocket holes` and select predefined screw. You can also change the settings for your custom screw. If you want more rounded hole finish play with increase `Pocket sink` option. To tilt the drill bit to the other side just change the sign at `Pocket rotation`. The angle is `75` by default because pocket holes are drilled with `15` degree angle, so `90 - 75 = 15`. However, you can play with the `Pocket rotation` option as well.

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles008.png)

* Now click button for drilling and you have it:

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles009.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles010.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/DrillPocketHoles011.png)

**Video tutorials:** 
* [Pocket holes & realistic screws](https://www.youtube.com/watch?v=eXzYXNbWwqM)

## Realistic parts

### Realistic screws and pilot holes

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

### Realistic screws and angles

* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/sketch2dowel.png"> First you have to create angles or any other fixture and drill holes according to this procedure: [Pilot holes for angles, hinges](#pilot-holes-for-angles-hinges). If you have it, first select face of the element, and next all `Sketches` of the holes. This allow you to create dowels directly from `Sketches` with exact orientation and size. If you have it selected click [sketch2dowel](#sketch2dowel):

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles001.png)
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles002.png)

* For other element also first select face of the element, and next all `Sketches` of the holes. This allow you to create dowels directly from `Sketches` with exact orientation and size. If you have it selected click [sketch2dowel](#sketch2dowel):
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles003.png)
  
* <img align="left" width="50" height="50" src="https://raw.githubusercontent.com/dprojects/Woodworking/master/Icons/panel2link.png"> Now merge realistic screw with your current active document. You can create such screw with PartDesign or even order such realistic part. For this case I use [Screw 4 x 16 mm](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture#screw-4-x-16-mm) from [Fixture examples](https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture). The dowels applied before is some kind of references points and they can be replaced with realistic screws. To replace the fake screws with realistic screws. Select the realistic screw and next all the fake dowels. Next click [panel2link](#panel2link) icon:
  
  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles004.png)
  
* As you see the screws are above the holes. To hide them all, select the `Body` container of the base screw, and move it down as much you want, you can use [magicMove](#magicmove) for that with exact step: 

  ![img](https://raw.githubusercontent.com/dprojects/Woodworking/master/Docs/Screenshots/RealisticAngles005.png)

> [!IMPORTANT]
> I use a little bigger screws for angles than normally should be, because they hold things a little better than `3 x 20 mm` ones, so the head of the screw is not flat with the surface but you can use any screw size with the same way. For hinges you can use `3 x 20 mm`, without pilot holes.

**Video tutorials:** 
* [Angles, Pilot holes, Screws](https://www.youtube.com/watch?v=CYaL-sGvIK8)

### Realistic screws and pocket holes

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

### Counterbore 2x with bolt

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

<br><br>

## Raw wood, Lumber

Working with raw wood is difficult, it requires a lot of knowledge about different types of wood and experience. The wood must be properly seasoned, dried, and the proper grain direction must be maintained during gluing or joining. If not the wood will crack later when it starts working. I remember a bread cutting board bought in a shop that broke. It was made of beech wood and I assume it was made by experienced carpenters, but it cracked.

Wood is a natural product, therefore it is also difficult to predict the exact size. For this reason, raw real wood is a product that is not very practical and difficult to process. Currently, it has been replaced by prefabricated panels. Nowadays, nobody makes furniture entirely from raw real wood for everyday use. Even these expensive furniture, as if made of real raw wood, are built on prefabricated boards, MDF, plywood, and only the front parts are made of raw real oak wood. However, raw real wood is making a comeback as a luxurious, expensive and healthy product.

Working with raw wood is an art of some sort. This is the true form of working with wood, so it deserves to be supported by furniture design programs. However, computers have slightly different rules. Here it starts with the dimensions and not the order of operations. However, with the right approach some real wood operations can be simulated.

### Glued table top

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

<br><br>
