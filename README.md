The Woodworking workbench started as a simple cut-list, as a macro for FreeCAD. However, Woodworking workbench now has so many additional tools, features and simplifications that it can be considered as a new CAD program based only on the FreeCAD kernel. The Woodworking workbench is mainly intended to make cabinet creation more simple, although it has many solutions to speed up and make more simple typical carpentry work and other CAD projects. I hope you will find something for yourself here.

**Key features:**
* Fast process of creating the main structure of the furniture with automatic recognition of the thickness of the elements, via [magicStart](https://github.com/dprojects/Woodworking/tree/master/Docs#how-to-start---magicstart) and other tools.
* Quick process of adding dowels and other mounting elements, screws, minifix via [magicDowels](https://github.com/dprojects/Woodworking/tree/master/Docs#magicdowels).
* Quick process of drilling holes according to the defined 32 mm furniture system via [magicDriller](https://github.com/dprojects/Woodworking/tree/master/Docs#magicdriller).
* Automatic parameterization on demend via [magicGlue](https://github.com/dprojects/Woodworking/tree/master/Docs#magicglue) tool, no Spreadsheet, no VarSet, no inventing mathematical formulas, no Assembly workbench needed.
* Automatic cut-list after design via [getDimensions](https://github.com/dprojects/Woodworking/tree/master/Docs#getdimensions) tool and export to format csv, json, html, markdown via [sheet2export](https://github.com/dprojects/Woodworking/tree/master/Docs#sheet2export).
* Full support for any metric system settings (inches, ft, mm) in all tools.

![intro](https://raw.githubusercontent.com/dprojects/media/master/intro.gif)

# Quick start

### Automatic for Linux

**Download and run installation package:** [magicCAD_1.0.AppImage](https://github.com/dprojects/Woodworking-package/releases/download/1.0/magicCAD_1.0.AppImage). 

> [!NOTE]
> This is experimental installation package with FreeCAD kernel and Woodworking workbench. 
> This `AppImage` will copy the Woodworking workbench into `~/.local/share/FreeCAD/Mod` folder, 
> will run the FreeCAD, and set the Woodworking workbench as default. 
> So you will be able to update later the Woodworking workbench via [debugInfo](https://github.com/dprojects/Woodworking/tree/master/Docs#debuginfo) tool.

### Manual steps

* **Step 0:** Download FreeCAD 1.0.1 [for Linux](https://github.com/FreeCAD/FreeCAD/releases/download/1.0.1/FreeCAD_1.0.1-conda-Linux-x86_64-py311.AppImage) or [for other OS](https://github.com/FreeCAD/FreeCAD/releases/tag/1.0.1)
* **Step 1:** Download [the latest Woodworking workbench version](https://github.com/dprojects/Woodworking/archive/refs/heads/master.zip)
* **Step 2:** Unpack Woodworking workbench to `Mod` folder.
* **Step 3:** Start FreeCAD.

> [!IMPORTANT]
> * The `README.md` file should be: `~/.local/share/FreeCAD/Mod/Woodworking/README.md` <br>
> * Read more about: [FreeCAD 1.0+ Support](https://github.com/dprojects/Woodworking/issues/49) <br>
> * For more details see: [Installation section at Woodworking workbench documentation](https://github.com/dprojects/Woodworking/tree/master/Docs#installation)

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

# License

FreeCAD is licensed under LGPL license but **Woodworking workbench is licensed under [MIT](https://github.com/dprojects/Woodworking/blob/master/LICENSE) license, only with the copyright preserved**. I can relese Woodworking workbench with any license because I use FreeCAD only as library, only as kernel. 

In my opinion, LGPL not allows you to earn from your additional work. Anything you change or add to LGPL code need to be licesend under LGPL license as well, so you cannot sell it. MIT license supports talented developers and allows them to earn, sell their work based on the MIT project. 

But **you always need to keep the note about real author**. You should never claim you invented Woodworking workbench or any MIT or LGPL projects, that's the author's rights.

### What you can

**For example:**

* You can change the Woodworking workbench code and sell it but you have to add info what is invented by you and what is not, just keep the license, or add info about your changes to the license, so will be fine.
* You can create your own YouTube or real life tutorials, voice over to existing ones, and earn, it is your hard work so you don't have to ask, but during tutorials you cannot say you invented Woodworking workbench or its features.
* You can translate Woodworking Workbench to any language and even sell such translation to anyone, it is your work, but you cannot say the Woodworking workbench is created by you. 

### What you cannot

**For example:**

* You cannot copy Woodworking workbench, or its features, to FreeCAD main branch without note about real author, and even get FPA grants for it. It is illegal, you can be sued, but also it is very bad behaviour, typical rats and thief strategy. 
* You cannot claim anywhere you invented Woodworking workbench or its features. If you add or change any code, you can say it only about your work.

> [!NOTE]
> Currently there are no plans to introduce a fee for using these additional tools. 
> I guess I will keep this repository with MIT forever. 
> If there will be paid version this will be new repository, new project.
> If you have still doubts, you can always open issue and ask.

# Contact

For questions, feature requests, please open issue at: [github.com/dprojects/Woodworking/issues](https://github.com/dprojects/Woodworking/issues)


|   |   |
|---|---|
| [![c1r1](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r1.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r1.png) | [![c2r1](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r1.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r1.png) |
| [![c1r2](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r2.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r2.png) | [![c2r2](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r2.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r2.png) |
| [![c1r3](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r3.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r3.png) | [![c2r3](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r3.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r3.png) |
| [![c1r4](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r4.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r4.png) | [![c2r4](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r4.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r4.png) |
| [![c1r5](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r5.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r5.png) | [![c2r5](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r5.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r5.png) |
| [![c1r6](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r6.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c1r6.png) | [![c2r6](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r6.png)](https://raw.githubusercontent.com/dprojects/Woodworking/master/Screenshots/matrix/c2r6.png) |
