import FreeCAD, FreeCADGui 
from PySide import QtGui, QtCore
import os, sys

import MagicPanels

translate = FreeCAD.Qt.translate

# ############################################################################
# Global definitions
# ############################################################################

# add new items only at the end and change self.sModeList
getMenuIndex = {
	translate('magicStart', 'Simple storage ( front outside, back full )'): 0, 
	translate('magicStart', 'Simple bookcase ( no front, back HDF )'): 1, 
	translate('magicStart', 'Bookcase ( import parametric )'): 2, 
	translate('magicStart', 'Simple drawer ( import parametric )'): 3, 
	translate('magicStart', 'Simple chair ( import parametric )'): 4, 
	translate('magicStart', 'Picture frame ( import parametric )'): 5, 
	translate('magicStart', 'Simple table ( import parametric )'): 6, 
	translate('magicStart', 'Storage box ( import parametric )'): 7, 
	translate('magicStart', 'Dowel 8x35 mm ( import parametric )'): 8, 
	translate('magicStart', 'Screw 4x40 mm ( import parametric )'): 9, 
	translate('magicStart', 'Modular storage ( front outside, 3 modules )'): 10, 
	translate('magicStart', 'Screw 3x20 mm for HDF ( import parametric )'): 11, 
	translate('magicStart', 'Screw 5x50 mm ( import parametric )'): 12, 
	translate('magicStart', 'Counterbore 2x 5x60 mm ( import parametric )'): 13, 
	translate('magicStart', 'Shelf Pin 5x16 mm ( import parametric )'): 14, 
	translate('magicStart', 'Angle 40x40x100 mm ( import parametric )'): 15, 
	translate('magicStart', 'Foot ( good for cleaning )'): 16, 
	translate('magicStart', 'Foot ( standard )'): 17, 
	translate('magicStart', 'Foot ( more stable )'): 18, 
	translate('magicStart', 'Foot ( decorated )'): 19, 
	translate('magicStart', 'Foot ( chair style )'): 20, 
	translate('magicStart', 'Drawer with front outside'): 21, 
	translate('magicStart', 'Drawer with front inside'): 22, 
	translate('magicStart', 'Front outside'): 23, 
	translate('magicStart', 'Front inside'): 24, 
	translate('magicStart', 'Shelf'): 25, 
	translate('magicStart', 'Center side'): 26, 
	translate('magicStart', 'Simple storage ( front outside, back HDF )'): 27, 
	translate('magicStart', 'Simple storage ( front inside, back full )'): 28, 
	translate('magicStart', 'Simple storage ( front inside, back HDF )'): 29, 
	translate('magicStart', 'Drawer series with front outside'): 30, 
	translate('magicStart', 'Drawer series with front inside'): 31, 
	translate('magicStart', 'Face Frame outside ( frame around )'): 32, 
	translate('magicStart', 'Face Frame outside ( frame with center )'): 33, 
	translate('magicStart', 'Face Frame outside ( frame for custom changes )'): 34, 
	translate('magicStart', 'Simple bookcase ( face frame, no front, back HDF )'): 35, 
	translate('magicStart', 'Simple storage ( face frame, no front, back HDF )'): 36, 
	translate('magicStart', 'Front outside with glass ( simple frame )'): 37, 
	translate('magicStart', 'Front outside with glass ( frame with decoration )'): 38, 
	translate('magicStart', 'Front inside with glass ( simple frame )'): 39, 
	translate('magicStart', 'Front inside with glass ( frame with decoration )'): 40, 
	translate('magicStart', 'Shelf series with equal space'): 41, 
	translate('magicStart', 'Table ( kitchen simple style )'): 42, 
	translate('magicStart', 'Table ( coffee simple style )'): 43, 
	translate('magicStart', 'Table ( kitchen modern style )'): 44, 
	translate('magicStart', 'Table ( coffee modern style )'): 45, 
	translate('magicStart', 'Table ( kitchen decorated style )'): 46, 
	translate('magicStart', 'Table ( coffee decorated style )'): 47, 
	translate('magicStart', 'Side'): 48, 
	translate('magicStart', 'Biscuits 4x16x48 mm ( import parametric )'): 49, 
	translate('magicStart', 'Biscuits 4x21x54 mm ( import parametric )'): 50, 
	translate('magicStart', 'Biscuits 4x24x57 mm ( import parametric )'): 51, 
	translate('magicStart', 'Pocket screw 4x40 mm ( import parametric )'): 52, 
	translate('magicStart', 'Angle 30x30x25 mm ( import parametric )'): 53, 
	translate('magicStart', 'Angle 80x80x20 mm ( import parametric )'): 54, 
	translate('magicStart', 'Front right (decoration, import parametric )'): 55, 
	translate('magicStart', 'Front left (decoration, import parametric )'): 56, 
	translate('magicStart', 'Top (decoration, import parametric )'): 57, 
	translate('magicStart', 'Drawer (decoration, import parametric )'): 58 # no comma 
}

# ############################################################################
# Qt Main
# ############################################################################

