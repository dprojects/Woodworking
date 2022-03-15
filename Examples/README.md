# Woodworking at FreeCAD - fully parametric examples

Idea behind this examples folder is to have fully parametric furniture examples that can be quickly resized via `settings` spreadsheet and adopted to the current project. You can change any size at `settings` spreadsheet and the furniture will change dimensions automatically (in some cases recompute might be needed). Also, You can generate new report with new dimensions.

All the examples here should follow the rules:
* Fully parametric as much as possible.
* Should be built in the supported way by [getDimensions](https://github.com/dprojects/getDimensions) macro tool. 

This approach will be more useful for future projects than static examples, I guess.

**Note:** Storage boxes based on `Sketch` pattern (StorageBox_003+) are partially supported by [getDimensions](https://github.com/dprojects/getDimensions) macro tool. This is because there is [bug related to named constraints and expressions](https://forum.freecadweb.org/viewtopic.php?f=10&t=67042). If the bug will be solved all needed constraints will be named so You will be able to get `c - report type` as well. Now, You can check settings spreadsheet or automatic report for dimensions. Also, for Your project You can throw out expressions and name needed constraints. Named constraints works with values fine at FreeCAD. Good Luck, and Have Fun !

* [Furniture](#furniture)
	* [Bookcase_001](#bookcase_001)
	* [Cabinet_modular_001](#cabinet_modular_001)
	* [Drawer_001](#drawer_001)
	* [Table_001](#table_001)
* [Storage boxes](#storage-boxes)
	* [StorageBox_001](#storagebox_001) - Box Joint
	* [StorageBox_002](#storagebox_002) - Dovetail Joint simple
	* [StorageBox_003](#storagebox_003) - Dovetail Joint advanced
	* [StorageBox_004](#storagebox_004) - Pin Joint
	* [StorageBox_005](#storagebox_005) - Slot Joint
	* [StorageBox_006](#storagebox_006) - Love Joint
	* [StorageBox_007](#storagebox_007) - X, Sew Joint

# Furniture

## Bookcase_001

![Bookcase_001](https://raw.githubusercontent.com/dprojects/Woodworking/master/Examples/Screenshots/Bookcase_001.png)

## Cabinet_modular_001

![Cabinet_modular_001](https://raw.githubusercontent.com/dprojects/Woodworking/master/Examples/Screenshots/Cabinet_modular_001.png)

## Drawer_001

![Drawer_001](https://raw.githubusercontent.com/dprojects/Woodworking/master/Examples/Screenshots/Drawer_001.png)

## Table_001

![Table_001](https://raw.githubusercontent.com/dprojects/Woodworking/master/Examples/Screenshots/Table_001.png)

# Storage boxes

## StorageBox_001

![StorageBox_001](https://raw.githubusercontent.com/dprojects/Woodworking/master/Examples/Screenshots/StorageBox_001.png)

## StorageBox_002

![StorageBox_002](https://raw.githubusercontent.com/dprojects/Woodworking/master/Examples/Screenshots/StorageBox_002.png)

## StorageBox_003

![StorageBox_003](https://raw.githubusercontent.com/dprojects/Woodworking/master/Examples/Screenshots/StorageBox_003.png)

## StorageBox_004

![StorageBox_004](https://raw.githubusercontent.com/dprojects/Woodworking/master/Examples/Screenshots/StorageBox_004.png)

## StorageBox_005

![StorageBox_005](https://raw.githubusercontent.com/dprojects/Woodworking/master/Examples/Screenshots/StorageBox_005.png)

## StorageBox_006

![StorageBox_006](https://raw.githubusercontent.com/dprojects/Woodworking/master/Examples/Screenshots/StorageBox_006.png)

## StorageBox_007

![StorageBox_007](https://raw.githubusercontent.com/dprojects/Woodworking/master/Examples/Screenshots/StorageBox_007.png)