def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# globals with self.
		# ############################################################################
		
		gFSX = 500   # furniture size X (width)
		gFSY = 400   # furniture size Y (depth)
		gFSZ = 760   # furniture size Z (height)
		gThick = 18  # wood thickness
		
		gSelectedFurniture = "F0"
		gColor = (0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 0.0)
		gR = FreeCAD.Rotation(0, 0, 0)
		
		gSingleDrawerPlane = "X"
		gSingleDrawerDirection = "+"
		
		gSideEdgePlane = "X"
		gSideDirection = "+"
		
		toolSW = 0
		toolSH = 0
		gPW = 0
		gPH = 0
		
		# ############################################################################
		# help info
		# ############################################################################

		# ############################################################################
		gHelpInfoF0 = "" 
		gHelpInfoF0 += translate('magicStart', 'To pre-calculate the starting point for creating the furniture and its dimensions, select one of the options 1, 2, 3, or 4, fill in the "Wood thickness" and, if necessary, "Offset XYZ" fields, if the furniture is to have an offset relative to the selected edge, vertex or plane, and then press the "calculate furniture" button.') + '<br><br>'
		gHelpInfoF0 += '<ul>'
		gHelpInfoF0 += '<li><b>'
		gHelpInfoF0 += translate('magicStart', 'X edge') + '</b>: '
		gHelpInfoF0 += translate('magicStart', 'means any edge along the X coordinate axis. In this case, the starting point will be the vertex of the edge and the width of the furniture will be the length of the edge.')
		gHelpInfoF0 += '</li>'
		gHelpInfoF0 += '<li><b>'
		gHelpInfoF0 += translate('magicStart', 'XY face') + '</b>: '
		gHelpInfoF0 += translate('magicStart', 'means the plane on the object along the X and Y coordinate axes, i.e. horizontal, such as the top of the object, to create the next furniture module on top. In this case, the width of the furniture and its depth will be calculated from the selected plane so that the furniture is in line with the previous identical module.')
		gHelpInfoF0 += '</li>'
		gHelpInfoF0 += '<li><b>'
		gHelpInfoF0 += translate('magicStart', 'Vertex') + '</b>: '
		gHelpInfoF0 += translate('magicStart', 'means selecting any vertex of the object. In this case, only the starting point for creating the furniture will be calculated.')
		gHelpInfoF0 += '</li>'
		gHelpInfoF0 += '</ul>'
		gHelpInfoF0 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')
		
		# ############################################################################
		gHelpInfoF16 = "" 
		gHelpInfoF16 += '<ul>'
		gHelpInfoF16 += '<li><b>'
		gHelpInfoF16 += translate('magicStart', 'Furniture width') + '</b>: '
		gHelpInfoF16 += translate('magicStart', 'means the width of the furniture for which the base is to be created. This means the size of the furniture in the direction of the X coordinate axis.')
		gHelpInfoF16 += '</li>'
		gHelpInfoF16 += '<li><b>'
		gHelpInfoF16 += translate('magicStart', 'Furniture depth') + '</b>: '
		gHelpInfoF16 += translate('magicStart', 'means the depth of the furniture for which the base is to be created. This means the size of the furniture in the direction of the Y coordinate axis.')
		gHelpInfoF16 += '</li>'
		gHelpInfoF16 += '<li><b>'
		gHelpInfoF16 += translate('magicStart', 'Foot height') + '</b>: '
		gHelpInfoF16 += translate('magicStart', 'means the height of the base to be created, i.e. the size of the base in the direction of the Z coordinate axis.')
		gHelpInfoF16 += '</li>'
		gHelpInfoF16 += '<li><b>'
		gHelpInfoF16 += translate('magicStart', 'Foot thickness') + '</b>: '
		gHelpInfoF16 += translate('magicStart', 'means the thickness of the elements from which the base will be created, i.e. the thickness of the wood.')
		gHelpInfoF16 += '</li>'
		gHelpInfoF16 += '<li><b>'
		gHelpInfoF16 += translate('magicStart', 'Front offset') + '</b>: '
		gHelpInfoF16 += translate('magicStart', 'means the distance from the front, i.e. in the direction of the Y coordinate axis.')
		gHelpInfoF16 += '</li>'
		gHelpInfoF16 += '</ul>'
		gHelpInfoF16 += translate('magicStart', 'The foot will be created at the starting position of the XYZ coordinate axis taking into account the height of the foot.')

		# ############################################################################
		gHelpInfoF21 = "" 
		gHelpInfoF21 += '<ul>'
		gHelpInfoF21 += '<li><b>'
		gHelpInfoF21 += translate('magicStart', 'top edge') + '</b>: '
		gHelpInfoF21 += translate('magicStart', 'The drawer will be created from the 0 position on the Z coordinate axis to the position of the selected top edge. The width of the drawer will be taken from the selected top edge size. The depth of the drawer will be taken from the object from the selected top edge. This is a kind of "quick shot" to create the drawer as quickly as possible without a long selection.')
		gHelpInfoF21 += '</li>'
		gHelpInfoF21 += '<li><b>'
		gHelpInfoF21 += translate('magicStart', 'top edge + back face') + '</b>: '
		gHelpInfoF21 += translate('magicStart', 'This is the same as above, but here selecting the back face allows you to set the depth in a more detailed way.')
		gHelpInfoF21 += '</li>'
		gHelpInfoF21 += '<li><b>'
		gHelpInfoF21 += translate('magicStart', 'bottom edge + top edge') + '</b>: '
		gHelpInfoF21 += translate('magicStart', 'The drawer will be created from the position of the first selected bottom edge to the position of the second selected top edge. The width and depth of the drawer will be taken from the object with the shortest edge. This is a kind of "quick shot" to create the drawer quickly without a long selection.')
		gHelpInfoF21 += '</li>'
		gHelpInfoF21 += '<li><b>'
		gHelpInfoF21 += translate('magicStart', 'bottom edge + top edge + back face') + '</b>: '
		gHelpInfoF21 += translate('magicStart', 'This is the same as above, but here selecting the back face allows you to set the depth in a more detailed way.')
		gHelpInfoF21 += '</li>'
		gHelpInfoF21 += '<li><b>'
		gHelpInfoF21 += translate('magicStart', 'bottom edge + top edge + left edge + right edge + back face') + '</b>: '
		gHelpInfoF21 += translate('magicStart', 'The drawer will be created from the position of the first selected bottom edge to the position of the second selected top edge. The width of the drawer will be obtained from the difference of the third and fourth selected edges. The depth of the drawer will be obtained from the selected back face. There are many more objects to select here, but this is the most precise version of determining the size of the drawer. So if you have trouble with any of the above, I recommend trying this method. Also this method solves the problem with longest bottom and top edges.')
		gHelpInfoF21 += '</li>'
		gHelpInfoF21 += '</ul>'
		gHelpInfoF21 += translate('magicStart', 'The edges can be in line with the X or Y coordinate axis, so the drawer can be created on all four sides of the furniture.')

		# ############################################################################
		gHelpInfoF23 = "" 
		gHelpInfoF23 += translate('magicStart', 'To initially calculate the starting point of the front and its dimensions, make selection, fill in the appropriate fields and click the "calculate front" button.')
		gHelpInfoF23 += '<ul>'
		gHelpInfoF23 += '<li><b>'
		gHelpInfoF23 += translate('magicStart', 'X bottom edge') + '</b>: '
		gHelpInfoF23 += translate('magicStart', 'means the inner bottom edge of the shelf or floor of the furniture along the X coordinate axis.')
		gHelpInfoF23 += '</li>'
		gHelpInfoF23 += '<li><b>'
		gHelpInfoF23 += translate('magicStart', 'X top edge') + '</b>: '
		gHelpInfoF23 += translate('magicStart', 'means the inner top edge of the shelf or top of the furniture along the X coordinate axis.')
		gHelpInfoF23 += '</li>'
		gHelpInfoF23 += '<li><b>'
		gHelpInfoF23 += translate('magicStart', 'Z left edge') + '</b>: '
		gHelpInfoF23 += translate('magicStart', 'means the inner left edge of the side of the furniture along the Z coordinate axis.')
		gHelpInfoF23 += '</li>'
		gHelpInfoF23 += '<li><b>'
		gHelpInfoF23 += translate('magicStart', 'Z right edge') + '</b>: '
		gHelpInfoF23 += translate('magicStart', 'means the inner right edge of the side of the furniture along the Z coordinate axis.')
		gHelpInfoF23 += '</li>'
		gHelpInfoF23 += '<li><b>'
		gHelpInfoF23 += translate('magicStart', 'Front thickness') + '</b>: '
		gHelpInfoF23 += translate('magicStart', 'means the thickness of the front, in line with the Y coordinate axis.')
		gHelpInfoF23 += '</li>'
		gHelpInfoF23 += '<li><b>'
		gHelpInfoF23 += translate('magicStart', 'Front offsets') + '</b>: '
		gHelpInfoF23 += translate('magicStart', 'in the case of an external front, it means how much the front will overlap the furniture, and in the case of an internal front, it means how big the gap will be between the front and the remaining parts of the furniture.')
		gHelpInfoF23 += '</li>'
		gHelpInfoF23 += '</ul>'
		gHelpInfoF23 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')

		# ############################################################################
		gHelpInfoF25 = "" 
		gHelpInfoF25 += translate('magicStart', 'To initially calculate the starting point of the shelf and its dimensions, make selection, fill in the appropriate fields and click the "calculate shelf" button. To calculate a shelf, you need to select the two side edges of the space where the shelf is to be placed and the back face of the gap to determine the shelf depth. There are two ways to create a shelf:')
		gHelpInfoF25 += '<ul>'
		gHelpInfoF25 += '<li><b>'
		gHelpInfoF25 += translate('magicStart', 'Method 1') + '</b>: '
		gHelpInfoF25 += translate('magicStart', 'By setting the shelf depth, then the front gap will be calculated as the difference between the free space and the desired shelf depth.')
		gHelpInfoF25 += '</li>'
		gHelpInfoF25 += '<li><b>'
		gHelpInfoF25 += translate('magicStart', 'Method 2') + '</b>: '
		gHelpInfoF25 += translate('magicStart', 'By entering a value of 0 as the depth and setting the offsets for the shelf. Then the depth and width of the shelf will be calculated taking into account the given offsets.')
		gHelpInfoF25 += '</li>'
		gHelpInfoF25 += '</ul>'
		gHelpInfoF25 += translate('magicStart', 'Meaning:')
		gHelpInfoF25 += '<ul>'
		gHelpInfoF25 += '<li><b>'
		gHelpInfoF25 += translate('magicStart', 'Z left edge') + '</b>: '
		gHelpInfoF25 += translate('magicStart', 'means the left inner edge of the side of the furniture in line with the Z coordinate axis, i.e. vertical.')
		gHelpInfoF25 += '</li>'
		gHelpInfoF25 += '<li><b>'
		gHelpInfoF25 += translate('magicStart', 'Z right edge') + '</b>: '
		gHelpInfoF25 += translate('magicStart', 'means the right inner edge of the side of the furniture in line with the Z coordinate axis, i.e. vertical.')
		gHelpInfoF25 += '</li>'
		gHelpInfoF25 += '<li><b>'
		gHelpInfoF25 += translate('magicStart', 'back face') + '</b>: '
		gHelpInfoF25 += translate('magicStart', 'means the inner plane of the back wall of the furniture. The plane should be in line with the X and Z coordinate axes.')
		gHelpInfoF25 += '</li>'
		gHelpInfoF25 += '<li><b>'
		gHelpInfoF25 += translate('magicStart', 'Shelf thickness') + '</b>: '
		gHelpInfoF25 += translate('magicStart', 'means the thickness of the shelf, i.e. in the direction of the Z coordinate axis.')
		gHelpInfoF25 += '</li>'
		gHelpInfoF25 += '</ul>'
		gHelpInfoF25 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')

		# ############################################################################
		gHelpInfoF26 = "" 
		gHelpInfoF26 += translate('magicStart', 'To initially calculate the starting point of the center side and its dimensions, make selection, fill in the appropriate fields and click the "calculate center side" button. There are two ways of selection:')
		gHelpInfoF26 += '<ul>'
		gHelpInfoF26 += '<li><b>'
		gHelpInfoF26 += translate('magicStart', 'Method 1') + '</b>: '
		gHelpInfoF26 += translate('magicStart', 'X top left edge + X top right edge + XY bottom face')
		gHelpInfoF26 += '</li>'
		gHelpInfoF26 += '<li><b>'
		gHelpInfoF26 += translate('magicStart', 'Method 2') + '</b>: '
		gHelpInfoF26 += translate('magicStart', 'X bottom left edge + X bottom right edge + XY top face')
		gHelpInfoF26 += '</li>'
		gHelpInfoF26 += '</ul>'
		gHelpInfoF26 += translate('magicStart', 'There are two ways to create a center side:')
		gHelpInfoF26 += '<ul>'
		gHelpInfoF26 += '<li><b>'
		gHelpInfoF26 += translate('magicStart', 'Method 1') + '</b>: '
		gHelpInfoF26 += translate('magicStart', 'By setting the side depth, then the front gap will be calculated as the difference between the free space and the desired side depth.')
		gHelpInfoF26 += '</li>'
		gHelpInfoF26 += '<li><b>'
		gHelpInfoF26 += translate('magicStart', 'Method 2') + '</b>: '
		gHelpInfoF26 += translate('magicStart', 'By entering a value of 0 as the depth and setting the offsets for the side. Then the depth and height of the center side will be calculated taking into account the given offsets.')
		gHelpInfoF26 += '</li>'
		gHelpInfoF26 += '</ul>'
		gHelpInfoF26 += translate('magicStart', 'Meaning:')
		gHelpInfoF26 += '<ul>'
		gHelpInfoF26 += '<li><b>'
		gHelpInfoF26 += translate('magicStart', 'Y left edge') + '</b>: '
		gHelpInfoF26 += translate('magicStart', 'means the left inner edge of the side of the furniture in line with the Y coordinate axis.')
		gHelpInfoF26 += '</li>'
		gHelpInfoF26 += '<li><b>'
		gHelpInfoF26 += translate('magicStart', 'Y right edge') + '</b>: '
		gHelpInfoF26 += translate('magicStart', 'means the right inner edge of the side of the furniture in line with the Y coordinate axis.')
		gHelpInfoF26 += '</li>'
		gHelpInfoF26 += '<li><b>'
		gHelpInfoF26 += translate('magicStart', 'XY face') + '</b>: '
		gHelpInfoF26 += translate('magicStart', 'means the inner plane of the gap, for example top or bottom surface of the shelf. The plane should be in line with the X and Y coordinate axes.')
		gHelpInfoF26 += '</li>'
		gHelpInfoF26 += '<li><b>'
		gHelpInfoF26 += translate('magicStart', 'Side thickness') + '</b>: '
		gHelpInfoF26 += translate('magicStart', 'means the thickness of the center side, i.e. in the direction of the X coordinate axis.')
		gHelpInfoF26 += '</li>'
		gHelpInfoF26 += '</ul>'
		gHelpInfoF26 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')

		# ############################################################################
		gHelpInfoF30 = "" 
		gHelpInfoF30 += translate('magicStart', 'To pre-calculate the starting point for series of drawers and its dimensions, make selection, fill desired fields and press the "calculate gaps" button.')
		gHelpInfoF30 += '<ul>'
		gHelpInfoF30 += '<li><b>'
		gHelpInfoF30 += translate('magicStart', 'X bottom edge') + '</b>: '
		gHelpInfoF30 += translate('magicStart', 'means the bottom edge in line with the X coordinate axis of the free space where you want to create a series of drawers, i.e. the horizontal edge of the bottom shelf.')
		gHelpInfoF30 += '</li>'
		gHelpInfoF30 += '<li><b>'
		gHelpInfoF30 += translate('magicStart', 'X top edge') + '</b>: '
		gHelpInfoF30 += translate('magicStart', 'means the top edge in line with the X coordinate axis of the free space where you want to create a series of drawers, i.e. the horizontal edge of the top shelf.')
		gHelpInfoF30 += '</li>'
		gHelpInfoF30 += '<li><b>'
		gHelpInfoF30 += translate('magicStart', 'Z left edge') + '</b>: '
		gHelpInfoF30 += translate('magicStart', 'means the left edge in line with the Z coordinate axis of the free space where you want to create a series of drawers, i.e. the vertical edge of the left side.')
		gHelpInfoF30 += '</li>'
		gHelpInfoF30 += '<li><b>'
		gHelpInfoF30 += translate('magicStart', 'Z right edge') + '</b>: '
		gHelpInfoF30 += translate('magicStart', 'means the right edge in line with the Z coordinate axis of the free space where you want to create a series of drawers, i.e. the vertical edge of the right side.')
		gHelpInfoF30 += '</li>'
		gHelpInfoF30 += '<li><b>'
		gHelpInfoF30 += translate('magicStart', 'back face') + '</b>: '
		gHelpInfoF30 += translate('magicStart', 'means the inner plane of the back wall of the furniture. The plane should be in line with the X and Z coordinate axes, i.e. vertical faced to the front.')
		gHelpInfoF30 += '</li>'
		gHelpInfoF30 += '<li><b>'
		gHelpInfoF30 += translate('magicStart', 'Wood thickness') + '</b>: '
		gHelpInfoF30 += translate('magicStart', 'means the thickness of the wood from which the walls and the front of the drawer will be made.')
		gHelpInfoF30 += '</li>'
		gHelpInfoF30 += '<li><b>'
		gHelpInfoF30 += translate('magicStart', 'Space between drawers') + '</b>: '
		gHelpInfoF30 += translate('magicStart', 'this is additional space between drawer fronts and drawers so that drawer fronts do not rub against each other.')
		gHelpInfoF30 += '</li>'
		gHelpInfoF30 += '<li><b>'
		gHelpInfoF30 += translate('magicStart', 'Drawer system offsets') + '</b>: '
		gHelpInfoF30 += translate('magicStart', 'these are the distances that must be taken into account when installing the drawer system rail. The most important is "Sides" for side guides.')
		gHelpInfoF30 += '</li>'
		gHelpInfoF30 += '</ul>'
		gHelpInfoF30 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')

		# ############################################################################
		gHelpInfoF32 = "" 
		gHelpInfoF32 += translate('magicStart', 'To pre-calculate the starting point for Face Frame and its dimensions, make selection, fill desired fields and press the "calculate Face Frame" button.')
		gHelpInfoF32 += '<ul>'
		gHelpInfoF32 += '<li><b>'
		gHelpInfoF32 += translate('magicStart', 'X bottom edge') + '</b>: '
		gHelpInfoF32 += translate('magicStart', 'means the inner edge of the furniture floor in line with the X coordinate axis.')
		gHelpInfoF32 += '</li>'
		gHelpInfoF32 += '<li><b>'
		gHelpInfoF32 += translate('magicStart', 'X top edge') + '</b>: '
		gHelpInfoF32 += translate('magicStart', 'means the inner edge of the top of the furniture in line with the X coordinate axis.')
		gHelpInfoF32 += '</li>'
		gHelpInfoF32 += '<li><b>'
		gHelpInfoF32 += translate('magicStart', 'Z left edge') + '</b>: '
		gHelpInfoF32 += translate('magicStart', 'means the inner edge of the left side of the furniture in line with the Z coordinate axis.')
		gHelpInfoF32 += '</li>'
		gHelpInfoF32 += '<li><b>'
		gHelpInfoF32 += translate('magicStart', 'Z right edge') + '</b>: '
		gHelpInfoF32 += translate('magicStart', 'means the inner edge of the right side of the furniture in line with the Z coordinate axis.')
		gHelpInfoF32 += '</li>'
		gHelpInfoF32 += '<li><b>'
		gHelpInfoF32 += translate('magicStart', 'Single bar width') + '</b>: '
		gHelpInfoF32 += translate('magicStart', 'means the width of the beam from which the Face Frame will be built, in line with the X coordinate axis.')
		gHelpInfoF32 += '</li>'
		gHelpInfoF32 += '<li><b>'
		gHelpInfoF32 += translate('magicStart', 'Single bar thickness') + '</b>: '
		gHelpInfoF32 += translate('magicStart', 'means the thickness of the beam from which the Face Frame will be built, in line with the Y coordinate axis.')
		gHelpInfoF32 += '</li>'
		gHelpInfoF32 += '<li><b>'
		gHelpInfoF32 += translate('magicStart', 'Lip outside') + '</b>: '
		gHelpInfoF32 += translate('magicStart', 'means how much the Face Frame will protrude outside the furniture.')
		gHelpInfoF32 += '</li>'
		gHelpInfoF32 += '<li><b>'
		gHelpInfoF32 += translate('magicStart', 'Delve into furniture') + '</b>: '
		gHelpInfoF32 += translate('magicStart', 'means sinking the Face Frame towards the furniture, i.e. in the direction of the Y coordinate axis. This allows you to take into account a possible groove, thanks to which the Face Frame can be placed on the edges of the furniture, which will stiffen the entire structure of the furniture.')
		gHelpInfoF32 += '</li>'
		gHelpInfoF32 += '</ul>'
		gHelpInfoF32 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')
		
		# ############################################################################
		gHelpInfoF37 = "" 
		gHelpInfoF37 += translate('magicStart', 'To pre-calculate the starting point for the Front with glass and its dimensions, make selection, fill in the required fields and press the "calculate front with glass" button.')
		gHelpInfoF37 += '<ul>'
		gHelpInfoF37 += '<li><b>'
		gHelpInfoF37 += translate('magicStart', 'X bottom edge') + '</b>: '
		gHelpInfoF37 += translate('magicStart', 'means the inner bottom edge of the space, in line with the X coordinate axis.')
		gHelpInfoF37 += '</li>'
		gHelpInfoF37 += '<li><b>'
		gHelpInfoF37 += translate('magicStart', 'X top edge') + '</b>: '
		gHelpInfoF37 += translate('magicStart', 'means the inner top edge of the space, in line with the X coordinate axis.')
		gHelpInfoF37 += '</li>'
		gHelpInfoF37 += '<li><b>'
		gHelpInfoF37 += translate('magicStart', 'Z left edge') + '</b>: '
		gHelpInfoF37 += translate('magicStart', 'means the inner left edge of the space, in line with the Z coordinate axis.')
		gHelpInfoF37 += '</li>'
		gHelpInfoF37 += '<li><b>'
		gHelpInfoF37 += translate('magicStart', 'Z right edge') + '</b>: '
		gHelpInfoF37 += translate('magicStart', 'means the inner right edge of the space, in line with the Z coordinate axis.')
		gHelpInfoF37 += '</li>'
		gHelpInfoF37 += '<li><b>'
		gHelpInfoF37 += translate('magicStart', 'Wood thickness') + '</b>: '
		gHelpInfoF37 += translate('magicStart', 'means the thickness of the beam of the frame, in line with the Y coordinate axis.')
		gHelpInfoF37 += '</li>'
		gHelpInfoF37 += '<li><b>'
		gHelpInfoF37 += translate('magicStart', 'Overlap horizontal') + '</b>: '
		gHelpInfoF37 += translate('magicStart', 'in the case of an outside front, this is the width by which the glass front will overlap the furniture elements. If the front is to cover the entire surface, set the same value as Wood thickness.')
		gHelpInfoF37 += '</li>'
		gHelpInfoF37 += '<li><b>'
		gHelpInfoF37 += translate('magicStart', 'Overlap vertical') + '</b>: '
		gHelpInfoF37 += translate('magicStart', 'in the case of an outside front, this is the height by which the glass front will overlap the furniture elements. If the front is to cover the entire surface, set the same value as Wood thickness.')
		gHelpInfoF37 += '</li>'
		gHelpInfoF37 += '<li><b>'
		gHelpInfoF37 += translate('magicStart', 'Offset horizontal') + '</b>: '
		gHelpInfoF37 += translate('magicStart', 'in the case of an inside front, this is the width of the gap between the front frame and the furniture elements.')
		gHelpInfoF37 += '</li>'
		gHelpInfoF37 += '<li><b>'
		gHelpInfoF37 += translate('magicStart', 'Offset vertical') + '</b>: '
		gHelpInfoF37 += translate('magicStart', 'in the case of an inside front, this is the height of the gap between the front frame and the furniture elements.')
		gHelpInfoF37 += '</li>'
		gHelpInfoF37 += '<li><b>'
		gHelpInfoF37 += translate('magicStart', 'Glass thickness') + '</b>: '
		gHelpInfoF37 += translate('magicStart', 'means the thickness of the glass, in line with the Y coordinate axis.')
		gHelpInfoF37 += '</li>'
		gHelpInfoF37 += '</ul>'
		gHelpInfoF37 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')

		# ############################################################################
		gHelpInfoF41 = "" 
		gHelpInfoF41 += translate('magicStart', 'To pre-calculate the starting point for shelf series and its dimensions, make selection, fill desired fields and press the "calculate shelf series" button.')
		gHelpInfoF41 += '<ul>'
		gHelpInfoF41 += '<li><b>'
		gHelpInfoF41 += translate('magicStart', 'X bottom edge') + '</b>: '
		gHelpInfoF41 += translate('magicStart', 'means the lower inner edge from which the series of shelves is to start. The selected edge should be in line with the X coordinate axis.')
		gHelpInfoF41 += '</li>'
		gHelpInfoF41 += '<li><b>'
		gHelpInfoF41 += translate('magicStart', 'X top edge') + '</b>: '
		gHelpInfoF41 += translate('magicStart', 'means the upper inner edge to which the series of shelves is to end. The selected edge should be in line with the X coordinate axis.')
		gHelpInfoF41 += '</li>'
		gHelpInfoF41 += '<li><b>'
		gHelpInfoF41 += translate('magicStart', 'Z left edge') + '</b>: '
		gHelpInfoF41 += translate('magicStart', 'means the left inner edge of the free space in which the series of shelves is to be created. The selected edge should be in line with the Z coordinate axis, i.e. the inner edge of the left side of the furniture.')
		gHelpInfoF41 += '</li>'
		gHelpInfoF41 += '<li><b>'
		gHelpInfoF41 += translate('magicStart', 'Z right edge') + '</b>: '
		gHelpInfoF41 += translate('magicStart', 'means the right inner edge of the free space in which the series of shelves is to be created. The selected edge should be in line with the Z coordinate axis, i.e. the inner edge of the right side of the furniture.')
		gHelpInfoF41 += '</li>'
		gHelpInfoF41 += '<li><b>'
		gHelpInfoF41 += translate('magicStart', 'back face') + '</b>: '
		gHelpInfoF41 += translate('magicStart', 'means the internal surface of the back wall of the furniture, which is in line with the X and Z coordinate axes.')
		gHelpInfoF41 += '</li>'
		gHelpInfoF41 += '<li><b>'
		gHelpInfoF41 += translate('magicStart', 'Single shelf thickness') + '</b>: '
		gHelpInfoF41 += translate('magicStart', 'means the thickness of a single shelf, i.e. in the direction of the Z coordinate axis.')
		gHelpInfoF41 += '</li>'
		gHelpInfoF41 += '<li><b>'
		gHelpInfoF41 += translate('magicStart', 'Number of shelves') + '</b>: '
		gHelpInfoF41 += translate('magicStart', 'means the number of shelves to be created at equal distances.')
		gHelpInfoF41 += '</li>'
		gHelpInfoF41 += '</ul>'
		gHelpInfoF41 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')
		
		# ############################################################################
		gHelpInfoF42 = "" 
		gHelpInfoF42 += translate('magicStart', 'To pre-calculate the location where the table will be created, select any vertex and press the "calculate table position" button.')
		gHelpInfoF42 += '<ul>'
		gHelpInfoF42 += '<li><b>'
		gHelpInfoF42 += translate('magicStart', 'Table width X') + '</b>: '
		gHelpInfoF42 += translate('magicStart', 'means the width of the table, i.e. the size according to the X coordinate axis.')
		gHelpInfoF42 += '</li>'
		gHelpInfoF42 += '<li><b>'
		gHelpInfoF42 += translate('magicStart', 'Table depth Y') + '</b>: '
		gHelpInfoF42 += translate('magicStart', 'means the depth of the table, i.e. the size according to the Y coordinate axis.')
		gHelpInfoF42 += '</li>'
		gHelpInfoF42 += '<li><b>'
		gHelpInfoF42 += translate('magicStart', 'Table height Z') + '</b>: '
		gHelpInfoF42 += translate('magicStart', 'means the height of the table, i.e. the size according to the Z coordinate axis.')
		gHelpInfoF42 += '</li>'
		gHelpInfoF42 += '<li><b>'
		gHelpInfoF42 += translate('magicStart', 'Table top thickness') + '</b>: '
		gHelpInfoF42 += translate('magicStart', 'means the thickness of the table top, i.e. the size according to the Z coordinate axis.')
		gHelpInfoF42 += '</li>'
		gHelpInfoF42 += '<li><b>'
		gHelpInfoF42 += translate('magicStart', 'Legs and Supporters thickness') + '</b>: '
		gHelpInfoF42 += translate('magicStart', 'this is the thickness of the wood from which the table legs and the supporting beams under the top will be made.')
		gHelpInfoF42 += '</li>'
		gHelpInfoF42 += '<li><b>'
		gHelpInfoF42 += translate('magicStart', 'Table top offset') + '</b>: '
		gHelpInfoF42 += translate('magicStart', 'means the distance of the legs and supporting beams from the top. If the top is not to have protruding corners, the value 0 should be entered.')
		gHelpInfoF42 += '</li>'
		gHelpInfoF42 += '</ul>'
		gHelpInfoF42 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')
		
		# ############################################################################
		gHelpInfoF48 = ""
		gHelpInfoF48 += translate('magicStart', 'To create a side, you need to select 4 edges in the correct order around the free space where you want to create the side:')
		gHelpInfoF48 += '<ul>'
		gHelpInfoF48 += '<li><b>'
		gHelpInfoF48 += translate('magicStart', 'X or Y bottom edge') + '</b>: '
		gHelpInfoF48 += translate('magicStart', 'means that the selected edge is to be the bottom edge, along the X or Y coordinate axis.')
		gHelpInfoF48 += '</li>'
		gHelpInfoF48 += '<li><b>'
		gHelpInfoF48 += translate('magicStart', 'X or Y top edge') + '</b>: '
		gHelpInfoF48 += translate('magicStart', 'means that the selected edge is to be the top edge, along the X or Y coordinate axis.')
		gHelpInfoF48 += '</li>'
		gHelpInfoF48 += '<li><b>'
		gHelpInfoF48 += translate('magicStart', 'Z left edge') + '</b>: '
		gHelpInfoF48 += translate('magicStart', 'means that the selected edge is to be the left edge, along the Z coordinate axis, i.e. vertical.')
		gHelpInfoF48 += '</li>'
		gHelpInfoF48 += '<li><b>'
		gHelpInfoF48 += translate('magicStart', 'Z right edge') + '</b>: '
		gHelpInfoF48 += translate('magicStart', 'means that the selected edge is to be the right edge, along the Z coordinate axis, i.e. vertical.')
		gHelpInfoF48 += '</li>'
		gHelpInfoF48 += '</ul>'
		gHelpInfoF48 += translate('magicStart', 'Next, you need to decide how the side to be created is to be calculated. There are 3 cases:')
		gHelpInfoF48 += '<ul>'
		gHelpInfoF48 += '<li><b>'
		gHelpInfoF48 += translate('magicStart', '0 width and 0 offsets') + '</b>: '
		gHelpInfoF48 += translate('magicStart', 'If you do not fill the widths and gaps, the side will fill the entire selected space.')
		gHelpInfoF48 += '</li>'
		gHelpInfoF48 += '<li><b>'
		gHelpInfoF48 += translate('magicStart', 'custom width and 0 offsets') + '</b>: '
		gHelpInfoF48 += translate('magicStart', 'If a width is given, the right spacing will be the difference between the width of the free space and the previously set desired width.')
		gHelpInfoF48 += '</li>'
		gHelpInfoF48 += '<li><b>'
		gHelpInfoF48 += translate('magicStart', '0 width and custom offsets') + '</b>: '
		gHelpInfoF48 += translate('magicStart', 'If offsets are set and the width is set to 0, the width and height of the side to be created will be calculated with the offsets taken into account.')
		gHelpInfoF48 += '</li>'
		gHelpInfoF48 += '</ul>'

		# ############################################################################
		# init
		# ############################################################################

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):

			# ############################################################################
			# set screen
			# ############################################################################
			
			# tool screen size
			self.toolSW = 450
			self.toolSH = 570
			
			# active screen size - FreeCAD main window
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			self.gPW = 0 + 50
			self.gPH = int( gSH - self.toolSH ) - 30

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(self.gPW, self.gPH, self.toolSW, self.toolSH)
			self.setWindowTitle(translate('magicStart', 'magicStart'))
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - selection
			# ############################################################################
			
			row = 10
	
			# not write here, copy text from getMenuIndex to avoid typo
			self.sModeList = (
				translate('magicStart', 'Simple storage ( front outside, back full )'), 
				translate('magicStart', 'Simple storage ( front outside, back HDF )'), 
				translate('magicStart', 'Simple storage ( front inside, back full )'), 
				translate('magicStart', 'Simple storage ( front inside, back HDF )'),
				translate('magicStart', 'Simple storage ( face frame, no front, back HDF )'), 
				translate('magicStart', 'Simple bookcase ( no front, back HDF )'), 
				translate('magicStart', 'Simple bookcase ( face frame, no front, back HDF )'), 
				translate('magicStart', 'Modular storage ( front outside, 3 modules )'), 
				translate('magicStart', 'Drawer with front outside'), 
				translate('magicStart', 'Drawer with front inside'), 
				translate('magicStart', 'Drawer series with front outside'), 
				translate('magicStart', 'Drawer series with front inside'), 
				translate('magicStart', 'Face Frame outside ( frame around )'), 
				translate('magicStart', 'Face Frame outside ( frame with center )'), 
				translate('magicStart', 'Face Frame outside ( frame for custom changes )'), 
				translate('magicStart', 'Front outside'), 
				translate('magicStart', 'Front outside with glass ( simple frame )'), 
				translate('magicStart', 'Front outside with glass ( frame with decoration )'), 
				translate('magicStart', 'Front inside'), 
				translate('magicStart', 'Front inside with glass ( simple frame )'), 
				translate('magicStart', 'Front inside with glass ( frame with decoration )'), 
				translate('magicStart', 'Shelf'), 
				translate('magicStart', 'Shelf series with equal space'), 
				translate('magicStart', 'Side'), 
				translate('magicStart', 'Center side'), 
				translate('magicStart', 'Foot ( good for cleaning )'), 
				translate('magicStart', 'Foot ( standard )'), 
				translate('magicStart', 'Foot ( more stable )'), 
				translate('magicStart', 'Foot ( decorated )'), 
				translate('magicStart', 'Foot ( chair style )'), 
				translate('magicStart', 'Table ( kitchen simple style )'), 
				translate('magicStart', 'Table ( kitchen modern style )'), 
				translate('magicStart', 'Table ( kitchen decorated style )'), 
				translate('magicStart', 'Table ( coffee simple style )'), 
				translate('magicStart', 'Table ( coffee modern style )'), 
				translate('magicStart', 'Table ( coffee decorated style )'), 
				translate('magicStart', 'Dowel 8x35 mm ( import parametric )'),
				translate('magicStart', 'Biscuits 4x16x48 mm ( import parametric )'), 
				translate('magicStart', 'Biscuits 4x21x54 mm ( import parametric )'), 
				translate('magicStart', 'Biscuits 4x24x57 mm ( import parametric )'), 
				translate('magicStart', 'Screw 3x20 mm for HDF ( import parametric )'), 
				translate('magicStart', 'Screw 4x40 mm ( import parametric )'), 
				translate('magicStart', 'Screw 5x50 mm ( import parametric )'), 
				translate('magicStart', 'Pocket screw 4x40 mm ( import parametric )'), 
				translate('magicStart', 'Counterbore 2x 5x60 mm ( import parametric )'), 
				translate('magicStart', 'Shelf Pin 5x16 mm ( import parametric )'), 
				translate('magicStart', 'Angle 30x30x25 mm ( import parametric )'), 
				translate('magicStart', 'Angle 80x80x20 mm ( import parametric )'), 
				translate('magicStart', 'Angle 40x40x100 mm ( import parametric )'), 
				translate('magicStart', 'Front left (decoration, import parametric )'), 
				translate('magicStart', 'Front right (decoration, import parametric )'), 
				translate('magicStart', 'Top (decoration, import parametric )'), 
				translate('magicStart', 'Bookcase ( import parametric )'), 
				translate('magicStart', 'Simple drawer ( import parametric )'), 
				translate('magicStart', 'Drawer (decoration, import parametric )'), 
				translate('magicStart', 'Simple chair ( import parametric )'), 
				translate('magicStart', 'Picture frame ( import parametric )'), 
				translate('magicStart', 'Simple table ( import parametric )'), 
				translate('magicStart', 'Storage box ( import parametric )')   # no comma
				)
			
			helpButtonSize = 80
			
			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(0)
			self.sMode.activated[str].connect(self.selectedOption)
			self.sMode.setFixedWidth(self.toolSW - 20 - 10 - helpButtonSize)
			self.sMode.setFixedHeight(40)
			self.sMode.move(10, 10)

			# ############################################################################
			# help buttons and info screen
			# ############################################################################
			
			# button
			self.helpBSHOW = QtGui.QPushButton(translate('magicStart', 'HELP >'), self)
			self.helpBSHOW.clicked.connect(self.helpSHOW)
			self.helpBSHOW.setFixedWidth(helpButtonSize)
			self.helpBSHOW.setFixedHeight(40)
			self.helpBSHOW.move(self.toolSW - helpButtonSize - 10, 10)

			# button
			self.helpBHIDE = QtGui.QPushButton(translate('magicStart', '< HELP'), self)
			self.helpBHIDE.clicked.connect(self.helpHIDE)
			self.helpBHIDE.setFixedWidth(80)
			self.helpBHIDE.setFixedHeight(40)
			self.helpBHIDE.move(self.toolSW - helpButtonSize - 10, 10)
			self.helpBHIDE.hide()
			
			# label
			self.helpInfo = QtGui.QLabel(self.gHelpInfoF0, self)
			self.helpInfo.move(self.toolSW + 10, 10)
			self.helpInfo.setFixedWidth(self.toolSW - 90)
			self.helpInfo.setFixedHeight(self.toolSH - 20)
			self.helpInfo.setWordWrap(True)
			self.helpInfo.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.helpInfo.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

			# ############################################################################
			# custom row settings
			# ############################################################################

			row += 70
			
			createSize = 40
			createRow = self.toolSH - createSize - 10
			
			rowhelp = row - 20
			rowgap = row - 20
			rowds = row - 20
			rowfoot = row
			rowtbl = row - 20
			rowfront = row
			rowfglass = row - 20
			rowfframe = row - 20
			rowshelf = row
			rowsseries = row - 20
			rowcside = row
			rowside = row - 20

			# ############################################################################
			# selection icon
			# ############################################################################
			
			icon = ""
			
			self.si = QtGui.QLabel(icon, self)
			self.si.setFixedWidth(200)
			self.si.setFixedHeight(200)
			self.si.setWordWrap(True)
			self.si.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.si.setOpenExternalLinks(True)
			self.setIcon("msf000")

			# ############################################################################
			# GUI for merge (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'This object has its own settings in spreadsheet and will be imported from Woodworking workbench Examples folder.')
			info += '<br><br>'
			info += translate('magicStart', 'More examples see at: ')
			info += '<ul>'
			info += '<li><a href="https://github.com/dprojects/Woodworking/tree/master/Examples/Parametric">'
			info += translate('magicStart', 'Fully parametric examples')
			info += '</a></li>'
			info += '<li><a href="https://github.com/dprojects/Woodworking/tree/master/Examples/Fixture">'
			info += translate('magicStart', 'Fixture examples')
			info += '</a></li>'
			info += '</ul>'
			self.minfo = QtGui.QLabel(info, self)
			self.minfo.move(10, row+3)
			self.minfo.setFixedWidth(200)
			self.minfo.setWordWrap(True)
			self.minfo.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.minfo.hide()
			
			# button
			self.mergeB = QtGui.QPushButton(translate('magicStart', 'import from examples'), self)
			self.mergeB.clicked.connect(self.createObject)
			self.mergeB.setFixedWidth(self.toolSW - 20)
			self.mergeB.setFixedHeight(createSize)
			self.mergeB.move(10, createRow)
			self.mergeB.hide()
			
			# ############################################################################
			# GUI for furniture (visible by default)
			# ############################################################################
			
			row -= 20
			
			# label
			info = translate('magicStart', 'Possible selections: <br><br> 1. X edge - to set XYZ position and width <br><br> 2. XY face - to put next module on top <br><br> 3. Vertex - to set XYZ position <br><br> 4. no selection - to create with custom settings')
			self.oo1i = QtGui.QLabel(info, self)
			self.oo1i.move(10, row+3)
			self.oo1i.setFixedWidth(200)
			self.oo1i.setWordWrap(True)
			self.oo1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			row += 200
			
			# label
			self.o4L = QtGui.QLabel(translate('magicStart', 'Wood thickness:'), self)
			self.o4L.move(10, row+3)

			# text input
			self.o4E = QtGui.QLineEdit(self)
			self.o4E.setText(str(self.gThick))
			self.o4E.setFixedWidth(90)
			self.o4E.move(120, row)
			
			row += 30
			
			# label
			self.oooL = QtGui.QLabel(translate('magicStart', 'Offset XYZ:'), self)
			self.oooL.move(10, row+3)
			
			# text input
			self.ooo1E = QtGui.QLineEdit(self)
			self.ooo1E.setText("0")
			self.ooo1E.setFixedWidth(90)
			self.ooo1E.move(120, row)
			
			# text input
			self.ooo2E = QtGui.QLineEdit(self)
			self.ooo2E.setText("0")
			self.ooo2E.setFixedWidth(90)
			self.ooo2E.move(220, row)
			
			# text input
			self.ooo3E = QtGui.QLineEdit(self)
			self.ooo3E.setText("0")
			self.ooo3E.setFixedWidth(90)
			self.ooo3E.move(320, row)
			
			row += 30
			
			# button
			self.oo1B1 = QtGui.QPushButton(translate('magicStart', 'calculate furniture'), self)
			self.oo1B1.clicked.connect(self.calculateFurniture)
			self.oo1B1.setFixedWidth(200)
			self.oo1B1.setFixedHeight(40)
			self.oo1B1.move(10, row)
			
			row += 70
			
			# label
			self.oo1L = QtGui.QLabel(translate('magicStart', 'Start XYZ:'), self)
			self.oo1L.move(10, row+3)
			
			# text input
			self.oo11E = QtGui.QLineEdit(self)
			self.oo11E.setText("0")
			self.oo11E.setFixedWidth(90)
			self.oo11E.move(120, row)
			
			# text input
			self.oo12E = QtGui.QLineEdit(self)
			self.oo12E.setText("0")
			self.oo12E.setFixedWidth(90)
			self.oo12E.move(220, row)
			
			# text input
			self.oo13E = QtGui.QLineEdit(self)
			self.oo13E.setText("0")
			self.oo13E.setFixedWidth(90)
			self.oo13E.move(320, row)
			
			row += 30
			
			# label
			self.o1L = QtGui.QLabel(translate('magicStart', 'Furniture width:'), self)
			self.o1L.move(10, row+3)
			
			# text input
			self.o1E = QtGui.QLineEdit(self)
			self.o1E.setText(str(self.gFSX))
			self.o1E.setFixedWidth(90)
			self.o1E.move(120, row)

			row += 30

			# label
			self.o2L = QtGui.QLabel(translate('magicStart', 'Furniture height:'), self)
			self.o2L.move(10, row+3)

			# text input
			self.o2E = QtGui.QLineEdit(self)
			self.o2E.setText(str(self.gFSZ))
			self.o2E.setFixedWidth(90)
			self.o2E.move(120, row)

			row += 30
			
			# label
			self.o3L = QtGui.QLabel(translate('magicStart', 'Furniture depth:'), self)
			self.o3L.move(10, row+3)

			# text input
			self.o3E = QtGui.QLineEdit(self)
			self.o3E.setText(str(self.gFSY))
			self.o3E.setFixedWidth(90)
			self.o3E.move(120, row)

			row += 40

			# button
			self.s1B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.s1B1.clicked.connect(self.createObject)
			self.s1B1.setFixedWidth(self.toolSW - 20)
			self.s1B1.setFixedHeight(createSize)
			self.s1B1.move(10, createRow)

			# ############################################################################
			# GUI for foot (hidden by default)
			# ############################################################################
			
			# label
			self.of1L = QtGui.QLabel(translate('magicStart', 'Furniture width:'), self)
			self.of1L.move(10, rowfoot+3)
			
			# text input
			self.of1E = QtGui.QLineEdit(self)
			self.of1E.setText(str(self.gFSX))
			self.of1E.setFixedWidth(90)
			self.of1E.move(120, rowfoot)

			rowfoot += 30

			# label
			self.of2L = QtGui.QLabel(translate('magicStart', 'Furniture depth:'), self)
			self.of2L.move(10, rowfoot+3)

			# text input
			self.of2E = QtGui.QLineEdit(self)
			self.of2E.setText(str(self.gFSY))
			self.of2E.setFixedWidth(90)
			self.of2E.move(120, rowfoot)

			rowfoot += 60

			# label
			self.of3L = QtGui.QLabel(translate('magicStart', 'Foot height:'), self)
			self.of3L.move(10, rowfoot+3)

			# text input
			self.of3E = QtGui.QLineEdit(self)
			self.of3E.setText("100")
			self.of3E.setFixedWidth(90)
			self.of3E.move(120, rowfoot)

			rowfoot += 30

			# label
			self.of4L = QtGui.QLabel(translate('magicStart', 'Foot thickness:'), self)
			self.of4L.move(10, rowfoot+3)

			# text input
			self.of4E = QtGui.QLineEdit(self)
			self.of4E.setText(str(self.gThick))
			self.of4E.setFixedWidth(90)
			self.of4E.move(120, rowfoot)

			rowfoot += 30

			# label
			self.of5L = QtGui.QLabel(translate('magicStart', 'Front offset:'), self)
			self.of5L.move(10, rowfoot+3)

			# text input
			self.of5E = QtGui.QLineEdit(self)
			self.of5E.setText(str(self.gThick))
			self.of5E.setFixedWidth(90)
			self.of5E.move(120, rowfoot)
			
			rowfoot += 60

			# button
			self.of6B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.of6B1.clicked.connect(self.createObject)
			self.of6B1.setFixedWidth(200)
			self.of6B1.setFixedHeight(40)
			self.of6B1.move(10, rowfoot)
			
			# hide by default
			self.of1L.hide()
			self.of1E.hide()
			self.of2L.hide()
			self.of2E.hide()
			self.of3L.hide()
			self.of3E.hide()
			self.of4L.hide()
			self.of4E.hide()
			self.of5L.hide()
			self.of5E.hide()
			self.of6B1.hide()

			# ############################################################################
			# GUI for Table (hidden by default)
			# ############################################################################
			
			# label
			info = translate('magicStart', 'Possible selections: <br><br>1. Vertex - to set XYZ position <br><br>2. no selection - to create with custom settings')
			self.otb1i = QtGui.QLabel(info, self)
			self.otb1i.move(10, rowtbl+3)
			self.otb1i.setFixedWidth(200)
			self.otb1i.setWordWrap(True)
			self.otb1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
		
			rowtbl += 120
			
			# label
			self.otb1L = QtGui.QLabel(translate('magicStart', 'Table width X:'), self)
			self.otb1L.move(10, rowtbl+3)
			
			# text input
			self.otb1E = QtGui.QLineEdit(self)
			self.otb1E.setText("990")
			self.otb1E.setFixedWidth(90)
			self.otb1E.move(120, rowtbl)

			rowtbl += 30

			# label
			self.otb2L = QtGui.QLabel(translate('magicStart', 'Table depth Y:'), self)
			self.otb2L.move(10, rowtbl+3)

			# text input
			self.otb2E = QtGui.QLineEdit(self)
			self.otb2E.setText("525")
			self.otb2E.setFixedWidth(90)
			self.otb2E.move(120, rowtbl)

			rowtbl += 30

			# label
			self.otb3L = QtGui.QLabel(translate('magicStart', 'Table height Z:'), self)
			self.otb3L.move(10, rowtbl+3)

			# text input
			self.otb3E = QtGui.QLineEdit(self)
			self.otb3E.setText("430")
			self.otb3E.setFixedWidth(90)
			self.otb3E.move(120, rowtbl)

			rowtbl += 30

			# label
			self.otb4L = QtGui.QLabel(translate('magicStart', 'Table top thickness:'), self)
			self.otb4L.move(10, rowtbl+3)

			# text input
			self.otb4E = QtGui.QLineEdit(self)
			self.otb4E.setText("18")
			self.otb4E.setFixedWidth(90)
			self.otb4E.move(220, rowtbl)

			rowtbl += 30

			# label
			self.otb5L = QtGui.QLabel(translate('magicStart', 'Legs and Supporters thickness:'), self)
			self.otb5L.move(10, rowtbl+3)

			# text input
			self.otb5E = QtGui.QLineEdit(self)
			self.otb5E.setText("80")
			self.otb5E.setFixedWidth(90)
			self.otb5E.move(220, rowtbl)
			
			rowtbl += 30

			# label
			self.otb6L = QtGui.QLabel(translate('magicStart', 'Table top offset:'), self)
			self.otb6L.move(10, rowtbl+3)

			# text input
			self.otb6E = QtGui.QLineEdit(self)
			self.otb6E.setText("35")
			self.otb6E.setFixedWidth(90)
			self.otb6E.move(220, rowtbl)
		
			rowtbl += 60
			
			# button
			self.otb7B = QtGui.QPushButton(translate('magicStart', 'calculate table position'), self)
			self.otb7B.clicked.connect(self.calculateTable)
			self.otb7B.setFixedWidth(200)
			self.otb7B.setFixedHeight(40)
			self.otb7B.move(10, rowtbl)
			
			rowtbl += 70
			
			# label
			self.otb8L = QtGui.QLabel(translate('magicStart', 'Start XYZ:'), self)
			self.otb8L.move(10, rowtbl+3)
			
			# text input
			self.otb81E = QtGui.QLineEdit(self)
			self.otb81E.setText("0")
			self.otb81E.setFixedWidth(90)
			self.otb81E.move(120, rowtbl)
			
			# text input
			self.otb82E = QtGui.QLineEdit(self)
			self.otb82E.setText("0")
			self.otb82E.setFixedWidth(90)
			self.otb82E.move(220, rowtbl)
			
			# text input
			self.otb83E = QtGui.QLineEdit(self)
			self.otb83E.setText("0")
			self.otb83E.setFixedWidth(90)
			self.otb83E.move(320, rowtbl)
			
			rowtbl += 40

			# button
			self.otb9B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.otb9B.clicked.connect(self.createObject)
			self.otb9B.setFixedWidth(self.toolSW - 20)
			self.otb9B.setFixedHeight(createSize)
			self.otb9B.move(10, createRow)
			
			# hide by default
			self.otb1i.hide()
			self.otb1L.hide()
			self.otb1E.hide()
			self.otb2L.hide()
			self.otb2E.hide()
			self.otb3L.hide()
			self.otb3E.hide()
			self.otb4L.hide()
			self.otb4E.hide()
			self.otb5L.hide()
			self.otb5E.hide()
			self.otb6L.hide()
			self.otb6E.hide()
			self.otb7B.hide()
			self.otb8L.hide()
			self.otb81E.hide()
			self.otb82E.hide()
			self.otb83E.hide()
			self.otb9B.hide()

			# ############################################################################
			# GUI for Single drawer (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Possible selections: <br><br>1. top edge<br>2. top edge + back face<br>3. bottom edge + top edge<br>4. bottom edge + top edge + back face<br>5. bottom edge + top edge + left edge + right edge + back face<br><br>The edge can be along X or Y axis.')
			self.og1i = QtGui.QLabel(info, self)
			self.og1i.move(10, rowgap+3)
			self.og1i.setFixedWidth(self.toolSW - 240)
			self.og1i.setWordWrap(True)
			self.og1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowgap += 170

			# button
			self.og4B1 = QtGui.QPushButton(translate('magicStart', 'calculate gap for drawer'), self)
			self.og4B1.clicked.connect(self.calculateSingleDrawer)
			self.og4B1.setFixedWidth(200)
			self.og4B1.setFixedHeight(40)
			self.og4B1.move(10, rowgap)
			
			rowgap += 60
			
			# label
			self.og2L = QtGui.QLabel(translate('magicStart', 'Gap start XYZ:'), self)
			self.og2L.move(10, rowgap+3)
			
			# text input
			self.og2E = QtGui.QLineEdit(self)
			self.og2E.setText("0")
			self.og2E.setFixedWidth(80)
			self.og2E.move(120, rowgap)
			
			# text input
			self.og3E = QtGui.QLineEdit(self)
			self.og3E.setText("0")
			self.og3E.setFixedWidth(80)
			self.og3E.move(210, rowgap)
			
			# text input
			self.og4E = QtGui.QLineEdit(self)
			self.og4E.setText("0")
			self.og4E.setFixedWidth(80)
			self.og4E.move(300, rowgap)
			
			rowgap += 30

			# label
			self.og5L = QtGui.QLabel(translate('magicStart', 'Gap width:'), self)
			self.og5L.move(10, rowgap+3)
			
			# text input
			self.og5E = QtGui.QLineEdit(self)
			self.og5E.setText("400")
			self.og5E.setFixedWidth(90)
			self.og5E.move(120, rowgap)
			
			rowgap += 30
			
			# label
			self.og6L = QtGui.QLabel(translate('magicStart', 'Gap height:'), self)
			self.og6L.move(10, rowgap+3)

			# text input
			self.og6E = QtGui.QLineEdit(self)
			self.og6E.setText("150")
			self.og6E.setFixedWidth(90)
			self.og6E.move(120, rowgap)
			
			rowgap += 30
			
			# label
			self.og7L = QtGui.QLabel(translate('magicStart', 'Gap depth:'), self)
			self.og7L.move(10, rowgap+3)

			# text input
			self.og7E = QtGui.QLineEdit(self)
			self.og7E.setText("350")
			self.og7E.setFixedWidth(90)
			self.og7E.move(120, rowgap)
			
			rowgap += 30
			
			# label
			self.og8L = QtGui.QLabel(translate('magicStart', 'Wood thickness:'), self)
			self.og8L.move(10, rowgap+3)

			# text input
			self.og8E = QtGui.QLineEdit(self)
			self.og8E.setText(str(self.gThick))
			self.og8E.setFixedWidth(90)
			self.og8E.move(120, rowgap)
			
			rowgap += 30
			
			# label
			self.og9L = QtGui.QLabel(translate('magicStart', 'Drawer system offsets:'), self)
			self.og9L.move(10, rowgap+3)

			rowgap += 20
			
			# label
			self.og91L = QtGui.QLabel(translate('magicStart', 'Sides:'), self)
			self.og91L.move(10, rowgap+3)
			
			# label
			self.og92L = QtGui.QLabel(translate('magicStart', 'Back:'), self)
			self.og92L.move(110, rowgap+3)
			
			# label
			self.og93L = QtGui.QLabel(translate('magicStart', 'Top:'), self)
			self.og93L.move(210, rowgap+3)
			
			# label
			self.og94L = QtGui.QLabel(translate('magicStart', 'Bottom:'), self)
			self.og94L.move(310, rowgap+3)

			rowgap += 20
			
			# text input
			self.og91E = QtGui.QLineEdit(self)
			self.og91E.setText("26")
			self.og91E.setFixedWidth(50)
			self.og91E.move(10, rowgap)
			
			# text input
			self.og92E = QtGui.QLineEdit(self)
			self.og92E.setText("20")
			self.og92E.setFixedWidth(50)
			self.og92E.move(110, rowgap)
			
			# text input
			self.og93E = QtGui.QLineEdit(self)
			self.og93E.setText("30")
			self.og93E.setFixedWidth(50)
			self.og93E.move(210, rowgap)
			
			# text input
			self.og94E = QtGui.QLineEdit(self)
			self.og94E.setText("10")
			self.og94E.setFixedWidth(50)
			self.og94E.move(310, rowgap)

			rowgap += 40

			# button
			self.og9B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.og9B1.clicked.connect(self.createObject)
			self.og9B1.setFixedWidth(self.toolSW - 20)
			self.og9B1.setFixedHeight(createSize)
			self.og9B1.move(10, createRow)

			# hide by default
			self.og1i.hide()
			self.og2L.hide()
			self.og2E.hide()
			self.og3E.hide()
			self.og4E.hide()
			self.og4B1.hide()
			self.og5L.hide()
			self.og5E.hide()
			self.og6L.hide()
			self.og6E.hide()
			self.og7L.hide()
			self.og7E.hide()
			self.og8L.hide()
			self.og8E.hide()
			self.og9L.hide()
			self.og91L.hide()
			self.og92L.hide()
			self.og93L.hide()
			self.og94L.hide()
			self.og91E.hide()
			self.og92E.hide()
			self.og93E.hide()
			self.og94E.hide()
			self.og9B1.hide()
			
			# ############################################################################
			# GUI for drawer series GAP (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 4 edges around the gap and back face: <br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge <br> 5. selection - back face')
			self.ods1i = QtGui.QLabel(info, self)
			self.ods1i.move(10, rowds+3)
			self.ods1i.setFixedWidth(200)
			self.ods1i.setWordWrap(True)
			self.ods1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowds += 120
			
			# label
			self.ods2L = QtGui.QLabel(translate('magicStart', 'Number of drawers:'), self)
			self.ods2L.move(10, rowds+3)
			
			# text input
			self.ods2E = QtGui.QLineEdit(self)
			self.ods2E.setText("4")
			self.ods2E.setFixedWidth(60)
			self.ods2E.move(180, rowds)
			
			rowds += 30
			
			# label
			self.ods3L = QtGui.QLabel(translate('magicStart', 'Wood thickness:'), self)
			self.ods3L.move(10, rowds+3)

			# text input
			self.ods3E = QtGui.QLineEdit(self)
			self.ods3E.setText(str(self.gThick))
			self.ods3E.setFixedWidth(60)
			self.ods3E.move(180, rowds)
			
			rowds += 30
			
			# label
			self.ods40L = QtGui.QLabel(translate('magicStart', 'Space between drawers:'), self)
			self.ods40L.move(10, rowds+3)

			# text input
			self.ods40E = QtGui.QLineEdit(self)
			self.ods40E.setText("2")
			self.ods40E.setFixedWidth(60)
			self.ods40E.move(180, rowds)
			
			rowds += 30
			
			# label
			self.ods4L = QtGui.QLabel(translate('magicStart', 'Drawer system offsets:'), self)
			self.ods4L.move(10, rowds+3)

			rowds += 20
			
			# label
			self.ods41L = QtGui.QLabel(translate('magicStart', 'Sides:'), self)
			self.ods41L.move(10, rowds+3)
			
			# label
			self.ods42L = QtGui.QLabel(translate('magicStart', 'Back:'), self)
			self.ods42L.move(110, rowds+3)
			
			# label
			self.ods43L = QtGui.QLabel(translate('magicStart', 'Top:'), self)
			self.ods43L.move(210, rowds+3)
			
			# label
			self.ods44L = QtGui.QLabel(translate('magicStart', 'Bottom:'), self)
			self.ods44L.move(310, rowds+3)

			rowds += 20
			
			# text input
			self.ods41E = QtGui.QLineEdit(self)
			self.ods41E.setText("26")
			self.ods41E.setFixedWidth(50)
			self.ods41E.move(10, rowds)
			
			# text input
			self.ods42E = QtGui.QLineEdit(self)
			self.ods42E.setText("20")
			self.ods42E.setFixedWidth(50)
			self.ods42E.move(110, rowds)
			
			# text input
			self.ods43E = QtGui.QLineEdit(self)
			self.ods43E.setText("30")
			self.ods43E.setFixedWidth(50)
			self.ods43E.move(210, rowds)
			
			# text input
			self.ods44E = QtGui.QLineEdit(self)
			self.ods44E.setText("10")
			self.ods44E.setFixedWidth(50)
			self.ods44E.move(310, rowds)

			rowds += 30
			
			# button
			self.ods5B = QtGui.QPushButton(translate('magicStart', 'calculate gaps'), self)
			self.ods5B.clicked.connect(self.calculateDrawerSeries)
			self.ods5B.setFixedWidth(200)
			self.ods5B.setFixedHeight(40)
			self.ods5B.move(10, rowds)
			
			rowds += 40 + 20
			
			# label
			self.ods6L = QtGui.QLabel(translate('magicStart', 'Gap start XYZ:'), self)
			self.ods6L.move(10, rowds+3)
			
			# text input
			self.ods61E = QtGui.QLineEdit(self)
			self.ods61E.setText("0")
			self.ods61E.setFixedWidth(90)
			self.ods61E.move(150, rowds)
			
			# text input
			self.ods62E = QtGui.QLineEdit(self)
			self.ods62E.setText("0")
			self.ods62E.setFixedWidth(90)
			self.ods62E.move(250, rowds)
			
			# text input
			self.ods63E = QtGui.QLineEdit(self)
			self.ods63E.setText("0")
			self.ods63E.setFixedWidth(90)
			self.ods63E.move(350, rowds)
			
			rowds += 30

			# label
			self.ods7L = QtGui.QLabel(translate('magicStart', 'Single gap width:'), self)
			self.ods7L.move(10, rowds+3)
			
			# text input
			self.ods7E = QtGui.QLineEdit(self)
			self.ods7E.setText("400")
			self.ods7E.setFixedWidth(90)
			self.ods7E.move(150, rowds)
			
			rowds += 30
			
			# label
			self.ods8L = QtGui.QLabel(translate('magicStart', 'Single gap height:'), self)
			self.ods8L.move(10, rowds+3)

			# text input
			self.ods8E = QtGui.QLineEdit(self)
			self.ods8E.setText("150")
			self.ods8E.setFixedWidth(90)
			self.ods8E.move(150, rowds)
			
			rowds += 30
			
			# label
			self.ods9L = QtGui.QLabel(translate('magicStart', 'Single gap depth:'), self)
			self.ods9L.move(10, rowds+3)

			# text input
			self.ods9E = QtGui.QLineEdit(self)
			self.ods9E.setText("350")
			self.ods9E.setFixedWidth(90)
			self.ods9E.move(150, rowds)
			
			rowds += 30

			# button
			self.ods10B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.ods10B.clicked.connect(self.createObject)
			self.ods10B.setFixedWidth(self.toolSW - 20)
			self.ods10B.setFixedHeight(createSize)
			self.ods10B.move(10, createRow)

			# hide by default
			self.ods1i.hide()
			self.ods2L.hide()
			self.ods2E.hide()
			self.ods3L.hide()
			self.ods3E.hide()
			self.ods40L.hide()
			self.ods40E.hide()
			self.ods4L.hide()
			self.ods41L.hide()
			self.ods42L.hide()
			self.ods43L.hide()
			self.ods44L.hide()
			self.ods41E.hide()
			self.ods42E.hide()
			self.ods43E.hide()
			self.ods44E.hide()
			self.ods5B.hide()
			self.ods6L.hide()
			self.ods61E.hide()
			self.ods62E.hide()
			self.ods63E.hide()
			self.ods7L.hide()
			self.ods7E.hide()
			self.ods8L.hide()
			self.ods8E.hide()
			self.ods9L.hide()
			self.ods9E.hide()
			self.ods10B.hide()
			
			# ############################################################################
			# GUI for Front from GAP (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 4 edges around the gap to calculate front size in this order: <br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge')
			self.ofr1i = QtGui.QLabel(info, self)
			self.ofr1i.move(10, rowfront+3)
			self.ofr1i.setFixedWidth(200)
			self.ofr1i.setWordWrap(True)
			self.ofr1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowfront += 130
			
			# label
			self.ofr7L = QtGui.QLabel(translate('magicStart', 'Front thickness:'), self)
			self.ofr7L.move(10, rowfront+3)

			# text input
			self.ofr7E = QtGui.QLineEdit(self)
			self.ofr7E.setText("18")
			self.ofr7E.setFixedWidth(90)
			self.ofr7E.move(120, rowfront)
		
			rowfront += 40
			
			# label
			self.ofr8L = QtGui.QLabel(translate('magicStart', 'Front offsets:'), self)
			self.ofr8L.move(10, rowfront+3)

			rowfront += 20
			
			# label
			self.ofr81L = QtGui.QLabel(translate('magicStart', 'Left side:'), self)
			self.ofr81L.move(10, rowfront+3)
			
			# label
			self.ofr82L = QtGui.QLabel(translate('magicStart', 'Right side:'), self)
			self.ofr82L.move(110, rowfront+3)
			
			# label
			self.ofr83L = QtGui.QLabel(translate('magicStart', 'Top:'), self)
			self.ofr83L.move(210, rowfront+3)
			
			# label
			self.ofr84L = QtGui.QLabel(translate('magicStart', 'Bottom:'), self)
			self.ofr84L.move(310, rowfront+3)

			rowfront += 20
			
			# text input
			self.ofr81E = QtGui.QLineEdit(self)
			self.ofr81E.setText("0")
			self.ofr81E.setFixedWidth(50)
			self.ofr81E.move(10, rowfront)
			
			# text input
			self.ofr82E = QtGui.QLineEdit(self)
			self.ofr82E.setText("0")
			self.ofr82E.setFixedWidth(50)
			self.ofr82E.move(110, rowfront)
			
			# text input
			self.ofr83E = QtGui.QLineEdit(self)
			self.ofr83E.setText("0")
			self.ofr83E.setFixedWidth(50)
			self.ofr83E.move(210, rowfront)
			
			# text input
			self.ofr84E = QtGui.QLineEdit(self)
			self.ofr84E.setText("0")
			self.ofr84E.setFixedWidth(50)
			self.ofr84E.move(310, rowfront)

			rowfront += 40
			
			# button
			self.ofr4B1 = QtGui.QPushButton(translate('magicStart', 'calculate front'), self)
			self.ofr4B1.clicked.connect(self.calculateFrontFromGap)
			self.ofr4B1.setFixedWidth(200)
			self.ofr4B1.setFixedHeight(40)
			self.ofr4B1.move(10, rowfront)
			
			rowfront += 80
			
			# label
			self.ofr2L = QtGui.QLabel(translate('magicStart', 'Front start XYZ:'), self)
			self.ofr2L.move(10, rowfront+3)
			
			# text input
			self.ofr2E = QtGui.QLineEdit(self)
			self.ofr2E.setText("0")
			self.ofr2E.setFixedWidth(90)
			self.ofr2E.move(120, rowfront)
			
			# text input
			self.ofr3E = QtGui.QLineEdit(self)
			self.ofr3E.setText("0")
			self.ofr3E.setFixedWidth(90)
			self.ofr3E.move(220, rowfront)
			
			# text input
			self.ofr4E = QtGui.QLineEdit(self)
			self.ofr4E.setText("0")
			self.ofr4E.setFixedWidth(90)
			self.ofr4E.move(320, rowfront)
			
			rowfront += 30

			# label
			self.ofr5L = QtGui.QLabel(translate('magicStart', 'Front width:'), self)
			self.ofr5L.move(10, rowfront+3)
			
			# text input
			self.ofr5E = QtGui.QLineEdit(self)
			self.ofr5E.setText("0")
			self.ofr5E.setFixedWidth(90)
			self.ofr5E.move(120, rowfront)
			
			rowfront += 30
			
			# label
			self.ofr6L = QtGui.QLabel(translate('magicStart', 'Front height:'), self)
			self.ofr6L.move(10, rowfront+3)

			# text input
			self.ofr6E = QtGui.QLineEdit(self)
			self.ofr6E.setText("0")
			self.ofr6E.setFixedWidth(90)
			self.ofr6E.move(120, rowfront)
			
			rowfront += 40

			# button
			self.ofr8B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.ofr8B1.clicked.connect(self.createObject)
			self.ofr8B1.setFixedWidth(self.toolSW - 20)
			self.ofr8B1.setFixedHeight(createSize)
			self.ofr8B1.move(10, createRow)

			# hide by default
			self.ofr1i.hide()
			self.ofr2L.hide()
			self.ofr2E.hide()
			self.ofr3E.hide()
			self.ofr4E.hide()
			self.ofr4B1.hide()
			self.ofr5L.hide()
			self.ofr5E.hide()
			self.ofr6L.hide()
			self.ofr6E.hide()
			self.ofr7L.hide()
			self.ofr7E.hide()
			self.ofr8L.hide()
			self.ofr81L.hide()
			self.ofr82L.hide()
			self.ofr83L.hide()
			self.ofr84L.hide()
			self.ofr81E.hide()
			self.ofr82E.hide()
			self.ofr83E.hide()
			self.ofr84E.hide()
			self.ofr8B1.hide()
			
			# ############################################################################
			# GUI for Front with glass (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 4 edges around the gap to calculate Front with glass: <br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge')
			self.ofglass1i = QtGui.QLabel(info, self)
			self.ofglass1i.move(10, rowfglass+3)
			self.ofglass1i.setFixedWidth(200)
			self.ofglass1i.setWordWrap(True)
			self.ofglass1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowfglass += 120
			
			# label
			self.ofglass2L = QtGui.QLabel(translate('magicStart', 'Wood thickness:'), self)
			self.ofglass2L.move(10, rowfglass+3)
			
			# text input
			self.ofglass2E = QtGui.QLineEdit(self)
			self.ofglass2E.setText("18")
			self.ofglass2E.setFixedWidth(90)
			self.ofglass2E.move(150, rowfglass)
			
			rowfglass += 30
			
			# label
			self.ofglass3L = QtGui.QLabel(translate('magicStart', 'Overlap horizontal:'), self)
			self.ofglass3L.setFixedWidth(120)
			self.ofglass3L.move(10, rowfglass+3)

			# text input
			self.ofglass3E = QtGui.QLineEdit(self)
			self.ofglass3E.setText("0")
			self.ofglass3E.setFixedWidth(90)
			self.ofglass3E.move(150, rowfglass)
		
			rowfglass += 30

			# label
			self.ofglass4L = QtGui.QLabel(translate('magicStart', 'Overlap vertical:'), self)
			self.ofglass4L.setFixedWidth(120)
			self.ofglass4L.move(10, rowfglass+3)

			# text input
			self.ofglass4E = QtGui.QLineEdit(self)
			self.ofglass4E.setText("0")
			self.ofglass4E.setFixedWidth(90)
			self.ofglass4E.move(150, rowfglass)
			
			rowfglass += 30
			
			# label
			self.ofglass5L = QtGui.QLabel(translate('magicStart', 'Glass thickness:'), self)
			self.ofglass5L.move(10, rowfglass+3)

			# text input
			self.ofglass5E = QtGui.QLineEdit(self)
			self.ofglass5E.setText("4")
			self.ofglass5E.setFixedWidth(90)
			self.ofglass5E.move(150, rowfglass)
			
			rowfglass += 40
			
			# button
			self.ofglass6B = QtGui.QPushButton(translate('magicStart', 'calculate front with glass'), self)
			self.ofglass6B.clicked.connect(self.calculateFrontWithGlass)
			self.ofglass6B.setFixedWidth(200)
			self.ofglass6B.setFixedHeight(40)
			self.ofglass6B.move(10, rowfglass)
			
			rowfglass += 80
			
			# label
			self.ofglass7L = QtGui.QLabel(translate('magicStart', 'Front start XYZ:'), self)
			self.ofglass7L.move(10, rowfglass+3)
			
			# text input
			self.ofglass71E = QtGui.QLineEdit(self)
			self.ofglass71E.setText("0")
			self.ofglass71E.setFixedWidth(90)
			self.ofglass71E.move(120, rowfglass)
			
			# text input
			self.ofglass72E = QtGui.QLineEdit(self)
			self.ofglass72E.setText("0")
			self.ofglass72E.setFixedWidth(90)
			self.ofglass72E.move(220, rowfglass)
			
			# text input
			self.ofglass73E = QtGui.QLineEdit(self)
			self.ofglass73E.setText("0")
			self.ofglass73E.setFixedWidth(90)
			self.ofglass73E.move(320, rowfglass)
			
			rowfglass += 30
			
			# label
			self.ofglass8L = QtGui.QLabel(translate('magicStart', 'Calculated single bar width:'), self)
			self.ofglass8L.move(10, rowfglass+3)
			
			# text input
			self.ofglass8E = QtGui.QLineEdit(self)
			self.ofglass8E.setText("0")
			self.ofglass8E.setFixedWidth(90)
			self.ofglass8E.move(220, rowfglass)
			
			rowfglass += 30
			
			# label
			self.ofglass9L = QtGui.QLabel(translate('magicStart', 'Calculated front width:'), self)
			self.ofglass9L.move(10, rowfglass+3)
			
			# text input
			self.ofglass9E = QtGui.QLineEdit(self)
			self.ofglass9E.setText("0")
			self.ofglass9E.setFixedWidth(90)
			self.ofglass9E.move(220, rowfglass)
			
			rowfglass += 30
			
			# label
			self.ofglass10L = QtGui.QLabel(translate('magicStart', 'Calculated front height:'), self)
			self.ofglass10L.move(10, rowfglass+3)

			# text input
			self.ofglass10E = QtGui.QLineEdit(self)
			self.ofglass10E.setText("0")
			self.ofglass10E.setFixedWidth(90)
			self.ofglass10E.move(220, rowfglass)
		
			rowfglass += 40

			# button
			self.ofglass11B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.ofglass11B.clicked.connect(self.createObject)
			self.ofglass11B.setFixedWidth(self.toolSW - 20)
			self.ofglass11B.setFixedHeight(createSize)
			self.ofglass11B.move(10, createRow)

			# hide by default
			self.ofglass1i.hide()
			self.ofglass2L.hide()
			self.ofglass2E.hide()
			self.ofglass3L.hide()
			self.ofglass3E.hide()
			self.ofglass4L.hide()
			self.ofglass4E.hide()
			self.ofglass5L.hide()
			self.ofglass5E.hide()
			self.ofglass6B.hide()
			self.ofglass7L.hide()
			self.ofglass71E.hide()
			self.ofglass72E.hide()
			self.ofglass73E.hide()
			self.ofglass8L.hide()
			self.ofglass8E.hide()
			self.ofglass9L.hide()
			self.ofglass9E.hide()
			self.ofglass10L.hide()
			self.ofglass10E.hide()
			self.ofglass11B.hide()
			
			# ############################################################################
			# GUI for Face Frame from GAP (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 4 edges around the gap to calculate Face Frame: <br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge')
			self.offrame1i = QtGui.QLabel(info, self)
			self.offrame1i.move(10, rowfframe+3)
			self.offrame1i.setFixedWidth(200)
			self.offrame1i.setWordWrap(True)
			self.offrame1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowfframe += 120
			
			# label
			self.offrame2L = QtGui.QLabel(translate('magicStart', 'Single bar width:'), self)
			self.offrame2L.move(10, rowfframe+3)
			
			# text input
			self.offrame2E = QtGui.QLineEdit(self)
			self.offrame2E.setText("38")
			self.offrame2E.setFixedWidth(90)
			self.offrame2E.move(150, rowfframe)
			
			rowfframe += 30
			
			# label
			self.offrame3L = QtGui.QLabel(translate('magicStart', 'Single bar thickness:'), self)
			self.offrame3L.move(10, rowfframe+3)

			# text input
			self.offrame3E = QtGui.QLineEdit(self)
			self.offrame3E.setText("19")
			self.offrame3E.setFixedWidth(90)
			self.offrame3E.move(150, rowfframe)
		
			rowfframe += 30

			# label
			self.offrame4L = QtGui.QLabel(translate('magicStart', 'Lip outside:'), self)
			self.offrame4L.move(10, rowfframe+3)

			# text input
			self.offrame4E = QtGui.QLineEdit(self)
			self.offrame4E.setText("0")
			self.offrame4E.setFixedWidth(90)
			self.offrame4E.move(150, rowfframe)
			
			rowfframe += 30
			
			# label
			self.offrame5L = QtGui.QLabel(translate('magicStart', 'Delve into furniture:'), self)
			self.offrame5L.move(10, rowfframe+3)

			# text input
			self.offrame5E = QtGui.QLineEdit(self)
			self.offrame5E.setText("0")
			self.offrame5E.setFixedWidth(90)
			self.offrame5E.move(150, rowfframe)
			
			rowfframe += 40
			
			# button
			self.offrame6B = QtGui.QPushButton(translate('magicStart', 'calculate Face Frame'), self)
			self.offrame6B.clicked.connect(self.calculateFaceframeFromGap)
			self.offrame6B.setFixedWidth(200)
			self.offrame6B.setFixedHeight(40)
			self.offrame6B.move(10, rowfframe)
			
			rowfframe += 80
			
			# label
			self.offrame7L = QtGui.QLabel(translate('magicStart', 'Frame start XYZ:'), self)
			self.offrame7L.move(10, rowfframe+3)
			
			# text input
			self.offrame71E = QtGui.QLineEdit(self)
			self.offrame71E.setText("0")
			self.offrame71E.setFixedWidth(90)
			self.offrame71E.move(120, rowfframe)
			
			# text input
			self.offrame72E = QtGui.QLineEdit(self)
			self.offrame72E.setText("0")
			self.offrame72E.setFixedWidth(90)
			self.offrame72E.move(220, rowfframe)
			
			# text input
			self.offrame73E = QtGui.QLineEdit(self)
			self.offrame73E.setText("0")
			self.offrame73E.setFixedWidth(90)
			self.offrame73E.move(320, rowfframe)
			
			rowfframe += 30
			
			# label
			self.offrame8L = QtGui.QLabel(translate('magicStart', 'Calculated Face Frame width:'), self)
			self.offrame8L.move(10, rowfframe+3)
			
			# text input
			self.offrame8E = QtGui.QLineEdit(self)
			self.offrame8E.setText("0")
			self.offrame8E.setFixedWidth(90)
			self.offrame8E.move(220, rowfframe)
			
			rowfframe += 30
			
			# label
			self.offrame9L = QtGui.QLabel(translate('magicStart', 'Calculated Face Frame height:'), self)
			self.offrame9L.move(10, rowfframe+3)

			# text input
			self.offrame9E = QtGui.QLineEdit(self)
			self.offrame9E.setText("0")
			self.offrame9E.setFixedWidth(90)
			self.offrame9E.move(220, rowfframe)
		
			rowfframe += 40

			# button
			self.offrame10B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.offrame10B.clicked.connect(self.createObject)
			self.offrame10B.setFixedWidth(self.toolSW - 20)
			self.offrame10B.setFixedHeight(createSize)
			self.offrame10B.move(10, createRow)

			# hide by default
			self.offrame1i.hide()
			self.offrame2L.hide()
			self.offrame2E.hide()
			self.offrame3L.hide()
			self.offrame3E.hide()
			self.offrame4L.hide()
			self.offrame4E.hide()
			self.offrame5L.hide()
			self.offrame5E.hide()
			self.offrame6B.hide()
			self.offrame7L.hide()
			self.offrame71E.hide()
			self.offrame72E.hide()
			self.offrame73E.hide()
			self.offrame8L.hide()
			self.offrame8E.hide()
			self.offrame9L.hide()
			self.offrame9E.hide()
			self.offrame10B.hide()

			# ############################################################################
			# GUI for Shelf from GAP (hidden by default)
			# ############################################################################
			
			rowshelf -= 20
			
			# label
			info = translate('magicStart', 'Please select 2 edges and face to calculate shelf: <br><br> 1. selection - Z left edge <br> 2. selection - Z right edge <br> 3. selection - back face <br><br> Please add "Shelf by depth" or "Shelf by offsets", if you do not want full depth.')
			self.osh1i = QtGui.QLabel(info, self)
			self.osh1i.move(10, rowshelf+3)
			self.osh1i.setFixedWidth(200)
			self.osh1i.setWordWrap(True)
			self.osh1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowshelf += 150
			
			# label
			self.osh1L = QtGui.QLabel(translate('magicStart', 'Shelf thickness:'), self)
			self.osh1L.move(10, rowshelf+3)

			# text input
			self.osh1E = QtGui.QLineEdit(self)
			self.osh1E.setText("18")
			self.osh1E.setFixedWidth(90)
			self.osh1E.move(120, rowshelf)
		
			rowshelf += 30
			
			# label
			self.osh2L = QtGui.QLabel(translate('magicStart', 'Shelf by depth:'), self)
			self.osh2L.move(10, rowshelf+3)

			# text input
			self.osh2E = QtGui.QLineEdit(self)
			self.osh2E.setText("0")
			self.osh2E.setFixedWidth(90)
			self.osh2E.move(120, rowshelf)
			
			rowshelf += 30
			
			# label
			self.osh3L = QtGui.QLabel(translate('magicStart', 'Shelf by offsets:'), self)
			self.osh3L.move(10, rowshelf+3)

			rowshelf += 20
			
			# label
			self.osh31L = QtGui.QLabel(translate('magicStart', 'Left side:'), self)
			self.osh31L.move(10, rowshelf+3)
			
			# label
			self.osh32L = QtGui.QLabel(translate('magicStart', 'Right side:'), self)
			self.osh32L.move(110, rowshelf+3)
			
			# label
			self.osh33L = QtGui.QLabel(translate('magicStart', 'Front:'), self)
			self.osh33L.move(210, rowshelf+3)
			
			# label
			self.osh34L = QtGui.QLabel(translate('magicStart', 'Back:'), self)
			self.osh34L.move(310, rowshelf+3)

			rowshelf += 20
			
			# text input
			self.osh31E = QtGui.QLineEdit(self)
			self.osh31E.setText("0")
			self.osh31E.setFixedWidth(50)
			self.osh31E.move(10, rowshelf)
			
			# text input
			self.osh32E = QtGui.QLineEdit(self)
			self.osh32E.setText("0")
			self.osh32E.setFixedWidth(50)
			self.osh32E.move(110, rowshelf)
			
			# text input
			self.osh33E = QtGui.QLineEdit(self)
			self.osh33E.setText("0")
			self.osh33E.setFixedWidth(50)
			self.osh33E.move(210, rowshelf)
			
			# text input
			self.osh34E = QtGui.QLineEdit(self)
			self.osh34E.setText("0")
			self.osh34E.setFixedWidth(50)
			self.osh34E.move(310, rowshelf)

			rowshelf += 40
			
			# button
			self.osh4B1 = QtGui.QPushButton(translate('magicStart', 'calculate shelf'), self)
			self.osh4B1.clicked.connect(self.calculateShelfFromGap)
			self.osh4B1.setFixedWidth(200)
			self.osh4B1.setFixedHeight(40)
			self.osh4B1.move(10, rowshelf)
			
			rowshelf += 70
			
			# label
			self.osh5L = QtGui.QLabel(translate('magicStart', 'Shelf start XYZ:'), self)
			self.osh5L.move(10, rowshelf+3)
			
			# text input
			self.osh51E = QtGui.QLineEdit(self)
			self.osh51E.setText("0")
			self.osh51E.setFixedWidth(90)
			self.osh51E.move(120, rowshelf)
			
			# text input
			self.osh52E = QtGui.QLineEdit(self)
			self.osh52E.setText("0")
			self.osh52E.setFixedWidth(90)
			self.osh52E.move(220, rowshelf)
			
			# text input
			self.osh53E = QtGui.QLineEdit(self)
			self.osh53E.setText("0")
			self.osh53E.setFixedWidth(90)
			self.osh53E.move(320, rowshelf)
			
			rowshelf += 30

			# label
			self.osh6L = QtGui.QLabel(translate('magicStart', 'Calculated shelf width:'), self)
			self.osh6L.move(10, rowshelf+3)
			
			# text input
			self.osh6E = QtGui.QLineEdit(self)
			self.osh6E.setText("0")
			self.osh6E.setFixedWidth(90)
			self.osh6E.move(220, rowshelf)
			
			rowshelf += 30
			
			# label
			self.osh7L = QtGui.QLabel(translate('magicStart', 'Calculated shelf depth:'), self)
			self.osh7L.move(10, rowshelf+3)

			# text input
			self.osh7E = QtGui.QLineEdit(self)
			self.osh7E.setText("0")
			self.osh7E.setFixedWidth(90)
			self.osh7E.move(220, rowshelf)
			
			rowshelf += 40

			# button
			self.osh8B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.osh8B1.clicked.connect(self.createObject)
			self.osh8B1.setFixedWidth(self.toolSW - 20)
			self.osh8B1.setFixedHeight(createSize)
			self.osh8B1.move(10, createRow)

			# hide by default
			self.osh1i.hide()
			self.osh1L.hide()
			self.osh1E.hide()
			self.osh2L.hide()
			self.osh2E.hide()
			self.osh3L.hide()
			self.osh31L.hide()
			self.osh32L.hide()
			self.osh33L.hide()
			self.osh34L.hide()
			self.osh31E.hide()
			self.osh32E.hide()
			self.osh33E.hide()
			self.osh34E.hide()
			self.osh4B1.hide()
			self.osh5L.hide()
			self.osh51E.hide()
			self.osh52E.hide()
			self.osh53E.hide()
			self.osh6L.hide()
			self.osh6E.hide()
			self.osh7L.hide()
			self.osh7E.hide()
			self.osh8B1.hide()

			# ############################################################################
			# GUI for Shelf series (hidden by default)
			# ############################################################################
			
			# label
			info = translate('magicStart', 'Please select 4 edges and face to calculate shelf series: <br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge <br> 5. selection - back face')
			self.oshs1i = QtGui.QLabel(info, self)
			self.oshs1i.move(10, rowsseries+3)
			self.oshs1i.setFixedWidth(200)
			self.oshs1i.setWordWrap(True)
			self.oshs1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowsseries += 150
			
			# label
			self.oshs1L = QtGui.QLabel(translate('magicStart', 'Single shelf thickness:'), self)
			self.oshs1L.move(10, rowsseries+3)

			# text input
			self.oshs1E = QtGui.QLineEdit(self)
			self.oshs1E.setText("18")
			self.oshs1E.setFixedWidth(90)
			self.oshs1E.move(150, rowsseries)
		
			rowsseries += 30
			
			# label
			self.oshs2L = QtGui.QLabel(translate('magicStart', 'Number of shelves:'), self)
			self.oshs2L.move(10, rowsseries+3)

			# text input
			self.oshs2E = QtGui.QLineEdit(self)
			self.oshs2E.setText("3")
			self.oshs2E.setFixedWidth(90)
			self.oshs2E.move(150, rowsseries)
			
			rowsseries += 40
			
			# button
			self.oshs3B = QtGui.QPushButton(translate('magicStart', 'calculate shelf series'), self)
			self.oshs3B.clicked.connect(self.calculateShelfSeries)
			self.oshs3B.setFixedWidth(200)
			self.oshs3B.setFixedHeight(40)
			self.oshs3B.move(10, rowsseries)
			
			rowsseries += 70
			
			# label
			self.oshs4L = QtGui.QLabel(translate('magicStart', 'Shelf start XYZ:'), self)
			self.oshs4L.move(10, rowsseries+3)
			
			# text input
			self.oshs41E = QtGui.QLineEdit(self)
			self.oshs41E.setText("0")
			self.oshs41E.setFixedWidth(90)
			self.oshs41E.move(120, rowsseries)
			
			# text input
			self.oshs42E = QtGui.QLineEdit(self)
			self.oshs42E.setText("0")
			self.oshs42E.setFixedWidth(90)
			self.oshs42E.move(220, rowsseries)
			
			# text input
			self.oshs43E = QtGui.QLineEdit(self)
			self.oshs43E.setText("0")
			self.oshs43E.setFixedWidth(90)
			self.oshs43E.move(320, rowsseries)
			
			rowsseries += 30

			# label
			self.oshs5L = QtGui.QLabel(translate('magicStart', 'Calculated shelf width:'), self)
			self.oshs5L.move(10, rowsseries+3)
			
			# text input
			self.oshs5E = QtGui.QLineEdit(self)
			self.oshs5E.setText("0")
			self.oshs5E.setFixedWidth(90)
			self.oshs5E.move(220, rowsseries)
			
			rowsseries += 30
			
			# label
			self.oshs6L = QtGui.QLabel(translate('magicStart', 'Calculated shelf depth:'), self)
			self.oshs6L.move(10, rowsseries+3)

			# text input
			self.oshs6E = QtGui.QLineEdit(self)
			self.oshs6E.setText("0")
			self.oshs6E.setFixedWidth(90)
			self.oshs6E.move(220, rowsseries)
			
			rowsseries += 30

			# label
			self.oshs7L = QtGui.QLabel(translate('magicStart', 'Calculated shelves space:'), self)
			self.oshs7L.move(10, rowsseries+3)
			
			# text input
			self.oshs7E = QtGui.QLineEdit(self)
			self.oshs7E.setText("0")
			self.oshs7E.setFixedWidth(90)
			self.oshs7E.move(220, rowsseries)
			
			rowsseries += 40

			# button
			self.oshs8B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.oshs8B.clicked.connect(self.createObject)
			self.oshs8B.setFixedWidth(self.toolSW - 20)
			self.oshs8B.setFixedHeight(createSize)
			self.oshs8B.move(10, createRow)

			# hide by default
			self.oshs1i.hide()
			self.oshs1L.hide()
			self.oshs1E.hide()
			self.oshs2L.hide()
			self.oshs2E.hide()
			self.oshs3B.hide()
			self.oshs4L.hide()
			self.oshs41E.hide()
			self.oshs42E.hide()
			self.oshs43E.hide()
			self.oshs5L.hide()
			self.oshs5E.hide()
			self.oshs6L.hide()
			self.oshs6E.hide()
			self.oshs7L.hide()
			self.oshs7E.hide()
			self.oshs8B.hide()

			# ############################################################################
			# GUI for Side from GAP (hidden by default)
			# ############################################################################
			
			rowside += 20
			
			# label
			info = translate('magicStart', 'Please select 4 edges around the gap to calculate Side: <br><br> 1. selection - X or Y bottom edge <br> 2. selection - X or Y top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge')
			self.oside1i = QtGui.QLabel(info, self)
			self.oside1i.move(10, rowside+3)
			self.oside1i.setFixedWidth(200)
			self.oside1i.setWordWrap(True)
			self.oside1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowside += 120
			
			# label
			self.oside1L = QtGui.QLabel(translate('magicStart', 'Side thickness:'), self)
			self.oside1L.move(10, rowside+3)

			# text input
			self.oside1E = QtGui.QLineEdit(self)
			self.oside1E.setText("18")
			self.oside1E.setFixedWidth(90)
			self.oside1E.move(120, rowside)
		
			rowside += 30
			
			# label
			self.oside2L = QtGui.QLabel(translate('magicStart', 'Side by width:'), self)
			self.oside2L.move(10, rowside+3)

			# text input
			self.oside2E = QtGui.QLineEdit(self)
			self.oside2E.setText("0")
			self.oside2E.setFixedWidth(90)
			self.oside2E.move(120, rowside)
			
			rowside += 30
			
			# label
			self.oside3L = QtGui.QLabel(translate('magicStart', 'Side by offsets:'), self)
			self.oside3L.move(10, rowside+3)

			rowside += 20
			
			# label
			self.oside31L = QtGui.QLabel(translate('magicStart', 'Left:'), self)
			self.oside31L.move(10, rowside+3)
			
			# label
			self.oside32L = QtGui.QLabel(translate('magicStart', 'Right:'), self)
			self.oside32L.move(110, rowside+3)
			
			# label
			self.oside33L = QtGui.QLabel(translate('magicStart', 'Top:'), self)
			self.oside33L.move(210, rowside+3)
			
			# label
			self.oside34L = QtGui.QLabel(translate('magicStart', 'Bottom:'), self)
			self.oside34L.move(310, rowside+3)

			rowside += 20
			
			# text input
			self.oside31E = QtGui.QLineEdit(self)
			self.oside31E.setText("0")
			self.oside31E.setFixedWidth(50)
			self.oside31E.move(10, rowside)
			
			# text input
			self.oside32E = QtGui.QLineEdit(self)
			self.oside32E.setText("0")
			self.oside32E.setFixedWidth(50)
			self.oside32E.move(110, rowside)
			
			# text input
			self.oside33E = QtGui.QLineEdit(self)
			self.oside33E.setText("0")
			self.oside33E.setFixedWidth(50)
			self.oside33E.move(210, rowside)
			
			# text input
			self.oside34E = QtGui.QLineEdit(self)
			self.oside34E.setText("0")
			self.oside34E.setFixedWidth(50)
			self.oside34E.move(310, rowside)

			rowside += 40
			
			# button
			self.oside4B1 = QtGui.QPushButton(translate('magicStart', 'calculate side'), self)
			self.oside4B1.clicked.connect(self.calculateSideFromGap)
			self.oside4B1.setFixedWidth(200)
			self.oside4B1.setFixedHeight(40)
			self.oside4B1.move(10, rowside)
			
			rowside += 70
			
			# label
			self.oside5L = QtGui.QLabel(translate('magicStart', 'Side start XYZ:'), self)
			self.oside5L.move(10, rowside+3)
			
			# text input
			self.oside51E = QtGui.QLineEdit(self)
			self.oside51E.setText("0")
			self.oside51E.setFixedWidth(90)
			self.oside51E.move(120, rowside)
			
			# text input
			self.oside52E = QtGui.QLineEdit(self)
			self.oside52E.setText("0")
			self.oside52E.setFixedWidth(90)
			self.oside52E.move(220, rowside)
			
			# text input
			self.oside53E = QtGui.QLineEdit(self)
			self.oside53E.setText("0")
			self.oside53E.setFixedWidth(90)
			self.oside53E.move(320, rowside)
			
			rowside += 30

			# label
			self.oside6L = QtGui.QLabel(translate('magicStart', 'Calculated side width:'), self)
			self.oside6L.move(10, rowside+3)
			
			# text input
			self.oside6E = QtGui.QLineEdit(self)
			self.oside6E.setText("0")
			self.oside6E.setFixedWidth(90)
			self.oside6E.move(220, rowside)
			
			rowside += 30
			
			# label
			self.oside7L = QtGui.QLabel(translate('magicStart', 'Calculated side height:'), self)
			self.oside7L.move(10, rowside+3)

			# text input
			self.oside7E = QtGui.QLineEdit(self)
			self.oside7E.setText("0")
			self.oside7E.setFixedWidth(90)
			self.oside7E.move(220, rowside)
			
			rowside += 40

			# button
			self.oside8B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.oside8B1.clicked.connect(self.createObject)
			self.oside8B1.setFixedWidth(self.toolSW - 20)
			self.oside8B1.setFixedHeight(createSize)
			self.oside8B1.move(10, createRow)

			# hide by default
			self.oside1i.hide()
			self.oside1L.hide()
			self.oside1E.hide()
			self.oside2L.hide()
			self.oside2E.hide()
			self.oside3L.hide()
			self.oside31L.hide()
			self.oside32L.hide()
			self.oside33L.hide()
			self.oside34L.hide()
			self.oside31E.hide()
			self.oside32E.hide()
			self.oside33E.hide()
			self.oside34E.hide()
			self.oside4B1.hide()
			self.oside5L.hide()
			self.oside51E.hide()
			self.oside52E.hide()
			self.oside53E.hide()
			self.oside6L.hide()
			self.oside6E.hide()
			self.oside7L.hide()
			self.oside7E.hide()
			self.oside8B1.hide()

			# ############################################################################
			# GUI for Center side from GAP (hidden by default)
			# ############################################################################
			
			rowcside -= 20
			
			# label
			info = translate('magicStart', 'Please select 2 edges (top or bottom at Y axis direction) and 1 face (bottom or top at XY plane) to calculate side in the center: <br><br> 1. selection - Y left edge <br> 2. selection - Y right edge <br> 3. selection - XY face')
			self.ocs1i = QtGui.QLabel(info, self)
			self.ocs1i.move(10, rowcside+3)
			self.ocs1i.setFixedWidth(200)
			self.ocs1i.setWordWrap(True)
			self.ocs1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowcside += 150
			
			# label
			self.ocs1L = QtGui.QLabel(translate('magicStart', 'Side thickness:'), self)
			self.ocs1L.move(10, rowcside+3)

			# text input
			self.ocs1E = QtGui.QLineEdit(self)
			self.ocs1E.setText("18")
			self.ocs1E.setFixedWidth(90)
			self.ocs1E.move(120, rowcside)
		
			rowcside += 30
			
			# label
			self.ocs2L = QtGui.QLabel(translate('magicStart', 'Side by depth:'), self)
			self.ocs2L.move(10, rowcside+3)

			# text input
			self.ocs2E = QtGui.QLineEdit(self)
			self.ocs2E.setText("0")
			self.ocs2E.setFixedWidth(90)
			self.ocs2E.move(120, rowcside)
			
			rowcside += 30
			
			# label
			self.ocs3L = QtGui.QLabel(translate('magicStart', 'Side by offsets:'), self)
			self.ocs3L.move(10, rowcside+3)

			rowcside += 20
			
			# label
			self.ocs31L = QtGui.QLabel(translate('magicStart', 'Top:'), self)
			self.ocs31L.move(10, rowcside+3)
			
			# label
			self.ocs32L = QtGui.QLabel(translate('magicStart', 'Bottom:'), self)
			self.ocs32L.move(110, rowcside+3)
			
			# label
			self.ocs33L = QtGui.QLabel(translate('magicStart', 'Front:'), self)
			self.ocs33L.move(210, rowcside+3)
			
			# label
			self.ocs34L = QtGui.QLabel(translate('magicStart', 'Back:'), self)
			self.ocs34L.move(310, rowcside+3)

			rowcside += 20
			
			# text input
			self.ocs31E = QtGui.QLineEdit(self)
			self.ocs31E.setText("0")
			self.ocs31E.setFixedWidth(50)
			self.ocs31E.move(10, rowcside)
			
			# text input
			self.ocs32E = QtGui.QLineEdit(self)
			self.ocs32E.setText("0")
			self.ocs32E.setFixedWidth(50)
			self.ocs32E.move(110, rowcside)
			
			# text input
			self.ocs33E = QtGui.QLineEdit(self)
			self.ocs33E.setText("0")
			self.ocs33E.setFixedWidth(50)
			self.ocs33E.move(210, rowcside)
			
			# text input
			self.ocs34E = QtGui.QLineEdit(self)
			self.ocs34E.setText("0")
			self.ocs34E.setFixedWidth(50)
			self.ocs34E.move(310, rowcside)

			rowcside += 40
			
			# button
			self.ocs4B1 = QtGui.QPushButton(translate('magicStart', 'calculate center side'), self)
			self.ocs4B1.clicked.connect(self.calculateCenterSideFromGap)
			self.ocs4B1.setFixedWidth(200)
			self.ocs4B1.setFixedHeight(40)
			self.ocs4B1.move(10, rowcside)
			
			rowcside += 70
			
			# label
			self.ocs5L = QtGui.QLabel(translate('magicStart', 'Side start XYZ:'), self)
			self.ocs5L.move(10, rowcside+3)
			
			# text input
			self.ocs51E = QtGui.QLineEdit(self)
			self.ocs51E.setText("0")
			self.ocs51E.setFixedWidth(90)
			self.ocs51E.move(120, rowcside)
			
			# text input
			self.ocs52E = QtGui.QLineEdit(self)
			self.ocs52E.setText("0")
			self.ocs52E.setFixedWidth(90)
			self.ocs52E.move(220, rowcside)
			
			# text input
			self.ocs53E = QtGui.QLineEdit(self)
			self.ocs53E.setText("0")
			self.ocs53E.setFixedWidth(90)
			self.ocs53E.move(320, rowcside)
			
			rowcside += 30

			# label
			self.ocs6L = QtGui.QLabel(translate('magicStart', 'Calculated center side height:'), self)
			self.ocs6L.move(10, rowcside+3)
			
			# text input
			self.ocs6E = QtGui.QLineEdit(self)
			self.ocs6E.setText("0")
			self.ocs6E.setFixedWidth(90)
			self.ocs6E.move(220, rowcside)
			
			rowcside += 30
			
			# label
			self.ocs7L = QtGui.QLabel(translate('magicStart', 'Calculated center side depth:'), self)
			self.ocs7L.move(10, rowcside+3)

			# text input
			self.ocs7E = QtGui.QLineEdit(self)
			self.ocs7E.setText("0")
			self.ocs7E.setFixedWidth(90)
			self.ocs7E.move(220, rowcside)
			
			rowcside += 40

			# button
			self.ocs8B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.ocs8B1.clicked.connect(self.createObject)
			self.ocs8B1.setFixedWidth(self.toolSW - 20)
			self.ocs8B1.setFixedHeight(createSize)
			self.ocs8B1.move(10, createRow)

			# hide by default
			self.ocs1i.hide()
			self.ocs1L.hide()
			self.ocs1E.hide()
			self.ocs2L.hide()
			self.ocs2E.hide()
			self.ocs3L.hide()
			self.ocs31L.hide()
			self.ocs32L.hide()
			self.ocs33L.hide()
			self.ocs34L.hide()
			self.ocs31E.hide()
			self.ocs32E.hide()
			self.ocs33E.hide()
			self.ocs34E.hide()
			self.ocs4B1.hide()
			self.ocs5L.hide()
			self.ocs51E.hide()
			self.ocs52E.hide()
			self.ocs53E.hide()
			self.ocs6L.hide()
			self.ocs6E.hide()
			self.ocs7L.hide()
			self.ocs7E.hide()
			self.ocs8B1.hide()
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()

		# ############################################################################
		# actions - GUI
		# ############################################################################

		# ############################################################################
		def setGUIInfo(self, iType="furniture"):

			# ##############################################
			# hide everything first
			# ##############################################
			
			# side
			self.oside1i.hide()
			self.oside1L.hide()
			self.oside1E.hide()
			self.oside2L.hide()
			self.oside2E.hide()
			self.oside3L.hide()
			self.oside31L.hide()
			self.oside32L.hide()
			self.oside33L.hide()
			self.oside34L.hide()
			self.oside31E.hide()
			self.oside32E.hide()
			self.oside33E.hide()
			self.oside34E.hide()
			self.oside4B1.hide()
			self.oside5L.hide()
			self.oside51E.hide()
			self.oside52E.hide()
			self.oside53E.hide()
			self.oside6L.hide()
			self.oside6E.hide()
			self.oside7L.hide()
			self.oside7E.hide()
			self.oside8B1.hide()
			
			# center side
			self.ocs1i.hide()
			self.ocs1L.hide()
			self.ocs1E.hide()
			self.ocs2L.hide()
			self.ocs2E.hide()
			self.ocs3L.hide()
			self.ocs31L.hide()
			self.ocs32L.hide()
			self.ocs33L.hide()
			self.ocs34L.hide()
			self.ocs31E.hide()
			self.ocs32E.hide()
			self.ocs33E.hide()
			self.ocs34E.hide()
			self.ocs4B1.hide()
			self.ocs5L.hide()
			self.ocs51E.hide()
			self.ocs52E.hide()
			self.ocs53E.hide()
			self.ocs6L.hide()
			self.ocs6E.hide()
			self.ocs7L.hide()
			self.ocs7E.hide()
			self.ocs8B1.hide()
			
			# shelf
			self.osh1i.hide()
			self.osh1L.hide()
			self.osh1E.hide()
			self.osh2L.hide()
			self.osh2E.hide()
			self.osh3L.hide()
			self.osh31L.hide()
			self.osh32L.hide()
			self.osh33L.hide()
			self.osh34L.hide()
			self.osh31E.hide()
			self.osh32E.hide()
			self.osh33E.hide()
			self.osh34E.hide()
			self.osh4B1.hide()
			self.osh5L.hide()
			self.osh51E.hide()
			self.osh52E.hide()
			self.osh53E.hide()
			self.osh6L.hide()
			self.osh6E.hide()
			self.osh7L.hide()
			self.osh7E.hide()
			self.osh8B1.hide()

			# shelf series
			self.oshs1i.hide()
			self.oshs1L.hide()
			self.oshs1E.hide()
			self.oshs2L.hide()
			self.oshs2E.hide()
			self.oshs3B.hide()
			self.oshs4L.hide()
			self.oshs41E.hide()
			self.oshs42E.hide()
			self.oshs43E.hide()
			self.oshs5L.hide()
			self.oshs5E.hide()
			self.oshs6L.hide()
			self.oshs6E.hide()
			self.oshs7L.hide()
			self.oshs7E.hide()
			self.oshs8B.hide()

			# front
			self.ofr1i.hide()
			self.ofr2L.hide()
			self.ofr2E.hide()
			self.ofr3E.hide()
			self.ofr4E.hide()
			self.ofr4B1.hide()
			self.ofr5L.hide()
			self.ofr5E.hide()
			self.ofr6L.hide()
			self.ofr6E.hide()
			self.ofr7L.hide()
			self.ofr7E.hide()
			self.ofr8L.hide()
			self.ofr81L.hide()
			self.ofr82L.hide()
			self.ofr83L.hide()
			self.ofr84L.hide()
			self.ofr81E.hide()
			self.ofr82E.hide()
			self.ofr83E.hide()
			self.ofr84E.hide()
			self.ofr8B1.hide()
		
			# front with glass
			self.ofglass1i.hide()
			self.ofglass2L.hide()
			self.ofglass2E.hide()
			self.ofglass3L.hide()
			self.ofglass3E.hide()
			self.ofglass4L.hide()
			self.ofglass4E.hide()
			self.ofglass5L.hide()
			self.ofglass5E.hide()
			self.ofglass6B.hide()
			self.ofglass7L.hide()
			self.ofglass71E.hide()
			self.ofglass72E.hide()
			self.ofglass73E.hide()
			self.ofglass8L.hide()
			self.ofglass8E.hide()
			self.ofglass9L.hide()
			self.ofglass9E.hide()
			self.ofglass10L.hide()
			self.ofglass10E.hide()
			self.ofglass11B.hide()
		
			# face frame
			self.offrame1i.hide()
			self.offrame2L.hide()
			self.offrame2E.hide()
			self.offrame3L.hide()
			self.offrame3E.hide()
			self.offrame4L.hide()
			self.offrame4E.hide()
			self.offrame5L.hide()
			self.offrame5E.hide()
			self.offrame6B.hide()
			self.offrame7L.hide()
			self.offrame71E.hide()
			self.offrame72E.hide()
			self.offrame73E.hide()
			self.offrame8L.hide()
			self.offrame8E.hide()
			self.offrame9L.hide()
			self.offrame9E.hide()
			self.offrame10B.hide()
			
			# drawer
			self.og1i.hide()
			self.og2L.hide()
			self.og2E.hide()
			self.og3E.hide()
			self.og4E.hide()
			self.og4B1.hide()
			self.og5L.hide()
			self.og5E.hide()
			self.og6L.hide()
			self.og6E.hide()
			self.og7L.hide()
			self.og7E.hide()
			self.og8L.hide()
			self.og8E.hide()
			self.og9L.hide()
			self.og91L.hide()
			self.og92L.hide()
			self.og93L.hide()
			self.og94L.hide()
			self.og91E.hide()
			self.og92E.hide()
			self.og93E.hide()
			self.og94E.hide()
			self.og9B1.hide()
		
			# drawer series
			self.ods1i.hide()
			self.ods2L.hide()
			self.ods2E.hide()
			self.ods3L.hide()
			self.ods3E.hide()
			self.ods40L.hide()
			self.ods40E.hide()
			self.ods4L.hide()
			self.ods41L.hide()
			self.ods42L.hide()
			self.ods43L.hide()
			self.ods44L.hide()
			self.ods41E.hide()
			self.ods42E.hide()
			self.ods43E.hide()
			self.ods44E.hide()
			self.ods5B.hide()
			self.ods6L.hide()
			self.ods61E.hide()
			self.ods62E.hide()
			self.ods63E.hide()
			self.ods7L.hide()
			self.ods7E.hide()
			self.ods8L.hide()
			self.ods8E.hide()
			self.ods9L.hide()
			self.ods9E.hide()
			self.ods10B.hide()
		
			# foot
			self.of1L.hide()
			self.of1E.hide()
			self.of2L.hide()
			self.of2E.hide()
			self.of3L.hide()
			self.of3E.hide()
			self.of4L.hide()
			self.of4E.hide()
			self.of5L.hide()
			self.of5E.hide()
			self.of6B1.hide()
			
			# table
			self.otb1i.hide()
			self.otb1L.hide()
			self.otb1E.hide()
			self.otb2L.hide()
			self.otb2E.hide()
			self.otb3L.hide()
			self.otb3E.hide()
			self.otb4L.hide()
			self.otb4E.hide()
			self.otb5L.hide()
			self.otb5E.hide()
			self.otb6L.hide()
			self.otb6E.hide()
			self.otb7B.hide()
			self.otb8L.hide()
			self.otb81E.hide()
			self.otb82E.hide()
			self.otb83E.hide()
			self.otb9B.hide()

			# merge
			self.minfo.hide()
			self.mergeB.hide()
			
			# furniture (default)
			self.oo1i.hide()
			self.oo1L.hide()
			self.oo11E.hide()
			self.oo12E.hide()
			self.oo13E.hide()
			self.oooL.hide()
			self.ooo1E.hide()
			self.ooo2E.hide()
			self.ooo3E.hide()
			self.oo1B1.hide()
			self.o1L.hide()
			self.o1E.hide()
			self.o2L.hide()
			self.o2E.hide()
			self.o3L.hide()
			self.o3E.hide()
			self.o4L.hide()
			self.o4E.hide()
			self.s1B1.hide()
			
			# ##############################################
			# show only needed
			# ##############################################
			
			if iType == "furniture":
				self.oo1i.show()
				self.oooL.show()
				self.ooo1E.show()
				self.ooo2E.show()
				self.ooo3E.show()
				self.oo1L.show()
				self.oo11E.show()
				self.oo12E.show()
				self.oo13E.show()
				self.oo1B1.show()
				self.o1L.show()
				self.o1E.show()
				self.o2L.show()
				self.o2E.show()
				self.o3L.show()
				self.o3E.show()
				self.o4L.show()
				self.o4E.show()
				self.s1B1.show()
			
			if iType == "side":
				self.oside1i.show()
				self.oside1L.show()
				self.oside1E.show()
				self.oside2L.show()
				self.oside2E.show()
				self.oside3L.show()
				self.oside31L.show()
				self.oside32L.show()
				self.oside33L.show()
				self.oside34L.show()
				self.oside31E.show()
				self.oside32E.show()
				self.oside33E.show()
				self.oside34E.show()
				self.oside4B1.show()
				self.oside5L.show()
				self.oside51E.show()
				self.oside52E.show()
				self.oside53E.show()
				self.oside6L.show()
				self.oside6E.show()
				self.oside7L.show()
				self.oside7E.show()
				self.oside8B1.show()

			if iType == "center side":
				self.ocs1i.show()
				self.ocs1L.show()
				self.ocs1E.show()
				self.ocs2L.show()
				self.ocs2E.show()
				self.ocs3L.show()
				self.ocs31L.show()
				self.ocs32L.show()
				self.ocs33L.show()
				self.ocs34L.show()
				self.ocs31E.show()
				self.ocs32E.show()
				self.ocs33E.show()
				self.ocs34E.show()
				self.ocs4B1.show()
				self.ocs5L.show()
				self.ocs51E.show()
				self.ocs52E.show()
				self.ocs53E.show()
				self.ocs6L.show()
				self.ocs6E.show()
				self.ocs7L.show()
				self.ocs7E.show()
				self.ocs8B1.show()

			if iType == "shelf":
				self.osh1i.show()
				self.osh1L.show()
				self.osh1E.show()
				self.osh2L.show()
				self.osh2E.show()
				self.osh3L.show()
				self.osh31L.show()
				self.osh32L.show()
				self.osh33L.show()
				self.osh34L.show()
				self.osh31E.show()
				self.osh32E.show()
				self.osh33E.show()
				self.osh34E.show()
				self.osh4B1.show()
				self.osh5L.show()
				self.osh51E.show()
				self.osh52E.show()
				self.osh53E.show()
				self.osh6L.show()
				self.osh6E.show()
				self.osh7L.show()
				self.osh7E.show()
				self.osh8B1.show()

			if iType == "shelf series":
				self.oshs1i.show()
				self.oshs1L.show()
				self.oshs1E.show()
				self.oshs2L.show()
				self.oshs2E.show()
				self.oshs3B.show()
				self.oshs4L.show()
				self.oshs41E.show()
				self.oshs42E.show()
				self.oshs43E.show()
				self.oshs5L.show()
				self.oshs5E.show()
				self.oshs6L.show()
				self.oshs6E.show()
				self.oshs7L.show()
				self.oshs7E.show()
				self.oshs8B.show()
			
			if iType == "front":
				self.ofr1i.show()
				self.ofr2L.show()
				self.ofr2E.show()
				self.ofr3E.show()
				self.ofr4E.show()
				self.ofr4B1.show()
				self.ofr5L.show()
				self.ofr5E.show()
				self.ofr6L.show()
				self.ofr6E.show()
				self.ofr7L.show()
				self.ofr7E.show()
				self.ofr8L.show()
				self.ofr81L.show()
				self.ofr82L.show()
				self.ofr83L.show()
				self.ofr84L.show()
				self.ofr81E.show()
				self.ofr82E.show()
				self.ofr83E.show()
				self.ofr84E.show()
				self.ofr8B1.show()
			
			if iType == "front with glass":
				self.ofglass1i.show()
				self.ofglass2L.show()
				self.ofglass2E.show()
				self.ofglass3L.show()
				self.ofglass3E.show()
				self.ofglass4L.show()
				self.ofglass4E.show()
				self.ofglass5L.show()
				self.ofglass5E.show()
				self.ofglass6B.show()
				self.ofglass7L.show()
				self.ofglass71E.show()
				self.ofglass72E.show()
				self.ofglass73E.show()
				self.ofglass8L.show()
				self.ofglass8E.show()
				self.ofglass9L.show()
				self.ofglass9E.show()
				self.ofglass10L.show()
				self.ofglass10E.show()
				self.ofglass11B.show()
			
			if iType == "face frame":
				self.offrame1i.show()
				self.offrame2L.show()
				self.offrame2E.show()
				self.offrame3L.show()
				self.offrame3E.show()
				self.offrame4L.show()
				self.offrame4E.show()
				self.offrame5L.show()
				self.offrame5E.show()
				self.offrame6B.show()
				self.offrame7L.show()
				self.offrame71E.show()
				self.offrame72E.show()
				self.offrame73E.show()
				self.offrame8L.show()
				self.offrame8E.show()
				self.offrame9L.show()
				self.offrame9E.show()
				self.offrame10B.show()

			if iType == "drawer":
				self.og1i.show()
				self.og2L.show()
				self.og2E.show()
				self.og3E.show()
				self.og4E.show()
				self.og4B1.show()
				self.og5L.show()
				self.og5E.show()
				self.og6L.show()
				self.og6E.show()
				self.og7L.show()
				self.og7E.show()
				self.og8L.show()
				self.og8E.show()
				self.og9L.show()
				self.og91L.show()
				self.og92L.show()
				self.og93L.show()
				self.og94L.show()
				self.og91E.show()
				self.og92E.show()
				self.og93E.show()
				self.og94E.show()
				self.og9B1.show()

			if iType == "drawer series":
				self.ods1i.show()
				self.ods2L.show()
				self.ods2E.show()
				self.ods3L.show()
				self.ods3E.show()
				self.ods40L.show()
				self.ods40E.show()
				self.ods4L.show()
				self.ods41L.show()
				self.ods42L.show()
				self.ods43L.show()
				self.ods44L.show()
				self.ods41E.show()
				self.ods42E.show()
				self.ods43E.show()
				self.ods44E.show()
				self.ods5B.show()
				self.ods6L.show()
				self.ods61E.show()
				self.ods62E.show()
				self.ods63E.show()
				self.ods7L.show()
				self.ods7E.show()
				self.ods8L.show()
				self.ods8E.show()
				self.ods9L.show()
				self.ods9E.show()
				self.ods10B.show()

			if iType == "foot":
				self.of1L.show()
				self.of1E.show()
				self.of2L.show()
				self.of2E.show()
				self.of3L.show()
				self.of3E.show()
				self.of4L.show()
				self.of4E.show()
				self.of5L.show()
				self.of5E.show()
				self.of6B1.show()
		
			if iType == "table":
				self.otb1i.show()
				self.otb1L.show()
				self.otb1E.show()
				self.otb2L.show()
				self.otb2E.show()
				self.otb3L.show()
				self.otb3E.show()
				self.otb4L.show()
				self.otb4E.show()
				self.otb5L.show()
				self.otb5E.show()
				self.otb6L.show()
				self.otb6E.show()
				self.otb7B.show()
				self.otb8L.show()
				self.otb81E.show()
				self.otb82E.show()
				self.otb83E.show()
				self.otb9B.show()

			if iType == "merge":
				self.minfo.show()
				self.mergeB.show()

		# ############################################################################	
		def selectedOption(self, selectedText):
			
			# the key is from translation so this needs to be tested...
			selectedIndex = getMenuIndex[selectedText]
			self.gSelectedFurniture = "F"+str(selectedIndex)
			
			# ####################################################
			# set icon
			# ####################################################
			
			if selectedIndex < 10:
				self.setIcon("msf00"+str(selectedIndex))
			if selectedIndex >= 10 and selectedIndex < 100:
				self.setIcon("msf0"+str(selectedIndex))
			if selectedIndex >= 100:
				self.setIcon("msf"+str(selectedIndex))
			
			# ####################################################
			# set GUI and help info
			# ####################################################
			
			if (
				selectedIndex == 2 or 
				selectedIndex == 3 or 
				selectedIndex == 4 or 
				selectedIndex == 5 or 
				selectedIndex == 6 or 
				selectedIndex == 7 or 
				selectedIndex == 8 or 
				selectedIndex == 9 or 
				selectedIndex == 11 or 
				selectedIndex == 12 or 
				selectedIndex == 13 or 
				selectedIndex == 14 or 
				selectedIndex == 15
				):
				self.setGUIInfo("merge")
				self.helpInfo.setText("")
				
			if (
				selectedIndex == 0 or 
				selectedIndex == 1 or 
				selectedIndex == 10 or
				selectedIndex == 27 or 
				selectedIndex == 28 or 
				selectedIndex == 29 or 
				selectedIndex == 35 or 
				selectedIndex == 36
				):
				self.setGUIInfo()
				self.helpInfo.setText(self.gHelpInfoF0)
			
			if (
				selectedIndex == 16 or 
				selectedIndex == 17 or 
				selectedIndex == 18 or 
				selectedIndex == 19 or 
				selectedIndex == 20
				):
				self.setGUIInfo("foot")
				self.helpInfo.setText(self.gHelpInfoF16)
			
			if selectedIndex == 21 or selectedIndex == 22:
				self.setGUIInfo("drawer")
				self.helpInfo.setText(self.gHelpInfoF21)
			
			if selectedIndex == 23 or selectedIndex == 24:
				self.setGUIInfo("front")
				self.helpInfo.setText(self.gHelpInfoF23)

			if selectedIndex == 25:
				self.setGUIInfo("shelf")
				self.helpInfo.setText(self.gHelpInfoF25)
			
			if selectedIndex == 26:
				self.setGUIInfo("center side")
				self.helpInfo.setText(self.gHelpInfoF26)

			if selectedIndex == 30 or selectedIndex == 31:
				self.setGUIInfo("drawer series")
				self.helpInfo.setText(self.gHelpInfoF30)
			
			if selectedIndex == 32 or selectedIndex == 33 or selectedIndex == 34:
				self.setGUIInfo("face frame")
				self.helpInfo.setText(self.gHelpInfoF32)
			
			if (
				selectedIndex == 37 or 
				selectedIndex == 38 or 
				selectedIndex == 39 or 
				selectedIndex == 40
				):
				self.setGUIInfo("front with glass")
				self.helpInfo.setText(self.gHelpInfoF37)
			
			if selectedIndex == 41:
				self.setGUIInfo("shelf series")
				self.helpInfo.setText(self.gHelpInfoF41)
			
			if (
				selectedIndex == 42 or 
				selectedIndex == 43 or 
				selectedIndex == 44 or 
				selectedIndex == 45 or 
				selectedIndex == 46 or 
				selectedIndex == 47
				):
				self.setGUIInfo("table")
				self.helpInfo.setText(self.gHelpInfoF42)
			
			if selectedIndex == 48:
				self.setGUIInfo("side")
				self.helpInfo.setText(self.gHelpInfoF48)

			# ####################################################
			# custom settings
			# ####################################################
			
			if selectedIndex == 10:
				self.o2E.setText("2300")
			else:
				self.o2E.setText("760")
				
			if selectedIndex == 20:
				self.of4E.setText("80")
			else:
				self.of4E.setText("18")
			
			if selectedIndex == 23:
				self.ofr7E.setText("18")
				self.ofr81E.setText("9")
				self.ofr82E.setText("9")
				self.ofr83E.setText("7")
				self.ofr84E.setText("7")
				
			if selectedIndex == 24:
				self.ofr7E.setText("18")
				self.ofr81E.setText("2")
				self.ofr82E.setText("2")
				self.ofr83E.setText("2")
				self.ofr84E.setText("2")
			
			if selectedIndex == 35 or selectedIndex == 36:
				self.o1E.setText("900")
			else:
				self.o1E.setText("500")
				
			if selectedIndex == 37 or selectedIndex == 38:
				self.ofglass3E.setText("9")
				self.ofglass4E.setText("7")
				self.ofglass3L.setText(translate('magicStart', 'Overlap horizontal:'))
				self.ofglass4L.setText(translate('magicStart', 'Overlap vertical:'))

			if selectedIndex == 39 or selectedIndex == 40:
				self.ofglass3E.setText("2")
				self.ofglass4E.setText("2")
				self.ofglass3L.setText(translate('magicStart', 'Offset horizontal:'))
				self.ofglass4L.setText(translate('magicStart', 'Offset vertical:'))
			
			if selectedIndex == 42:
				self.otb1E.setText("1050")
				self.otb2E.setText("600")
				self.otb3E.setText("780")
				self.otb4E.setText("18")
				self.otb5E.setText("60")
				self.otb6E.setText("35")
				
			if selectedIndex == 43:
				self.otb1E.setText("990")
				self.otb2E.setText("525")
				self.otb3E.setText("430")
				self.otb4E.setText("18")
				self.otb5E.setText("80")
				self.otb6E.setText("35")

			if selectedIndex == 44:
				self.otb1E.setText("1050")
				self.otb2E.setText("600")
				self.otb3E.setText("780")
				self.otb4E.setText("18")
				self.otb5E.setText("150")
				self.otb6E.setText("0")
				
			if selectedIndex == 45:
				self.otb1E.setText("990")
				self.otb2E.setText("525")
				self.otb3E.setText("430")
				self.otb4E.setText("18")
				self.otb5E.setText("150")
				self.otb6E.setText("0")
			
			if selectedIndex == 46:
				self.otb1E.setText("1150")
				self.otb2E.setText("700")
				self.otb3E.setText("780")
				self.otb4E.setText("36")
				self.otb5E.setText("100")
				self.otb6E.setText("40")
				
			if selectedIndex == 47:
				self.otb1E.setText("1150")
				self.otb2E.setText("700")
				self.otb3E.setText("450")
				self.otb4E.setText("36")
				self.otb5E.setText("80")
				self.otb6E.setText("0")

		# ############################################################################
		def createObject(self):

			self.gFSX = float(self.o1E.text())
			self.gFSZ = float(self.o2E.text())
			self.gFSY = float(self.o3E.text())
			self.gThick = float(self.o4E.text())

			if self.gSelectedFurniture == "F0":
				self.createF0()
			
			if self.gSelectedFurniture == "F1":
				self.createF1()
			
			if self.gSelectedFurniture == "F2":
				self.mergeF("Bookcase_002.FCStd")

			if self.gSelectedFurniture == "F3":
				self.mergeF("Drawer_001.FCStd")
			
			if self.gSelectedFurniture == "F4":
				self.mergeF("Chair_001.FCStd")
				
			if self.gSelectedFurniture == "F5":
				self.mergeF("PictureFrame_002.FCStd")
			
			if self.gSelectedFurniture == "F6":
				self.mergeF("Table_001.FCStd")
			
			if self.gSelectedFurniture == "F7":
				self.mergeF("StorageBox_001.FCStd", "box")
			
			if self.gSelectedFurniture == "F8":
				self.mergeF("Dowel_8_x_35_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F9":
				self.mergeF("Screw_4_x_40_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F10":
				self.createF10()
			
			if self.gSelectedFurniture == "F11":
				self.mergeF("Screw_3_x_20_mm.FCStd", "mount")
				
			if self.gSelectedFurniture == "F12":
				self.mergeF("Screw_5_x_50_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F13":
				self.mergeF("Counterbore2x_5_x_60_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F14":
				self.mergeF("Shelf_Pin_5_x_16.FCStd", "mount")
			
			if self.gSelectedFurniture == "F15":
				self.mergeF("Angle_40_x_40_x_100_mm.FCStd", "angles")
			
			if self.gSelectedFurniture == "F16":
				self.createF16()
			
			if self.gSelectedFurniture == "F17":
				self.createF17()
				
			if self.gSelectedFurniture == "F18":
				self.createF18()
				
			if self.gSelectedFurniture == "F19":
				self.createF19()
				
			if self.gSelectedFurniture == "F20":
				self.createF20()
			
			if self.gSelectedFurniture == "F21":
				self.createF21()
			
			if self.gSelectedFurniture == "F22":
				self.createF22()
			
			if self.gSelectedFurniture == "F23":
				self.createF23()
			
			if self.gSelectedFurniture == "F24":
				self.createF24()
			
			if self.gSelectedFurniture == "F25":
				self.createF25()
			
			if self.gSelectedFurniture == "F26":
				self.createF26()
			
			if self.gSelectedFurniture == "F27":
				self.createF27()
			
			if self.gSelectedFurniture == "F28":
				self.createF28()
				
			if self.gSelectedFurniture == "F29":
				self.createF29()
			
			if self.gSelectedFurniture == "F30":
				self.createF30()
			
			if self.gSelectedFurniture == "F31":
				self.createF31()
			
			if self.gSelectedFurniture == "F32":
				self.createF32()
			
			if self.gSelectedFurniture == "F33":
				self.createF33()
				
			if self.gSelectedFurniture == "F34":
				self.createF34()
			
			if self.gSelectedFurniture == "F35":
				self.createF35()
			
			if self.gSelectedFurniture == "F36":
				self.createF36()
			
			if self.gSelectedFurniture == "F37" or self.gSelectedFurniture == "F39":
				self.createF37()
			
			if self.gSelectedFurniture == "F38" or self.gSelectedFurniture == "F40":
				self.createF38()
			
			if self.gSelectedFurniture == "F41":
				self.createF41()
			
			if self.gSelectedFurniture == "F42" or self.gSelectedFurniture == "F43":
				self.createF42()
			
			if self.gSelectedFurniture == "F44" or self.gSelectedFurniture == "F45":
				self.createF44()
			
			if self.gSelectedFurniture == "F46" or self.gSelectedFurniture == "F47":
				self.createF46()
			
			if self.gSelectedFurniture == "F48":
				self.createF48()
			
			if self.gSelectedFurniture == "F49":
				self.mergeF("Biscuits_4_x_16_x_48_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F50":
				self.mergeF("Biscuits_4_x_21_x_54_mm.FCStd", "mount")
				
			if self.gSelectedFurniture == "F51":
				self.mergeF("Biscuits_4_x_24_x_57_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F52":
				self.mergeF("Pocket_screw_4_x_40_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F53":
				self.mergeF("Angle_30_x_30_x_25_mm.FCStd", "angles")
				
			if self.gSelectedFurniture == "F54":
				self.mergeF("Angle_80_x_80_x_20_mm.FCStd", "angles")
			
			if self.gSelectedFurniture == "F55":
				self.mergeF("Front_001.FCStd")
			
			if self.gSelectedFurniture == "F56":
				self.mergeF("Front_002.FCStd")
				
			if self.gSelectedFurniture == "F57":
				self.mergeF("Top_001.FCStd")
			
			if self.gSelectedFurniture == "F58":
				self.mergeF("Drawer_002.FCStd")
				
			# here to allow recalculation with selection
			FreeCADGui.Selection.clearSelection()

		# ############################################################################
		# actions - special functions
		# ############################################################################
		
		# ############################################################################
		def setIcon(self, iName):
			
			path = FreeCADGui.activeWorkbench().path
			iconPath = str(os.path.join(path, "Icons"))
			f = os.path.join(iconPath, iName+".png")
			
			if os.path.exists(f):
				filename = f
				icon = '<img src="'+ filename + '" width="200" height="200" align="right">'
				self.si.hide()
				self.si = QtGui.QLabel(icon, self)
				self.si.move(250, 50)
				self.si.show()

		# ############################################################################
		def getPathToMerge(self, iName, iType):
			
			if iType == "F":
				path = FreeCADGui.activeWorkbench().path
				path = str(os.path.join(path, "Examples"))
				path = str(os.path.join(path, "Parametric"))
				path = str(os.path.join(path, "Furniture"))
				path = str(os.path.join(path, iName))

			if iType == "box":
				path = FreeCADGui.activeWorkbench().path
				path = str(os.path.join(path, "Examples"))
				path = str(os.path.join(path, "Parametric"))
				path = str(os.path.join(path, "Storage boxes"))
				path = str(os.path.join(path, iName))
			
			if iType == "mount":
				path = FreeCADGui.activeWorkbench().path
				path = str(os.path.join(path, "Examples"))
				path = str(os.path.join(path, "Fixture"))
				path = str(os.path.join(path, "Mount"))
				path = str(os.path.join(path, iName))
			
			if iType == "angles":
				path = FreeCADGui.activeWorkbench().path
				path = str(os.path.join(path, "Examples"))
				path = str(os.path.join(path, "Fixture"))
				path = str(os.path.join(path, "Angles"))
				path = str(os.path.join(path, iName))
				
			return path

		# ############################################################################
		def mergeF(self, iName, iType="F"):
		
			# merge
			FreeCAD.ActiveDocument.mergeProject(self.getPathToMerge(iName, iType))
		
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def getStartVertex(self, iEdge, iEdgePlane):
		
			# prefer left vertex
			
			if iEdgePlane == "X":
				
				v0 =  float(MagicPanels.touchTypo(iEdge)[0].X)
				v1 =  float(MagicPanels.touchTypo(iEdge)[1].X)
				
				if self.gSingleDrawerDirection == "+":
					if  v0 < v1:
						return v0
					else:
						return v1
			
				if self.gSingleDrawerDirection == "-":
					if  v0 > v1:
						return v0
					else:
						return v1
						
			if iEdgePlane == "Y":
				
				v0 =  float(MagicPanels.touchTypo(iEdge)[0].Y)
				v1 =  float(MagicPanels.touchTypo(iEdge)[1].Y)
			
				if self.gSingleDrawerDirection == "+":
					if  v0 > v1:
						return v0
					else:
						return v1
			
				if self.gSingleDrawerDirection == "-":
					if  v0 < v1:
						return v0
					else:
						return v1
		
		# ############################################################################
		def helpSHOW(self):
			
			self.resize(self.toolSW + 400, self.toolSH)
			self.helpBSHOW.hide()
			self.helpBHIDE.show()
			self.helpInfo.show()

		# ############################################################################
		def helpHIDE(self):
			
			self.resize(self.toolSW, self.toolSH)
			self.helpBSHOW.show()
			self.helpBHIDE.hide()
			self.helpInfo.hide()

		# ############################################################################
		# actions - calculation functions
		# ############################################################################

		# ############################################################################
		def calculateFurniture(self):
			
			obj = False
			sub = False
			
			try:
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

			except:
				return
			
			width = 0
			height = 0
			depth = 0
			startX = 0
			startY = 0
			startZ = 0

			if sub.ShapeType == "Edge":
				
				width = float(sub.Length)
				
				if float(MagicPanels.touchTypo(sub)[0].X) < float(MagicPanels.touchTypo(sub)[1].X):
					startX = float(MagicPanels.touchTypo(sub)[0].X)
				else:
					startX = float(MagicPanels.touchTypo(sub)[1].X)
				
				startY = float(sub.CenterOfMass.y)
				startZ = float(sub.CenterOfMass.z)
				
			if sub.ShapeType == "Face":
				
				woodt = float(self.o4E.text())
				width = float(obj.Length.Value)
				thick = float(obj.Height.Value)
				
				if self.gSelectedFurniture == "F1":
					depth = float(obj.Width.Value) + 3
					startY = float(sub.Placement.Base.y)
				
				elif self.gSelectedFurniture == "F27":
					depth = float(obj.Width.Value) + woodt + 3
					startY = float(sub.Placement.Base.y) - woodt

				elif self.gSelectedFurniture == "F28":
					depth = float(obj.Width.Value)
					startY = float(sub.Placement.Base.y)
				
				elif self.gSelectedFurniture == "F29":
					depth = float(obj.Width.Value) + 3
					startY = float(sub.Placement.Base.y)
				
				elif self.gSelectedFurniture == "F35":
					depth = float(obj.Width.Value) + 3 + 19
					startY = float(sub.Placement.Base.y)
				
				elif self.gSelectedFurniture == "F36":
					depth = float(obj.Width.Value) + 3 + 19
					startY = float(sub.Placement.Base.y)

				else:
					depth = float(obj.Width.Value) + woodt
					startY = float(sub.Placement.Base.y) - woodt
				
				startX = float(sub.Placement.Base.x)
				startZ = float(sub.Placement.Base.z) + thick

			if sub.ShapeType == "Vertex":
				
				startX = float(sub.Point.x)
				startY = float(sub.Point.y)
				startZ = float(sub.Point.z)

			# add offsets
			startX = startX + float(self.ooo1E.text())
			startY = startY + float(self.ooo2E.text())
			startZ = startZ + float(self.ooo3E.text())

			# set values to text fields
			self.oo11E.setText(str(startX))
			self.oo12E.setText(str(startY))
			self.oo13E.setText(str(startZ))
			
			if width != 0:
				self.o1E.setText(str(width))
			
			if height != 0:
				self.o2E.setText(str(height))
			
			if depth != 0:
				self.o3E.setText(str(depth))

		# ############################################################################
		def calculateSingleDrawer(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			obj4 = False
			obj5 = False
			
			edge1 = False
			edge2 = False
			edge3 = False
			edge4 = False
			edge5 = False
			face1 = False # 2, 3, 5
			
			# possible selections
			# edge1
			# edge1 + face
			# edge1 + edge2
			# edge1 + edge2 + face
			# edge1 + edge2 + edge3 + edge4 + face
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

				if sub.ShapeType == "Edge":
					edge1 = sub
				else:
					return
			except:
				skip = 1
			
			try:
				obj2 = FreeCADGui.Selection.getSelection()[1]
				sub = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]

				if sub.ShapeType == "Edge":
					edge2 = sub
			
				if sub.ShapeType == "Face":
					face1 = sub
			except:
				skip = 1
			
			try:
				obj3 = FreeCADGui.Selection.getSelection()[2]
				sub = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
				
				if sub.ShapeType == "Edge":
					edge3 = sub
			
				if sub.ShapeType == "Face":
					face1 = sub
			except:
				skip = 1

			try:
				obj4 = FreeCADGui.Selection.getSelection()[3]
				sub = FreeCADGui.Selection.getSelectionEx()[3].SubObjects[0]
				
				if sub.ShapeType == "Edge":
					edge4 = sub
			except:
				skip = 1

			try:
				obj5 = FreeCADGui.Selection.getSelection()[4]
				sub = FreeCADGui.Selection.getSelectionEx()[4].SubObjects[0]
				
				if sub.ShapeType == "Face":
					face1 = sub
			except:
				skip = 1

			# set edge plane
			self.gSingleDrawerPlane = MagicPanels.getEdgePlane(obj1, edge1, "clean")

			startX = 0
			startY = 0
			startZ = 0
			width = 0
			height = 0
			depth = 0
			
			if self.gSingleDrawerPlane == "X":
				
				startZ = float(edge1.CenterOfMass.z)

				# set drawer direction
				if face1 != False:

					sign = float(face1.CenterOfMass.y) - float(edge1.CenterOfMass.y)
					
					if sign >= 0:
						self.gSingleDrawerDirection = "+"
					else:
						self.gSingleDrawerDirection = "-"
					
				if edge1 != False and edge2 == False:
					
					width = float(edge1.Length)
					height = float(edge1.CenterOfMass.z)
					depth = float(obj1.Width.Value)
					startX = self.getStartVertex(edge1, "X")
					startY = float(edge1.CenterOfMass.y)
					startZ = 0

				if edge1 != False and edge2 != False:
					
					height = float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z)
					
					# first short shelf and second long top
					if float(edge1.Length) < float(edge2.Length):
						width = float(edge1.Length)
						startX = self.getStartVertex(edge1, "X")
						startY = float(edge2.CenterOfMass.y) # shelf might be inside, so depth to other
					
					# first long bottom floor and second short shelf
					else:
						width = float(edge2.Length)
						startX = self.getStartVertex(edge2, "X")
						startY = float(edge1.CenterOfMass.y) # shelf might be inside, so depth to other
					
					# first short shelf and second long top
					if float(obj1.Width.Value) < float(obj2.Width.Value):
						depth = float(obj1.Width.Value)
					
					# first long bottom floor and second short shelf
					else:
						depth = float(obj2.Width.Value)
				
				# try to fix depth if face selected
				if face1 != False:
					depth = abs(float(face1.CenterOfMass.y) - startY)
			
				if (
					edge1 != False and 
					edge2 != False and 
					edge3 != False and 
					edge4 != False and 
					face1 != False
					):
					
					startX = float(edge3.CenterOfMass.x)
					startY = float(edge1.CenterOfMass.y)
					startZ = float(edge1.CenterOfMass.z)
					
					width = abs(float(edge4.CenterOfMass.x) - float(edge3.CenterOfMass.x))
					height = abs(float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z))
					
					# set drawer direction
					if face1 != False:

						depth = float(face1.CenterOfMass.y) - startY
						
						if sign >= 0:
							self.gSingleDrawerDirection = "+"
						else:
							self.gSingleDrawerDirection = "-"
							depth = abs(depth)

			if self.gSingleDrawerPlane == "Y":
				
				startZ = float(edge1.CenterOfMass.z)

				# set drawer direction
				if face1 != False:

					sign = float(face1.CenterOfMass.x) - float(edge1.CenterOfMass.x)
					
					if sign >= 0:
						self.gSingleDrawerDirection = "+"
					else:
						self.gSingleDrawerDirection = "-"
					
				if edge1 != False and edge2 == False:
					
					width = float(edge1.Length)
					height = float(edge1.CenterOfMass.z)
					depth = float(obj1.Length.Value)
					startX = float(edge1.CenterOfMass.x)
					startY = self.getStartVertex(edge1, "Y")
					startZ = 0

				if edge1 != False and edge2 != False:
					
					height = float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z)
					
					# first short shelf and second long top
					if float(edge1.Length) < float(edge2.Length):
						width = float(edge1.Length)
						startX = float(edge2.CenterOfMass.x) # shelf might be inside, so depth to other
						startY = self.getStartVertex(edge1, "Y")
					
					# first long bottom floor and second short shelf
					else:
						width = float(edge2.Length)
						startX = float(edge1.CenterOfMass.x) # shelf might be inside, so depth to other
						startY = self.getStartVertex(edge2, "Y")
					
					# first short shelf and second long top
					if float(obj1.Length.Value) < float(obj2.Length.Value):
						depth = float(obj1.Length.Value)
					
					# first long bottom floor and second short shelf
					else:
						depth = float(obj2.Length.Value)
				
				# try to fix depth if face selected
				if face1 != False:
					depth = abs(float(face1.CenterOfMass.x) - startX)
			
				if (
					edge1 != False and 
					edge2 != False and 
					edge3 != False and 
					edge4 != False and 
					face1 != False
					):
					
					startX = float(edge1.CenterOfMass.x)
					startY = float(edge3.CenterOfMass.y)
					startZ = float(edge1.CenterOfMass.z)
					
					width = abs(float(edge4.CenterOfMass.y) - float(edge3.CenterOfMass.y))
					height = abs(float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z))
					
					# set drawer direction
					if face1 != False:

						depth = float(face1.CenterOfMass.x) - startX
						
						if sign >= 0:
							self.gSingleDrawerDirection = "+"
						else:
							self.gSingleDrawerDirection = "-"
							depth = abs(depth)

			# set values to text fields
			self.og2E.setText(str(startX))
			self.og3E.setText(str(startY))
			self.og4E.setText(str(startZ))
			self.og5E.setText(str(width))
			self.og6E.setText(str(height))
			self.og7E.setText(str(depth))

		# ############################################################################
		def calculateFrontFromGap(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			obj4 = False
			
			edge1 = False
			edge2 = False
			edge3 = False
			edge4 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				obj2 = FreeCADGui.Selection.getSelection()[1]
				edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				obj3 = FreeCADGui.Selection.getSelection()[2]
				edge3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
				
				obj4 = FreeCADGui.Selection.getSelection()[3]
				edge4 = FreeCADGui.Selection.getSelectionEx()[3].SubObjects[0]
				
			except:
				return

			gh = float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z)
			gw = float(edge4.CenterOfMass.x) - float(edge3.CenterOfMass.x)
			
			sx = float(edge3.CenterOfMass.x)
			sy = float(edge3.CenterOfMass.y)
			sz = float(edge1.CenterOfMass.z)
			
			thick = float(self.ofr7E.text())
			
			offL = float(self.ofr81E.text())
			offR = float(self.ofr82E.text())
			offT = float(self.ofr83E.text())
			offB = float(self.ofr84E.text())
			
			# outside
			if self.gSelectedFurniture == "F23":
				width = offL + gw + offR
				height = offB + gh + offT
				startX = sx - offL
				startY = sy - thick
				startZ = sz - offB

			# inside
			if self.gSelectedFurniture == "F24":
				width = gw - offL - offR
				height = gh - offB - offT
				startX = sx + offL
				startY = sy
				startZ = sz + offB
	
			# set values to text fields
			self.ofr2E.setText(str(startX))
			self.ofr3E.setText(str(startY))
			self.ofr4E.setText(str(startZ))
			self.ofr5E.setText(str(width))
			self.ofr6E.setText(str(height))

		# ############################################################################
		def calculateFrontWithGlass(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			obj4 = False
			
			edge1 = False
			edge2 = False
			edge3 = False
			edge4 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				obj2 = FreeCADGui.Selection.getSelection()[1]
				edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				obj3 = FreeCADGui.Selection.getSelection()[2]
				edge3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
				
				obj4 = FreeCADGui.Selection.getSelection()[3]
				edge4 = FreeCADGui.Selection.getSelectionEx()[3].SubObjects[0]
				
			except:
				return

			gh = abs(float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z))
			gw = abs(float(edge4.CenterOfMass.x) - float(edge3.CenterOfMass.x))
			
			gsx = float(edge3.CenterOfMass.x)
			gsy = float(edge3.CenterOfMass.y)
			gsz = float(edge1.CenterOfMass.z)
			
			thick = float(self.ofglass2E.text())
			overlapH = float(self.ofglass3E.text())
			overlapV = float(self.ofglass4E.text())
			
			# outside
			if self.gSelectedFurniture == "F37" or self.gSelectedFurniture == "F38":
				
				width = gw + (2 * overlapH)
				height = gh + (2 * overlapV)
			
				startX = gsx - overlapH
				startY = gsy - thick
				startZ = gsz - overlapV

			# inside
			if self.gSelectedFurniture == "F39" or self.gSelectedFurniture == "F40":
				
				width = gw - (2 * overlapH)
				height = gh - (2 * overlapV)
			
				startX = gsx + overlapH
				startY = gsy
				startZ = gsz + overlapV

			# simple
			if self.gSelectedFurniture == "F37" or self.gSelectedFurniture == "F39":
				barWidth = int(width / 10)

			# decorated
			if self.gSelectedFurniture == "F38" or self.gSelectedFurniture == "F40":
				barWidth = int(width / 20)
				
			# set values to text fields
			self.ofglass71E.setText(str(startX))
			self.ofglass72E.setText(str(startY))
			self.ofglass73E.setText(str(startZ))
			self.ofglass8E.setText(str(barWidth))
			self.ofglass9E.setText(str(width))
			self.ofglass10E.setText(str(height))

		# ############################################################################
		def calculateFaceframeFromGap(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			obj4 = False
			
			edge1 = False
			edge2 = False
			edge3 = False
			edge4 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				obj2 = FreeCADGui.Selection.getSelection()[1]
				edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				obj3 = FreeCADGui.Selection.getSelection()[2]
				edge3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
				
				obj4 = FreeCADGui.Selection.getSelection()[3]
				edge4 = FreeCADGui.Selection.getSelectionEx()[3].SubObjects[0]
				
			except:
				return

			gh = abs(float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z))
			gw = abs(float(edge4.CenterOfMass.x) - float(edge3.CenterOfMass.x))
			
			gsx = float(edge3.CenterOfMass.x)
			gsy = float(edge3.CenterOfMass.y)
			gsz = float(edge1.CenterOfMass.z)
			
			barThick = float(self.offrame3E.text())
			offX = float(self.offrame4E.text())
			offY = float(self.offrame5E.text())
			
			# get furniture thickness from left side
			sizes = []
			sizes = MagicPanels.getSizes(obj3)
			sizes.sort()
			sideThick = sizes[0]
			
			width = offX + sideThick + gw + sideThick + offX
			height = offX + sideThick + gh + sideThick + offX
			startX = gsx - sideThick - offX
			startY = gsy - barThick + offY
			startZ = gsz - sideThick - offX

			# set values to text fields
			self.offrame71E.setText(str(startX))
			self.offrame72E.setText(str(startY))
			self.offrame73E.setText(str(startZ))
			self.offrame8E.setText(str(width))
			self.offrame9E.setText(str(height))

		# ############################################################################
		def calculateShelfFromGap(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			
			edge1 = False
			edge2 = False
			face1 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				obj2 = FreeCADGui.Selection.getSelection()[1]
				edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				obj3 = FreeCADGui.Selection.getSelection()[2]
				face1 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
				
			except:
				return

			gdepth = float(face1.CenterOfMass.y) - float(edge1.CenterOfMass.y)
			gwidth = float(edge2.CenterOfMass.x) - float(edge1.CenterOfMass.x)
			
			sx = float(edge1.CenterOfMass.x)
			sy = float(edge1.CenterOfMass.y)
			sz = float(edge1.CenterOfMass.z)
			
			thick = float(self.osh1E.text())
			udepth = float(self.osh2E.text())
			
			offL = float(self.osh31E.text())
			offR = float(self.osh32E.text())
			offF = float(self.osh33E.text())
			offB = float(self.osh34E.text())
			
			width = gwidth - offL - offR
			
			if udepth == 0:
				depth = gdepth - offF - offB
			else:
				depth = udepth
				offB = 0
				offF = gdepth - depth
			
			startX = sx + offL
			startY = sy + offF
			startZ = sz

			# set values to text fields
			self.osh2E.setText(str(depth))
			self.osh31E.setText(str(offL))
			self.osh32E.setText(str(offR))
			self.osh33E.setText(str(offF))
			self.osh34E.setText(str(offB))
			
			self.osh51E.setText(str(startX))
			self.osh52E.setText(str(startY))
			self.osh53E.setText(str(startZ))
			
			self.osh6E.setText(str(width))
			self.osh7E.setText(str(depth))

		# ############################################################################
		def calculateShelfSeries(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			obj4 = False
			obj5 = False
			
			edge1 = False
			edge2 = False
			edge3 = False
			edge4 = False
			face1 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				obj2 = FreeCADGui.Selection.getSelection()[1]
				edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				obj3 = FreeCADGui.Selection.getSelection()[2]
				edge3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
				
				obj4 = FreeCADGui.Selection.getSelection()[3]
				edge4 = FreeCADGui.Selection.getSelectionEx()[3].SubObjects[0]
				
				obj5 = FreeCADGui.Selection.getSelection()[4]
				face1 = FreeCADGui.Selection.getSelectionEx()[4].SubObjects[0]
				
			except:
				return
				
			gh = abs(float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z))
			gw = abs(float(edge4.CenterOfMass.x) - float(edge3.CenterOfMass.x))
			gd = abs(float(face1.CenterOfMass.y) - float(edge3.CenterOfMass.y))
			
			sx = float(edge3.CenterOfMass.x)
			sy = float(edge3.CenterOfMass.y)
			sz = float(edge1.CenterOfMass.z)
			
			thick = float(self.oshs1E.text())
			num = int(self.oshs2E.text())
			
			startX = sx
			startY = sy
			startZ = sz
			
			width = gw
			depth = gd
			
			offset = (gh - (num * thick)) / (num + 1)
			
			# set values to text fields
			self.oshs41E.setText(str(startX))
			self.oshs42E.setText(str(startY))
			self.oshs43E.setText(str(startZ))

			self.oshs5E.setText(str(width))
			self.oshs6E.setText(str(depth))
			self.oshs7E.setText(str(offset))

		# ############################################################################
		def calculateSideFromGap(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			obj4 = False
			
			edge1 = False
			edge2 = False
			edge3 = False
			edge4 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				obj2 = FreeCADGui.Selection.getSelection()[1]
				edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				obj3 = FreeCADGui.Selection.getSelection()[2]
				edge3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
				
				obj4 = FreeCADGui.Selection.getSelection()[3]
				edge4 = FreeCADGui.Selection.getSelectionEx()[3].SubObjects[0]

			except:
				return
			
			thick = float(self.oside1E.text())
			uwidth = float(self.oside2E.text())
			offL = float(self.oside31E.text())
			offR = float(self.oside32E.text())
			offT = float(self.oside33E.text())
			offB = float(self.oside34E.text())
			
			self.gSideEdgePlane = MagicPanels.getEdgePlane(obj1, edge1, "clean")
			
			if self.gSideEdgePlane == "X":
				
				gheight = abs(float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z))
				gwidth = float(edge4.CenterOfMass.x) - float(edge3.CenterOfMass.x)
				
				if gwidth > 0:
					self.gSideDirection = "+"
				else:
					self.gSideDirection = "-"
					gwidth = abs(gwidth)

				if uwidth == 0:
					width = gwidth - offL - offR
					height = gheight - offT - offB
				
				else:
					width = uwidth
					offL = 0
					offR = gwidth - width
					
					height = gheight
					offT = 0
					offB = 0
				
				if self.gSideDirection == "+":
					startX = float(edge3.CenterOfMass.x) + offL
					startY = float(edge3.CenterOfMass.y)
					startZ = float(edge1.CenterOfMass.z) + offB

				if self.gSideDirection == "-":
					startX = float(edge3.CenterOfMass.x) - offL - width
					startY = float(edge3.CenterOfMass.y) - thick 
					startZ = float(edge1.CenterOfMass.z) + offB

			if self.gSideEdgePlane == "Y":
				
				gheight = abs(float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z))
				gwidth = float(edge4.CenterOfMass.y) - float(edge3.CenterOfMass.y)
				
				if gwidth > 0:
					self.gSideDirection = "+"
				else:
					self.gSideDirection = "-"
					gwidth = abs(gwidth)

				if uwidth == 0:
					width = gwidth - offL - offR
					height = gheight - offT - offB
				
				else:
					width = uwidth
					offL = 0
					offR = gwidth - width
					
					height = gheight
					offT = 0
					offB = 0
				
				if self.gSideDirection == "+":
					startX = float(edge3.CenterOfMass.x) - thick
					startY = float(edge3.CenterOfMass.y) + offL
					startZ = float(edge1.CenterOfMass.z) + offB

				if self.gSideDirection == "-":
					startX = float(edge3.CenterOfMass.x)
					startY = float(edge3.CenterOfMass.y) - offL - width
					startZ = float(edge1.CenterOfMass.z) + offB

			# set values to text fields
			self.oside2E.setText(str(width))
			self.oside31E.setText(str(offL))
			self.oside32E.setText(str(offR))
			self.oside33E.setText(str(offT))
			self.oside34E.setText(str(offB))
			
			self.oside51E.setText(str(startX))
			self.oside52E.setText(str(startY))
			self.oside53E.setText(str(startZ))
			
			self.oside6E.setText(str(width))
			self.oside7E.setText(str(height))

			
			
			'''
			# face below
			if float(face1.CenterOfMass.z) < float(edge1.CenterOfMass.z):
				gheight = float(edge1.CenterOfMass.z) - float(face1.CenterOfMass.z)
				sz = float(face1.CenterOfMass.z)
				
			# face above I hope so :-)
			else: 
				gheight = float(face1.CenterOfMass.z) - float(edge1.CenterOfMass.z)
				sz = float(MagicPanels.touchTypo(edge1)[0].Z)
				
			gdepth = float(edge1.Length)
			
			# prefer closer point to start
			if float(MagicPanels.touchTypo(edge1)[0].Y) < float(MagicPanels.touchTypo(edge1)[1].Y):
				sx = float(MagicPanels.touchTypo(edge1)[0].X)
				sy = float(MagicPanels.touchTypo(edge1)[0].Y)
				
			else:
				sx = float(MagicPanels.touchTypo(edge1)[1].X)
				sy = float(MagicPanels.touchTypo(edge1)[1].Y)
				
			
			thick = float(self.ocs1E.text())
			udepth = float(self.ocs2E.text())
			
			offTo = float(self.ocs31E.text())
			offBo = float(self.ocs32E.text())
			offFr = float(self.ocs33E.text())
			offBa = float(self.ocs34E.text())
			
			height = gheight - offBo - offTo
			
			if udepth == 0:
				depth = gdepth - offFr - offBa
			else:
				depth = udepth
				offBa = 0
				offFr = gdepth - depth
			
			width = float(edge2.CenterOfMass.x) - float(edge1.CenterOfMass.x)
			startX = sx + (width / 2) - (thick / 2) 
			startY = sy + offFr
			startZ = sz + offBo
			'''
			
		# ############################################################################
		def calculateCenterSideFromGap(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			
			edge1 = False
			edge2 = False
			face1 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				obj2 = FreeCADGui.Selection.getSelection()[1]
				edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				obj3 = FreeCADGui.Selection.getSelection()[2]
				face1 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
				
			except:
			
				try:
					obj1 = FreeCADGui.Selection.getSelection()[0]
					edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
					
					obj2 = FreeCADGui.Selection.getSelection()[0]
					edge2 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[1]
					
					obj3 = FreeCADGui.Selection.getSelection()[1]
					face1 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
					
				except:
					return
				
			# face below
			if float(face1.CenterOfMass.z) < float(edge1.CenterOfMass.z):
				gheight = float(edge1.CenterOfMass.z) - float(face1.CenterOfMass.z)
				sz = float(face1.CenterOfMass.z)
				
			# face above I hope so :-)
			else: 
				gheight = float(face1.CenterOfMass.z) - float(edge1.CenterOfMass.z)
				sz = float(MagicPanels.touchTypo(edge1)[0].Z)
				
			gdepth = float(edge1.Length)
			
			# prefer closer point to start
			if float(MagicPanels.touchTypo(edge1)[0].Y) < float(MagicPanels.touchTypo(edge1)[1].Y):
				sx = float(MagicPanels.touchTypo(edge1)[0].X)
				sy = float(MagicPanels.touchTypo(edge1)[0].Y)
				
			else:
				sx = float(MagicPanels.touchTypo(edge1)[1].X)
				sy = float(MagicPanels.touchTypo(edge1)[1].Y)
				
			
			thick = float(self.ocs1E.text())
			udepth = float(self.ocs2E.text())
			
			offTo = float(self.ocs31E.text())
			offBo = float(self.ocs32E.text())
			offFr = float(self.ocs33E.text())
			offBa = float(self.ocs34E.text())
			
			height = gheight - offBo - offTo
			
			if udepth == 0:
				depth = gdepth - offFr - offBa
			else:
				depth = udepth
				offBa = 0
				offFr = gdepth - depth
			
			width = float(edge2.CenterOfMass.x) - float(edge1.CenterOfMass.x)
			startX = sx + (width / 2) - (thick / 2) 
			startY = sy + offFr
			startZ = sz + offBo

			# set values to text fields
			self.ocs2E.setText(str(depth))
			self.ocs31E.setText(str(offTo))
			self.ocs32E.setText(str(offBo))
			self.ocs33E.setText(str(offFr))
			self.ocs34E.setText(str(offBa))
			
			self.ocs51E.setText(str(startX))
			self.ocs52E.setText(str(startY))
			self.ocs53E.setText(str(startZ))
			
			self.ocs6E.setText(str(height))
			self.ocs7E.setText(str(depth))

		# ############################################################################
		def calculateDrawerSeries(self):
			
			obj1 = False
			obj2 = False
			obj3 = False
			obj4 = False
			obj5 = False
			
			edge1 = False
			edge2 = False
			edge3 = False
			edge4 = False
			
			face1 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
				
				obj2 = FreeCADGui.Selection.getSelection()[1]
				edge2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
				
				obj3 = FreeCADGui.Selection.getSelection()[2]
				edge3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]
				
				obj4 = FreeCADGui.Selection.getSelection()[3]
				edge4 = FreeCADGui.Selection.getSelectionEx()[3].SubObjects[0]
				
				obj5 = FreeCADGui.Selection.getSelection()[4]
				face1 = FreeCADGui.Selection.getSelectionEx()[4].SubObjects[0]
			
			except:
				return

			startX = float(edge3.CenterOfMass.x)
			startY = float(edge3.CenterOfMass.y)
			startZ = float(edge1.CenterOfMass.z)
			
			gw = abs(float(edge4.CenterOfMass.x) - float(edge3.CenterOfMass.x))
			gh = abs(float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z))
			gd = abs(float(face1.CenterOfMass.y) - float(edge3.CenterOfMass.y))
			
			num = int(self.ods2E.text())
			offset = float(self.ods40E.text())
			
			width = gw
			height = ( gh - ((num + 1) * offset) ) / num
			depth = gd
			
			# set values to text fields
			self.ods61E.setText(str(startX))
			self.ods62E.setText(str(startY))
			self.ods63E.setText(str(startZ))
			self.ods7E.setText(str(width))
			self.ods8E.setText(str(height))
			self.ods9E.setText(str(depth))

		# ############################################################################
		def calculateTable(self):

			obj = False
			sub = False
			
			try:
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

			except:
				return
			
			if sub.ShapeType == "Vertex":
				
				startX = float(sub.Point.x)
				startY = float(sub.Point.y)
				startZ = float(sub.Point.z)

				# set values to text fields
				self.otb81E.setText(str(startX))
				self.otb82E.setText(str(startY))
				self.otb83E.setText(str(startZ))

		# ############################################################################
		# actions - draw functions
		# ############################################################################

		# ############################################################################
		def createF0(self):
			
			sx = float(self.oo11E.text())
			sy = float(self.oo12E.text())
			sz = float(self.oo13E.text())
			
			depth = self.gFSY - self.gThick
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(sx, sy + self.gThick, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ - (2 * self.gThick)
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy + self.gThick, sz + self.gThick)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ - (2 * self.gThick)
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy + self.gThick, sz + self.gThick)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX - (2 * self.gThick)
			o4.Height = self.gFSZ - (2 * self.gThick)
			o4.Width = self.gThick
			pl = FreeCAD.Vector(sx + self.gThick, sy + depth, sz + self.gThick)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(sx, sy + self.gThick, sz + self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor
			
			# Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o6.Label = translate('magicStart', 'Front')
			o6.Length = self.gFSX - self.gThick
			o6.Height = self.gFSZ - self.gThick - 4
			o6.Width = self.gThick
			pl = FreeCAD.Vector(sx + (self.gThick / 2), sy, sz + (self.gThick / 2) + 2)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.ShapeColor = self.gColor
			
			# Shelf
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o7.Label = translate('magicStart', 'Shelf')
			o7.Length = self.gFSX - (2 * self.gThick)
			o7.Height = self.gThick
			o7.Width = depth - (3 * self.gThick)
			pl = FreeCAD.Vector(sx + self.gThick, sy + (3 * self.gThick), sz + (self.gFSZ / 2) - (self.gThick / 2))
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			o7.ViewObject.ShapeColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','FurnitureModule')
			container.setLink([o1, o2, o3, o4, o5, o6, o7])
			container.Label = "Furniture, Module"

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF1(self):
			
			sx = float(self.oo11E.text())
			sy = float(self.oo12E.text())
			sz = float(self.oo13E.text())
			
			depth = self.gFSY - 3
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX - (2 * self.gThick)
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy, sz + (self.gFSZ / 10))
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX
			o4.Height = self.gFSZ - (self.gFSZ / 10)
			o4.Width = 3
			pl = FreeCAD.Vector(sx, sy + depth, sz + (self.gFSZ / 10))
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX - (2 * self.gThick)
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy, sz + self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor

			# Shelf
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o6.Label = translate('magicStart', 'Shelf')
			o6.Length = self.gFSX - (2 * self.gThick)
			o6.Height = self.gThick
			o6.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy, sz + (self.gFSZ / 2) - (self.gThick / 2))
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.ShapeColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','FurnitureModule')
			container.setLink([o1, o2, o3, o4, o5, o6])
			container.Label = "Furniture, Module"

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF10(self):
			
			sx = float(self.oo11E.text())
			sy = float(self.oo12E.text())
			sz = float(self.oo13E.text())
			
			# calculation
			mNum = 3
			sideZ = ((self.gFSZ - self.gThick - (mNum * self.gThick)) / mNum)
			depth = self.gFSY - self.gThick
			
			# #######################
			# Modules
			# #######################
			
			for i in range(mNum):
			
				posZ = (i * sideZ) + (i * self.gThick)
			
				# Floor
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
				o1.Label = translate('magicStart', 'Floor M'+str(i))
				o1.Length = self.gFSX
				o1.Height = self.gThick
				o1.Width = depth
				pl = FreeCAD.Vector(sx, sy + self.gThick, sz + posZ)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				o1.ViewObject.ShapeColor = self.gColor
				
				# Left Side
				o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
				o2.Label = translate('magicStart', 'Left M'+str(i))
				o2.Length = self.gThick
				o2.Height = sideZ
				o2.Width = depth
				pl = FreeCAD.Vector(sx, sy + self.gThick, sz + posZ + self.gThick)
				o2.Placement = FreeCAD.Placement(pl, self.gR)
				o2.ViewObject.ShapeColor = self.gColor
				
				# Right Side
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
				o3.Label = translate('magicStart', 'Right M'+str(i))
				o3.Length = self.gThick
				o3.Height = sideZ
				o3.Width = depth
				pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy + self.gThick, sz + posZ + self.gThick)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				o3.ViewObject.ShapeColor = self.gColor
				
				# Back
				o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
				o4.Label = translate('magicStart', 'Back M'+str(i))
				o4.Length = self.gFSX - (2 * self.gThick)
				o4.Height = sideZ
				o4.Width = self.gThick
				pl = FreeCAD.Vector(sx + self.gThick, sy + depth, sz + posZ + self.gThick)
				o4.Placement = FreeCAD.Placement(pl, self.gR)
				o4.ViewObject.ShapeColor = self.gColor
				
				# Front
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
				o5.Label = translate('magicStart', 'Front M'+str(i))
				o5.Length = self.gFSX - self.gThick
				o5.Height = sideZ + self.gThick - 4
				o5.Width = self.gThick
				pl = FreeCAD.Vector(sx + (self.gThick / 2), sy, sz + posZ + (self.gThick / 2) + 2)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				o5.ViewObject.ShapeColor = self.gColor
				
				# Shelf
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
				o6.Label = translate('magicStart', 'Shelf M'+str(i))
				o6.Length = self.gFSX - (2 * self.gThick)
				o6.Height = self.gThick
				o6.Width = depth - (3 * self.gThick)
				pZ = ((2 * i) + 1) * ((self.gThick + sideZ) / 2)
				pl = FreeCAD.Vector(sx + self.gThick, sy + (3 * self.gThick), sz + pZ)
				o6.Placement = FreeCAD.Placement(pl, self.gR)
				o6.ViewObject.ShapeColor = self.gColor
				
				# create folder
				group = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroup','Group')
				group.Label = translate('magicStart', 'Module '+str(i))
				group.addObject(o1)
				group.addObject(o2)
				group.addObject(o3)
				group.addObject(o4)
				group.addObject(o5)
				group.addObject(o6)
			
			# #######################
			# Top cover
			# #######################
			
			# final top
			t1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			t1.Label = translate('magicStart', 'Top cover')
			t1.Length = self.gFSX
			t1.Height = self.gThick
			t1.Width = depth
			pZ = mNum * (self.gThick + sideZ)
			pl = FreeCAD.Vector(sx, sy + self.gThick, sz + pZ)
			t1.Placement = FreeCAD.Placement(pl, self.gR)
			t1.ViewObject.ShapeColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF16(self):
			
			FSX = float(self.of1E.text())
			FSY = float(self.of2E.text())
			height = float(self.of3E.text())
			thick = float(self.of4E.text())
			frontOF = float(self.of5E.text())
			depth = self.gFSY - frontOF
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(0, frontOF, -height)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(FSX - thick, frontOF, -height)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFoot')
			container.setLink([o1, o2])
			container.Label = "Container, Foot"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF17(self):
			
			FSX = float(self.of1E.text())
			FSY = float(self.of2E.text())
			height = float(self.of3E.text())
			thick = float(self.of4E.text())
			frontOF = float(self.of5E.text())
			depth = FSY - frontOF
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(0, frontOF, -height)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(FSX - thick, frontOF, -height)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootBack")
			o3.Label = translate('magicStart', 'Foot Back')
			o3.Length = FSX - (2 * thick)
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(thick, frontOF + depth - thick, -height)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Front
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootFront")
			o4.Label = translate('magicStart', 'Foot Front')
			o4.Length = FSX - (2 * thick)
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(thick, frontOF, -height)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFoot')
			container.setLink([o1, o2, o3, o4])
			container.Label = "Container, Foot"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF18(self):
			
			FSX = float(self.of1E.text())
			FSY = float(self.of2E.text())
			height = float(self.of3E.text())
			thick = float(self.of4E.text())
			frontOF = float(self.of5E.text())
			depth = FSY - frontOF

			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(0, frontOF, -height)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(FSX - thick, frontOF, -height)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootBack")
			o3.Label = translate('magicStart', 'Foot Back')
			o3.Length = FSX - (2 * thick)
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(thick, frontOF + depth - thick, -height)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Front
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootFront")
			o4.Label = translate('magicStart', 'Foot Front')
			o4.Length = FSX - (2 * thick)
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(thick, frontOF, -height)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Center
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootCenter")
			o5.Label = translate('magicStart', 'Foot Center')
			o5.Length = FSX - (2 * thick)
			o5.Height = height
			o5.Width = thick
			py = frontOF + (depth / 2) - (thick / 2)
			pl = FreeCAD.Vector(thick, py, -height)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFoot')
			container.setLink([o1, o2, o3, o4, o5])
			container.Label = "Container, Foot"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF19(self):
			
			FSX = float(self.of1E.text())
			FSY = float(self.of2E.text())
			height = float(self.of3E.text())
			thick = float(self.of4E.text())
			frontOF = float(self.of5E.text())
			depth = FSY - frontOF

			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(0, frontOF, -height)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(FSX - thick, frontOF, -height)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootBack")
			o3.Label = translate('magicStart', 'Foot Back')
			o3.Length = FSX - (2 * thick)
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(thick, frontOF + depth - thick, -height)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Front
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootFront")
			o4.Label = translate('magicStart', 'Foot Front')
			o4.Length = FSX - (2 * thick)
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(thick, frontOF + thick, -height)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFoot')
			container.setLink([o1, o2, o3, o4])
			container.Label = "Container, Foot"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF20(self):
			
			FSX = float(self.of1E.text())
			FSY = float(self.of2E.text())
			height = float(self.of3E.text())
			thick = float(self.of4E.text())
			frontOF = float(self.of5E.text())
			depth = FSY - frontOF
			
			# Left Front
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeftFront")
			o1.Label = translate('magicStart', 'Foot Left Front')
			o1.Length = thick
			o1.Height = height
			o1.Width = thick
			pl = FreeCAD.Vector(0, frontOF, -height)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Left Back
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeftBack")
			o2.Label = translate('magicStart', 'Foot Left Back')
			o2.Length = thick
			o2.Height = height
			o2.Width = thick
			pl = FreeCAD.Vector(0, frontOF + depth - thick, -height)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Right Front
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRightFront")
			o3.Label = translate('magicStart', 'Foot Right Front')
			o3.Length = thick
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(FSX - thick, frontOF, -height)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Right Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRightBack")
			o4.Label = translate('magicStart', 'Foot Right Back')
			o4.Length = thick
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(FSX - thick, frontOF + depth - thick, -height)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFoot')
			container.setLink([o1, o2, o3, o4])
			container.Label = "Container, Foot"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF21(self):
			
			p0X = float(self.og2E.text())
			p0Y = float(self.og3E.text())
			p0Z = float(self.og4E.text())
			
			width = float(self.og5E.text())
			height = float(self.og6E.text())
			depth = float(self.og7E.text())
			
			thick = float(self.og8E.text())
			
			sidesOF = float(self.og91E.text())
			sideOF = sidesOF / 2
			backOF = float(self.og92E.text())
			topOF = float(self.og93E.text())
			bottomOF = float(self.og94E.text())
			
			if self.gSingleDrawerPlane == "X":
			
				if self.gSingleDrawerDirection == "+":

					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = thick
					o1.Height = height - bottomOF - topOF - 3
					o1.Width = depth - backOF
					pl = FreeCAD.Vector(p0X + sideOF, p0Y, p0Z + bottomOF + 3)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					o1.ViewObject.ShapeColor = self.gColor
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = thick
					o2.Height = height - bottomOF - topOF - 3
					o2.Width = depth - backOF
					pl = FreeCAD.Vector(p0X + width - thick - sideOF, p0Y, p0Z + bottomOF + 3)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					o2.ViewObject.ShapeColor = self.gColor
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = width - (2 * thick) - sidesOF
					o3.Height = height - bottomOF - topOF - 3
					o3.Width = thick
					pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y + depth - thick - backOF, p0Z + bottomOF + 3)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					o3.ViewObject.ShapeColor = self.gColor
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = width - (2 * thick) - sidesOF
					o4.Height = height - bottomOF - topOF - 3
					o4.Width = thick
					pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y, p0Z + bottomOF + 3)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					o4.ViewObject.ShapeColor = self.gColor

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = width - sidesOF
					o5.Height = 3
					o5.Width = depth - backOF
					pl = FreeCAD.Vector(p0X + sideOF, p0Y, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					o5.ViewObject.ShapeColor = self.gColor

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = width + thick
					o6.Height = height + thick - 4
					o6.Width = thick
					pl = FreeCAD.Vector(p0X - (thick / 2), p0Y - thick, p0Z - (thick / 2) + 2)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					o6.ViewObject.ShapeColor = self.gColor

					container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDrawer')
					container.setLink([o1, o2, o3, o4, o5, o6])
					container.Label = "Container, Drawer"
				
					# recompute
					FreeCAD.ActiveDocument.recompute()
			
				if self.gSingleDrawerDirection == "-":

					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = thick
					o1.Height = height - bottomOF - topOF - 3
					o1.Width = depth - backOF
					pl = FreeCAD.Vector(p0X - sideOF - thick, p0Y - depth + backOF, p0Z + bottomOF + 3)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					o1.ViewObject.ShapeColor = self.gColor
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = thick
					o2.Height = height - bottomOF - topOF - 3
					o2.Width = depth - backOF
					pl = FreeCAD.Vector(p0X - width + sideOF, p0Y - depth + backOF, p0Z + bottomOF + 3)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					o2.ViewObject.ShapeColor = self.gColor
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = width - (2 * thick) - sidesOF
					o3.Height = height - bottomOF - topOF - 3
					o3.Width = thick
					pl = FreeCAD.Vector(p0X - width + sideOF + thick, p0Y - depth + backOF, p0Z + bottomOF + 3)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					o3.ViewObject.ShapeColor = self.gColor
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = width - (2 * thick) - sidesOF
					o4.Height = height - bottomOF - topOF - 3
					o4.Width = thick
					pl = FreeCAD.Vector(p0X - width + sideOF + thick, p0Y - thick, p0Z + bottomOF + 3)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					o4.ViewObject.ShapeColor = self.gColor

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = width - sidesOF
					o5.Height = 3
					o5.Width = depth - backOF
					pl = FreeCAD.Vector(p0X - width + sideOF, p0Y - depth + backOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					o5.ViewObject.ShapeColor = self.gColor

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = width + thick
					o6.Height = height + thick - 4
					o6.Width = thick
					pl = FreeCAD.Vector(p0X - width - (thick / 2), p0Y, p0Z - (thick / 2) + 2)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					o6.ViewObject.ShapeColor = self.gColor

					container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDrawer')
					container.setLink([o1, o2, o3, o4, o5, o6])
					container.Label = "Container, Drawer"
				
					# recompute
					FreeCAD.ActiveDocument.recompute()

			if self.gSingleDrawerPlane == "Y":
			
				if self.gSingleDrawerDirection == "+":
				
					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = depth - backOF
					o1.Height = height - bottomOF - topOF - 3
					o1.Width = thick
					pl = FreeCAD.Vector(p0X, p0Y - sideOF - thick, p0Z + bottomOF + 3)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					o1.ViewObject.ShapeColor = self.gColor
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = depth - backOF
					o2.Height = height - bottomOF - topOF - 3
					o2.Width = thick
					pl = FreeCAD.Vector(p0X, p0Y - width + sideOF, p0Z + bottomOF + 3)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					o2.ViewObject.ShapeColor = self.gColor
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = thick
					o3.Height = height - bottomOF - topOF - 3
					o3.Width = width - (2 * thick) - sidesOF
					pl = FreeCAD.Vector(p0X + depth - thick - backOF, p0Y - width + sideOF + thick, p0Z + bottomOF + 3)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					o3.ViewObject.ShapeColor = self.gColor
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = thick
					o4.Height = height - bottomOF - topOF - 3
					o4.Width = width - (2 * thick) - sidesOF
					pl = FreeCAD.Vector(p0X, p0Y - width + sideOF + thick, p0Z + bottomOF + 3)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					o4.ViewObject.ShapeColor = self.gColor

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = depth - backOF
					o5.Height = 3
					o5.Width = width - sidesOF
					pl = FreeCAD.Vector(p0X, p0Y - width + sideOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					o5.ViewObject.ShapeColor = self.gColor

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = thick
					o6.Height = height + thick - 4
					o6.Width = width + thick
					pl = FreeCAD.Vector(p0X - thick, p0Y - width - (thick / 2), p0Z - (thick / 2) + 2)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					o6.ViewObject.ShapeColor = self.gColor

					container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDrawer')
					container.setLink([o1, o2, o3, o4, o5, o6])
					container.Label = "Container, Drawer"
				
					# recompute
					FreeCAD.ActiveDocument.recompute()
		
				if self.gSingleDrawerDirection == "-":
				
					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = depth - backOF
					o1.Height = height - bottomOF - topOF - 3
					o1.Width = thick
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF, p0Z + bottomOF + 3)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					o1.ViewObject.ShapeColor = self.gColor
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = depth - backOF
					o2.Height = height - bottomOF - topOF - 3
					o2.Width = thick
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + width - sideOF - thick, p0Z + bottomOF + 3)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					o2.ViewObject.ShapeColor = self.gColor
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = thick
					o3.Height = height - bottomOF - topOF - 3
					o3.Width = width - (2 * thick) - sidesOF
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF + thick, p0Z + bottomOF + 3)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					o3.ViewObject.ShapeColor = self.gColor
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = thick
					o4.Height = height - bottomOF - topOF - 3
					o4.Width = width - (2 * thick) - sidesOF
					pl = FreeCAD.Vector(p0X - thick, p0Y + sideOF + thick, p0Z + bottomOF + 3)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					o4.ViewObject.ShapeColor = self.gColor

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = depth - backOF
					o5.Height = 3
					o5.Width = width - sidesOF
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					o5.ViewObject.ShapeColor = self.gColor

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = thick
					o6.Height = height + thick - 4
					o6.Width = width + thick
					pl = FreeCAD.Vector(p0X, p0Y - (thick / 2), p0Z - (thick / 2) + 2)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					o6.ViewObject.ShapeColor = self.gColor

					container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDrawer')
					container.setLink([o1, o2, o3, o4, o5, o6])
					container.Label = "Container, Drawer"
				
					# recompute
					FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF22(self):
			
			p0X = float(self.og2E.text())
			p0Y = float(self.og3E.text())
			p0Z = float(self.og4E.text())
			
			width = float(self.og5E.text())
			height = float(self.og6E.text())
			depth = float(self.og7E.text())
			
			thick = float(self.og8E.text())
			
			sidesOF = float(self.og91E.text())
			sideOF = sidesOF / 2
			backOF = float(self.og92E.text())
			topOF = float(self.og93E.text())
			bottomOF = float(self.og94E.text())
			
			if self.gSingleDrawerPlane == "X":
			
				if self.gSingleDrawerDirection == "+":

					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = thick
					o1.Height = height - bottomOF - topOF - 3
					o1.Width = depth - backOF - thick
					pl = FreeCAD.Vector(p0X + sideOF, p0Y + thick, p0Z + bottomOF + 3)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					o1.ViewObject.ShapeColor = self.gColor
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = thick
					o2.Height = height - bottomOF - topOF - 3
					o2.Width = depth - backOF - thick
					pl = FreeCAD.Vector(p0X + width - thick - sideOF, p0Y + thick, p0Z + bottomOF + 3)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					o2.ViewObject.ShapeColor = self.gColor
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = width - (2 * thick) - sidesOF
					o3.Height = height - bottomOF - topOF - 3
					o3.Width = thick
					pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y + depth - thick - backOF, p0Z + bottomOF + 3)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					o3.ViewObject.ShapeColor = self.gColor
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = width - (2 * thick) - sidesOF
					o4.Height = height - bottomOF - topOF - 3
					o4.Width = thick
					pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y + thick, p0Z + bottomOF + 3)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					o4.ViewObject.ShapeColor = self.gColor

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = width - sidesOF
					o5.Height = 3
					o5.Width = depth - backOF - thick
					pl = FreeCAD.Vector(p0X + sideOF, p0Y + thick, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					o5.ViewObject.ShapeColor = self.gColor

					# Front outside make inside as well
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = width - 4
					o6.Height = height - 4
					o6.Width = thick
					pl = FreeCAD.Vector(p0X + 2, p0Y, p0Z + 2)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					o6.ViewObject.ShapeColor = self.gColor

					container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDrawer')
					container.setLink([o1, o2, o3, o4, o5, o6])
					container.Label = "Container, Drawer"
				
					# recompute
					FreeCAD.ActiveDocument.recompute()
			
				if self.gSingleDrawerDirection == "-":

					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = thick
					o1.Height = height - bottomOF - topOF - 3
					o1.Width = depth - backOF - thick
					pl = FreeCAD.Vector(p0X - sideOF - thick, p0Y - depth + backOF, p0Z + bottomOF + 3)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					o1.ViewObject.ShapeColor = self.gColor
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = thick
					o2.Height = height - bottomOF - topOF - 3
					o2.Width = depth - backOF - thick
					pl = FreeCAD.Vector(p0X - width + sideOF, p0Y - depth + backOF, p0Z + bottomOF + 3)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					o2.ViewObject.ShapeColor = self.gColor
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = width - (2 * thick) - sidesOF
					o3.Height = height - bottomOF - topOF - 3
					o3.Width = thick
					pl = FreeCAD.Vector(p0X - width + sideOF + thick, p0Y - depth + backOF, p0Z + bottomOF + 3)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					o3.ViewObject.ShapeColor = self.gColor
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = width - (2 * thick) - sidesOF
					o4.Height = height - bottomOF - topOF - 3
					o4.Width = thick
					pl = FreeCAD.Vector(p0X - width + sideOF + thick, p0Y - (2 * thick), p0Z + bottomOF + 3)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					o4.ViewObject.ShapeColor = self.gColor

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = width - sidesOF
					o5.Height = 3
					o5.Width = depth - backOF - thick
					pl = FreeCAD.Vector(p0X - width + sideOF, p0Y - depth + backOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					o5.ViewObject.ShapeColor = self.gColor

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = width - 4
					o6.Height = height - 4
					o6.Width = thick
					pl = FreeCAD.Vector(p0X - width + 2, p0Y - thick, p0Z + 2)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					o6.ViewObject.ShapeColor = self.gColor

					container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDrawer')
					container.setLink([o1, o2, o3, o4, o5, o6])
					container.Label = "Container, Drawer"
				
					# recompute
					FreeCAD.ActiveDocument.recompute()

			if self.gSingleDrawerPlane == "Y":
			
				if self.gSingleDrawerDirection == "+":
				
					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = depth - backOF - thick
					o1.Height = height - bottomOF - topOF - 3
					o1.Width = thick
					pl = FreeCAD.Vector(p0X + thick, p0Y - sideOF - thick, p0Z + bottomOF + 3)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					o1.ViewObject.ShapeColor = self.gColor
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = depth - backOF - thick
					o2.Height = height - bottomOF - topOF - 3
					o2.Width = thick
					pl = FreeCAD.Vector(p0X + thick, p0Y - width + sideOF, p0Z + bottomOF + 3)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					o2.ViewObject.ShapeColor = self.gColor
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = thick
					o3.Height = height - bottomOF - topOF - 3
					o3.Width = width - (2 * thick) - sidesOF
					pl = FreeCAD.Vector(p0X + depth - backOF - thick, p0Y - width + sideOF + thick, p0Z + bottomOF + 3)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					o3.ViewObject.ShapeColor = self.gColor
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = thick
					o4.Height = height - bottomOF - topOF - 3
					o4.Width = width - (2 * thick) - sidesOF
					pl = FreeCAD.Vector(p0X + thick, p0Y - width + sideOF + thick, p0Z + bottomOF + 3)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					o4.ViewObject.ShapeColor = self.gColor

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = depth - backOF - thick
					o5.Height = 3
					o5.Width = width - sidesOF
					pl = FreeCAD.Vector(p0X + thick, p0Y - width + sideOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					o5.ViewObject.ShapeColor = self.gColor

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = thick
					o6.Height = height - 4
					o6.Width = width - 4
					pl = FreeCAD.Vector(p0X, p0Y - width + 2, p0Z + 2)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					o6.ViewObject.ShapeColor = self.gColor

					container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDrawer')
					container.setLink([o1, o2, o3, o4, o5, o6])
					container.Label = "Container, Drawer"
				
					# recompute
					FreeCAD.ActiveDocument.recompute()
		
				if self.gSingleDrawerDirection == "-":
				
					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = depth - backOF - thick
					o1.Height = height - bottomOF - topOF - 3
					o1.Width = thick
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF, p0Z + bottomOF + 3)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					o1.ViewObject.ShapeColor = self.gColor
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = depth - backOF - thick
					o2.Height = height - bottomOF - topOF - 3
					o2.Width = thick
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + width - sideOF - thick, p0Z + bottomOF + 3)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					o2.ViewObject.ShapeColor = self.gColor
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = thick
					o3.Height = height - bottomOF - topOF - 3
					o3.Width = width - (2 * thick) - sidesOF
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF + thick, p0Z + bottomOF + 3)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					o3.ViewObject.ShapeColor = self.gColor
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = thick
					o4.Height = height - bottomOF - topOF - 3
					o4.Width = width - (2 * thick) - sidesOF
					pl = FreeCAD.Vector(p0X - (2 * thick), p0Y + sideOF + thick, p0Z + bottomOF + 3)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					o4.ViewObject.ShapeColor = self.gColor

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = depth - backOF - thick
					o5.Height = 3
					o5.Width = width - sidesOF
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					o5.ViewObject.ShapeColor = self.gColor

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = thick
					o6.Height = height - 4
					o6.Width = width - 4
					pl = FreeCAD.Vector(p0X - thick, p0Y + 2, p0Z + 2)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					o6.ViewObject.ShapeColor = self.gColor

					container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDrawer')
					container.setLink([o1, o2, o3, o4, o5, o6])
					container.Label = "Container, Drawer"
				
					# recompute
					FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF23(self):
			
			p0X = float(self.ofr2E.text())
			p0Y = float(self.ofr3E.text())
			p0Z = float(self.ofr4E.text())
			
			width = float(self.ofr5E.text())
			height = float(self.ofr6E.text())
			thick = float(self.ofr7E.text())
			
			# Front outside
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FrontOutside")
			o1.Label = translate('magicStart', 'Front outside')
			o1.Length = width
			o1.Height = height
			o1.Width = thick
			pl = FreeCAD.Vector(p0X, p0Y, p0Z)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF24(self):

			p0X = float(self.ofr2E.text())
			p0Y = float(self.ofr3E.text())
			p0Z = float(self.ofr4E.text())
			
			width = float(self.ofr5E.text())
			height = float(self.ofr6E.text())
			thick = float(self.ofr7E.text())
			
			# Front outside
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FrontInside")
			o1.Label = translate('magicStart', 'Front inside')
			o1.Length = width
			o1.Height = height
			o1.Width = thick
			pl = FreeCAD.Vector(p0X, p0Y, p0Z)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF25(self):
	
			p0X = float(self.osh51E.text())
			p0Y = float(self.osh52E.text())
			p0Z = float(self.osh53E.text())
			
			width = float(self.osh6E.text())
			depth = float(self.osh7E.text())
			thick = float(self.osh1E.text())
			
			# Front outside
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o1.Label = translate('magicStart', 'Shelf')
			o1.Length = width
			o1.Height = thick
			o1.Width = depth
			pl = FreeCAD.Vector(p0X, p0Y, p0Z)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF26(self):
	
			p0X = float(self.ocs51E.text())
			p0Y = float(self.ocs52E.text())
			p0Z = float(self.ocs53E.text())
			
			height = float(self.ocs6E.text())
			depth = float(self.ocs7E.text())
			thick = float(self.ocs1E.text())
			
			# Side center
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "SideCenter")
			o1.Label = translate('magicStart', 'Side Center')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(p0X, p0Y, p0Z)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF27(self):
			
			sx = float(self.oo11E.text())
			sy = float(self.oo12E.text())
			sz = float(self.oo13E.text())
			
			depth = self.gFSY - self.gThick - 3
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(sx, sy + self.gThick, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ - (2 * self.gThick)
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy + self.gThick, sz + self.gThick)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ - (2 * self.gThick)
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy + self.gThick, sz + self.gThick)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Back HDF
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "BackHDF")
			o4.Label = translate('magicStart', 'Back HDF')
			o4.Length = self.gFSX
			o4.Height = self.gFSZ
			o4.Width = 3
			pl = FreeCAD.Vector(sx, sy + depth + self.gThick, sz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(sx, sy + self.gThick, sz + self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor
			
			# Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o6.Label = translate('magicStart', 'Front')
			o6.Length = self.gFSX - self.gThick
			o6.Height = self.gFSZ - self.gThick - 4
			o6.Width = self.gThick
			pl = FreeCAD.Vector(sx + (self.gThick / 2), sy, sz + (self.gThick / 2) + 2)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.ShapeColor = self.gColor
			
			# Shelf
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o7.Label = translate('magicStart', 'Shelf')
			o7.Length = self.gFSX - (2 * self.gThick)
			o7.Height = self.gThick
			o7.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy + self.gThick, sz + (self.gFSZ / 2) - (self.gThick / 2))
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			o7.ViewObject.ShapeColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','FurnitureModule')
			container.setLink([o1, o2, o3, o4, o5, o6, o7])
			container.Label = "Furniture, Module"
		
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF28(self):
			
			sx = float(self.oo11E.text())
			sy = float(self.oo12E.text())
			sz = float(self.oo13E.text())
			
			depth = self.gFSY
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ - (2 * self.gThick)
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + self.gThick)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ - (2 * self.gThick)
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz + self.gThick)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX - (2 * self.gThick)
			o4.Height = self.gFSZ - (2 * self.gThick)
			o4.Width = self.gThick
			pl = FreeCAD.Vector(sx + self.gThick, sy + depth - self.gThick, sz + self.gThick)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor
			
			# Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o6.Label = translate('magicStart', 'Front')
			o6.Length = self.gFSX - (2 * self.gThick) - 4
			o6.Height = self.gFSZ - (2 * self.gThick) - 4
			o6.Width = self.gThick
			pl = FreeCAD.Vector(sx + self.gThick + 2, sy, sz + self.gThick + 2)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.ShapeColor = self.gColor
			
			# Shelf
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o7.Label = translate('magicStart', 'Shelf')
			o7.Length = self.gFSX - (2 * self.gThick)
			o7.Height = self.gThick
			o7.Width = depth - (3 * self.gThick)
			pl = FreeCAD.Vector(sx + self.gThick, sy + (2 * self.gThick), sz + (self.gFSZ / 2) - (self.gThick / 2))
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			o7.ViewObject.ShapeColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','FurnitureModule')
			container.setLink([o1, o2, o3, o4, o5, o6, o7])
			container.Label = "Furniture, Module"

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF29(self):
			
			sx = float(self.oo11E.text())
			sy = float(self.oo12E.text())
			sz = float(self.oo13E.text())
			
			depth = self.gFSY - 3
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ - (2 * self.gThick)
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + self.gThick)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ - (2 * self.gThick)
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz + self.gThick)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Back HDF
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX
			o4.Height = self.gFSZ
			o4.Width = 3
			pl = FreeCAD.Vector(sx, sy + depth, sz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor
			
			# Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o6.Label = translate('magicStart', 'Front')
			o6.Length = self.gFSX - (2 * self.gThick) - 4
			o6.Height = self.gFSZ - (2 * self.gThick) - 4
			o6.Width = self.gThick
			pl = FreeCAD.Vector(sx + self.gThick + 2, sy, sz + self.gThick + 2)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.ShapeColor = self.gColor
			
			# Shelf
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o7.Label = translate('magicStart', 'Shelf')
			o7.Length = self.gFSX - (2 * self.gThick)
			o7.Height = self.gThick
			o7.Width = depth - (2 * self.gThick)
			pl = FreeCAD.Vector(sx + self.gThick, sy + (2 * self.gThick), sz + (self.gFSZ / 2) - (self.gThick / 2))
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			o7.ViewObject.ShapeColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','FurnitureModule')
			container.setLink([o1, o2, o3, o4, o5, o6, o7])
			container.Label = "Furniture, Module"

			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF30(self):
			
			p0X = float(self.ods61E.text())
			p0Y = float(self.ods62E.text())
			startZ = float(self.ods63E.text())
			
			gapX = float(self.ods7E.text())
			gapZ = float(self.ods8E.text())
			gapY = float(self.ods9E.text())
			
			num = int(self.ods2E.text())
			offset = float(self.ods40E.text())
			thick = float(self.ods3E.text())
			
			sidesOF = float(self.ods41E.text())
			sideOF = sidesOF / 2
			backOF = float(self.ods42E.text())
			topOF = float(self.ods43E.text())
			bottomOF = float(self.ods44E.text())
			
			for i in range(0, num):
			
				p0Z = startZ + (i * offset) + (i * gapZ)
			
				# Left Side
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSLeft")
				o1.Label = translate('magicStart', 'DS ' + str(i+1) + ' Left')
				o1.Length = thick
				o1.Height = gapZ - bottomOF - topOF - 3
				o1.Width = gapY - backOF
				pl = FreeCAD.Vector(p0X + sideOF, p0Y, p0Z + bottomOF + 3)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				o1.ViewObject.ShapeColor = self.gColor
				
				# Right Side
				o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSRight")
				o2.Label = translate('magicStart', 'DS ' + str(i+1) + ' Right')
				o2.Length = thick
				o2.Height = gapZ - bottomOF - topOF - 3
				o2.Width = gapY - backOF
				pl = FreeCAD.Vector(p0X + gapX - thick - sideOF, p0Y, p0Z + bottomOF + 3)
				o2.Placement = FreeCAD.Placement(pl, self.gR)
				o2.ViewObject.ShapeColor = self.gColor
				
				# Back
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBack")
				o3.Label = translate('magicStart', 'DS ' + str(i+1) + ' Back')
				o3.Length = gapX - (2 * thick) - sidesOF
				o3.Height = gapZ - bottomOF - topOF - 3
				o3.Width = thick
				pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y + gapY - thick - backOF, p0Z + bottomOF + 3)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				o3.ViewObject.ShapeColor = self.gColor
				
				# Front inside
				o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSFrontInside")
				o4.Label = translate('magicStart', 'DS ' + str(i+1) + ' Front Inside')
				o4.Length = gapX - (2 * thick) - sidesOF
				o4.Height = gapZ - bottomOF - topOF - 3
				o4.Width = thick
				pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y, p0Z + bottomOF + 3)
				o4.Placement = FreeCAD.Placement(pl, self.gR)
				o4.ViewObject.ShapeColor = self.gColor

				# HDF bottom
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBottom")
				o5.Label = translate('magicStart', 'DS ' + str(i+1) + ' Bottom HDF')
				o5.Length = gapX - sidesOF
				o5.Height = 3
				o5.Width = gapY - backOF
				pl = FreeCAD.Vector(p0X + sideOF, p0Y, p0Z  + bottomOF)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				o5.ViewObject.ShapeColor = self.gColor

				# Front outside
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSFrontOutside")
				o6.Label = translate('magicStart', 'DS ' + str(i+1) + ' Front Outside')
				o6.Length = gapX + thick
				o6.Height = gapZ + offset
				o6.Width = thick
				pz = p0Z - offset + (i * offset)
				pl = FreeCAD.Vector(p0X - (thick / 2), p0Y - thick, pz)
				o6.Placement = FreeCAD.Placement(pl, self.gR)
				o6.ViewObject.ShapeColor = self.gColor

				container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDS')
				container.setLink([o1, o2, o3, o4, o5, o6])
				container.Label = "Container, Drawer series " + str(i+1)
		
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF31(self):
			
			p0X = float(self.ods61E.text())
			p0Y = float(self.ods62E.text())
			startZ = float(self.ods63E.text())
			
			gapX = float(self.ods7E.text())
			gapZ = float(self.ods8E.text())
			gapY = float(self.ods9E.text())
			
			num = int(self.ods2E.text())
			offset = float(self.ods40E.text())
			thick = float(self.ods3E.text())
			
			sidesOF = float(self.ods41E.text())
			sideOF = sidesOF / 2
			backOF = float(self.ods42E.text())
			topOF = float(self.ods43E.text())
			bottomOF = float(self.ods44E.text())
			
			for i in range(0, num):
			
				p0Z = startZ + (i * offset) + (i * gapZ)
				
				# Left Side
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSLeft")
				o1.Label = translate('magicStart', 'DS ' + str(i+1) + ' Left')
				o1.Length = thick
				o1.Height = gapZ - bottomOF - topOF - 3
				o1.Width = gapY - backOF - thick
				pl = FreeCAD.Vector(p0X + sideOF, p0Y + thick, p0Z + bottomOF + 3)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				o1.ViewObject.ShapeColor = self.gColor
				
				# Right Side
				o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSRight")
				o2.Label = translate('magicStart', 'DS ' + str(i+1) + ' Right')
				o2.Length = thick
				o2.Height = gapZ - bottomOF - topOF - 3
				o2.Width = gapY - backOF - thick
				pl = FreeCAD.Vector(p0X + gapX - thick - sideOF, p0Y + thick, p0Z + bottomOF + 3)
				o2.Placement = FreeCAD.Placement(pl, self.gR)
				o2.ViewObject.ShapeColor = self.gColor
				
				# Back
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBack")
				o3.Label = translate('magicStart', 'DS ' + str(i+1) + ' Back')
				o3.Length = gapX - (2 * thick) - sidesOF
				o3.Height = gapZ - bottomOF - topOF - 3
				o3.Width = thick
				pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y + gapY - thick - backOF, p0Z + bottomOF + 3)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				o3.ViewObject.ShapeColor = self.gColor
				
				# Front inside
				o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSFrontInside")
				o4.Label = translate('magicStart', 'DS ' + str(i+1) + ' Front Inside')
				o4.Length = gapX - (2 * thick) - sidesOF
				o4.Height = gapZ - bottomOF - topOF - 3
				o4.Width = thick
				pl = FreeCAD.Vector(p0X + sideOF + thick, p0Y + thick, p0Z + bottomOF + 3)
				o4.Placement = FreeCAD.Placement(pl, self.gR)
				o4.ViewObject.ShapeColor = self.gColor

				# HDF bottom
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBottom")
				o5.Label = translate('magicStart', 'DS ' + str(i+1) + ' Bottom HDF')
				o5.Length = gapX - sidesOF
				o5.Height = 3
				o5.Width = gapY - backOF - thick
				pl = FreeCAD.Vector(p0X + sideOF, p0Y + thick, p0Z  + bottomOF)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				o5.ViewObject.ShapeColor = self.gColor

				# Front outside make inside as well
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSFrontOutside")
				o6.Label = translate('magicStart', 'DS ' + str(i+1) + ' Front Outside')
				o6.Length = gapX - (2 * offset)
				o6.Height = gapZ
				o6.Width = thick
				pl = FreeCAD.Vector(p0X + offset, p0Y, p0Z + offset)
				o6.Placement = FreeCAD.Placement(pl, self.gR)
				o6.ViewObject.ShapeColor = self.gColor

				container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerDS')
				container.setLink([o1, o2, o3, o4, o5, o6])
				container.Label = "Container, Drawer series " + str(i+1)

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF32(self):
			
			barWidth = float(self.offrame2E.text())
			barThick = float(self.offrame3E.text())
			
			FSX = float(self.offrame71E.text())
			FSY = float(self.offrame72E.text())
			FSZ = float(self.offrame73E.text())
			
			FFWidth = float(self.offrame8E.text())
			FFHeight = float(self.offrame9E.text())
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFLeft")
			o1.Label = translate('magicStart', 'Face Frame Left')
			o1.Length = barWidth
			o1.Height = FFHeight - (2 * barWidth)
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + barWidth)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFRight")
			o2.Label = translate('magicStart', 'Face Frame Right')
			o2.Length = barWidth
			o2.Height = FFHeight - (2 * barWidth)
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFBottom")
			o3.Label = translate('magicStart', 'Face Frame Bottom')
			o3.Length = FFWidth
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFTop")
			o4.Label = translate('magicStart', 'Face Frame Top')
			o4.Length = FFWidth
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFF')
			container.setLink([o1, o2, o3, o4])
			container.Label = "Container, Face Frame"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF33(self):
			
			barWidth = float(self.offrame2E.text())
			barThick = float(self.offrame3E.text())
			
			FSX = float(self.offrame71E.text())
			FSY = float(self.offrame72E.text())
			FSZ = float(self.offrame73E.text())
			
			FFWidth = float(self.offrame8E.text())
			FFHeight = float(self.offrame9E.text())
			
			centerFSX = FSX + (FFWidth / 2) - barWidth

			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFLeft")
			o1.Label = translate('magicStart', 'Face Frame Left')
			o1.Length = barWidth
			o1.Height = FFHeight - (2 * barWidth)
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + barWidth)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFRight")
			o2.Label = translate('magicStart', 'Face Frame Right')
			o2.Length = barWidth
			o2.Height = FFHeight - (2 * barWidth)
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFBottom")
			o3.Label = translate('magicStart', 'Face Frame Bottom')
			o3.Length = FFWidth
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFTop")
			o4.Label = translate('magicStart', 'Face Frame Top')
			o4.Length = FFWidth
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Center Side
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFCenter")
			o5.Label = translate('magicStart', 'Face Frame Center')
			o5.Length = 2 * barWidth
			o5.Height = FFHeight - (2 * barWidth)
			o5.Width = barThick
			pl = FreeCAD.Vector(centerFSX, FSY, FSZ + barWidth)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFF')
			container.setLink([o1, o2, o3, o4, o5])
			container.Label = "Container, Face Frame"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF34(self):
			
			barWidth = float(self.offrame2E.text())
			barThick = float(self.offrame3E.text())
			
			FSX = float(self.offrame71E.text())
			FSY = float(self.offrame72E.text())
			FSZ = float(self.offrame73E.text())
			
			FFWidth = float(self.offrame8E.text())
			FFHeight = float(self.offrame9E.text())
			
			centerFSX = FSX + (FFWidth / 2) - barWidth
			horizontalFSX = FSX + (FFWidth / 2) + barWidth
			horizontalFSZ = FSZ + (FFHeight / 2) - barWidth
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFLeft")
			o1.Label = translate('magicStart', 'Face Frame Left')
			o1.Length = barWidth
			o1.Height = FFHeight - (2 * barWidth)
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + barWidth)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFRight")
			o2.Label = translate('magicStart', 'Face Frame Right')
			o2.Length = barWidth
			o2.Height = FFHeight - (2 * barWidth)
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFBottom")
			o3.Label = translate('magicStart', 'Face Frame Bottom')
			o3.Length = FFWidth
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFTop")
			o4.Label = translate('magicStart', 'Face Frame Top')
			o4.Length = FFWidth
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Center Side
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFCenter")
			o5.Label = translate('magicStart', 'Face Frame Center')
			o5.Length = 2 * barWidth
			o5.Height = FFHeight - (2 * barWidth)
			o5.Width = barThick
			pl = FreeCAD.Vector(centerFSX, FSY, FSZ + barWidth)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor
			
			# Horizontal bar
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFHorizontal")
			o6.Label = translate('magicStart', 'Face Frame Horizontal')
			o6.Length = (FFWidth / 2) - barWidth - barWidth
			o6.Height = 2 * barWidth
			o6.Width = barThick
			pl = FreeCAD.Vector(horizontalFSX, FSY, horizontalFSZ)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.ShapeColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFF')
			container.setLink([o1, o2, o3, o4, o5, o6])
			container.Label = "Container, Face Frame"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF35(self):
			
			# Face Frame predefined
			
			barWidth = 38
			barThick = 19
			
			# Furniture - settings
			
			sx = float(self.oo11E.text())
			sy = float(self.oo12E.text()) + barThick
			sz = float(self.oo13E.text())
			
			depth = self.gFSY - 3 - barThick
			
			# Face Frame - settings
			
			FSX = sx
			FSY = sy - barThick
			FSZ = sz + self.gThick
			
			FFWidth = self.gFSX
			FFHeight = self.gFSZ - self.gThick
			
			centerFSX = FSX + (FFWidth / 2) - barWidth
			horizontalFSX = FSX + (FFWidth / 2) + barWidth
			horizontalFSZ = FSZ + (FFHeight / 2) - barWidth
			
			# Furniture - draw
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX - (2 * self.gThick)
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy, sz + self.gThick)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX
			o4.Height = self.gFSZ - self.gThick
			o4.Width = 3
			pl = FreeCAD.Vector(sx, sy + depth, sz + self.gThick)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX - (2 * self.gThick)
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy, sz + self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor

			# Face Frame - draw

			# Left Side
			ff1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFLeft")
			ff1.Label = translate('magicStart', 'Face Frame Left')
			ff1.Length = barWidth
			ff1.Height = FFHeight - (2 * barWidth)
			ff1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + barWidth)
			ff1.Placement = FreeCAD.Placement(pl, self.gR)
			ff1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			ff2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFRight")
			ff2.Label = translate('magicStart', 'Face Frame Right')
			ff2.Length = barWidth
			ff2.Height = FFHeight - (2 * barWidth)
			ff2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			ff2.Placement = FreeCAD.Placement(pl, self.gR)
			ff2.ViewObject.ShapeColor = self.gColor
			
			# Bottom
			ff3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFBottom")
			ff3.Label = translate('magicStart', 'Face Frame Bottom')
			ff3.Length = FFWidth
			ff3.Height = barWidth
			ff3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			ff3.Placement = FreeCAD.Placement(pl, self.gR)
			ff3.ViewObject.ShapeColor = self.gColor
			
			# Top
			ff4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFTop")
			ff4.Label = translate('magicStart', 'Face Frame Top')
			ff4.Length = FFWidth
			ff4.Height = barWidth
			ff4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			ff4.Placement = FreeCAD.Placement(pl, self.gR)
			ff4.ViewObject.ShapeColor = self.gColor
			
			# Center Side
			ff5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFCenter")
			ff5.Label = translate('magicStart', 'Face Frame Center')
			ff5.Length = 2 * barWidth
			ff5.Height = FFHeight - (2 * barWidth)
			ff5.Width = barThick
			pl = FreeCAD.Vector(centerFSX, FSY, FSZ + barWidth)
			ff5.Placement = FreeCAD.Placement(pl, self.gR)
			ff5.ViewObject.ShapeColor = self.gColor
			
			# Horizontal bar
			ff6 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFHorizontal")
			ff6.Label = translate('magicStart', 'Face Frame Horizontal')
			ff6.Length = (FFWidth / 2) - barWidth - barWidth
			ff6.Height = 2 * barWidth
			ff6.Width = barThick
			pl = FreeCAD.Vector(horizontalFSX, FSY, horizontalFSZ)
			ff6.Placement = FreeCAD.Placement(pl, self.gR)
			ff6.ViewObject.ShapeColor = self.gColor

			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','FurnitureModule')
			container.setLink([o1, o2, o3, o4, o5, ff1, ff2, ff3, ff4, ff5, ff6])
			container.Label = "Furniture, Module"

			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF36(self):
			
			# Face Frame predefined
			
			barWidth = 38
			barThick = 19
			
			# Furniture - settings
			
			sx = float(self.oo11E.text())
			sy = float(self.oo12E.text()) + barThick
			sz = float(self.oo13E.text())
			
			depth = self.gFSY - 3 - barThick
			
			# Face Frame - settings
			
			FSX = sx
			FSY = sy - barThick
			FSZ = sz
			
			FFWidth = self.gFSX
			FFHeight = self.gFSZ
			
			centerFSX = FSX + (FFWidth / 2) - barWidth
			
			horizontalFSX1 = FSX + barWidth
			horizontalFSZ1 = FSZ + (FFHeight / 2) - barWidth
			
			horizontalFSX2 = FSX + (FFWidth / 2) + barWidth
			horizontalFSZ2 = FSZ + (FFHeight / 2) - barWidth
			
			# Furniture - draw
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ - (2 * self.gThick)
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + self.gThick)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ - (2 * self.gThick)
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz + self.gThick)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX
			o4.Height = self.gFSZ
			o4.Width = 3
			pl = FreeCAD.Vector(sx, sy + depth, sz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor

			# Face Frame - draw

			# Left Side
			ff1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFLeft")
			ff1.Label = translate('magicStart', 'Face Frame Left')
			ff1.Length = barWidth
			ff1.Height = FFHeight - (2 * barWidth)
			ff1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + barWidth)
			ff1.Placement = FreeCAD.Placement(pl, self.gR)
			ff1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			ff2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFRight")
			ff2.Label = translate('magicStart', 'Face Frame Right')
			ff2.Length = barWidth
			ff2.Height = FFHeight - (2 * barWidth)
			ff2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			ff2.Placement = FreeCAD.Placement(pl, self.gR)
			ff2.ViewObject.ShapeColor = self.gColor
			
			# Bottom
			ff3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFBottom")
			ff3.Label = translate('magicStart', 'Face Frame Bottom')
			ff3.Length = FFWidth
			ff3.Height = barWidth
			ff3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			ff3.Placement = FreeCAD.Placement(pl, self.gR)
			ff3.ViewObject.ShapeColor = self.gColor
			
			# Top
			ff4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFTop")
			ff4.Label = translate('magicStart', 'Face Frame Top')
			ff4.Length = FFWidth
			ff4.Height = barWidth
			ff4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			ff4.Placement = FreeCAD.Placement(pl, self.gR)
			ff4.ViewObject.ShapeColor = self.gColor
			
			# Center Side
			ff5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFCenter")
			ff5.Label = translate('magicStart', 'Face Frame Center')
			ff5.Length = 2 * barWidth
			ff5.Height = FFHeight - (2 * barWidth)
			ff5.Width = barThick
			pl = FreeCAD.Vector(centerFSX, FSY, FSZ + barWidth)
			ff5.Placement = FreeCAD.Placement(pl, self.gR)
			ff5.ViewObject.ShapeColor = self.gColor
			
			# Horizontal bar left
			ff6 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFHorizontalLeft")
			ff6.Label = translate('magicStart', 'Face Frame Horizontal Left')
			ff6.Length = (FFWidth / 2) - barWidth - barWidth
			ff6.Height = 2 * barWidth
			ff6.Width = barThick
			pl = FreeCAD.Vector(horizontalFSX1, FSY, horizontalFSZ1)
			ff6.Placement = FreeCAD.Placement(pl, self.gR)
			ff6.ViewObject.ShapeColor = self.gColor
			
			# Horizontal bar right
			ff7 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFHorizontalRight")
			ff7.Label = translate('magicStart', 'Face Frame Horizontal Right')
			ff7.Length = (FFWidth / 2) - barWidth - barWidth
			ff7.Height = 2 * barWidth
			ff7.Width = barThick
			pl = FreeCAD.Vector(horizontalFSX2, FSY, horizontalFSZ2)
			ff7.Placement = FreeCAD.Placement(pl, self.gR)
			ff7.ViewObject.ShapeColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','FurnitureModule')
			container.setLink([o1, o2, o3, o4, o5, ff1, ff2, ff3, ff4, ff5, ff6, ff7])
			container.Label = "Furniture, Module"

			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF37(self):
			
			barThick = float(self.ofglass2E.text())
			barWidth = float(self.ofglass8E.text())
			
			glassThick = float(self.ofglass5E.text())
			glassSink = 6
			
			FSX = float(self.ofglass71E.text())
			FSY = float(self.ofglass72E.text())
			FSZ = float(self.ofglass73E.text())
			
			FFWidth = float(self.ofglass9E.text())
			FFHeight = float(self.ofglass10E.text())
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGLeft")
			o1.Label = translate('magicStart', 'FG Left')
			o1.Length = barWidth
			o1.Height = FFHeight - (2 * barWidth)
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + barWidth)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGRight")
			o2.Label = translate('magicStart', 'FG Right')
			o2.Length = barWidth
			o2.Height = FFHeight - (2 * barWidth)
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGBottom")
			o3.Label = translate('magicStart', 'FG Bottom')
			o3.Length = FFWidth
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGTop")
			o4.Label = translate('magicStart', 'FG Top')
			o4.Length = FFWidth
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Glass
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGGlass")
			o5.Label = translate('magicStart', 'FG Glass')
			o5.Length = FFWidth - (2 * barWidth) + (2 * glassSink)
			o5.Height = FFHeight - (2 * barWidth) + (2 * glassSink)
			o5.Width = glassThick
			plx = FSX + barWidth - glassSink
			ply = FSY + (barThick/2) - (glassThick/2)
			plz = FSZ + barWidth - glassSink
			pl = FreeCAD.Vector(plx, ply, plz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = (255, 255, 255)
			o5.ViewObject.Transparency = 60
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFG')
			container.setLink([o1, o2, o3, o4, o5])
			container.Label = "Container, Front with GLass"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF38(self):
			
			barThick = float(self.ofglass2E.text())
			barWidth = float(self.ofglass8E.text())
			
			glassThick = float(self.ofglass5E.text())
			glassSink = 6
			
			decWidth = int(barWidth/4)
			decThick = int( (barThick - glassThick) / 2 )
			
			FSX = float(self.ofglass71E.text())
			FSY = float(self.ofglass72E.text())
			FSZ = float(self.ofglass73E.text())
			
			FFWidth = float(self.ofglass9E.text())
			FFHeight = float(self.ofglass10E.text())
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGLeft")
			o1.Label = translate('magicStart', 'FG Left')
			o1.Length = barWidth
			o1.Height = FFHeight - (2 * barWidth)
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + barWidth)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGRight")
			o2.Label = translate('magicStart', 'FG Right')
			o2.Length = barWidth
			o2.Height = FFHeight - (2 * barWidth)
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGBottom")
			o3.Label = translate('magicStart', 'FG Bottom')
			o3.Length = FFWidth
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGTop")
			o4.Label = translate('magicStart', 'FG Top')
			o4.Length = FFWidth
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Glass
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGGlass")
			o5.Label = translate('magicStart', 'FG Glass')
			o5.Length = FFWidth - (2 * barWidth) + (2 * glassSink)
			o5.Height = FFHeight - (2 * barWidth) + (2 * glassSink)
			o5.Width = glassThick
			plx = FSX + barWidth - glassSink
			ply = FSY + (barThick/2) - (glassThick/2)
			plz = FSZ + barWidth - glassSink
			pl = FreeCAD.Vector(plx, ply, plz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = (255, 255, 255)
			o5.ViewObject.Transparency = 60
			
			# Vertical decoration
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGVertical")
			o6.Label = translate('magicStart', 'FG Vertical')
			o6.Length = decWidth
			o6.Height = FFHeight - (2 * barWidth)
			o6.Width = decThick
			plx = FSX + (FFWidth / 2) - (decWidth / 2)
			pl = FreeCAD.Vector(plx, FSY, FSZ + barWidth)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.ShapeColor = self.gColor
			
			h14 = ((FFHeight - (2 * barWidth)) / 4) - (decWidth / 2)
			h34 = ( 3 * (FFHeight - (2 * barWidth)) / 4) - (decWidth / 2)
			
			# Horizontal decoration 1
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGHorizontal1")
			o7.Label = translate('magicStart', 'FG Horizontal 1')
			o7.Length = (FFWidth - (2 * barWidth) - decWidth) / 2
			o7.Height = decWidth
			o7.Width = decThick
			plx = FSX + barWidth
			ply = FSY
			plz = FSZ + barWidth +  h14
			pl = FreeCAD.Vector(plx, ply, plz)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			o7.ViewObject.ShapeColor = self.gColor
		
			# Horizontal decoration 2
			o8 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGHorizontal2")
			o8.Label = translate('magicStart', 'FG Horizontal 2')
			o8.Length = (FFWidth - (2 * barWidth) - decWidth) / 2
			o8.Height = decWidth
			o8.Width = decThick
			plx = FSX + barWidth
			ply = FSY
			plz = FSZ + barWidth +  h34
			pl = FreeCAD.Vector(plx, ply, plz)
			o8.Placement = FreeCAD.Placement(pl, self.gR)
			o8.ViewObject.ShapeColor = self.gColor
		
			# Horizontal decoration 3
			o9 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGHorizontal3")
			o9.Label = translate('magicStart', 'FG Horizontal 3')
			o9.Length = (FFWidth - (2 * barWidth) - decWidth) / 2
			o9.Height = decWidth
			o9.Width = decThick
			plx = FSX + (FFWidth / 2) + (decWidth / 2)
			ply = FSY
			plz = FSZ + barWidth +  h14
			pl = FreeCAD.Vector(plx, ply, plz)
			o9.Placement = FreeCAD.Placement(pl, self.gR)
			o9.ViewObject.ShapeColor = self.gColor
		
			# Horizontal decoration 4
			o10 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGHorizontal4")
			o10.Label = translate('magicStart', 'FG Horizontal 4')
			o10.Length = (FFWidth - (2 * barWidth) - decWidth) / 2
			o10.Height = decWidth
			o10.Width = decThick
			plx = FSX + (FFWidth / 2) + (decWidth / 2)
			ply = FSY
			plz = FSZ + barWidth +  h34
			pl = FreeCAD.Vector(plx, ply, plz)
			o10.Placement = FreeCAD.Placement(pl, self.gR)
			o10.ViewObject.ShapeColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerFG')
			container.setLink([o1, o2, o3, o4, o5, o6, o7, o8, o9, o10])
			container.Label = "Container, Front with GLass"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF41(self):
	
			thick = float(self.oshs1E.text())
			num = int(self.oshs2E.text())
			
			p0X = float(self.oshs41E.text())
			p0Y = float(self.oshs42E.text())
			p0Z = float(self.oshs43E.text())
			
			width = float(self.oshs5E.text())
			depth = float(self.oshs6E.text())
			offset = float(self.oshs7E.text())
			
			shelvesArr = []
			
			for i in range(0, num):
				
				# single shelf
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "ShelfSeries")
				o1.Label = translate('magicStart', 'Shelf '+str(i+1))
				o1.Length = width
				o1.Height = thick
				o1.Width = depth
				pz = p0Z + ((i + 1) * offset) + (i * thick)
				pl = FreeCAD.Vector(p0X, p0Y, pz)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				o1.ViewObject.ShapeColor = self.gColor
				
				shelvesArr.append(o1)
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerShelfSeries')
			container.setLink(shelvesArr)
			container.Label = "Container, Shelf Series"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF42(self):
			
			width = float(self.otb1E.text())
			depth = float(self.otb2E.text())
			height = float(self.otb3E.text())
			topThick = float(self.otb4E.text())
			legThick = float(self.otb5E.text())
			offset = float(self.otb6E.text())
			
			sx = float(self.otb81E.text())
			sy = float(self.otb82E.text())
			sz = float(self.otb83E.text())
			
			# Leg Left Front
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLF")
			o1.Label = translate('magicStart', 'Table Leg LF')
			o1.Length = legThick
			o1.Height = height - topThick
			o1.Width = legThick
			pl = FreeCAD.Vector(sx + offset, sy + offset, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Leg Left Back
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLB")
			o2.Label = translate('magicStart', 'Table Leg LB')
			o2.Length = legThick
			o2.Height = height - topThick
			o2.Width = legThick
			psy = sy + depth - offset - legThick
			pl = FreeCAD.Vector(sx + offset, psy, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Leg Right Front
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLRF")
			o3.Label = translate('magicStart', 'Table Leg RF')
			o3.Length = legThick
			o3.Height = height - topThick
			o3.Width = legThick
			psx = sx + width - offset - legThick
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Leg Right Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLRB")
			o4.Label = translate('magicStart', 'Table Leg RB')
			o4.Length = legThick
			o4.Height = height - topThick
			o4.Width = legThick
			psx = sx + width - offset - legThick
			psy = sy + depth - offset - legThick
			pl = FreeCAD.Vector(psx, psy, sz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Supporter Front
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSF")
			o5.Label = translate('magicStart', 'Table Supporter Front')
			o5.Length = width - (2 * offset) - (2 * legThick)
			o5.Height = legThick
			o5.Width = legThick
			psx = sx + offset + legThick
			psy = sy + offset
			psz = sz + height - topThick - legThick
			pl = FreeCAD.Vector(psx, psy, psz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor
			
			# Supporter Back
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSB")
			o6.Label = translate('magicStart', 'Table Supporter Back')
			o6.Length = width - (2 * offset) - (2 * legThick)
			o6.Height = legThick
			o6.Width = legThick
			psx = sx + offset + legThick
			psy = sy + depth - offset - legThick
			psz = sz + height - topThick - legThick
			pl = FreeCAD.Vector(psx, psy, psz)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.ShapeColor = self.gColor
			
			# Supporter Left
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSL")
			o7.Label = translate('magicStart', 'Table Supporter Left')
			o7.Length = legThick
			o7.Height = legThick
			o7.Width = depth - (2 * offset) - (2 * legThick)
			psx = sx + offset
			psy = sy + offset + legThick
			psz = sz + height - topThick - legThick
			pl = FreeCAD.Vector(psx, psy, psz)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			o7.ViewObject.ShapeColor = self.gColor
			
			# Supporter Right
			o8 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSR")
			o8.Label = translate('magicStart', 'Table Supporter Right')
			o8.Length = legThick
			o8.Height = legThick
			o8.Width = depth - (2 * offset) - (2 * legThick)
			psx = sx + width - offset - legThick
			psy = sy + offset + legThick
			psz = sz + height - topThick - legThick
			pl = FreeCAD.Vector(psx, psy, psz)
			o8.Placement = FreeCAD.Placement(pl, self.gR)
			o8.ViewObject.ShapeColor = self.gColor
			
			# Table Top
			o9 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableTop")
			o9.Label = translate('magicStart', 'Table Top')
			o9.Length = width
			o9.Height = topThick
			o9.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + height - topThick)
			o9.Placement = FreeCAD.Placement(pl, self.gR)
			o9.ViewObject.ShapeColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerTable')
			container.setLink([o1, o2, o3, o4, o5, o6, o7, o8, o9])
			container.Label = "Container, Table"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF44(self):
			
			width = float(self.otb1E.text())
			depth = float(self.otb2E.text())
			height = float(self.otb3E.text())
			topThick = float(self.otb4E.text())
			legThick = float(self.otb5E.text())
			offset = float(self.otb6E.text())
			
			sx = float(self.otb81E.text())
			sy = float(self.otb82E.text())
			sz = float(self.otb83E.text())
			
			# Leg Left Front
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLF1")
			o1.Label = translate('magicStart', 'Table Leg LF1')
			o1.Length = topThick
			o1.Height = height - topThick
			o1.Width = legThick
			pl = FreeCAD.Vector(sx + offset, sy + offset, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = self.gColor
			
			# Leg Left Front
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLF2")
			o2.Label = translate('magicStart', 'Table Leg LF2')
			o2.Length = legThick
			o2.Height = height - topThick
			o2.Width = topThick
			pl = FreeCAD.Vector(sx + offset, sy + offset, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = self.gColor
			
			# Leg Left Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLB1")
			o3.Label = translate('magicStart', 'Table Leg LB1')
			o3.Length = topThick
			o3.Height = height - topThick
			o3.Width = legThick
			psy = sy + depth - offset - legThick
			pl = FreeCAD.Vector(sx + offset, psy, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = self.gColor
			
			# Leg Left Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLB2")
			o4.Label = translate('magicStart', 'Table Leg LB2')
			o4.Length = legThick
			o4.Height = height - topThick
			o4.Width = topThick
			psy = sy + depth - offset - topThick
			pl = FreeCAD.Vector(sx + offset, psy, sz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = self.gColor
			
			# Leg Right Front
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLRF1")
			o5.Label = translate('magicStart', 'Table Leg RF1')
			o5.Length = legThick
			o5.Height = height - topThick
			o5.Width = topThick
			psx = sx + width - offset - legThick
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = self.gColor
			
			# Leg Right Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLRF2")
			o6.Label = translate('magicStart', 'Table Leg RF2')
			o6.Length = topThick
			o6.Height = height - topThick
			o6.Width = legThick
			psx = sx + width - offset - topThick
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.ShapeColor = self.gColor
			
			# Leg Right Back
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLRB1")
			o7.Label = translate('magicStart', 'Table Leg RB1')
			o7.Length = topThick
			o7.Height = height - topThick
			o7.Width = legThick
			psx = sx + width - offset - topThick
			psy = sy + depth - offset - legThick
			pl = FreeCAD.Vector(psx, psy, sz)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			o7.ViewObject.ShapeColor = self.gColor
			
			# Leg Right Back
			o8 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLRB2")
			o8.Label = translate('magicStart', 'Table Leg RB2')
			o8.Length = legThick
			o8.Height = height - topThick
			o8.Width = topThick
			psx = sx + width - offset - legThick
			psy = sy + depth - offset - topThick
			pl = FreeCAD.Vector(psx, psy, sz)
			o8.Placement = FreeCAD.Placement(pl, self.gR)
			o8.ViewObject.ShapeColor = self.gColor
			
			# Supporter Front
			o9 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSF")
			o9.Label = translate('magicStart', 'Table Supporter Front')
			o9.Length = width - (2 * offset) - (2 * topThick)
			o9.Height = legThick
			o9.Width = topThick
			psx = sx + offset + topThick
			psy = sy + offset + topThick
			psz = sz + height - topThick - legThick
			pl = FreeCAD.Vector(psx, psy, psz)
			o9.Placement = FreeCAD.Placement(pl, self.gR)
			o9.ViewObject.ShapeColor = self.gColor
			
			# Supporter Back
			o10 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSB")
			o10.Label = translate('magicStart', 'Table Supporter Back')
			o10.Length = width - (2 * offset) - (2 * topThick)
			o10.Height = legThick
			o10.Width = topThick
			psx = sx + offset + topThick
			psy = sy + depth - offset - topThick - topThick
			psz = sz + height - topThick - legThick
			pl = FreeCAD.Vector(psx, psy, psz)
			o10.Placement = FreeCAD.Placement(pl, self.gR)
			o10.ViewObject.ShapeColor = self.gColor
			
			# Supporter Left
			o11 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSL")
			o11.Label = translate('magicStart', 'Table Supporter Left')
			o11.Length = topThick
			o11.Height = legThick
			o11.Width = depth - (2 * offset) - (2 * topThick)
			psx = sx + offset + topThick
			psy = sy + offset + topThick
			psz = sz + height - topThick - legThick
			pl = FreeCAD.Vector(psx, psy, psz)
			o11.Placement = FreeCAD.Placement(pl, self.gR)
			o11.ViewObject.ShapeColor = self.gColor
			
			# Supporter Right
			o12 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSR")
			o12.Label = translate('magicStart', 'Table Supporter Right')
			o12.Length = topThick
			o12.Height = legThick
			o12.Width = depth - (2 * offset) - (2 * topThick)
			psx = sx + width - offset - topThick - topThick
			psy = sy + offset + topThick
			psz = sz + height - topThick - legThick
			pl = FreeCAD.Vector(psx, psy, psz)
			o12.Placement = FreeCAD.Placement(pl, self.gR)
			o12.ViewObject.ShapeColor = self.gColor
			
			# Table Top
			o13 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableTop")
			o13.Label = translate('magicStart', 'Table Top')
			o13.Length = width
			o13.Height = topThick
			o13.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + height - topThick)
			o13.Placement = FreeCAD.Placement(pl, self.gR)
			o13.ViewObject.ShapeColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerTable')
			container.setLink([o1, o2, o3, o4, o5, o6, o7, o8, o9, o10, o11, o12, o13])
			container.Label = "Container, Table"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF46(self):
			
			width = float(self.otb1E.text())
			depth = float(self.otb2E.text())
			height = float(self.otb3E.text())
			topThick = float(self.otb4E.text())
			legThick = float(self.otb5E.text())
			offset = float(self.otb6E.text())
			
			sx = float(self.otb81E.text())
			sy = float(self.otb82E.text())
			sz = float(self.otb83E.text())
			
			# Leg Left Front
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLF")
			o1.Label = translate('magicStart', 'Table Leg LF')
			o1.Length = legThick
			o1.Height = height - topThick
			o1.Width = legThick / 2
			pl = FreeCAD.Vector(sx + offset, sy + offset, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			o1.ViewObject.ShapeColor = (0, 0, 0, 0)
			
			# Leg Left Back
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLB")
			o2.Label = translate('magicStart', 'Table Leg LB')
			o2.Length = legThick
			o2.Height = height - topThick
			o2.Width = legThick / 2
			psy = sy + depth - offset - (legThick / 2)
			pl = FreeCAD.Vector(sx + offset, psy, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			o2.ViewObject.ShapeColor = (0, 0, 0, 0)
			
			# Leg Right Front
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLRF")
			o3.Label = translate('magicStart', 'Table Leg RF')
			o3.Length = legThick
			o3.Height = height - topThick
			o3.Width = legThick / 2
			psx = sx + width - offset - legThick
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			o3.ViewObject.ShapeColor = (0, 0, 0, 0)
			
			# Leg Right Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLRB")
			o4.Label = translate('magicStart', 'Table Leg RB')
			o4.Length = legThick
			o4.Height = height - topThick
			o4.Width = legThick / 2
			psx = sx + width - offset - legThick
			psy = sy + depth - offset - (legThick / 2)
			pl = FreeCAD.Vector(psx, psy, sz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			o4.ViewObject.ShapeColor = (0, 0, 0, 0)
			
			# Supporter Left Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSLT")
			o5.Label = translate('magicStart', 'Table SLT')
			o5.Length = legThick
			o5.Height = legThick / 2
			o5.Width = depth - (2 * offset) - legThick
			psx = sx + offset
			psy = sy + offset + (legThick / 2)
			psz = sz + height - topThick - (legThick / 2)
			pl = FreeCAD.Vector(psx, psy, psz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			o5.ViewObject.ShapeColor = (0, 0, 0, 0)
			
			# Supporter Left Bottom
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSLB")
			o6.Label = translate('magicStart', 'Table SLB')
			o6.Length = legThick
			o6.Height = legThick / 2
			o6.Width = depth - (2 * offset) - legThick
			psx = sx + offset
			psy = sy + offset + (legThick / 2)
			psz = sz
			pl = FreeCAD.Vector(psx, psy, psz)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			o6.ViewObject.ShapeColor = (0, 0, 0, 0)
			
			# Supporter Right Top
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSRT")
			o7.Label = translate('magicStart', 'Table SRT')
			o7.Length = legThick
			o7.Height = legThick / 2
			o7.Width = depth - (2 * offset) - legThick
			psx = sx + width - offset - legThick
			psy = sy + offset + (legThick / 2)
			psz = sz + height - topThick - (legThick / 2)
			pl = FreeCAD.Vector(psx, psy, psz)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			o7.ViewObject.ShapeColor = (0, 0, 0, 0)
			
			# Supporter Right Bottom
			o8 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSRB")
			o8.Label = translate('magicStart', 'Table SRB')
			o8.Length = legThick
			o8.Height = legThick / 2
			o8.Width = depth - (2 * offset) - legThick
			psx = sx + width - offset - legThick
			psy = sy + offset + (legThick / 2)
			psz = sz
			pl = FreeCAD.Vector(psx, psy, psz)
			o8.Placement = FreeCAD.Placement(pl, self.gR)
			o8.ViewObject.ShapeColor = (0, 0, 0, 0)
			
			# Table Top
			o9 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableTop")
			o9.Label = translate('magicStart', 'Table Top')
			o9.Length = width
			o9.Height = topThick
			o9.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + height - topThick)
			o9.Placement = FreeCAD.Placement(pl, self.gR)
			o9.ViewObject.ShapeColor = self.gColor
			
			container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','ContainerTable')
			container.setLink([o1, o2, o3, o4, o5, o6, o7, o8, o9])
			container.Label = "Container, Table"
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF48(self):
	
			p0X = float(self.oside51E.text())
			p0Y = float(self.oside52E.text())
			p0Z = float(self.oside53E.text())
			
			width = float(self.oside6E.text())
			height = float(self.oside7E.text())
			thick = float(self.oside1E.text())
			
			if self.gSideEdgePlane == "X":
				
				# Side
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Side")
				o1.Label = translate('magicStart', 'Side')
				o1.Length = width
				o1.Height = height
				o1.Width = thick
				pl = FreeCAD.Vector(p0X, p0Y, p0Z)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				o1.ViewObject.ShapeColor = self.gColor
				
				# recompute
				FreeCAD.ActiveDocument.recompute()
			
			if self.gSideEdgePlane == "Y":
				
				# Side
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Side")
				o1.Label = translate('magicStart', 'Side')
				o1.Length = thick
				o1.Height = height
				o1.Width = width
				pl = FreeCAD.Vector(p0X, p0Y, p0Z)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				o1.ViewObject.ShapeColor = self.gColor
				
				# recompute
				FreeCAD.ActiveDocument.recompute()

	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################

