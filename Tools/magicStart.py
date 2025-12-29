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
	"------------------------------------------------------------------------------------": -1,
	translate('magicStart', 'Storage module ( front outside, back inside, veneer )'): 0, 
	translate('magicStart', 'Bookcase module ( no front, back outside, veneer )'): 1, 
	translate('magicStart', 'Bookcase ( import parametric )'): 2, 
	translate('magicStart', 'Drawer ( simple, parametric )'): 3, 
	translate('magicStart', 'Simple chair ( import parametric )'): 4, 
	translate('magicStart', 'Picture frame ( import parametric )'): 5, 
	translate('magicStart', 'Table ( simple, import parametric )'): 6, 
	translate('magicStart', 'Storage box ( import parametric )'): 7, 
	translate('magicStart', 'Dowel 8x35 mm ( import parametric )'): 8, 
	translate('magicStart', 'Screw 4x40 mm ( import parametric )'): 9, 
	translate('magicStart', 'Storage ( front outside, back inside, heavy duty )'): 10, 
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
	translate('magicStart', 'Drawer ( single, X or Y direction, front outside )'): 21, 
	translate('magicStart', 'Drawer ( single, X or Y direction, front inside )'): 22, 
	translate('magicStart', 'Front outside'): 23, 
	translate('magicStart', 'Front inside'): 24, 
	translate('magicStart', 'Shelf'): 25, 
	translate('magicStart', 'Center side'): 26, 
	translate('magicStart', 'Storage module ( front outside, back outside, veneer )'): 27, 
	translate('magicStart', 'Storage module ( front inside, back inside, veneer )'): 28, 
	translate('magicStart', 'Storage module ( front inside, back outside, veneer )'): 29, 
	translate('magicStart', 'Drawer ( series, front outside )'): 30, 
	translate('magicStart', 'Drawer ( series, front inside )'): 31, 
	translate('magicStart', 'Face Frame ( horizontal, around )'): 32, 
	translate('magicStart', 'Face Frame ( horizontal, with center )'): 33, 
	translate('magicStart', 'Face Frame ( horizontal, for custom changes )'): 34, 
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
	translate('magicStart', 'Drawer ( decoration, parametric )'): 58, 
	translate('magicStart', 'Front outside ( decorative )'): 59, 
	translate('magicStart', 'Front inside ( decorative )'): 60, 
	translate('magicStart', 'Front decoration ( simple frame )'): 61, 
	translate('magicStart', 'Side decoration ( simple frame )'): 62, 
	translate('magicStart', 'Minifix 15x45 mm ( import parametric )'): 63,
	translate('magicStart', 'Face Frame ( vertical, for custom changes )'): 64, 
	translate('magicStart', 'Kitchen cabinet ( US style )'): 65, 
	translate('magicStart', 'Kitchen wall module ( front outside, back outside, veneer )'): 66, 
	translate('magicStart', 'Kitchen wall cabinet ( US style )'): 67, 
	translate('magicStart', 'Handle ( single hole )'): 68, 
	translate('magicStart', 'Handle ( double hole )'): 69, 
	translate('magicStart', 'Brackets for wall cabinets ( Camar 807 )'): 70, 
	translate('magicStart', 'Drawer ( series, Blum, Hafele, GTV, Amix, front outside )'): 71, 
	translate('magicStart', 'Drawer ( series, Blum, Hafele, GTV, Amix, front inside )'): 72, 
	translate('magicStart', 'Workspace platform'): 73, 
	translate('magicStart', 'Back outside ( HDF )'): 74, 
	translate('magicStart', 'Back inside ( full )'): 75, 
	translate('magicStart', 'Handle ( single hole, decorated )'): 76, 
	translate('magicStart', 'Handle ( double hole, decorated )'): 77, 
	translate('magicStart', 'Bookcase ( no front, back inside, simple )'): 78, 
	translate('magicStart', 'Bookcase ( no front, back outside, simple )'): 79, 
	translate('magicStart', 'Table ( school desk, single right side )'): 80, 
	translate('magicStart', 'Table ( School desk, single left side )'): 81, 
	translate('magicStart', 'Table ( school desk, both sides )'): 82, 
	translate('magicStart', 'Sides with holes ( import parametric )'): 83, 
	translate('magicStart', 'Wardrobe ( front outside, back outside, 2x clothes width )'): 84, 
	translate('magicStart', 'Wardrobe ( front outside, back outside, clothes hangers )'): 85,
	translate('magicStart', 'Module on top ( back inside, veneer )'): 86,
	translate('magicStart', 'Module on top ( back outside, veneer )'): 87,
	translate('magicStart', 'Module base ( back inside, veneer )'): 88,
	translate('magicStart', 'Module base ( back outside, veneer )'): 89 # no comma
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
		gThick = MagicPanels.gWoodThickness  # wood thickness
		
		gSelectedFurniture = "F73"
		gColor = MagicPanels.gDefaultColor
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
		gHelpInfoF0 += translate('magicStart', 'Choose one method and make selection before calculate or create button press. Possible selections:')
		gHelpInfoF0 += '<ul>'
		gHelpInfoF0 += '<li><b>' + translate('magicStart', 'X edge') + ' - </b>'
		gHelpInfoF0 += translate('magicStart', 'to set XYZ position and width. X edge means any edge along the X coordinate axis. In this case, the starting point will be the vertex of the edge and the width of the furniture will be the length of the edge.') + '</li>'
		gHelpInfoF0 += '<li><b>' + translate('magicStart', 'XY face') + ' - </b>'
		gHelpInfoF0 += translate('magicStart', 'to put next module on top. XY face means the plane on the object along the X and Y coordinate axes, i.e. horizontal, such as the top of the object, to create the next furniture module on top. In this case, the width of the furniture and its depth will be calculated from the selected plane so that the furniture is in line with the previous identical module.') + '</li>'
		gHelpInfoF0 += '<li><b>' + translate('magicStart', 'Vertex') + ' - </b>'
		gHelpInfoF0 += translate('magicStart', 'to set XYZ position only. Vertex means selecting any vertex of the object. In this case, only the starting point for creating the furniture will be calculated.') + '</li>'
		gHelpInfoF0 += '<li><b>' + translate('magicStart', 'no selection') + ' - </b>'
		gHelpInfoF0 += translate('magicStart', 'to create with custom settings') + '</li>'
		gHelpInfoF0 += '</ul>'
		gHelpInfoF0 += translate('magicStart', 'To calculate the furniture and its dimensions, make selection, change fields, and then press the "calculate furniture" button. Before pressing the "create" button, you can manually correct some values ​​if necessary.')
		
		# ############################################################################
		gHelpInfoF16 = "" 

		gHelpInfoF16 += translate('magicStart', 'To initially calculate the the Foot, make selection, fill in the appropriate fields and click the "calculate foot" button. Possible selections:')
		gHelpInfoF16 += '<ul>'
		gHelpInfoF16 += '<li><b>'
		gHelpInfoF16 += translate('magicStart', 'XY face') + '</b>: '
		gHelpInfoF16 += translate('magicStart', 'indicates the face of the bottom panel of the furniture. In this case, the position, width, and depth of the foot will be taken from the selected face.')
		gHelpInfoF16 += '</li>'
		gHelpInfoF16 += '<li><b>'
		gHelpInfoF16 += translate('magicStart', 'X edge') + '</b>: '
		gHelpInfoF16 += translate('magicStart', 'indicates the X edge of the bottom panel of the furniture. In this case, the position and width of the foot will be taken from the selected face. The depth needs to be added by you.')
		gHelpInfoF16 += '</li>'
		gHelpInfoF16 += '<li><b>'
		gHelpInfoF16 += translate('magicStart', 'Vertex') + '</b>: '
		gHelpInfoF16 += translate('magicStart', 'indicates any vertex at any object to set the XYZ start position for the foot creation. In this case, the width and depth needs to be added by you.')
		gHelpInfoF16 += '</li>'
		gHelpInfoF16 += '</ul>'
		gHelpInfoF16 += translate('magicStart', 'Fields:')
		gHelpInfoF16 += '<ul>'
		gHelpInfoF16 += '<li><b>'
		gHelpInfoF16 += translate('magicStart', 'Wood thickness') + '</b>: '
		gHelpInfoF16 += translate('magicStart', 'means the thickness of the elements from which the foot will be created, i.e. the thickness of the wood.')
		gHelpInfoF16 += '</li>'
		gHelpInfoF16 += '<li><b>'
		gHelpInfoF16 += translate('magicStart', 'Foot height') + '</b>: '
		gHelpInfoF16 += translate('magicStart', 'means the size of the foot elements, relative to the Z coordinate axis.')
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
		gHelpInfoF59 = "" 
		gHelpInfoF59 += translate('magicStart', 'To pre-calculate the starting point for the Decorative front and its dimensions, make selection, fill in the required fields and press the "calculate decorative front" button.')
		gHelpInfoF59 += '<ul>'
		gHelpInfoF59 += '<li><b>'
		gHelpInfoF59 += translate('magicStart', 'X bottom edge') + '</b>: '
		gHelpInfoF59 += translate('magicStart', 'means the inner bottom edge of the space, in line with the X coordinate axis.')
		gHelpInfoF59 += '</li>'
		gHelpInfoF59 += '<li><b>'
		gHelpInfoF59 += translate('magicStart', 'X top edge') + '</b>: '
		gHelpInfoF59 += translate('magicStart', 'means the inner top edge of the space, in line with the X coordinate axis.')
		gHelpInfoF59 += '</li>'
		gHelpInfoF59 += '<li><b>'
		gHelpInfoF59 += translate('magicStart', 'Z left edge') + '</b>: '
		gHelpInfoF59 += translate('magicStart', 'means the inner left edge of the space, in line with the Z coordinate axis.')
		gHelpInfoF59 += '</li>'
		gHelpInfoF59 += '<li><b>'
		gHelpInfoF59 += translate('magicStart', 'Z right edge') + '</b>: '
		gHelpInfoF59 += translate('magicStart', 'means the inner right edge of the space, in line with the Z coordinate axis.')
		gHelpInfoF59 += '</li>'
		gHelpInfoF59 += '<li><b>'
		gHelpInfoF59 += translate('magicStart', 'Single beam thickness') + '</b>: '
		gHelpInfoF59 += translate('magicStart', 'means the thickness of the beam of the frame, in line with the Y coordinate axis.')
		gHelpInfoF59 += '</li>'
		gHelpInfoF59 += '<li><b>'
		gHelpInfoF59 += translate('magicStart', 'Front overlap horizontal') + '</b>: '
		gHelpInfoF59 += translate('magicStart', 'in the case of an outside front, this is the width by which the front will overlap the furniture elements. If the front is to cover the entire surface, set the same value as "Single beam thickness".')
		gHelpInfoF59 += '</li>'
		gHelpInfoF59 += '<li><b>'
		gHelpInfoF59 += translate('magicStart', 'Front overlap vertical') + '</b>: '
		gHelpInfoF59 += translate('magicStart', 'in the case of an outside front, this is the height by which the front will overlap the furniture elements. If the front is to cover the entire surface, set the same value as "Single beam thickness".')
		gHelpInfoF59 += '</li>'
		gHelpInfoF59 += '<li><b>'
		gHelpInfoF59 += translate('magicStart', 'Front offset horizontal') + '</b>: '
		gHelpInfoF59 += translate('magicStart', 'in the case of an inside front, this is the width of the gap between the front frame and the furniture elements.')
		gHelpInfoF59 += '</li>'
		gHelpInfoF59 += '<li><b>'
		gHelpInfoF59 += translate('magicStart', 'Front offset vertical') + '</b>: '
		gHelpInfoF59 += translate('magicStart', 'in the case of an inside front, this is the height of the gap between the front frame and the furniture elements.')
		gHelpInfoF59 += '</li>'
		gHelpInfoF59 += '<li><b>'
		gHelpInfoF59 += translate('magicStart', 'Inner board thickness') + '</b>: '
		gHelpInfoF59 += translate('magicStart', 'means the thickness of the board inside the frame, in line with the Y coordinate axis.')
		gHelpInfoF59 += '</li>'
		gHelpInfoF59 += '</ul>'
		gHelpInfoF59 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')

		# ############################################################################
		gHelpInfoF61 = "" 
		gHelpInfoF61 += translate('magicStart', 'To pre-calculate the starting point for the Front decoration and its dimensions, make selection, fill in the required fields and press the "calculate front decoration" button.')
		gHelpInfoF61 += '<ul>'
		gHelpInfoF61 += '<li><b>'
		gHelpInfoF61 += translate('magicStart', 'XZ face of front') + '</b>: '
		gHelpInfoF61 += translate('magicStart', 'means the front surface where you want to place the decoration, in line with the X and Z coordinate axes.')
		gHelpInfoF61 += '</li>'
		gHelpInfoF61 += '<li><b>'
		gHelpInfoF61 += translate('magicStart', 'X bottom edge') + '</b>: '
		gHelpInfoF61 += translate('magicStart', 'means the bottom edge of the front where you want to place the decoration, in line with the X coordinate axis.')
		gHelpInfoF61 += '</li>'
		gHelpInfoF61 += '<li><b>'
		gHelpInfoF61 += translate('magicStart', 'X top edge') + '</b>: '
		gHelpInfoF61 += translate('magicStart', 'means the top edge of the front where you want to place the decoration, in line with the X coordinate axis.')
		gHelpInfoF61 += '</li>'
		gHelpInfoF61 += '<li><b>'
		gHelpInfoF61 += translate('magicStart', 'Z left edge') + '</b>: '
		gHelpInfoF61 += translate('magicStart', 'means the left edge of the front where you want to place the decoration, in line with the Z coordinate axis.')
		gHelpInfoF61 += '</li>'
		gHelpInfoF61 += '<li><b>'
		gHelpInfoF61 += translate('magicStart', 'Z right edge') + '</b>: '
		gHelpInfoF61 += translate('magicStart', 'means the right edge of the front where you want to place the decoration, in line with the Z coordinate axis.')
		gHelpInfoF61 += '</li>'
		gHelpInfoF61 += '<li><b>'
		gHelpInfoF61 += translate('magicStart', 'Single bar width') + '</b>: '
		gHelpInfoF61 += translate('magicStart', 'means the width of the beam of the frame, in line with the X or Z coordinate axis.')
		gHelpInfoF61 += '</li>'
		gHelpInfoF61 += '<li><b>'
		gHelpInfoF61 += translate('magicStart', 'Single bar thickness') + '</b>: '
		gHelpInfoF61 += translate('magicStart', 'means the thickness of the beam of the frame, in line with the Y coordinate axis.')
		gHelpInfoF61 += '</li>'
		gHelpInfoF61 += '<li><b>'
		gHelpInfoF61 += translate('magicStart', 'Offset from edge') + '</b>: '
		gHelpInfoF61 += translate('magicStart', 'this is the distance of the decoration from the selected edges of the front towards the inside of the front.')
		gHelpInfoF61 += '</li>'
		gHelpInfoF61 += '</ul>'
		gHelpInfoF61 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')

		# ############################################################################
		gHelpInfoF62 = "" 
		gHelpInfoF62 += translate('magicStart', 'To pre-calculate the starting point for the Side decoration and its dimensions, make selection, fill in the required fields and press the "calculate side decoration" button.')
		gHelpInfoF62 += '<ul>'
		gHelpInfoF62 += '<li><b>'
		gHelpInfoF62 += translate('magicStart', 'YZ face of side') + '</b>: '
		gHelpInfoF62 += translate('magicStart', 'means the side surface where you want to place the decoration, in line with the Y and Z coordinate axes.')
		gHelpInfoF62 += '</li>'
		gHelpInfoF62 += '<li><b>'
		gHelpInfoF62 += translate('magicStart', 'Y bottom edge') + '</b>: '
		gHelpInfoF62 += translate('magicStart', 'means the bottom edge of the side where you want to place the decoration, in line with the Y coordinate axis.')
		gHelpInfoF62 += '</li>'
		gHelpInfoF62 += '<li><b>'
		gHelpInfoF62 += translate('magicStart', 'Y top edge') + '</b>: '
		gHelpInfoF62 += translate('magicStart', 'means the top edge of the side where you want to place the decoration, in line with the Y coordinate axis.')
		gHelpInfoF62 += '</li>'
		gHelpInfoF62 += '<li><b>'
		gHelpInfoF62 += translate('magicStart', 'Z left edge') + '</b>: '
		gHelpInfoF62 += translate('magicStart', 'means the left edge of the side where you want to place the decoration, in line with the Z coordinate axis.')
		gHelpInfoF62 += '</li>'
		gHelpInfoF62 += '<li><b>'
		gHelpInfoF62 += translate('magicStart', 'Z right edge') + '</b>: '
		gHelpInfoF62 += translate('magicStart', 'means the right edge of the side where you want to place the decoration, in line with the Z coordinate axis.')
		gHelpInfoF62 += '</li>'
		gHelpInfoF62 += '<li><b>'
		gHelpInfoF62 += translate('magicStart', 'Single bar width') + '</b>: '
		gHelpInfoF62 += translate('magicStart', 'means the width of the beam of the frame, in line with the Y or Z coordinate axis.')
		gHelpInfoF62 += '</li>'
		gHelpInfoF62 += '<li><b>'
		gHelpInfoF62 += translate('magicStart', 'Single bar thickness') + '</b>: '
		gHelpInfoF62 += translate('magicStart', 'means the thickness of the beam of the frame, in line with the X coordinate axis.')
		gHelpInfoF62 += '</li>'
		gHelpInfoF62 += '<li><b>'
		gHelpInfoF62 += translate('magicStart', 'Offset from edge') + '</b>: '
		gHelpInfoF62 += translate('magicStart', 'this is the distance of the decoration from the selected edges of the side towards the inside of the side.')
		gHelpInfoF62 += '</li>'
		gHelpInfoF62 += '</ul>'
		gHelpInfoF62 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')
		
		# ############################################################################
		gHelpInfoF73 = "" 
		gHelpInfoF73 += translate('magicStart', 'This workspace allows you to create reference platform. So you can use the workspace edges or faces as reference point for other tools. This is dedicated mostly for specific custom projects to make start easier. The Z size will be used later to workspace resize step. This workspace will not be listed at BOM, cut-list report, so you do not have to remove it later.')
		gHelpInfoF73 += '<br><br>'
		gHelpInfoF73 += translate('magicStart', 'To pre-calculate the starting point for the workspace platform, make selection, fill in fields you want to change and press the "calculate workspace position" button. To create workspace press "create" button.')
		gHelpInfoF73 += '<ul>'
		gHelpInfoF73 += '<li><b>'
		gHelpInfoF73 += translate('magicStart', 'X size') + '</b>: '
		gHelpInfoF73 += translate('magicStart', 'means the workspace platform size along X coordinate axis.')
		gHelpInfoF73 += '</li>'
		gHelpInfoF73 += '<li><b>'
		gHelpInfoF73 += translate('magicStart', 'Y size') + '</b>: '
		gHelpInfoF73 += translate('magicStart', 'means the workspace platform size along Y coordinate axis.')
		gHelpInfoF73 += '</li>'
		gHelpInfoF73 += '<li><b>'
		gHelpInfoF73 += translate('magicStart', 'Z size') + '</b>: '
		gHelpInfoF73 += translate('magicStart', 'means the workspace platform size along Z coordinate axis.')
		gHelpInfoF73 += '</li>'
		gHelpInfoF73 += '<li><b>'
		gHelpInfoF73 += translate('magicStart', 'Start XYZ') + '</b>: '
		gHelpInfoF73 += translate('magicStart', 'means the point the workspace will be created. The workspace will be created in Z position according to its thickness to allow creating abjects on the platfor with (0, 0, 0) start position.')
		gHelpInfoF73 += '</li>'
		gHelpInfoF73 += '</ul>'
		gHelpInfoF73 += translate('magicStart', 'Before pressing the <b>create</b> button, you can manually correct some values ​​if necessary.')
		
		# ############################################################################
		gHelpInfoF74 = "" 
		gHelpInfoF74 += translate('magicStart', 'To pre-calculate the starting point for the Back and its dimensions, make selection, fill in the required fields and press the "calculate back" button.')
		gHelpInfoF74 += '<ul>'
		gHelpInfoF74 += '<li><b>'
		gHelpInfoF74 += translate('magicStart', 'X bottom edge') + '</b>: '
		gHelpInfoF74 += translate('magicStart', 'means the inner bottom edge of the furniture where you want to place the back, in line with the X coordinate axis.')
		gHelpInfoF74 += '</li>'
		gHelpInfoF74 += '<li><b>'
		gHelpInfoF74 += translate('magicStart', 'X top edge') + '</b>: '
		gHelpInfoF74 += translate('magicStart', 'means the inner top edge of the furniture where you want to place the back, in line with the X coordinate axis.')
		gHelpInfoF74 += '</li>'
		gHelpInfoF74 += '<li><b>'
		gHelpInfoF74 += translate('magicStart', 'Z left edge from back model view') + '</b>: '
		gHelpInfoF74 += translate('magicStart', 'means the inner left edge of the furniture where you want to place the back, in line with the Z coordinate axis but looking at the model from the back side.')
		gHelpInfoF74 += '</li>'
		gHelpInfoF74 += '<li><b>'
		gHelpInfoF74 += translate('magicStart', 'Z right edge') + '</b>: '
		gHelpInfoF74 += translate('magicStart', 'means the inner right edge of the furniture where you want to place the back, in line with the Z coordinate axis but looking at the model from the back side.')
		gHelpInfoF74 += '</li>'
		gHelpInfoF74 += '<li><b>'
		gHelpInfoF74 += translate('magicStart', 'Back thickness along Y') + '</b>: '
		gHelpInfoF74 += translate('magicStart', 'means the thickness of the wood, in line with the Y coordinate axis.')
		gHelpInfoF74 += '</li>'
		gHelpInfoF74 += '<li><b>'
		gHelpInfoF74 += translate('magicStart', 'Back overlaps') + '</b>: '
		gHelpInfoF74 += translate('magicStart', 'this is the size by which the back will overlap the furniture parts, looking from the back of the model.')
		gHelpInfoF74 += '</li>'
		gHelpInfoF74 += '<li><b>'
		gHelpInfoF74 += translate('magicStart', 'Back offsets') + '</b>: '
		gHelpInfoF74 += translate('magicStart', 'this is the size by which the back will be reduced and will create free space between the parts of the furniture, when looking at the model from the back.')
		gHelpInfoF74 += '</li>'
		gHelpInfoF74 += '</ul>'
		gHelpInfoF74 += translate('magicStart', 'Before pressing the "create" button, you can manually correct some values ​​if necessary.')
		
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
			self.toolSW = 550           # tool screen width
			self.toolSH = 680           # tool screen height
			
			self.helpSW = 500           # help info screen width
			self.helpSH = self.toolSH   # help info screen height
			
			# active screen size - FreeCAD main window
			gSW = FreeCADGui.getMainWindow().width()
			gSH = FreeCADGui.getMainWindow().height()

			# tool screen position
			self.gPW = 0
			self.gPH = int( gSH - self.toolSH )

			# ############################################################################
			# main window
			# ############################################################################
			
			self.result = userCancelled
			self.setGeometry(self.gPW, self.gPH, self.toolSW, self.toolSH)
			self.setWindowTitle(translate('magicStart', 'magicStart'))
			if MagicPanels.gWindowStaysOnTop == True:
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# options - settings
			# ############################################################################
			
			row = 10                                           # main row
			area = self.toolSW - 20                            # full width gui area
			infoarea = area - 220                              # area for first info
			
			createSize = 40                                    # create button size
			createRow = self.toolSH - createSize - 10          # row for create button
			
			ioffset = 10                                       # items offset
			
			starttfs = 120                                     # start text field size
			startcZ = area - starttfs + 10                     # column for Z
			startcY = startcZ - ioffset - starttfs             # column for Y
			startcX = startcY - ioffset - starttfs             # column for X
			
			rsize1x = starttfs                                 # row size 1
			rsize2x = (2 * starttfs) + ioffset                 # row size 2 x row
			rsize3x = (3 * starttfs) + (2 * ioffset)           # row size 3 x row
			
			fieldSize = 100                                    # text field size
			fieldSize2x = (2 * fieldSize) + ioffset            # text field size x2
			fieldSize3x = (3 * fieldSize) + (2 * ioffset)      # text field size x3
			
			column0 = 10                                       # column 0 for label
			column1 = 200                                      # column 1 for 1st text field
			column2 = column1 + fieldSize + ioffset            # column 2 for 2nd text field
			column3 = column2 + fieldSize + ioffset            # column 3 for 3rd text field
			
			# ############################################################################
			# options - selection
			# ############################################################################
	
			# not write here, copy text from getMenuIndex to avoid typo
			self.sModeList = (
				translate('magicStart', 'Workspace platform'),
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Storage module ( front outside, back inside, veneer )'), 
				translate('magicStart', 'Storage module ( front outside, back outside, veneer )'), 
				translate('magicStart', 'Storage module ( front inside, back inside, veneer )'), 
				translate('magicStart', 'Storage module ( front inside, back outside, veneer )'), 
				translate('magicStart', 'Kitchen wall module ( front outside, back outside, veneer )'), 
				translate('magicStart', 'Bookcase module ( no front, back outside, veneer )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Storage ( front outside, back inside, heavy duty )'), 
				translate('magicStart', 'Wardrobe ( front outside, back outside, 2x clothes width )'), 
				translate('magicStart', 'Wardrobe ( front outside, back outside, clothes hangers )'), 
				translate('magicStart', 'Bookcase ( no front, back inside, simple )'), 
				translate('magicStart', 'Bookcase ( no front, back outside, simple )'), 
				translate('magicStart', 'Bookcase ( import parametric )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Module base ( back inside, veneer )'), 
				translate('magicStart', 'Module on top ( back inside, veneer )'), 
				translate('magicStart', 'Module base ( back outside, veneer )'), 
				translate('magicStart', 'Module on top ( back outside, veneer )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Simple storage ( face frame, no front, back HDF )'), 
				translate('magicStart', 'Simple bookcase ( face frame, no front, back HDF )'), 
				translate('magicStart', 'Kitchen cabinet ( US style )'), 
				translate('magicStart', 'Kitchen wall cabinet ( US style )'), 
				translate('magicStart', 'Face Frame ( vertical, for custom changes )'), 
				translate('magicStart', 'Face Frame ( horizontal, around )'), 
				translate('magicStart', 'Face Frame ( horizontal, with center )'), 
				translate('magicStart', 'Face Frame ( horizontal, for custom changes )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Drawer ( single, X or Y direction, front outside )'), 
				translate('magicStart', 'Drawer ( single, X or Y direction, front inside )'), 
				translate('magicStart', 'Drawer ( series, front outside )'), 
				translate('magicStart', 'Drawer ( series, front inside )'), 
				translate('magicStart', 'Drawer ( series, Blum, Hafele, GTV, Amix, front outside )'), 
				translate('magicStart', 'Drawer ( series, Blum, Hafele, GTV, Amix, front inside )'), 
				translate('magicStart', 'Drawer ( simple, parametric )'), 
				translate('magicStart', 'Drawer ( decoration, parametric )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Front outside'), 
				translate('magicStart', 'Front outside ( decorative )'), 
				translate('magicStart', 'Front outside with glass ( simple frame )'), 
				translate('magicStart', 'Front outside with glass ( frame with decoration )'), 
				translate('magicStart', 'Front inside'), 
				translate('magicStart', 'Front inside ( decorative )'), 
				translate('magicStart', 'Front inside with glass ( simple frame )'), 
				translate('magicStart', 'Front inside with glass ( frame with decoration )'), 
				translate('magicStart', 'Front decoration ( simple frame )'), 
				translate('magicStart', 'Front left (decoration, import parametric )'), 
				translate('magicStart', 'Front right (decoration, import parametric )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Shelf'), 
				translate('magicStart', 'Shelf series with equal space'), 
				translate('magicStart', 'Top (decoration, import parametric )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Side'), 
				translate('magicStart', 'Center side'), 
				translate('magicStart', 'Side decoration ( simple frame )'), 
				translate('magicStart', 'Sides with holes ( import parametric )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Back outside ( HDF )'), 
				translate('magicStart', 'Back inside ( full )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Foot ( good for cleaning )'), 
				translate('magicStart', 'Foot ( standard )'), 
				translate('magicStart', 'Foot ( more stable )'), 
				translate('magicStart', 'Foot ( decorated )'), 
				translate('magicStart', 'Foot ( chair style )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Table ( kitchen simple style )'), 
				translate('magicStart', 'Table ( kitchen modern style )'), 
				translate('magicStart', 'Table ( kitchen decorated style )'), 
				translate('magicStart', 'Table ( coffee simple style )'), 
				translate('magicStart', 'Table ( coffee modern style )'), 
				translate('magicStart', 'Table ( coffee decorated style )'), 
				translate('magicStart', 'Table ( school desk, single right side )'), 
				translate('magicStart', 'Table ( School desk, single left side )'), 
				translate('magicStart', 'Table ( school desk, both sides )'), 
				translate('magicStart', 'Table ( simple, import parametric )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Dowel 8x35 mm ( import parametric )'),
				translate('magicStart', 'Biscuits 4x16x48 mm ( import parametric )'), 
				translate('magicStart', 'Biscuits 4x21x54 mm ( import parametric )'), 
				translate('magicStart', 'Biscuits 4x24x57 mm ( import parametric )'), 
				translate('magicStart', 'Screw 3x20 mm for HDF ( import parametric )'), 
				translate('magicStart', 'Screw 4x40 mm ( import parametric )'), 
				translate('magicStart', 'Screw 5x50 mm ( import parametric )'), 
				translate('magicStart', 'Pocket screw 4x40 mm ( import parametric )'), 
				translate('magicStart', 'Minifix 15x45 mm ( import parametric )'), 
				translate('magicStart', 'Counterbore 2x 5x60 mm ( import parametric )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Shelf Pin 5x16 mm ( import parametric )'), 
				translate('magicStart', 'Handle ( single hole )'), 
				translate('magicStart', 'Handle ( single hole, decorated )'), 
				translate('magicStart', 'Handle ( double hole )'), 
				translate('magicStart', 'Handle ( double hole, decorated )'), 
				translate('magicStart', 'Brackets for wall cabinets ( Camar 807 )'), 
				translate('magicStart', 'Angle 30x30x25 mm ( import parametric )'), 
				translate('magicStart', 'Angle 80x80x20 mm ( import parametric )'), 
				translate('magicStart', 'Angle 40x40x100 mm ( import parametric )'), 
				"------------------------------------------------------------------------------------", 
				translate('magicStart', 'Simple chair ( import parametric )'), 
				translate('magicStart', 'Picture frame ( import parametric )'), 
				translate('magicStart', 'Storage box ( import parametric )')   # no comma
			)
			
			helpButtonSize = 80
			
			self.sMode = QtGui.QComboBox(self)
			self.sMode.addItems(self.sModeList)
			self.sMode.setCurrentIndex(0)
			self.sMode.textActivated[str].connect(self.selectedOption)
			self.sMode.resize(area - 30 - helpButtonSize, 40)
			self.sMode.move(10, 10)

			# ############################################################################
			# help buttons and info screen
			# ############################################################################
			
			# button
			self.helpBSHOW = QtGui.QPushButton(translate('magicStart', 'HELP >'), self)
			self.helpBSHOW.clicked.connect(self.helpSHOW)
			self.helpBSHOW.resize(helpButtonSize, 40)
			self.helpBSHOW.move(self.toolSW - helpButtonSize - 30, 10)

			# button
			self.helpBHIDE = QtGui.QPushButton(translate('magicStart', '< HELP'), self)
			self.helpBHIDE.clicked.connect(self.helpHIDE)
			self.helpBHIDE.resize(helpButtonSize, 40)
			self.helpBHIDE.move(self.toolSW - helpButtonSize - 30, 10)
			self.helpBHIDE.hide()
			
			# label
			self.helpInfo = QtGui.QLabel(self.gHelpInfoF73, self)
			self.helpInfo.move(self.toolSW + 10, 10)
			self.helpInfo.setFixedWidth(self.helpSW - 20)
			self.helpInfo.setFixedHeight(self.helpSH - 20)
			self.helpInfo.setWordWrap(True)
			self.helpInfo.setTextFormat(QtCore.Qt.TextFormat.RichText)
			self.helpInfo.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

			# ############################################################################
			# custom row settings
			# ############################################################################

			row += 70
			
			rowhelp = row - 20
			rowgap = row - 20
			rowds = row - 20
			rowfoot = row
			rowtbl = row - 20
			rowfront = row
			rowfglass = row - 20
			rowfdec = row - 20
			rowodf = row - 20
			rowfframe = row - 20
			rowshelf = row
			rowsseries = row - 20
			rowcside = row
			rowside = row - 20
			rowsdec = row - 20
			rowwsp = row - 20
			rowback = row - 20
			
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
			self.setIcon("msf073")

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
			self.mergeB.resize(area, createSize)
			self.mergeB.move(10, createRow)
			self.mergeB.hide()
			
			# ############################################################################
			# GUI for Workspace (visible by default)
			# ############################################################################
			
			# label
			info = translate('magicStart', 'Choose one selection method and make selection before calculate or create button press, possible selections: <br><br> 1. Edge - to set workspace start XYZ position same as edge center <br><br> 2. Face - to set workspace start XYZ position same as face center <br><br> 3. Vertex - to set workspace start XYZ position same as vertex position <br><br> 4. no selection - to create with custom settings')
			self.oworkspaceInfo = QtGui.QLabel(info, self)
			self.oworkspaceInfo.move(10, rowwsp+3)
			self.oworkspaceInfo.setFixedWidth(infoarea)
			self.oworkspaceInfo.setWordWrap(True)
			self.oworkspaceInfo.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowwsp += 220
			
			# label
			self.oworkspaceXL = QtGui.QLabel(translate('magicStart', 'X size:'), self)
			self.oworkspaceXL.move(10, rowwsp+3)

			# text input
			self.oworkspaceXE = QtGui.QLineEdit(self)
			self.oworkspaceXE.setText(MagicPanels.unit2gui(3000))
			self.oworkspaceXE.setFixedWidth(200)
			self.oworkspaceXE.move(120, rowwsp)
		
			rowwsp += 30
			
			# label
			self.oworkspaceYL = QtGui.QLabel(translate('magicStart', 'Y size:'), self)
			self.oworkspaceYL.move(10, rowwsp+3)

			# text input
			self.oworkspaceYE = QtGui.QLineEdit(self)
			self.oworkspaceYE.setText(MagicPanels.unit2gui(1500))
			self.oworkspaceYE.setFixedWidth(200)
			self.oworkspaceYE.move(120, rowwsp)
			
			rowwsp += 30
			
			# label
			self.oworkspaceZL = QtGui.QLabel(translate('magicStart', 'Z size:'), self)
			self.oworkspaceZL.move(10, rowwsp+3)

			# text input
			self.oworkspaceZE = QtGui.QLineEdit(self)
			self.oworkspaceZE.setText(MagicPanels.unit2gui(10))
			self.oworkspaceZE.setFixedWidth(200)
			self.oworkspaceZE.move(120, rowwsp)
			
			rowwsp += 60
			
			# button
			self.oworkspaceBCL = QtGui.QPushButton(translate('magicStart', 'calculate workspace position'), self)
			self.oworkspaceBCL.clicked.connect(self.calculateWorkspace)
			self.oworkspaceBCL.resize(area, createSize)
			self.oworkspaceBCL.move(10, rowwsp)
			
			rowwsp += 80
			
			# label
			self.oworkspaceSL = QtGui.QLabel(translate('magicStart', 'Start XYZ:'), self)
			self.oworkspaceSL.move(10, rowwsp+3)
			
			# text input
			self.oworkspaceSXE = QtGui.QLineEdit(self)
			self.oworkspaceSXE.setText(MagicPanels.unit2gui(0))
			self.oworkspaceSXE.setFixedWidth(starttfs)
			self.oworkspaceSXE.move(startcX, rowwsp)
			
			# text input
			self.oworkspaceSYE = QtGui.QLineEdit(self)
			self.oworkspaceSYE.setText(MagicPanels.unit2gui(0))
			self.oworkspaceSYE.setFixedWidth(starttfs)
			self.oworkspaceSYE.move(startcY, rowwsp)
			
			# text input
			self.oworkspaceSZE = QtGui.QLineEdit(self)
			self.oworkspaceSZE.setText(MagicPanels.unit2gui(-10))
			self.oworkspaceSZE.setFixedWidth(starttfs)
			self.oworkspaceSZE.move(startcZ, rowwsp)
			
			rowwsp += 40

			# button
			self.oworkspaceBCR = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.oworkspaceBCR.clicked.connect(self.createObject)
			self.oworkspaceBCR.resize(area, createSize)
			self.oworkspaceBCR.move(10, createRow)

			# ############################################################################
			# GUI for furniture
			# ############################################################################
			
			# label
			self.oThickL = QtGui.QLabel(translate('magicStart', 'Construction wood thickness:'), self)
			self.oThickL.move(column0, row+3)

			# text input
			self.oThickE = QtGui.QLineEdit(self)
			self.oThickE.setText(MagicPanels.unit2gui(self.gThick))
			self.oThickE.setFixedWidth(fieldSize)
			self.oThickE.move(column1, row)
			
			row += 30
			
			# label
			self.oThickBackL = QtGui.QLabel(translate('magicStart', 'Back wood thickness:'), self)
			self.oThickBackL.move(column0, row+3)

			# text input
			self.oThickBackE = QtGui.QLineEdit(self)
			self.oThickBackE.setText(MagicPanels.unit2gui(self.gThick))
			self.oThickBackE.setFixedWidth(fieldSize)
			self.oThickBackE.move(column1, row)
			
			row += 30
			
			# label
			self.oThickShelfL = QtGui.QLabel(translate('magicStart', 'Shelf wood thickness:'), self)
			self.oThickShelfL.move(column0, row+3)

			# text input
			self.oThickShelfE = QtGui.QLineEdit(self)
			self.oThickShelfE.setText(MagicPanels.unit2gui(self.gThick))
			self.oThickShelfE.setFixedWidth(fieldSize)
			self.oThickShelfE.move(column1, row)
			
			row += 30
			
			# label
			self.oThickFrontL = QtGui.QLabel(translate('magicStart', 'Front wood thickness:'), self)
			self.oThickFrontL.move(column0, row+3)

			# text input
			self.oThickFrontE = QtGui.QLineEdit(self)
			self.oThickFrontE.setText(MagicPanels.unit2gui(self.gThick))
			self.oThickFrontE.setFixedWidth(fieldSize)
			self.oThickFrontE.move(column1, row)
			
			row += 30
			
			# label
			self.oOffsetFrontLL = QtGui.QLabel(translate('magicStart', 'Left front offset:'), self)
			self.oOffsetFrontLL.move(column0, row+3)

			# text input
			self.oOffsetFrontLE = QtGui.QLineEdit(self)
			self.oOffsetFrontLE.setText(MagicPanels.unit2gui(self.gThick))
			self.oOffsetFrontLE.setFixedWidth(fieldSize)
			self.oOffsetFrontLE.move(column1, row)
			
			row += 30
			
			# label
			self.oOffsetFrontRL = QtGui.QLabel(translate('magicStart', 'Right front offset:'), self)
			self.oOffsetFrontRL.move(column0, row+3)

			# text input
			self.oOffsetFrontRE = QtGui.QLineEdit(self)
			self.oOffsetFrontRE.setText(MagicPanels.unit2gui(self.gThick))
			self.oOffsetFrontRE.setFixedWidth(fieldSize)
			self.oOffsetFrontRE.move(column1, row)
			
			row += 30
			
			# label
			self.oOffsetFrontTL = QtGui.QLabel(translate('magicStart', 'Top front offset:'), self)
			self.oOffsetFrontTL.move(column0, row+3)

			# text input
			self.oOffsetFrontTE = QtGui.QLineEdit(self)
			self.oOffsetFrontTE.setText(MagicPanels.unit2gui(self.gThick))
			self.oOffsetFrontTE.setFixedWidth(fieldSize)
			self.oOffsetFrontTE.move(column1, row)
			
			row += 30
			
			# label
			self.oOffsetFrontBL = QtGui.QLabel(translate('magicStart', 'Bottom front offset:'), self)
			self.oOffsetFrontBL.move(column0, row+3)

			# text input
			self.oOffsetFrontBE = QtGui.QLineEdit(self)
			self.oOffsetFrontBE.setText(MagicPanels.unit2gui(self.gThick))
			self.oOffsetFrontBE.setFixedWidth(fieldSize)
			self.oOffsetFrontBE.move(column1, row)
			
			row += 30
			
			# label
			self.oModulesNumL = QtGui.QLabel(translate('magicStart', 'Modules number:'), self)
			self.oModulesNumL.move(column0, row+3)

			# text input
			self.oModulesNumE = QtGui.QLineEdit(self)
			self.oModulesNumE.setText("0")
			self.oModulesNumE.setFixedWidth(fieldSize)
			self.oModulesNumE.move(column1, row)
			
			row += 30
			
			# label
			self.oSelectionOffsetL = QtGui.QLabel(translate('magicStart', 'Offset from selection XYZ:'), self)
			self.oSelectionOffsetL.move(column0, row+3)
			
			# text input
			self.oSelectionOffset1E = QtGui.QLineEdit(self)
			self.oSelectionOffset1E.setText(MagicPanels.unit2gui(0))
			self.oSelectionOffset1E.setFixedWidth(fieldSize)
			self.oSelectionOffset1E.move(column1, row)
			
			# text input
			self.oSelectionOffset2E = QtGui.QLineEdit(self)
			self.oSelectionOffset2E.setText(MagicPanels.unit2gui(0))
			self.oSelectionOffset2E.setFixedWidth(fieldSize)
			self.oSelectionOffset2E.move(column2, row)
			
			# text input
			self.oSelectionOffset3E = QtGui.QLineEdit(self)
			self.oSelectionOffset3E.setText(MagicPanels.unit2gui(0))
			self.oSelectionOffset3E.setFixedWidth(fieldSize)
			self.oSelectionOffset3E.move(column3, row)
			
			row += 30

			# label
			self.oHeightL = QtGui.QLabel(translate('magicStart', 'Furniture along Z (height):'), self)
			self.oHeightL.move(10, row+3)

			# text input
			self.oHeightE = QtGui.QLineEdit(self)
			self.oHeightE.setText(MagicPanels.unit2gui(self.gFSZ))
			self.oHeightE.setFixedWidth(fieldSize3x)
			self.oHeightE.move(column1, row)

			row += 50
			
			# button
			self.oCalculateB1 = QtGui.QPushButton(translate('magicStart', 'calculate furniture from selection'), self)
			self.oCalculateB1.clicked.connect(self.calculateFurniture)
			self.oCalculateB1.resize(area, createSize)
			self.oCalculateB1.move(10, row)
			
			row += 80
			
			# label
			self.oStartXYZL = QtGui.QLabel(translate('magicStart', 'Start XYZ:'), self)
			self.oStartXYZL.move(column0, row+3)
			
			# text input
			self.oStartXE = QtGui.QLineEdit(self)
			self.oStartXE.setText(MagicPanels.unit2gui(0))
			self.oStartXE.setFixedWidth(fieldSize)
			self.oStartXE.move(column1, row)
			
			# text input
			self.oStartYE = QtGui.QLineEdit(self)
			self.oStartYE.setText(MagicPanels.unit2gui(0))
			self.oStartYE.setFixedWidth(fieldSize)
			self.oStartYE.move(column2, row)
			
			# text input
			self.oStartZE = QtGui.QLineEdit(self)
			self.oStartZE.setText(MagicPanels.unit2gui(0))
			self.oStartZE.setFixedWidth(fieldSize)
			self.oStartZE.move(column3, row)

			row += 30
			
			# label
			self.oWidthL = QtGui.QLabel(translate('magicStart', 'Furniture along X (width):'), self)
			self.oWidthL.move(10, row+3)
			
			# text input
			self.oWidthE = QtGui.QLineEdit(self)
			self.oWidthE.setText(MagicPanels.unit2gui(self.gFSX))
			self.oWidthE.setFixedWidth(fieldSize3x)
			self.oWidthE.move(column1, row)

			row += 30
			
			# label
			self.oDepthL = QtGui.QLabel(translate('magicStart', 'Furniture along Y (depth):'), self)
			self.oDepthL.move(10, row+3)

			# text input
			self.oDepthE = QtGui.QLineEdit(self)
			self.oDepthE.setText(MagicPanels.unit2gui(self.gFSY))
			self.oDepthE.setFixedWidth(fieldSize3x)
			self.oDepthE.move(column1, row)
			
			row += 40

			# button
			self.oCreateB1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.oCreateB1.clicked.connect(self.createObject)
			self.oCreateB1.resize(area, createSize)
			self.oCreateB1.move(10, createRow)

			# hide by default
			self.oThickL.hide()
			self.oThickE.hide()
			self.oThickBackL.hide()
			self.oThickBackE.hide()
			self.oThickShelfL.hide()
			self.oThickShelfE.hide()
			self.oThickFrontL.hide()
			self.oThickFrontE.hide()
			self.oOffsetFrontLL.hide()
			self.oOffsetFrontLE.hide()
			self.oOffsetFrontRL.hide()
			self.oOffsetFrontRE.hide()
			self.oOffsetFrontTL.hide()
			self.oOffsetFrontTE.hide()
			self.oOffsetFrontBL.hide()
			self.oOffsetFrontBE.hide()
			self.oModulesNumL.hide()
			self.oModulesNumE.hide()
			self.oSelectionOffsetL.hide()
			self.oSelectionOffset1E.hide()
			self.oSelectionOffset2E.hide()
			self.oSelectionOffset3E.hide()
			self.oHeightL.hide()
			self.oHeightE.hide()
			self.oCalculateB1.hide()
			self.oStartXYZL.hide()
			self.oStartXE.hide()
			self.oStartYE.hide()
			self.oStartZE.hide()
			self.oWidthL.hide()
			self.oWidthE.hide()
			self.oDepthL.hide()
			self.oDepthE.hide()
			self.oCreateB1.hide()

			# ############################################################################
			# GUI for foot (hidden by default)
			# ############################################################################
			
			rowfoot -= 20
			
			# label
			info = translate('magicStart', 'Possible selections, choose one method and make selection before calculate or create button press: <br><br> 1. XY face - to set size and position <br><br> 2. X edge - to set X size and position <br><br> 3. Vertex - to set XYZ start position <br><br> 4. no selection - to create with custom settings')
			self.oFootInfo = QtGui.QLabel(info, self)
			self.oFootInfo.move(10, rowfoot+3)
			self.oFootInfo.setFixedWidth(infoarea)
			self.oFootInfo.setWordWrap(True)
			self.oFootInfo.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowfoot += 200

			# label
			self.oFootThickL = QtGui.QLabel(translate('magicStart', 'Wood thickness:'), self)
			self.oFootThickL.move(10, rowfoot+3)

			# text input
			self.oFootThickE = QtGui.QLineEdit(self)
			self.oFootThickE.setText(MagicPanels.unit2gui(self.gThick))
			self.oFootThickE.setFixedWidth(90)
			self.oFootThickE.move(190, rowfoot)

			rowfoot += 30
			
			# label
			self.oFootSizeZL = QtGui.QLabel(translate('magicStart', 'Foot height (Z axis):'), self)
			self.oFootSizeZL.move(10, rowfoot+3)

			# text input
			self.oFootSizeZE = QtGui.QLineEdit(self)
			self.oFootSizeZE.setText(MagicPanels.unit2gui(100))
			self.oFootSizeZE.setFixedWidth(90)
			self.oFootSizeZE.move(190, rowfoot)

			rowfoot += 30
			
			# button
			self.oFootCalculateB = QtGui.QPushButton(translate('magicStart', 'calculate foot'), self)
			self.oFootCalculateB.clicked.connect(self.calculateFoot)
			self.oFootCalculateB.resize(area, createSize)
			self.oFootCalculateB.move(10, rowfoot)
			
			rowfoot += 70
			
			# label
			self.oFootStartL = QtGui.QLabel(translate('magicStart', 'Start XYZ:'), self)
			self.oFootStartL.move(10, rowfoot+3)
			
			# text input
			self.oFootStartXE = QtGui.QLineEdit(self)
			self.oFootStartXE.setText(MagicPanels.unit2gui(0))
			self.oFootStartXE.setFixedWidth(starttfs)
			self.oFootStartXE.move(startcX, rowfoot)
			
			# text input
			self.oFootStartYE = QtGui.QLineEdit(self)
			self.oFootStartYE.setText(MagicPanels.unit2gui(0))
			self.oFootStartYE.setFixedWidth(starttfs)
			self.oFootStartYE.move(startcY, rowfoot)
			
			# text input
			self.oFootStartZE = QtGui.QLineEdit(self)
			self.oFootStartZE.setText(MagicPanels.unit2gui(0))
			self.oFootStartZE.setFixedWidth(starttfs)
			self.oFootStartZE.move(startcZ, rowfoot)

			rowfoot += 30

			# label
			self.oFootSizeXL = QtGui.QLabel(translate('magicStart', 'Foot width (X axis):'), self)
			self.oFootSizeXL.move(10, rowfoot+3)
			
			# text input
			self.oFootSizeXE = QtGui.QLineEdit(self)
			self.oFootSizeXE.setText(MagicPanels.unit2gui(0))
			self.oFootSizeXE.setFixedWidth(rsize2x)
			self.oFootSizeXE.move(startcY, rowfoot)

			rowfoot += 30

			# label
			self.oFootSizeYL = QtGui.QLabel(translate('magicStart', 'Foot depth (Y axis):'), self)
			self.oFootSizeYL.move(10, rowfoot+3)

			# text input
			self.oFootSizeYE = QtGui.QLineEdit(self)
			self.oFootSizeYE.setText(MagicPanels.unit2gui(0))
			self.oFootSizeYE.setFixedWidth(rsize2x)
			self.oFootSizeYE.move(startcY, rowfoot)

			rowfoot += 60

			# button
			self.oFootCreateB = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.oFootCreateB.clicked.connect(self.createObject)
			self.oFootCreateB.resize(area, createSize)
			self.oFootCreateB.move(10, createRow)

			# hide by default
			self.oFootInfo.hide()
			self.oFootThickL.hide()
			self.oFootThickE.hide()
			self.oFootSizeZL.hide()
			self.oFootSizeZE.hide()
			self.oFootCalculateB.hide()
			self.oFootStartL.hide()
			self.oFootStartXE.hide()
			self.oFootStartYE.hide()
			self.oFootStartZE.hide()
			self.oFootSizeXL.hide()
			self.oFootSizeXE.hide()
			self.oFootSizeYL.hide()
			self.oFootSizeYE.hide()
			self.oFootCreateB.hide()

			# ############################################################################
			# GUI for Table (hidden by default)
			# ############################################################################
			
			# label
			info = translate('magicStart', 'Possible selections: <br><br>1. Vertex - to set XYZ position <br><br>2. no selection - to create with custom settings')
			self.oTableInfo = QtGui.QLabel(info, self)
			self.oTableInfo.move(10, rowtbl+3)
			self.oTableInfo.setFixedWidth(infoarea)
			self.oTableInfo.setWordWrap(True)
			self.oTableInfo.setTextFormat(QtCore.Qt.TextFormat.RichText)
		
			rowtbl += 120
			
			# label
			self.oTableSizeXL = QtGui.QLabel(translate('magicStart', 'Table width X:'), self)
			self.oTableSizeXL.move(10, rowtbl+3)
			
			# text input
			self.oTableSizeXE = QtGui.QLineEdit(self)
			self.oTableSizeXE.setText(MagicPanels.unit2gui(990))
			self.oTableSizeXE.setFixedWidth(90)
			self.oTableSizeXE.move(150, rowtbl)

			rowtbl += 30

			# label
			self.oTableSizeYL = QtGui.QLabel(translate('magicStart', 'Table depth Y:'), self)
			self.oTableSizeYL.move(10, rowtbl+3)

			# text input
			self.oTableSizeYE = QtGui.QLineEdit(self)
			self.oTableSizeYE.setText(MagicPanels.unit2gui(525))
			self.oTableSizeYE.setFixedWidth(90)
			self.oTableSizeYE.move(150, rowtbl)

			rowtbl += 30

			# label
			self.oTableSizeZL = QtGui.QLabel(translate('magicStart', 'Table height Z:'), self)
			self.oTableSizeZL.move(10, rowtbl+3)

			# text input
			self.oTableSizeZE = QtGui.QLineEdit(self)
			self.oTableSizeZE.setText(MagicPanels.unit2gui(430))
			self.oTableSizeZE.setFixedWidth(90)
			self.oTableSizeZE.move(150, rowtbl)

			rowtbl += 30

			# label
			self.oTableTopThickL = QtGui.QLabel(translate('magicStart', 'Table top thickness:'), self)
			self.oTableTopThickL.move(10, rowtbl+3)

			# text input
			self.oTableTopThickE = QtGui.QLineEdit(self)
			self.oTableTopThickE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			self.oTableTopThickE.setFixedWidth(90)
			self.oTableTopThickE.move(220, rowtbl)

			rowtbl += 30

			# label
			self.oTableLegThickL = QtGui.QLabel(translate('magicStart', 'Legs and Supporters thickness:'), self)
			self.oTableLegThickL.move(10, rowtbl+3)

			# text input
			self.oTableLegThickE = QtGui.QLineEdit(self)
			self.oTableLegThickE.setText(MagicPanels.unit2gui(80))
			self.oTableLegThickE.setFixedWidth(90)
			self.oTableLegThickE.move(220, rowtbl)
			
			rowtbl += 30

			# label
			self.oTableTopOffsetL = QtGui.QLabel(translate('magicStart', 'Table top offset:'), self)
			self.oTableTopOffsetL.move(10, rowtbl+3)

			# text input
			self.oTableTopOffsetE = QtGui.QLineEdit(self)
			self.oTableTopOffsetE.setText(MagicPanels.unit2gui(35))
			self.oTableTopOffsetE.setFixedWidth(90)
			self.oTableTopOffsetE.move(220, rowtbl)
		
			rowtbl += 60
			
			# button
			self.oTableCalculateB = QtGui.QPushButton(translate('magicStart', 'calculate table position'), self)
			self.oTableCalculateB.clicked.connect(self.calculateTable)
			self.oTableCalculateB.resize(area, createSize)
			self.oTableCalculateB.move(10, rowtbl)
			
			rowtbl += 70
			
			# label
			self.oTableStartInfoL = QtGui.QLabel(translate('magicStart', 'Start XYZ:'), self)
			self.oTableStartInfoL.move(10, rowtbl+3)
			
			# text input
			self.oTableStartXE = QtGui.QLineEdit(self)
			self.oTableStartXE.setText(MagicPanels.unit2gui(0))
			self.oTableStartXE.setFixedWidth(starttfs)
			self.oTableStartXE.move(startcX, rowtbl)
			
			# text input
			self.oTableStartYE = QtGui.QLineEdit(self)
			self.oTableStartYE.setText(MagicPanels.unit2gui(0))
			self.oTableStartYE.setFixedWidth(starttfs)
			self.oTableStartYE.move(startcY, rowtbl)
			
			# text input
			self.oTableStartZE = QtGui.QLineEdit(self)
			self.oTableStartZE.setText(MagicPanels.unit2gui(0))
			self.oTableStartZE.setFixedWidth(starttfs)
			self.oTableStartZE.move(startcZ, rowtbl)
			
			rowtbl += 40

			# button
			self.oTableCreateB = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.oTableCreateB.clicked.connect(self.createObject)
			self.oTableCreateB.resize(area, createSize)
			self.oTableCreateB.move(10, createRow)
			
			# hide by default
			self.oTableInfo.hide()
			self.oTableSizeXL.hide()
			self.oTableSizeXE.hide()
			self.oTableSizeYL.hide()
			self.oTableSizeYE.hide()
			self.oTableSizeZL.hide()
			self.oTableSizeZE.hide()
			self.oTableTopThickL.hide()
			self.oTableTopThickE.hide()
			self.oTableLegThickL.hide()
			self.oTableLegThickE.hide()
			self.oTableTopOffsetL.hide()
			self.oTableTopOffsetE.hide()
			self.oTableCalculateB.hide()
			self.oTableStartInfoL.hide()
			self.oTableStartXE.hide()
			self.oTableStartYE.hide()
			self.oTableStartZE.hide()
			self.oTableCreateB.hide()

			# ############################################################################
			# GUI for Single drawer (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Possible selections: <br><br>1. top edge<br>2. top edge + back face<br>3. bottom edge + top edge<br>4. bottom edge + top edge + back face<br>5. bottom edge + top edge + left edge + right edge + back face<br><br>The edge can be along X or Y axis.')
			self.og1i = QtGui.QLabel(info, self)
			self.og1i.move(10, rowgap+3)
			self.og1i.setFixedWidth(infoarea)
			self.og1i.setWordWrap(True)
			self.og1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowgap += 150

			# label
			self.og10L = QtGui.QLabel(translate('magicStart', 'Drawer front overlap:'), self)
			self.og10L.setFixedWidth(150)
			self.og10L.move(10, rowgap+3)

			rowgap += 20

			# label
			self.og101L = QtGui.QLabel(translate('magicStart', 'Horizontal:'), self)
			self.og101L.move(10, rowgap+3)
			
			# label
			self.og102L = QtGui.QLabel(translate('magicStart', 'Vertical:'), self)
			self.og102L.move(110, rowgap+3)
			
			rowgap += 20
			
			# text input
			self.og101E = QtGui.QLineEdit(self)
			self.og101E.setText(MagicPanels.unit2gui(9))
			self.og101E.setFixedWidth(80)
			self.og101E.move(10, rowgap)
			
			# text input
			self.og102E = QtGui.QLineEdit(self)
			self.og102E.setText(MagicPanels.unit2gui(7))
			self.og102E.setFixedWidth(80)
			self.og102E.move(110, rowgap)
		
			rowgap += 30
			
			# label
			self.og8L = QtGui.QLabel(translate('magicStart', 'Drawer wood thickness:'), self)
			self.og8L.move(10, rowgap+3)

			rowgap += 20

			# label
			self.og81L = QtGui.QLabel(translate('magicStart', 'Front:'), self)
			self.og81L.move(10, rowgap+3)
			
			# label
			self.og82L = QtGui.QLabel(translate('magicStart', 'Sides:'), self)
			self.og82L.move(110, rowgap+3)
			
			# label
			self.og83L = QtGui.QLabel(translate('magicStart', 'Bottom:'), self)
			self.og83L.move(210, rowgap+3)
			
			rowgap += 20
			
			# text input
			self.og81E = QtGui.QLineEdit(self)
			self.og81E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			self.og81E.setFixedWidth(80)
			self.og81E.move(10, rowgap)
			
			# text input
			self.og82E = QtGui.QLineEdit(self)
			self.og82E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			self.og82E.setFixedWidth(80)
			self.og82E.move(110, rowgap)
			
			# text input
			self.og83E = QtGui.QLineEdit(self)
			self.og83E.setText(MagicPanels.unit2gui(3))
			self.og83E.setFixedWidth(80)
			self.og83E.move(210, rowgap)
			
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
			self.og91E.setText(MagicPanels.unit2gui(26))
			self.og91E.setFixedWidth(80)
			self.og91E.move(10, rowgap)
			
			# text input
			self.og92E = QtGui.QLineEdit(self)
			self.og92E.setText(MagicPanels.unit2gui(20))
			self.og92E.setFixedWidth(80)
			self.og92E.move(110, rowgap)
			
			# text input
			self.og93E = QtGui.QLineEdit(self)
			self.og93E.setText(MagicPanels.unit2gui(30))
			self.og93E.setFixedWidth(80)
			self.og93E.move(210, rowgap)
			
			# text input
			self.og94E = QtGui.QLineEdit(self)
			self.og94E.setText(MagicPanels.unit2gui(10))
			self.og94E.setFixedWidth(80)
			self.og94E.move(310, rowgap)

			rowgap += 50

			# button
			self.og4B1 = QtGui.QPushButton(translate('magicStart', 'calculate gap for drawer'), self)
			self.og4B1.clicked.connect(self.calculateSingleDrawer)
			self.og4B1.resize(area, createSize)
			self.og4B1.move(10, rowgap)
			
			rowgap += 60
			
			# label
			self.og2L = QtGui.QLabel(translate('magicStart', 'Gap start XYZ:'), self)
			self.og2L.move(10, rowgap+3)
			
			# text input
			self.og2E = QtGui.QLineEdit(self)
			self.og2E.setText(MagicPanels.unit2gui(0))
			self.og2E.setFixedWidth(starttfs)
			self.og2E.move(startcX, rowgap)
			
			# text input
			self.og3E = QtGui.QLineEdit(self)
			self.og3E.setText(MagicPanels.unit2gui(0))
			self.og3E.setFixedWidth(starttfs)
			self.og3E.move(startcY, rowgap)
			
			# text input
			self.og4E = QtGui.QLineEdit(self)
			self.og4E.setText(MagicPanels.unit2gui(0))
			self.og4E.setFixedWidth(starttfs)
			self.og4E.move(startcZ, rowgap)
			
			rowgap += 30

			# label
			self.og5L = QtGui.QLabel(translate('magicStart', 'Gap width:'), self)
			self.og5L.move(10, rowgap+3)
			
			# text input
			self.og5E = QtGui.QLineEdit(self)
			self.og5E.setText(MagicPanels.unit2gui(400))
			self.og5E.setFixedWidth(rsize2x)
			self.og5E.move(startcY, rowgap)
			
			rowgap += 30
			
			# label
			self.og6L = QtGui.QLabel(translate('magicStart', 'Gap height:'), self)
			self.og6L.move(10, rowgap+3)

			# text input
			self.og6E = QtGui.QLineEdit(self)
			self.og6E.setText(MagicPanels.unit2gui(150))
			self.og6E.setFixedWidth(rsize2x)
			self.og6E.move(startcY, rowgap)
			
			rowgap += 30
			
			# label
			self.og7L = QtGui.QLabel(translate('magicStart', 'Gap depth:'), self)
			self.og7L.move(10, rowgap+3)

			# text input
			self.og7E = QtGui.QLineEdit(self)
			self.og7E.setText(MagicPanels.unit2gui(350))
			self.og7E.setFixedWidth(rsize2x)
			self.og7E.move(startcY, rowgap)
			
		
			# button
			self.og9B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.og9B1.clicked.connect(self.createObject)
			self.og9B1.resize(area, createSize)
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
			self.og81L.hide()
			self.og82L.hide()
			self.og83L.hide()
			self.og81E.hide()
			self.og82E.hide()
			self.og83E.hide()
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
			self.og10L.hide()
			self.og101L.hide()
			self.og102L.hide()
			self.og101E.hide()
			self.og102E.hide()
			
			# ############################################################################
			# GUI for drawer series GAP (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 4 edges around the gap and back face: <br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge <br> 5. selection - back face')
			self.ods1i = QtGui.QLabel(info, self)
			self.ods1i.move(10, rowds+3)
			self.ods1i.setFixedWidth(infoarea)
			self.ods1i.setWordWrap(True)
			self.ods1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowds += 130
			
			# label
			self.ods2L = QtGui.QLabel(translate('magicStart', 'Number of drawers:'), self)
			self.ods2L.move(10, rowds+3)
			
			# text input
			self.ods2E = QtGui.QLineEdit(self)
			self.ods2E.setText("4")
			self.ods2E.setFixedWidth(80)
			self.ods2E.move(180, rowds)
		
			rowds += 30
		
			# label
			self.ods11L = QtGui.QLabel(translate('magicStart', 'Drawer front overlap:'), self)
			self.ods11L.setFixedWidth(150)
			self.ods11L.move(10, rowds+3)

			rowds += 20

			# label
			self.ods111L = QtGui.QLabel(translate('magicStart', 'Horizontal:'), self)
			self.ods111L.move(10, rowds+3)
			
			# label
			self.ods112L = QtGui.QLabel(translate('magicStart', 'Vertical:'), self)
			self.ods112L.move(110, rowds+3)
			
			# label
			self.ods113L = QtGui.QLabel(translate('magicStart', 'Space between:'), self)
			self.ods113L.move(210, rowds+3)
			
			rowds += 20
			
			# text input
			self.ods111E = QtGui.QLineEdit(self)
			self.ods111E.setText(MagicPanels.unit2gui(9))
			self.ods111E.setFixedWidth(90)
			self.ods111E.move(10, rowds)
			
			# text input
			self.ods112E = QtGui.QLineEdit(self)
			self.ods112E.setText(MagicPanels.unit2gui(7))
			self.ods112E.setFixedWidth(90)
			self.ods112E.move(110, rowds)
		
			# text input
			self.ods113E = QtGui.QLineEdit(self)
			self.ods113E.setText(MagicPanels.unit2gui(4))
			self.ods113E.setFixedWidth(90)
			self.ods113E.move(210, rowds)
			
			rowds += 30
			
			# label
			self.ods3L = QtGui.QLabel(translate('magicStart', 'Drawer wood thickness:'), self)
			self.ods3L.move(10, rowds+3)

			rowds += 20

			# label
			self.ods31L = QtGui.QLabel(translate('magicStart', 'Front:'), self)
			self.ods31L.move(10, rowds+3)
			
			# label
			self.ods32L = QtGui.QLabel(translate('magicStart', 'Sides:'), self)
			self.ods32L.move(110, rowds+3)
			
			# label
			self.ods33L = QtGui.QLabel(translate('magicStart', 'Bottom:'), self)
			self.ods33L.move(210, rowds+3)
			
			rowds += 20
			
			# text input
			self.ods31E = QtGui.QLineEdit(self)
			self.ods31E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			self.ods31E.setFixedWidth(80)
			self.ods31E.move(10, rowds)
			
			# text input
			self.ods32E = QtGui.QLineEdit(self)
			self.ods32E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			self.ods32E.setFixedWidth(80)
			self.ods32E.move(110, rowds)
			
			# text input
			self.ods33E = QtGui.QLineEdit(self)
			self.ods33E.setText(MagicPanels.unit2gui(3))
			self.ods33E.setFixedWidth(80)
			self.ods33E.move(210, rowds)
			
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
			
			# label
			self.ods45L = QtGui.QLabel(translate('magicStart', 'Back sides:'), self)
			self.ods45L.move(410, rowds+3)
			
			rowds += 20
			
			# text input
			self.ods41E = QtGui.QLineEdit(self)
			self.ods41E.setText(MagicPanels.unit2gui(26))
			self.ods41E.setFixedWidth(80)
			self.ods41E.move(10, rowds)
			
			# text input
			self.ods42E = QtGui.QLineEdit(self)
			self.ods42E.setText(MagicPanels.unit2gui(20))
			self.ods42E.setFixedWidth(80)
			self.ods42E.move(110, rowds)
			
			# text input
			self.ods43E = QtGui.QLineEdit(self)
			self.ods43E.setText(MagicPanels.unit2gui(30))
			self.ods43E.setFixedWidth(80)
			self.ods43E.move(210, rowds)
			
			# text input
			self.ods44E = QtGui.QLineEdit(self)
			self.ods44E.setText(MagicPanels.unit2gui(10))
			self.ods44E.setFixedWidth(80)
			self.ods44E.move(310, rowds)
			
			# text input
			self.ods45E = QtGui.QLineEdit(self)
			self.ods45E.setText(MagicPanels.unit2gui(87))
			self.ods45E.setFixedWidth(80)
			self.ods45E.move(410, rowds)
			
			rowds += 30
			
			# button
			self.ods5B = QtGui.QPushButton(translate('magicStart', 'calculate gaps'), self)
			self.ods5B.clicked.connect(self.calculateDrawerSeries)
			self.ods5B.resize(area, createSize)
			self.ods5B.move(10, rowds)
			
			rowds += 60
			
			# label
			self.ods6L = QtGui.QLabel(translate('magicStart', 'Gap start XYZ:'), self)
			self.ods6L.move(10, rowds+3)
			
			# text input
			self.ods61E = QtGui.QLineEdit(self)
			self.ods61E.setText(MagicPanels.unit2gui(0))
			self.ods61E.setFixedWidth(starttfs)
			self.ods61E.move(startcX, rowds)
			
			# text input
			self.ods62E = QtGui.QLineEdit(self)
			self.ods62E.setText(MagicPanels.unit2gui(0))
			self.ods62E.setFixedWidth(starttfs)
			self.ods62E.move(startcY, rowds)
			
			# text input
			self.ods63E = QtGui.QLineEdit(self)
			self.ods63E.setText(MagicPanels.unit2gui(0))
			self.ods63E.setFixedWidth(starttfs)
			self.ods63E.move(startcZ, rowds)
			
			rowds += 30

			# label
			self.ods7L = QtGui.QLabel(translate('magicStart', 'Single gap width:'), self)
			self.ods7L.move(10, rowds+3)
			
			# text input
			self.ods7E = QtGui.QLineEdit(self)
			self.ods7E.setText(MagicPanels.unit2gui(400))
			self.ods7E.setFixedWidth(rsize2x)
			self.ods7E.move(startcY, rowds)
			
			rowds += 30
			
			# label
			self.ods8L = QtGui.QLabel(translate('magicStart', 'Single gap height:'), self)
			self.ods8L.move(10, rowds+3)

			# text input
			self.ods8E = QtGui.QLineEdit(self)
			self.ods8E.setText(MagicPanels.unit2gui(150))
			self.ods8E.setFixedWidth(rsize2x)
			self.ods8E.move(startcY, rowds)
			
			rowds += 30
			
			# label
			self.ods9L = QtGui.QLabel(translate('magicStart', 'Single gap depth:'), self)
			self.ods9L.move(10, rowds+3)

			# text input
			self.ods9E = QtGui.QLineEdit(self)
			self.ods9E.setText(MagicPanels.unit2gui(350))
			self.ods9E.setFixedWidth(rsize2x)
			self.ods9E.move(startcY, rowds)
			
			rowds += 30

			# button
			self.ods10B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.ods10B.clicked.connect(self.createObject)
			self.ods10B.resize(area, createSize)
			self.ods10B.move(10, createRow)

			# hide by default
			self.ods1i.hide()
			self.ods2L.hide()
			self.ods2E.hide()
			self.ods3L.hide()
			self.ods31L.hide()
			self.ods32L.hide()
			self.ods33L.hide()
			self.ods31E.hide()
			self.ods32E.hide()
			self.ods33E.hide()
			self.ods4L.hide()
			self.ods41L.hide()
			self.ods42L.hide()
			self.ods43L.hide()
			self.ods44L.hide()
			self.ods45L.hide()
			self.ods41E.hide()
			self.ods42E.hide()
			self.ods43E.hide()
			self.ods44E.hide()
			self.ods45E.hide()
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
			self.ods11L.hide()
			self.ods111L.hide()
			self.ods112L.hide()
			self.ods113L.hide()
			self.ods111E.hide()
			self.ods112E.hide()
			self.ods113E.hide()
			
			# ############################################################################
			# GUI for Front from GAP (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 4 edges around the gap to calculate front size in this order: <br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge')
			self.ofr1i = QtGui.QLabel(info, self)
			self.ofr1i.move(10, rowfront+3)
			self.ofr1i.setFixedWidth(infoarea)
			self.ofr1i.setWordWrap(True)
			self.ofr1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowfront += 130
			
			# label
			self.ofr7L = QtGui.QLabel(translate('magicStart', 'Front thickness:'), self)
			self.ofr7L.move(10, rowfront+3)

			# text input
			self.ofr7E = QtGui.QLineEdit(self)
			self.ofr7E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
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
			self.ofr81E.setText(MagicPanels.unit2gui(0))
			self.ofr81E.setFixedWidth(80)
			self.ofr81E.move(10, rowfront)
			
			# text input
			self.ofr82E = QtGui.QLineEdit(self)
			self.ofr82E.setText(MagicPanels.unit2gui(0))
			self.ofr82E.setFixedWidth(80)
			self.ofr82E.move(110, rowfront)
			
			# text input
			self.ofr83E = QtGui.QLineEdit(self)
			self.ofr83E.setText(MagicPanels.unit2gui(0))
			self.ofr83E.setFixedWidth(80)
			self.ofr83E.move(210, rowfront)
			
			# text input
			self.ofr84E = QtGui.QLineEdit(self)
			self.ofr84E.setText(MagicPanels.unit2gui(0))
			self.ofr84E.setFixedWidth(80)
			self.ofr84E.move(310, rowfront)

			rowfront += 40
			
			# button
			self.ofr4B1 = QtGui.QPushButton(translate('magicStart', 'calculate front'), self)
			self.ofr4B1.clicked.connect(self.calculateFrontFromGap)
			self.ofr4B1.resize(area, createSize)
			self.ofr4B1.move(10, rowfront)
			
			rowfront += 80
			
			# label
			self.ofr2L = QtGui.QLabel(translate('magicStart', 'Front start XYZ:'), self)
			self.ofr2L.move(10, rowfront+3)
			
			# text input
			self.ofr2E = QtGui.QLineEdit(self)
			self.ofr2E.setText(MagicPanels.unit2gui(0))
			self.ofr2E.setFixedWidth(starttfs)
			self.ofr2E.move(startcX, rowfront)
			
			# text input
			self.ofr3E = QtGui.QLineEdit(self)
			self.ofr3E.setText(MagicPanels.unit2gui(0))
			self.ofr3E.setFixedWidth(starttfs)
			self.ofr3E.move(startcY, rowfront)
			
			# text input
			self.ofr4E = QtGui.QLineEdit(self)
			self.ofr4E.setText(MagicPanels.unit2gui(0))
			self.ofr4E.setFixedWidth(starttfs)
			self.ofr4E.move(startcZ, rowfront)
			
			rowfront += 30

			# label
			self.ofr5L = QtGui.QLabel(translate('magicStart', 'Front width:'), self)
			self.ofr5L.move(10, rowfront+3)
			
			# text input
			self.ofr5E = QtGui.QLineEdit(self)
			self.ofr5E.setText(MagicPanels.unit2gui(0))
			self.ofr5E.setFixedWidth(rsize2x)
			self.ofr5E.move(startcY, rowfront)
			
			rowfront += 30
			
			# label
			self.ofr6L = QtGui.QLabel(translate('magicStart', 'Front height:'), self)
			self.ofr6L.move(10, rowfront+3)

			# text input
			self.ofr6E = QtGui.QLineEdit(self)
			self.ofr6E.setText(MagicPanels.unit2gui(0))
			self.ofr6E.setFixedWidth(rsize2x)
			self.ofr6E.move(startcY, rowfront)
			
			rowfront += 40

			# button
			self.ofr8B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.ofr8B1.clicked.connect(self.createObject)
			self.ofr8B1.resize(area, createSize)
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
			# GUI for Back from GAP (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 4 edges around the gap to calculate back: <br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge from back model view <br> 4. selection - Z right edge from back model view')
			self.oBackInfo = QtGui.QLabel(info, self)
			self.oBackInfo.move(10, rowback+3)
			self.oBackInfo.setFixedWidth(infoarea)
			self.oBackInfo.setWordWrap(True)
			self.oBackInfo.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowback += 130
			
			# label
			self.oBackThickL = QtGui.QLabel(translate('magicStart', 'Back thickness along Y:'), self)
			self.oBackThickL.move(10, rowback+3)

			# text input
			self.oBackThickE = QtGui.QLineEdit(self)
			self.oBackThickE.setText(MagicPanels.unit2gui(0))
			self.oBackThickE.setFixedWidth(90)
			self.oBackThickE.move(190, rowback)
		
			rowback += 40
			
			# label
			self.oBackOffsetsL = QtGui.QLabel(translate('magicStart', 'Back offsets:'), self)
			self.oBackOffsetsL.setFixedWidth(150)
			self.oBackOffsetsL.move(10, rowback+3)

			rowback += 20
			
			# label
			self.oBackOffsets1L = QtGui.QLabel(translate('magicStart', 'Left side:'), self)
			self.oBackOffsets1L.move(10, rowback+3)
			
			# label
			self.oBackOffsets2L = QtGui.QLabel(translate('magicStart', 'Right side:'), self)
			self.oBackOffsets2L.move(110, rowback+3)
			
			# label
			self.oBackOffsets3L = QtGui.QLabel(translate('magicStart', 'Top:'), self)
			self.oBackOffsets3L.move(210, rowback+3)
			
			# label
			self.oBackOffsets4L = QtGui.QLabel(translate('magicStart', 'Bottom:'), self)
			self.oBackOffsets4L.move(310, rowback+3)

			rowback += 20
			
			# text input
			self.oBackOffsets1E = QtGui.QLineEdit(self)
			self.oBackOffsets1E.setText(MagicPanels.unit2gui(0))
			self.oBackOffsets1E.setFixedWidth(80)
			self.oBackOffsets1E.move(10, rowback)
			
			# text input
			self.oBackOffsets2E = QtGui.QLineEdit(self)
			self.oBackOffsets2E.setText(MagicPanels.unit2gui(0))
			self.oBackOffsets2E.setFixedWidth(80)
			self.oBackOffsets2E.move(110, rowback)
			
			# text input
			self.oBackOffsets3E = QtGui.QLineEdit(self)
			self.oBackOffsets3E.setText(MagicPanels.unit2gui(0))
			self.oBackOffsets3E.setFixedWidth(80)
			self.oBackOffsets3E.move(210, rowback)
			
			# text input
			self.oBackOffsets4E = QtGui.QLineEdit(self)
			self.oBackOffsets4E.setText(MagicPanels.unit2gui(0))
			self.oBackOffsets4E.setFixedWidth(80)
			self.oBackOffsets4E.move(310, rowback)

			rowback += 40
			
			# button
			self.oBackBCL = QtGui.QPushButton(translate('magicStart', 'calculate back'), self)
			self.oBackBCL.clicked.connect(self.calculateBack)
			self.oBackBCL.resize(area, createSize)
			self.oBackBCL.move(10, rowback)
			
			rowback += 80
			
			# label
			self.oBackStartL = QtGui.QLabel(translate('magicStart', 'Start XYZ:'), self)
			self.oBackStartL.move(10, rowback+3)
			
			# text input
			self.oBackSXE = QtGui.QLineEdit(self)
			self.oBackSXE.setText(MagicPanels.unit2gui(0))
			self.oBackSXE.setFixedWidth(starttfs)
			self.oBackSXE.move(startcX, rowback)
			
			# text input
			self.oBackSYE = QtGui.QLineEdit(self)
			self.oBackSYE.setText(MagicPanels.unit2gui(0))
			self.oBackSYE.setFixedWidth(starttfs)
			self.oBackSYE.move(startcY, rowback)
			
			# text input
			self.oBackSZE = QtGui.QLineEdit(self)
			self.oBackSZE.setText(MagicPanels.unit2gui(0))
			self.oBackSZE.setFixedWidth(starttfs)
			self.oBackSZE.move(startcZ, rowback)
			
			rowback += 30

			# label
			self.oBackSizeXL = QtGui.QLabel(translate('magicStart', 'Calculated back width along X:'), self)
			self.oBackSizeXL.move(10, rowback+3)
			
			# text input
			self.oBackSizeXE = QtGui.QLineEdit(self)
			self.oBackSizeXE.setText(MagicPanels.unit2gui(0))
			self.oBackSizeXE.setFixedWidth(rsize2x)
			self.oBackSizeXE.move(startcY, rowback)
			
			rowback += 30
			
			# label
			self.oBackSizeYL = QtGui.QLabel(translate('magicStart', 'Calculated back height along Z:'), self)
			self.oBackSizeYL.move(10, rowback+3)

			# text input
			self.oBackSizeYE = QtGui.QLineEdit(self)
			self.oBackSizeYE.setText(MagicPanels.unit2gui(0))
			self.oBackSizeYE.setFixedWidth(rsize2x)
			self.oBackSizeYE.move(startcY, rowback)
			
			rowback += 40

			# button
			self.oBackBCR = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.oBackBCR.clicked.connect(self.createObject)
			self.oBackBCR.resize(area, createSize)
			self.oBackBCR.move(10, createRow)

			# hide by default
			self.oBackInfo.hide()
			self.oBackThickL.hide()
			self.oBackThickE.hide()
			self.oBackOffsetsL.hide()
			self.oBackOffsets1L.hide()
			self.oBackOffsets2L.hide()
			self.oBackOffsets3L.hide()
			self.oBackOffsets4L.hide()
			self.oBackOffsets1E.hide()
			self.oBackOffsets2E.hide()
			self.oBackOffsets3E.hide()
			self.oBackOffsets4E.hide()
			self.oBackBCL.hide()
			self.oBackStartL.hide()
			self.oBackSXE.hide()
			self.oBackSYE.hide()
			self.oBackSZE.hide()
			self.oBackSizeXL.hide()
			self.oBackSizeXE.hide()
			self.oBackSizeYL.hide()
			self.oBackSizeYE.hide()
			self.oBackBCR.hide()
			
			# ############################################################################
			# GUI for Front with glass (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 4 edges around the gap to calculate Front with glass: <br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge')
			self.ofglass1i = QtGui.QLabel(info, self)
			self.ofglass1i.move(10, rowfglass+3)
			self.ofglass1i.setFixedWidth(infoarea)
			self.ofglass1i.setWordWrap(True)
			self.ofglass1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowfglass += 120
			
			# label
			self.ofglass2L = QtGui.QLabel(translate('magicStart', 'Wood thickness:'), self)
			self.ofglass2L.move(10, rowfglass+3)
			
			# text input
			self.ofglass2E = QtGui.QLineEdit(self)
			self.ofglass2E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			self.ofglass2E.setFixedWidth(90)
			self.ofglass2E.move(150, rowfglass)
			
			rowfglass += 30
			
			# label
			self.ofglass3L = QtGui.QLabel(translate('magicStart', 'Overlap horizontal:'), self)
			self.ofglass3L.setFixedWidth(120)
			self.ofglass3L.move(10, rowfglass+3)

			# text input
			self.ofglass3E = QtGui.QLineEdit(self)
			self.ofglass3E.setText(MagicPanels.unit2gui(0))
			self.ofglass3E.setFixedWidth(90)
			self.ofglass3E.move(150, rowfglass)
		
			rowfglass += 30

			# label
			self.ofglass4L = QtGui.QLabel(translate('magicStart', 'Overlap vertical:'), self)
			self.ofglass4L.setFixedWidth(120)
			self.ofglass4L.move(10, rowfglass+3)

			# text input
			self.ofglass4E = QtGui.QLineEdit(self)
			self.ofglass4E.setText(MagicPanels.unit2gui(0))
			self.ofglass4E.setFixedWidth(90)
			self.ofglass4E.move(150, rowfglass)
			
			rowfglass += 30
			
			# label
			self.ofglass5L = QtGui.QLabel(translate('magicStart', 'Glass thickness:'), self)
			self.ofglass5L.move(10, rowfglass+3)

			# text input
			self.ofglass5E = QtGui.QLineEdit(self)
			self.ofglass5E.setText(MagicPanels.unit2gui(4))
			self.ofglass5E.setFixedWidth(90)
			self.ofglass5E.move(150, rowfglass)
			
			rowfglass += 40
			
			# button
			self.ofglass6B = QtGui.QPushButton(translate('magicStart', 'calculate front with glass'), self)
			self.ofglass6B.clicked.connect(self.calculateFrontWithGlass)
			self.ofglass6B.resize(area, createSize)
			self.ofglass6B.move(10, rowfglass)
			
			rowfglass += 80
			
			# label
			self.ofglass7L = QtGui.QLabel(translate('magicStart', 'Front start XYZ:'), self)
			self.ofglass7L.move(10, rowfglass+3)
			
			# text input
			self.ofglass71E = QtGui.QLineEdit(self)
			self.ofglass71E.setText(MagicPanels.unit2gui(0))
			self.ofglass71E.setFixedWidth(starttfs)
			self.ofglass71E.move(startcX, rowfglass)
			
			# text input
			self.ofglass72E = QtGui.QLineEdit(self)
			self.ofglass72E.setText(MagicPanels.unit2gui(0))
			self.ofglass72E.setFixedWidth(starttfs)
			self.ofglass72E.move(startcY, rowfglass)
			
			# text input
			self.ofglass73E = QtGui.QLineEdit(self)
			self.ofglass73E.setText(MagicPanels.unit2gui(0))
			self.ofglass73E.setFixedWidth(starttfs)
			self.ofglass73E.move(startcZ, rowfglass)
			
			rowfglass += 30
			
			# label
			self.ofglass8L = QtGui.QLabel(translate('magicStart', 'Calculated single bar width:'), self)
			self.ofglass8L.move(10, rowfglass+3)
			
			# text input
			self.ofglass8E = QtGui.QLineEdit(self)
			self.ofglass8E.setText(MagicPanels.unit2gui(0))
			self.ofglass8E.setFixedWidth(rsize2x)
			self.ofglass8E.move(startcY, rowfglass)
			
			rowfglass += 30
			
			# label
			self.ofglass9L = QtGui.QLabel(translate('magicStart', 'Calculated front width:'), self)
			self.ofglass9L.move(10, rowfglass+3)
			
			# text input
			self.ofglass9E = QtGui.QLineEdit(self)
			self.ofglass9E.setText(MagicPanels.unit2gui(0))
			self.ofglass9E.setFixedWidth(rsize2x)
			self.ofglass9E.move(startcY, rowfglass)
			
			rowfglass += 30
			
			# label
			self.ofglass10L = QtGui.QLabel(translate('magicStart', 'Calculated front height:'), self)
			self.ofglass10L.move(10, rowfglass+3)

			# text input
			self.ofglass10E = QtGui.QLineEdit(self)
			self.ofglass10E.setText(MagicPanels.unit2gui(0))
			self.ofglass10E.setFixedWidth(rsize2x)
			self.ofglass10E.move(startcY, rowfglass)
		
			rowfglass += 40

			# button
			self.ofglass11B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.ofglass11B.clicked.connect(self.createObject)
			self.ofglass11B.resize(area, createSize)
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
			# GUI for Decorative front (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 4 edges around the gap to calculate decorative front: <br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge')
			self.odf1i = QtGui.QLabel(info, self)
			self.odf1i.move(10, rowodf+3)
			self.odf1i.setFixedWidth(infoarea)
			self.odf1i.setWordWrap(True)
			self.odf1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowodf += 120
			
			# label
			self.odf2L = QtGui.QLabel(translate('magicStart', 'Single beam thickness:'), self)
			self.odf2L.setFixedWidth(160)
			self.odf2L.move(10, rowodf+3)
			
			# text input
			self.odf2E = QtGui.QLineEdit(self)
			self.odf2E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			self.odf2E.setFixedWidth(90)
			self.odf2E.move(170, rowodf)
			
			rowodf += 30
			
			# label
			self.odf3L = QtGui.QLabel(translate('magicStart', 'Front overlap horizontal:'), self)
			self.odf3L.setFixedWidth(160)
			self.odf3L.move(10, rowodf+3)

			# text input
			self.odf3E = QtGui.QLineEdit(self)
			self.odf3E.setText(MagicPanels.unit2gui(0))
			self.odf3E.setFixedWidth(90)
			self.odf3E.move(170, rowodf)
		
			rowodf += 30

			# label
			self.odf4L = QtGui.QLabel(translate('magicStart', 'Front overlap vertical:'), self)
			self.odf4L.setFixedWidth(160)
			self.odf4L.move(10, rowodf+3)

			# text input
			self.odf4E = QtGui.QLineEdit(self)
			self.odf4E.setText(MagicPanels.unit2gui(0))
			self.odf4E.setFixedWidth(90)
			self.odf4E.move(170, rowodf)
			
			rowodf += 30
			
			# label
			self.odf5L = QtGui.QLabel(translate('magicStart', 'Inner board thickness:'), self)
			self.odf5L.setFixedWidth(160)
			self.odf5L.move(10, rowodf+3)

			# text input
			self.odf5E = QtGui.QLineEdit(self)
			self.odf5E.setText(MagicPanels.unit2gui(6))
			self.odf5E.setFixedWidth(90)
			self.odf5E.move(170, rowodf)
			
			rowodf += 40
			
			# button
			self.odf6B = QtGui.QPushButton(translate('magicStart', 'calculate decorative front'), self)
			self.odf6B.clicked.connect(self.calculateDecorativeFront)
			self.odf6B.resize(area, createSize)
			self.odf6B.move(10, rowodf)
			
			rowodf += 80
			
			# label
			self.odf7L = QtGui.QLabel(translate('magicStart', 'Front start XYZ:'), self)
			self.odf7L.move(10, rowodf+3)
			
			# text input
			self.odf71E = QtGui.QLineEdit(self)
			self.odf71E.setText(MagicPanels.unit2gui(0))
			self.odf71E.setFixedWidth(starttfs)
			self.odf71E.move(startcX, rowodf)
			
			# text input
			self.odf72E = QtGui.QLineEdit(self)
			self.odf72E.setText(MagicPanels.unit2gui(0))
			self.odf72E.setFixedWidth(starttfs)
			self.odf72E.move(startcY, rowodf)
			
			# text input
			self.odf73E = QtGui.QLineEdit(self)
			self.odf73E.setText(MagicPanels.unit2gui(0))
			self.odf73E.setFixedWidth(starttfs)
			self.odf73E.move(startcZ, rowodf)
			
			rowodf += 30
			
			# label
			self.odf8L = QtGui.QLabel(translate('magicStart', 'Calculated single beam width:'), self)
			self.odf8L.move(10, rowodf+3)
			
			# text input
			self.odf8E = QtGui.QLineEdit(self)
			self.odf8E.setText(MagicPanels.unit2gui(0))
			self.odf8E.setFixedWidth(rsize2x)
			self.odf8E.move(startcY, rowodf)
			
			rowodf += 30
			
			# label
			self.odf9L = QtGui.QLabel(translate('magicStart', 'Calculated front width:'), self)
			self.odf9L.move(10, rowodf+3)
			
			# text input
			self.odf9E = QtGui.QLineEdit(self)
			self.odf9E.setText(MagicPanels.unit2gui(0))
			self.odf9E.setFixedWidth(rsize2x)
			self.odf9E.move(startcY, rowodf)
			
			rowodf += 30
			
			# label
			self.odf10L = QtGui.QLabel(translate('magicStart', 'Calculated front height:'), self)
			self.odf10L.move(10, rowodf+3)

			# text input
			self.odf10E = QtGui.QLineEdit(self)
			self.odf10E.setText(MagicPanels.unit2gui(0))
			self.odf10E.setFixedWidth(rsize2x)
			self.odf10E.move(startcY, rowodf)
		
			rowodf += 40

			# button
			self.odf11B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.odf11B.clicked.connect(self.createObject)
			self.odf11B.resize(area, createSize)
			self.odf11B.move(10, createRow)

			# hide by default
			self.odf1i.hide()
			self.odf2L.hide()
			self.odf2E.hide()
			self.odf3L.hide()
			self.odf3E.hide()
			self.odf4L.hide()
			self.odf4E.hide()
			self.odf5L.hide()
			self.odf5E.hide()
			self.odf6B.hide()
			self.odf7L.hide()
			self.odf71E.hide()
			self.odf72E.hide()
			self.odf73E.hide()
			self.odf8L.hide()
			self.odf8E.hide()
			self.odf9L.hide()
			self.odf9E.hide()
			self.odf10L.hide()
			self.odf10E.hide()
			self.odf11B.hide()
			
			# ############################################################################
			# GUI for Front decoration (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select face or 4 edges around the front to calculate Front decoration: <br><br> 1. selection - XZ face of front<br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge')
			self.ofdec1i = QtGui.QLabel(info, self)
			self.ofdec1i.move(10, rowfdec+3)
			self.ofdec1i.setFixedWidth(infoarea)
			self.ofdec1i.setWordWrap(True)
			self.ofdec1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowfdec += 170
			
			# label
			self.ofdec2L = QtGui.QLabel(translate('magicStart', 'Single bar width:'), self)
			self.ofdec2L.move(10, rowfdec+3)
			
			# text input
			self.ofdec2E = QtGui.QLineEdit(self)
			self.ofdec2E.setText(MagicPanels.unit2gui(25))
			self.ofdec2E.setFixedWidth(rsize1x)
			self.ofdec2E.move(startcX, rowfdec)
			
			rowfdec += 30
			
			# label
			self.ofdec3L = QtGui.QLabel(translate('magicStart', 'Single bar thickness:'), self)
			self.ofdec3L.move(10, rowfdec+3)

			# text input
			self.ofdec3E = QtGui.QLineEdit(self)
			self.ofdec3E.setText(MagicPanels.unit2gui(20))
			self.ofdec3E.setFixedWidth(rsize1x)
			self.ofdec3E.move(startcX, rowfdec)
		
			rowfdec += 30

			# label
			self.ofdecOHL = QtGui.QLabel(translate('magicStart', 'Offset from edge horizontal:'), self)
			self.ofdecOHL.move(10, rowfdec+3)

			# text input
			self.ofdecOHE = QtGui.QLineEdit(self)
			self.ofdecOHE.setText(MagicPanels.unit2gui(50))
			self.ofdecOHE.setFixedWidth(rsize1x)
			self.ofdecOHE.move(startcY, rowfdec)
			
			rowfdec += 30

			# label
			self.ofdecOVL = QtGui.QLabel(translate('magicStart', 'Offset from edge vertical:'), self)
			self.ofdecOVL.move(10, rowfdec+3)

			# text input
			self.ofdecOVE = QtGui.QLineEdit(self)
			self.ofdecOVE.setText(MagicPanels.unit2gui(50))
			self.ofdecOVE.setFixedWidth(rsize1x)
			self.ofdecOVE.move(startcY, rowfdec)
			
			rowfdec += 40
			
			# button
			self.ofdec5B = QtGui.QPushButton(translate('magicStart', 'calculate front decoration'), self)
			self.ofdec5B.clicked.connect(self.calculateFrontDecoration)
			self.ofdec5B.resize(area, createSize)
			self.ofdec5B.move(10, rowfdec)
			
			rowfdec += 80
			
			# label
			self.ofdec6L = QtGui.QLabel(translate('magicStart', 'Start XYZ:'), self)
			self.ofdec6L.move(10, rowfdec+3)
			
			# text input
			self.ofdec61E = QtGui.QLineEdit(self)
			self.ofdec61E.setText(MagicPanels.unit2gui(0))
			self.ofdec61E.setFixedWidth(starttfs)
			self.ofdec61E.move(startcX, rowfdec)
			
			# text input
			self.ofdec62E = QtGui.QLineEdit(self)
			self.ofdec62E.setText(MagicPanels.unit2gui(0))
			self.ofdec62E.setFixedWidth(starttfs)
			self.ofdec62E.move(startcY, rowfdec)
			
			# text input
			self.ofdec63E = QtGui.QLineEdit(self)
			self.ofdec63E.setText(MagicPanels.unit2gui(0))
			self.ofdec63E.setFixedWidth(starttfs)
			self.ofdec63E.move(startcZ, rowfdec)
			
			rowfdec += 30
			
			# label
			self.ofdec7L = QtGui.QLabel(translate('magicStart', 'Calculated decoration width:'), self)
			self.ofdec7L.move(10, rowfdec+3)
			
			# text input
			self.ofdec7E = QtGui.QLineEdit(self)
			self.ofdec7E.setText(MagicPanels.unit2gui(0))
			self.ofdec7E.setFixedWidth(rsize2x)
			self.ofdec7E.move(startcY, rowfdec)
			
			rowfdec += 30
			
			# label
			self.ofdec8L = QtGui.QLabel(translate('magicStart', 'Calculated decoration height:'), self)
			self.ofdec8L.move(10, rowfdec+3)

			# text input
			self.ofdec8E = QtGui.QLineEdit(self)
			self.ofdec8E.setText(MagicPanels.unit2gui(0))
			self.ofdec8E.setFixedWidth(rsize2x)
			self.ofdec8E.move(startcY, rowfdec)
		
			rowfdec += 40

			# button
			self.ofdec9B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.ofdec9B.clicked.connect(self.createObject)
			self.ofdec9B.resize(area, createSize)
			self.ofdec9B.move(10, createRow)

			# hide by default
			self.ofdec1i.hide()
			self.ofdec2L.hide()
			self.ofdec2E.hide()
			self.ofdec3L.hide()
			self.ofdec3E.hide()
			self.ofdecOHL.hide()
			self.ofdecOHE.hide()
			self.ofdecOVL.hide()
			self.ofdecOVE.hide()
			self.ofdec5B.hide()
			self.ofdec6L.hide()
			self.ofdec61E.hide()
			self.ofdec62E.hide()
			self.ofdec63E.hide()
			self.ofdec7L.hide()
			self.ofdec7E.hide()
			self.ofdec8L.hide()
			self.ofdec8E.hide()
			self.ofdec9B.hide()

			# ############################################################################
			# GUI for Face Frame from GAP (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select 4 edges around the gap to calculate Face Frame: <br><br> 1. selection - X bottom edge <br> 2. selection - X top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge')
			self.offrame1i = QtGui.QLabel(info, self)
			self.offrame1i.move(10, rowfframe+3)
			self.offrame1i.setFixedWidth(infoarea)
			self.offrame1i.setWordWrap(True)
			self.offrame1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowfframe += 120
			
			# label
			self.offrame2L = QtGui.QLabel(translate('magicStart', 'Single bar width:'), self)
			self.offrame2L.move(10, rowfframe+3)
			
			# text input
			self.offrame2E = QtGui.QLineEdit(self)
			self.offrame2E.setText(MagicPanels.unit2gui(38))
			self.offrame2E.setFixedWidth(90)
			self.offrame2E.move(150, rowfframe)
			
			rowfframe += 30
			
			# label
			self.offrame3L = QtGui.QLabel(translate('magicStart', 'Single bar thickness:'), self)
			self.offrame3L.move(10, rowfframe+3)

			# text input
			self.offrame3E = QtGui.QLineEdit(self)
			self.offrame3E.setText(MagicPanels.unit2gui(19))
			self.offrame3E.setFixedWidth(90)
			self.offrame3E.move(150, rowfframe)
		
			rowfframe += 30

			# label
			self.offrame4L = QtGui.QLabel(translate('magicStart', 'Lip outside:'), self)
			self.offrame4L.move(10, rowfframe+3)

			# text input
			self.offrame4E = QtGui.QLineEdit(self)
			self.offrame4E.setText(MagicPanels.unit2gui(0))
			self.offrame4E.setFixedWidth(90)
			self.offrame4E.move(150, rowfframe)
			
			rowfframe += 30
			
			# label
			self.offrame5L = QtGui.QLabel(translate('magicStart', 'Delve into furniture:'), self)
			self.offrame5L.move(10, rowfframe+3)

			# text input
			self.offrame5E = QtGui.QLineEdit(self)
			self.offrame5E.setText(MagicPanels.unit2gui(0))
			self.offrame5E.setFixedWidth(90)
			self.offrame5E.move(150, rowfframe)
			
			rowfframe += 40
			
			# button
			self.offrame6B = QtGui.QPushButton(translate('magicStart', 'calculate Face Frame'), self)
			self.offrame6B.clicked.connect(self.calculateFaceframeFromGap)
			self.offrame6B.resize(area, createSize)
			self.offrame6B.move(10, rowfframe)
			
			rowfframe += 80
			
			# label
			self.offrame7L = QtGui.QLabel(translate('magicStart', 'Frame start XYZ:'), self)
			self.offrame7L.move(10, rowfframe+3)
			
			# text input
			self.offrame71E = QtGui.QLineEdit(self)
			self.offrame71E.setText(MagicPanels.unit2gui(0))
			self.offrame71E.setFixedWidth(starttfs)
			self.offrame71E.move(startcX, rowfframe)
			
			# text input
			self.offrame72E = QtGui.QLineEdit(self)
			self.offrame72E.setText(MagicPanels.unit2gui(0))
			self.offrame72E.setFixedWidth(starttfs)
			self.offrame72E.move(startcY, rowfframe)
			
			# text input
			self.offrame73E = QtGui.QLineEdit(self)
			self.offrame73E.setText(MagicPanels.unit2gui(0))
			self.offrame73E.setFixedWidth(starttfs)
			self.offrame73E.move(startcZ, rowfframe)
			
			rowfframe += 30
			
			# label
			self.offrame8L = QtGui.QLabel(translate('magicStart', 'Calculated Face Frame width:'), self)
			self.offrame8L.move(10, rowfframe+3)
			
			# text input
			self.offrame8E = QtGui.QLineEdit(self)
			self.offrame8E.setText(MagicPanels.unit2gui(0))
			self.offrame8E.setFixedWidth(rsize2x)
			self.offrame8E.move(startcY, rowfframe)
			
			rowfframe += 30
			
			# label
			self.offrame9L = QtGui.QLabel(translate('magicStart', 'Calculated Face Frame height:'), self)
			self.offrame9L.move(10, rowfframe+3)

			# text input
			self.offrame9E = QtGui.QLineEdit(self)
			self.offrame9E.setText(MagicPanels.unit2gui(0))
			self.offrame9E.setFixedWidth(rsize2x)
			self.offrame9E.move(startcY, rowfframe)
		
			rowfframe += 40

			# button
			self.offrame10B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.offrame10B.clicked.connect(self.createObject)
			self.offrame10B.resize(area, createSize)
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
			self.osh1i.setFixedWidth(infoarea)
			self.osh1i.setWordWrap(True)
			self.osh1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowshelf += 150
			
			# label
			self.osh1L = QtGui.QLabel(translate('magicStart', 'Shelf thickness:'), self)
			self.osh1L.move(10, rowshelf+3)

			# text input
			self.osh1E = QtGui.QLineEdit(self)
			self.osh1E.setText(MagicPanels.unit2gui(MagicPanels.gShelfThickness))
			self.osh1E.setFixedWidth(90)
			self.osh1E.move(120, rowshelf)
		
			rowshelf += 30
			
			# label
			self.osh2L = QtGui.QLabel(translate('magicStart', 'Shelf by depth:'), self)
			self.osh2L.move(10, rowshelf+3)

			# text input
			self.osh2E = QtGui.QLineEdit(self)
			self.osh2E.setText(MagicPanels.unit2gui(0))
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
			self.osh31E.setText(MagicPanels.unit2gui(0))
			self.osh31E.setFixedWidth(80)
			self.osh31E.move(10, rowshelf)
			
			# text input
			self.osh32E = QtGui.QLineEdit(self)
			self.osh32E.setText(MagicPanels.unit2gui(0))
			self.osh32E.setFixedWidth(80)
			self.osh32E.move(110, rowshelf)
			
			# text input
			self.osh33E = QtGui.QLineEdit(self)
			self.osh33E.setText(MagicPanels.unit2gui(0))
			self.osh33E.setFixedWidth(80)
			self.osh33E.move(210, rowshelf)
			
			# text input
			self.osh34E = QtGui.QLineEdit(self)
			self.osh34E.setText(MagicPanels.unit2gui(0))
			self.osh34E.setFixedWidth(80)
			self.osh34E.move(310, rowshelf)

			rowshelf += 40
			
			# button
			self.osh4B1 = QtGui.QPushButton(translate('magicStart', 'calculate shelf'), self)
			self.osh4B1.clicked.connect(self.calculateShelfFromGap)
			self.osh4B1.resize(area, createSize)
			self.osh4B1.move(10, rowshelf)
			
			rowshelf += 70
			
			# label
			self.osh5L = QtGui.QLabel(translate('magicStart', 'Shelf start XYZ:'), self)
			self.osh5L.move(10, rowshelf+3)
			
			# text input
			self.osh51E = QtGui.QLineEdit(self)
			self.osh51E.setText(MagicPanels.unit2gui(0))
			self.osh51E.setFixedWidth(starttfs)
			self.osh51E.move(startcX, rowshelf)
			
			# text input
			self.osh52E = QtGui.QLineEdit(self)
			self.osh52E.setText(MagicPanels.unit2gui(0))
			self.osh52E.setFixedWidth(starttfs)
			self.osh52E.move(startcY, rowshelf)
			
			# text input
			self.osh53E = QtGui.QLineEdit(self)
			self.osh53E.setText(MagicPanels.unit2gui(0))
			self.osh53E.setFixedWidth(starttfs)
			self.osh53E.move(startcZ, rowshelf)
			
			rowshelf += 30

			# label
			self.osh6L = QtGui.QLabel(translate('magicStart', 'Calculated shelf width:'), self)
			self.osh6L.move(10, rowshelf+3)
			
			# text input
			self.osh6E = QtGui.QLineEdit(self)
			self.osh6E.setText(MagicPanels.unit2gui(0))
			self.osh6E.setFixedWidth(rsize2x)
			self.osh6E.move(startcY, rowshelf)
			
			rowshelf += 30
			
			# label
			self.osh7L = QtGui.QLabel(translate('magicStart', 'Calculated shelf depth:'), self)
			self.osh7L.move(10, rowshelf+3)

			# text input
			self.osh7E = QtGui.QLineEdit(self)
			self.osh7E.setText(MagicPanels.unit2gui(0))
			self.osh7E.setFixedWidth(rsize2x)
			self.osh7E.move(startcY, rowshelf)
			
			rowshelf += 40

			# button
			self.osh8B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.osh8B1.clicked.connect(self.createObject)
			self.osh8B1.resize(area, createSize)
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
			self.oshs1i.setFixedWidth(infoarea)
			self.oshs1i.setWordWrap(True)
			self.oshs1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowsseries += 150
			
			# label
			self.oshs1L = QtGui.QLabel(translate('magicStart', 'Single shelf thickness:'), self)
			self.oshs1L.move(10, rowsseries+3)

			# text input
			self.oshs1E = QtGui.QLineEdit(self)
			self.oshs1E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
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
			self.oshs3B.resize(area, createSize)
			self.oshs3B.move(10, rowsseries)
			
			rowsseries += 70
			
			# label
			self.oshs4L = QtGui.QLabel(translate('magicStart', 'Shelf start XYZ:'), self)
			self.oshs4L.move(10, rowsseries+3)
			
			# text input
			self.oshs41E = QtGui.QLineEdit(self)
			self.oshs41E.setText(MagicPanels.unit2gui(0))
			self.oshs41E.setFixedWidth(starttfs)
			self.oshs41E.move(startcX, rowsseries)
			
			# text input
			self.oshs42E = QtGui.QLineEdit(self)
			self.oshs42E.setText(MagicPanels.unit2gui(0))
			self.oshs42E.setFixedWidth(starttfs)
			self.oshs42E.move(startcY, rowsseries)
			
			# text input
			self.oshs43E = QtGui.QLineEdit(self)
			self.oshs43E.setText(MagicPanels.unit2gui(0))
			self.oshs43E.setFixedWidth(starttfs)
			self.oshs43E.move(startcZ, rowsseries)
			
			rowsseries += 30

			# label
			self.oshs5L = QtGui.QLabel(translate('magicStart', 'Calculated shelf width:'), self)
			self.oshs5L.move(10, rowsseries+3)
			
			# text input
			self.oshs5E = QtGui.QLineEdit(self)
			self.oshs5E.setText(MagicPanels.unit2gui(0))
			self.oshs5E.setFixedWidth(rsize2x)
			self.oshs5E.move(startcY, rowsseries)
			
			rowsseries += 30
			
			# label
			self.oshs6L = QtGui.QLabel(translate('magicStart', 'Calculated shelf depth:'), self)
			self.oshs6L.move(10, rowsseries+3)

			# text input
			self.oshs6E = QtGui.QLineEdit(self)
			self.oshs6E.setText(MagicPanels.unit2gui(0))
			self.oshs6E.setFixedWidth(rsize2x)
			self.oshs6E.move(startcY, rowsseries)
			
			rowsseries += 30

			# label
			self.oshs7L = QtGui.QLabel(translate('magicStart', 'Calculated shelves space:'), self)
			self.oshs7L.move(10, rowsseries+3)
			
			# text input
			self.oshs7E = QtGui.QLineEdit(self)
			self.oshs7E.setText(MagicPanels.unit2gui(0))
			self.oshs7E.setFixedWidth(rsize2x)
			self.oshs7E.move(startcY, rowsseries)
			
			rowsseries += 40

			# button
			self.oshs8B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.oshs8B.clicked.connect(self.createObject)
			self.oshs8B.resize(area, createSize)
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
			self.oside1i.setFixedWidth(infoarea)
			self.oside1i.setWordWrap(True)
			self.oside1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowside += 120
			
			# label
			self.oside1L = QtGui.QLabel(translate('magicStart', 'Side thickness:'), self)
			self.oside1L.move(10, rowside+3)

			# text input
			self.oside1E = QtGui.QLineEdit(self)
			self.oside1E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			self.oside1E.setFixedWidth(90)
			self.oside1E.move(120, rowside)
		
			rowside += 30
			
			# label
			self.oside2L = QtGui.QLabel(translate('magicStart', 'Side by width:'), self)
			self.oside2L.move(10, rowside+3)

			# text input
			self.oside2E = QtGui.QLineEdit(self)
			self.oside2E.setText(MagicPanels.unit2gui(0))
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
			self.oside31E.setText(MagicPanels.unit2gui(0))
			self.oside31E.setFixedWidth(80)
			self.oside31E.move(10, rowside)
			
			# text input
			self.oside32E = QtGui.QLineEdit(self)
			self.oside32E.setText(MagicPanels.unit2gui(0))
			self.oside32E.setFixedWidth(80)
			self.oside32E.move(110, rowside)
			
			# text input
			self.oside33E = QtGui.QLineEdit(self)
			self.oside33E.setText(MagicPanels.unit2gui(0))
			self.oside33E.setFixedWidth(80)
			self.oside33E.move(210, rowside)
			
			# text input
			self.oside34E = QtGui.QLineEdit(self)
			self.oside34E.setText(MagicPanels.unit2gui(0))
			self.oside34E.setFixedWidth(80)
			self.oside34E.move(310, rowside)

			rowside += 40
			
			# button
			self.oside4B1 = QtGui.QPushButton(translate('magicStart', 'calculate side'), self)
			self.oside4B1.clicked.connect(self.calculateSideFromGap)
			self.oside4B1.resize(area, createSize)
			self.oside4B1.move(10, rowside)
			
			rowside += 70
			
			# label
			self.oside5L = QtGui.QLabel(translate('magicStart', 'Side start XYZ:'), self)
			self.oside5L.move(10, rowside+3)
			
			# text input
			self.oside51E = QtGui.QLineEdit(self)
			self.oside51E.setText(MagicPanels.unit2gui(0))
			self.oside51E.setFixedWidth(starttfs)
			self.oside51E.move(startcX, rowside)
			
			# text input
			self.oside52E = QtGui.QLineEdit(self)
			self.oside52E.setText(MagicPanels.unit2gui(0))
			self.oside52E.setFixedWidth(starttfs)
			self.oside52E.move(startcY, rowside)
			
			# text input
			self.oside53E = QtGui.QLineEdit(self)
			self.oside53E.setText(MagicPanels.unit2gui(0))
			self.oside53E.setFixedWidth(starttfs)
			self.oside53E.move(startcZ, rowside)
			
			rowside += 30

			# label
			self.oside6L = QtGui.QLabel(translate('magicStart', 'Calculated side width:'), self)
			self.oside6L.move(10, rowside+3)
			
			# text input
			self.oside6E = QtGui.QLineEdit(self)
			self.oside6E.setText(MagicPanels.unit2gui(0))
			self.oside6E.setFixedWidth(rsize2x)
			self.oside6E.move(startcY, rowside)
			
			rowside += 30
			
			# label
			self.oside7L = QtGui.QLabel(translate('magicStart', 'Calculated side height:'), self)
			self.oside7L.move(10, rowside+3)

			# text input
			self.oside7E = QtGui.QLineEdit(self)
			self.oside7E.setText(MagicPanels.unit2gui(0))
			self.oside7E.setFixedWidth(rsize2x)
			self.oside7E.move(startcY, rowside)
			
			rowside += 40

			# button
			self.oside8B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.oside8B1.clicked.connect(self.createObject)
			self.oside8B1.resize(area, createSize)
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
			self.ocs1i.setFixedWidth(infoarea)
			self.ocs1i.setWordWrap(True)
			self.ocs1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowcside += 150
			
			# label
			self.ocs1L = QtGui.QLabel(translate('magicStart', 'Side thickness:'), self)
			self.ocs1L.move(10, rowcside+3)

			# text input
			self.ocs1E = QtGui.QLineEdit(self)
			self.ocs1E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			self.ocs1E.setFixedWidth(90)
			self.ocs1E.move(120, rowcside)
		
			rowcside += 30
			
			# label
			self.ocs2L = QtGui.QLabel(translate('magicStart', 'Side by depth:'), self)
			self.ocs2L.move(10, rowcside+3)

			# text input
			self.ocs2E = QtGui.QLineEdit(self)
			self.ocs2E.setText(MagicPanels.unit2gui(0))
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
			self.ocs31E.setText(MagicPanels.unit2gui(0))
			self.ocs31E.setFixedWidth(80)
			self.ocs31E.move(10, rowcside)
			
			# text input
			self.ocs32E = QtGui.QLineEdit(self)
			self.ocs32E.setText(MagicPanels.unit2gui(0))
			self.ocs32E.setFixedWidth(80)
			self.ocs32E.move(110, rowcside)
			
			# text input
			self.ocs33E = QtGui.QLineEdit(self)
			self.ocs33E.setText(MagicPanels.unit2gui(0))
			self.ocs33E.setFixedWidth(80)
			self.ocs33E.move(210, rowcside)
			
			# text input
			self.ocs34E = QtGui.QLineEdit(self)
			self.ocs34E.setText(MagicPanels.unit2gui(0))
			self.ocs34E.setFixedWidth(80)
			self.ocs34E.move(310, rowcside)

			rowcside += 40
			
			# button
			self.ocs4B1 = QtGui.QPushButton(translate('magicStart', 'calculate center side'), self)
			self.ocs4B1.clicked.connect(self.calculateCenterSideFromGap)
			self.ocs4B1.resize(area, createSize)
			self.ocs4B1.move(10, rowcside)
			
			rowcside += 70
			
			# label
			self.ocs5L = QtGui.QLabel(translate('magicStart', 'Side start XYZ:'), self)
			self.ocs5L.move(10, rowcside+3)
			
			# text input
			self.ocs51E = QtGui.QLineEdit(self)
			self.ocs51E.setText(MagicPanels.unit2gui(0))
			self.ocs51E.setFixedWidth(starttfs)
			self.ocs51E.move(startcX, rowcside)
			
			# text input
			self.ocs52E = QtGui.QLineEdit(self)
			self.ocs52E.setText(MagicPanels.unit2gui(0))
			self.ocs52E.setFixedWidth(starttfs)
			self.ocs52E.move(startcY, rowcside)
			
			# text input
			self.ocs53E = QtGui.QLineEdit(self)
			self.ocs53E.setText(MagicPanels.unit2gui(0))
			self.ocs53E.setFixedWidth(starttfs)
			self.ocs53E.move(startcZ, rowcside)
			
			rowcside += 30

			# label
			self.ocs6L = QtGui.QLabel(translate('magicStart', 'Calculated center side height:'), self)
			self.ocs6L.move(10, rowcside+3)
			
			# text input
			self.ocs6E = QtGui.QLineEdit(self)
			self.ocs6E.setText(MagicPanels.unit2gui(0))
			self.ocs6E.setFixedWidth(rsize2x)
			self.ocs6E.move(startcY, rowcside)
			
			rowcside += 30
			
			# label
			self.ocs7L = QtGui.QLabel(translate('magicStart', 'Calculated center side depth:'), self)
			self.ocs7L.move(10, rowcside+3)

			# text input
			self.ocs7E = QtGui.QLineEdit(self)
			self.ocs7E.setText(MagicPanels.unit2gui(0))
			self.ocs7E.setFixedWidth(rsize2x)
			self.ocs7E.move(startcY, rowcside)
			
			rowcside += 40

			# button
			self.ocs8B1 = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.ocs8B1.clicked.connect(self.createObject)
			self.ocs8B1.resize(area, createSize)
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
			# GUI for Side decoration (hidden by default)
			# ############################################################################

			# label
			info = translate('magicStart', 'Please select face or 4 edges around the side to calculate Side decoration: <br><br> 1. selection - YZ face of side <br><br> 1. selection - Y bottom edge <br> 2. selection - Y top edge <br> 3. selection - Z left edge <br> 4. selection - Z right edge')
			self.osdec1i = QtGui.QLabel(info, self)
			self.osdec1i.move(10, rowsdec+3)
			self.osdec1i.setFixedWidth(infoarea)
			self.osdec1i.setWordWrap(True)
			self.osdec1i.setTextFormat(QtCore.Qt.TextFormat.RichText)
			
			rowsdec += 170
			
			# label
			self.osdec2L = QtGui.QLabel(translate('magicStart', 'Single bar width:'), self)
			self.osdec2L.move(10, rowsdec+3)
			
			# text input
			self.osdec2E = QtGui.QLineEdit(self)
			self.osdec2E.setText(MagicPanels.unit2gui(25))
			self.osdec2E.setFixedWidth(rsize1x)
			self.osdec2E.move(startcX, rowsdec)
			
			rowsdec += 30
			
			# label
			self.osdec3L = QtGui.QLabel(translate('magicStart', 'Single bar thickness:'), self)
			self.osdec3L.move(10, rowsdec+3)

			# text input
			self.osdec3E = QtGui.QLineEdit(self)
			self.osdec3E.setText(MagicPanels.unit2gui(20))
			self.osdec3E.setFixedWidth(rsize1x)
			self.osdec3E.move(startcX, rowsdec)
		
			rowsdec += 30

			# label
			self.osdecOHL = QtGui.QLabel(translate('magicStart', 'Offset from edge horizontal:'), self)
			self.osdecOHL.move(10, rowsdec+3)

			# text input
			self.osdecOHE = QtGui.QLineEdit(self)
			self.osdecOHE.setText(MagicPanels.unit2gui(50))
			self.osdecOHE.setFixedWidth(rsize1x)
			self.osdecOHE.move(startcY, rowsdec)
			
			rowsdec += 30

			# label
			self.osdecOVL = QtGui.QLabel(translate('magicStart', 'Offset from edge vertical:'), self)
			self.osdecOVL.move(10, rowsdec+3)

			# text input
			self.osdecOVE = QtGui.QLineEdit(self)
			self.osdecOVE.setText(MagicPanels.unit2gui(50))
			self.osdecOVE.setFixedWidth(rsize1x)
			self.osdecOVE.move(startcY, rowsdec)
			
			rowsdec += 40
			
			# button
			self.osdec5B = QtGui.QPushButton(translate('magicStart', 'calculate side decoration'), self)
			self.osdec5B.clicked.connect(self.calculateSideDecoration)
			self.osdec5B.resize(area, createSize)
			self.osdec5B.move(10, rowsdec)
			
			rowsdec += 80
			
			# label
			self.osdec6L = QtGui.QLabel(translate('magicStart', 'Start XYZ:'), self)
			self.osdec6L.move(10, rowsdec+3)
			
			# text input
			self.osdec61E = QtGui.QLineEdit(self)
			self.osdec61E.setText(MagicPanels.unit2gui(0))
			self.osdec61E.setFixedWidth(starttfs)
			self.osdec61E.move(startcX, rowsdec)
			
			# text input
			self.osdec62E = QtGui.QLineEdit(self)
			self.osdec62E.setText(MagicPanels.unit2gui(0))
			self.osdec62E.setFixedWidth(starttfs)
			self.osdec62E.move(startcY, rowsdec)
			
			# text input
			self.osdec63E = QtGui.QLineEdit(self)
			self.osdec63E.setText(MagicPanels.unit2gui(0))
			self.osdec63E.setFixedWidth(starttfs)
			self.osdec63E.move(startcZ, rowsdec)
			
			rowsdec += 30
			
			# label
			self.osdec7L = QtGui.QLabel(translate('magicStart', 'Calculated decoration width:'), self)
			self.osdec7L.move(10, rowsdec+3)
			
			# text input
			self.osdec7E = QtGui.QLineEdit(self)
			self.osdec7E.setText(MagicPanels.unit2gui(0))
			self.osdec7E.setFixedWidth(rsize2x)
			self.osdec7E.move(startcY, rowsdec)
			
			rowsdec += 30
			
			# label
			self.osdec8L = QtGui.QLabel(translate('magicStart', 'Calculated decoration height:'), self)
			self.osdec8L.move(10, rowsdec+3)

			# text input
			self.osdec8E = QtGui.QLineEdit(self)
			self.osdec8E.setText(MagicPanels.unit2gui(0))
			self.osdec8E.setFixedWidth(rsize2x)
			self.osdec8E.move(startcY, rowsdec)
		
			rowsdec += 40

			# button
			self.osdec9B = QtGui.QPushButton(translate('magicStart', 'create'), self)
			self.osdec9B.clicked.connect(self.createObject)
			self.osdec9B.resize(area, createSize)
			self.osdec9B.move(10, createRow)

			# hide by default
			self.osdec1i.hide()
			self.osdec2L.hide()
			self.osdec2E.hide()
			self.osdec3L.hide()
			self.osdec3E.hide()
			self.osdecOHL.hide()
			self.osdecOHE.hide()
			self.osdecOVL.hide()
			self.osdecOVE.hide()
			self.osdec5B.hide()
			self.osdec6L.hide()
			self.osdec61E.hide()
			self.osdec62E.hide()
			self.osdec63E.hide()
			self.osdec7L.hide()
			self.osdec7E.hide()
			self.osdec8L.hide()
			self.osdec8E.hide()
			self.osdec9B.hide()
			
			# ############################################################################
			# show & init defaults
			# ############################################################################

			# show window
			self.show()

			# set theme
			QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
			self.setStyleSheet(QtCSS)
		
		# ############################################################################
		# actions - GUI
		# ############################################################################

		# ############################################################################
		def setGUIInfo(self, iType="furniture"):

			# ##############################################
			# hide everything first
			# ##############################################
			
			# workspace
			self.oworkspaceInfo.hide()
			self.oworkspaceXL.hide()
			self.oworkspaceXE.hide()
			self.oworkspaceYL.hide()
			self.oworkspaceYE.hide()
			self.oworkspaceZL.hide()
			self.oworkspaceZE.hide()
			self.oworkspaceBCL.hide()
			self.oworkspaceSL.hide()
			self.oworkspaceSXE.hide()
			self.oworkspaceSYE.hide()
			self.oworkspaceSZE.hide()
			self.oworkspaceBCR.hide()
			
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
			
			# side decoration
			self.osdec1i.hide()
			self.osdec2L.hide()
			self.osdec2E.hide()
			self.osdec3L.hide()
			self.osdec3E.hide()
			self.osdecOHL.hide()
			self.osdecOHE.hide()
			self.osdecOVL.hide()
			self.osdecOVE.hide()
			self.osdec5B.hide()
			self.osdec6L.hide()
			self.osdec61E.hide()
			self.osdec62E.hide()
			self.osdec63E.hide()
			self.osdec7L.hide()
			self.osdec7E.hide()
			self.osdec8L.hide()
			self.osdec8E.hide()
			self.osdec9B.hide()
			
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
		
			# back
			self.oBackInfo.hide()
			self.oBackThickL.hide()
			self.oBackThickE.hide()
			self.oBackOffsetsL.hide()
			self.oBackOffsets1L.hide()
			self.oBackOffsets2L.hide()
			self.oBackOffsets3L.hide()
			self.oBackOffsets4L.hide()
			self.oBackOffsets1E.hide()
			self.oBackOffsets2E.hide()
			self.oBackOffsets3E.hide()
			self.oBackOffsets4E.hide()
			self.oBackBCL.hide()
			self.oBackStartL.hide()
			self.oBackSXE.hide()
			self.oBackSYE.hide()
			self.oBackSZE.hide()
			self.oBackSizeXL.hide()
			self.oBackSizeXE.hide()
			self.oBackSizeYL.hide()
			self.oBackSizeYE.hide()
			self.oBackBCR.hide()
		
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
		
			# decorative front
			self.odf1i.hide()
			self.odf2L.hide()
			self.odf2E.hide()
			self.odf3L.hide()
			self.odf3E.hide()
			self.odf4L.hide()
			self.odf4E.hide()
			self.odf5L.hide()
			self.odf5E.hide()
			self.odf6B.hide()
			self.odf7L.hide()
			self.odf71E.hide()
			self.odf72E.hide()
			self.odf73E.hide()
			self.odf8L.hide()
			self.odf8E.hide()
			self.odf9L.hide()
			self.odf9E.hide()
			self.odf10L.hide()
			self.odf10E.hide()
			self.odf11B.hide()
		
			# front decoration
			self.ofdec1i.hide()
			self.ofdec2L.hide()
			self.ofdec2E.hide()
			self.ofdec3L.hide()
			self.ofdec3E.hide()
			self.ofdecOHL.hide()
			self.ofdecOHE.hide()
			self.ofdecOVL.hide()
			self.ofdecOVE.hide()
			self.ofdec5B.hide()
			self.ofdec6L.hide()
			self.ofdec61E.hide()
			self.ofdec62E.hide()
			self.ofdec63E.hide()
			self.ofdec7L.hide()
			self.ofdec7E.hide()
			self.ofdec8L.hide()
			self.ofdec8E.hide()
			self.ofdec9B.hide()
		
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
			self.og81L.hide()
			self.og82L.hide()
			self.og83L.hide()
			self.og81E.hide()
			self.og82E.hide()
			self.og83E.hide()
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
			self.og10L.hide()
			self.og101L.hide()
			self.og102L.hide()
			self.og101E.hide()
			self.og102E.hide()
		
			# drawer series
			self.ods1i.hide()
			self.ods2L.hide()
			self.ods2E.hide()
			self.ods3L.hide()
			self.ods31L.hide()
			self.ods32L.hide()
			self.ods33L.hide()
			self.ods31E.hide()
			self.ods32E.hide()
			self.ods33E.hide()
			self.ods4L.hide()
			self.ods41L.hide()
			self.ods42L.hide()
			self.ods43L.hide()
			self.ods44L.hide()
			self.ods45L.hide()
			self.ods41E.hide()
			self.ods42E.hide()
			self.ods43E.hide()
			self.ods44E.hide()
			self.ods45E.hide()
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
			self.ods11L.hide()
			self.ods111L.hide()
			self.ods112L.hide()
			self.ods113L.hide()
			self.ods111E.hide()
			self.ods112E.hide()
			self.ods113E.hide()
		
			# foot
			self.oFootInfo.hide()
			self.oFootThickL.hide()
			self.oFootThickE.hide()
			self.oFootSizeZL.hide()
			self.oFootSizeZE.hide()
			self.oFootCalculateB.hide()
			self.oFootStartL.hide()
			self.oFootStartXE.hide()
			self.oFootStartYE.hide()
			self.oFootStartZE.hide()
			self.oFootSizeXL.hide()
			self.oFootSizeXE.hide()
			self.oFootSizeYL.hide()
			self.oFootSizeYE.hide()
			self.oFootCreateB.hide()
			
			# table
			self.oTableInfo.hide()
			self.oTableSizeXL.hide()
			self.oTableSizeXE.hide()
			self.oTableSizeYL.hide()
			self.oTableSizeYE.hide()
			self.oTableSizeZL.hide()
			self.oTableSizeZE.hide()
			self.oTableTopThickL.hide()
			self.oTableTopThickE.hide()
			self.oTableLegThickL.hide()
			self.oTableLegThickE.hide()
			self.oTableTopOffsetL.hide()
			self.oTableTopOffsetE.hide()
			self.oTableCalculateB.hide()
			self.oTableStartInfoL.hide()
			self.oTableStartXE.hide()
			self.oTableStartYE.hide()
			self.oTableStartZE.hide()
			self.oTableCreateB.hide()

			# merge
			self.minfo.hide()
			self.mergeB.hide()
			
			# furniture (default)
			self.oThickL.hide()
			self.oThickE.hide()
			self.oThickBackL.hide()
			self.oThickBackE.hide()
			self.oThickShelfL.hide()
			self.oThickShelfE.hide()
			self.oThickFrontL.hide()
			self.oThickFrontE.hide()
			self.oOffsetFrontLL.hide()
			self.oOffsetFrontLE.hide()
			self.oOffsetFrontRL.hide()
			self.oOffsetFrontRE.hide()
			self.oOffsetFrontTL.hide()
			self.oOffsetFrontTE.hide()
			self.oOffsetFrontBL.hide()
			self.oOffsetFrontBE.hide()
			self.oModulesNumL.hide()
			self.oModulesNumE.hide()
			self.oSelectionOffsetL.hide()
			self.oSelectionOffset1E.hide()
			self.oSelectionOffset2E.hide()
			self.oSelectionOffset3E.hide()
			self.oHeightL.hide()
			self.oHeightE.hide()
			self.oCalculateB1.hide()
			self.oStartXYZL.hide()
			self.oStartXE.hide()
			self.oStartYE.hide()
			self.oStartZE.hide()
			self.oWidthL.hide()
			self.oWidthE.hide()
			self.oDepthL.hide()
			self.oDepthE.hide()
			self.oCreateB1.hide()
			
			# ##############################################
			# show only needed
			# ##############################################
			
			if iType == "workspace":
				self.oworkspaceInfo.show()
				self.oworkspaceXL.show()
				self.oworkspaceXE.show()
				self.oworkspaceYL.show()
				self.oworkspaceYE.show()
				self.oworkspaceZL.show()
				self.oworkspaceZE.show()
				self.oworkspaceBCL.show()
				self.oworkspaceSL.show()
				self.oworkspaceSXE.show()
				self.oworkspaceSYE.show()
				self.oworkspaceSZE.show()
				self.oworkspaceBCR.show()

			if iType == "furniture":
				self.oThickL.show()
				self.oThickE.show()
				self.oThickBackL.show()
				self.oThickBackE.show()
				self.oThickShelfL.show()
				self.oThickShelfE.show()
				self.oThickFrontL.show()
				self.oThickFrontE.show()
				self.oOffsetFrontLL.hide()
				self.oOffsetFrontLE.hide()
				self.oOffsetFrontRL.hide()
				self.oOffsetFrontRE.hide()
				self.oOffsetFrontTL.hide()
				self.oOffsetFrontTE.hide()
				self.oOffsetFrontBL.hide()
				self.oOffsetFrontBE.hide()
				self.oModulesNumL.hide()
				self.oModulesNumE.hide()
				self.oSelectionOffsetL.show()
				self.oSelectionOffset1E.show()
				self.oSelectionOffset2E.show()
				self.oSelectionOffset3E.show()
				self.oHeightL.show()
				self.oHeightE.show()
				self.oCalculateB1.show()
				self.oStartXYZL.show()
				self.oStartXE.show()
				self.oStartYE.show()
				self.oStartZE.show()
				self.oWidthL.show()
				self.oWidthE.show()
				self.oDepthL.show()
				self.oDepthE.show()
				self.oCreateB1.show()
				
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

			if iType == "side decoration":
				self.osdec1i.show()
				self.osdec2L.show()
				self.osdec2E.show()
				self.osdec3L.show()
				self.osdec3E.show()
				self.osdecOHL.show()
				self.osdecOHE.show()
				self.osdecOVL.show()
				self.osdecOVE.show()
				self.osdec5B.show()
				self.osdec6L.show()
				self.osdec61E.show()
				self.osdec62E.show()
				self.osdec63E.show()
				self.osdec7L.show()
				self.osdec7E.show()
				self.osdec8L.show()
				self.osdec8E.show()
				self.osdec9B.show()

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
			
			if iType == "back":
				self.oBackInfo.show()
				self.oBackThickL.show()
				self.oBackThickE.show()
				self.oBackOffsetsL.show()
				self.oBackOffsets1L.show()
				self.oBackOffsets2L.show()
				self.oBackOffsets3L.show()
				self.oBackOffsets4L.show()
				self.oBackOffsets1E.show()
				self.oBackOffsets2E.show()
				self.oBackOffsets3E.show()
				self.oBackOffsets4E.show()
				self.oBackBCL.show()
				self.oBackStartL.show()
				self.oBackSXE.show()
				self.oBackSYE.show()
				self.oBackSZE.show()
				self.oBackSizeXL.show()
				self.oBackSizeXE.show()
				self.oBackSizeYL.show()
				self.oBackSizeYE.show()
				self.oBackBCR.show()
			
			if iType == "decorative front":
				self.odf1i.show()
				self.odf2L.show()
				self.odf2E.show()
				self.odf3L.show()
				self.odf3E.show()
				self.odf4L.show()
				self.odf4E.show()
				self.odf5L.show()
				self.odf5E.show()
				self.odf6B.show()
				self.odf7L.show()
				self.odf71E.show()
				self.odf72E.show()
				self.odf73E.show()
				self.odf8L.show()
				self.odf8E.show()
				self.odf9L.show()
				self.odf9E.show()
				self.odf10L.show()
				self.odf10E.show()
				self.odf11B.show()
			
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
			
			if iType == "front decoration":
				self.ofdec1i.show()
				self.ofdec2L.show()
				self.ofdec2E.show()
				self.ofdec3L.show()
				self.ofdec3E.show()
				self.ofdecOHL.show()
				self.ofdecOHE.show()
				self.ofdecOVL.show()
				self.ofdecOVE.show()
				self.ofdec5B.show()
				self.ofdec6L.show()
				self.ofdec61E.show()
				self.ofdec62E.show()
				self.ofdec63E.show()
				self.ofdec7L.show()
				self.ofdec7E.show()
				self.ofdec8L.show()
				self.ofdec8E.show()
				self.ofdec9B.show()
			
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
				self.og81L.show()
				self.og82L.show()
				self.og83L.show()
				self.og81E.show()
				self.og82E.show()
				self.og83E.show()
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
				self.og10L.show()
				self.og101L.show()
				self.og102L.show()
				self.og101E.show()
				self.og102E.show()

			if iType == "drawer hafele":
				self.ods1i.show()
				self.ods2L.show()
				self.ods2E.show()
				self.ods3L.show()
				self.ods31L.show()
				self.ods32L.show()
				self.ods33L.show()
				self.ods31E.show()
				self.ods32E.show()
				self.ods33E.show()
				self.ods4L.show()
				self.ods41L.show()
				self.ods42L.show()
				self.ods43L.show()
				self.ods44L.show()
				self.ods45L.show()
				self.ods41E.show()
				self.ods42E.show()
				self.ods43E.show()
				self.ods44E.show()
				self.ods45E.show()
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
				self.ods11L.show()
				self.ods111L.show()
				self.ods112L.show()
				self.ods113L.show()
				self.ods111E.show()
				self.ods112E.show()
				self.ods113E.show()

			if iType == "drawer series":
				self.ods1i.show()
				self.ods2L.show()
				self.ods2E.show()
				self.ods3L.show()
				self.ods31L.show()
				self.ods32L.show()
				self.ods33L.show()
				self.ods31E.show()
				self.ods32E.show()
				self.ods33E.show()
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
				self.ods11L.show()
				self.ods111L.show()
				self.ods112L.show()
				self.ods113L.show()
				self.ods111E.show()
				self.ods112E.show()
				self.ods113E.show()

			if iType == "foot":
				self.oFootInfo.show()
				self.oFootThickL.show()
				self.oFootThickE.show()
				self.oFootSizeZL.show()
				self.oFootSizeZE.show()
				self.oFootCalculateB.show()
				self.oFootStartL.show()
				self.oFootStartXE.show()
				self.oFootStartYE.show()
				self.oFootStartZE.show()
				self.oFootSizeXL.show()
				self.oFootSizeXE.show()
				self.oFootSizeYL.show()
				self.oFootSizeYE.show()
				self.oFootCreateB.show()
		
			if iType == "table":
				self.oTableInfo.show()
				self.oTableSizeXL.show()
				self.oTableSizeXE.show()
				self.oTableSizeYL.show()
				self.oTableSizeYE.show()
				self.oTableSizeZL.show()
				self.oTableSizeZE.show()
				self.oTableTopThickL.show()
				self.oTableTopThickE.show()
				self.oTableLegThickL.show()
				self.oTableLegThickE.show()
				self.oTableTopOffsetL.show()
				self.oTableTopOffsetE.show()
				self.oTableCalculateB.show()
				self.oTableStartInfoL.show()
				self.oTableStartXE.show()
				self.oTableStartYE.show()
				self.oTableStartZE.show()
				self.oTableCreateB.show()

			if iType == "merge":
				self.minfo.show()
				self.mergeB.show()

		# ############################################################################	
		def selectedOption(self, selectedText):
			
			# the key is from translation so this needs to be tested...
			selectedIndex = getMenuIndex[selectedText]
			self.gSelectedFurniture = "F"+str(selectedIndex)
			
			# ##########################################################################
			# set icon
			# ##########################################################################
			
			if selectedIndex < 10:
				self.setIcon("msf00"+str(selectedIndex))
			if selectedIndex >= 10 and selectedIndex < 100:
				self.setIcon("msf0"+str(selectedIndex))
			if selectedIndex >= 100:
				self.setIcon("msf"+str(selectedIndex))
			
			# ##########################################################################
			# set GUI and help info
			# ##########################################################################

			if selectedIndex == -1:
				self.setGUIInfo("empty")
				self.helpInfo.setText("")
				self.setIcon("empty")
			
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
				selectedIndex == 15 or 
				selectedIndex == 49 or 
				selectedIndex == 50 or 
				selectedIndex == 51 or 
				selectedIndex == 52 or 
				selectedIndex == 53 or 
				selectedIndex == 54 or 
				selectedIndex == 55 or 
				selectedIndex == 56 or 
				selectedIndex == 57 or 
				selectedIndex == 58 or 
				selectedIndex == 63 or 
				selectedIndex == 68 or 
				selectedIndex == 69 or 
				selectedIndex == 70 or 
				selectedIndex == 76 or 
				selectedIndex == 77 or 
				selectedIndex == 83
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
				selectedIndex == 36 or 
				selectedIndex == 65 or 
				selectedIndex == 66 or 
				selectedIndex == 67 or 
				selectedIndex == 78 or 
				selectedIndex == 79 or 
				selectedIndex == 84 or 
				selectedIndex == 85 or 
				selectedIndex == 86 or 
				selectedIndex == 87 or 
				selectedIndex == 88 or 
				selectedIndex == 89
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
			
			if selectedIndex == 32 or selectedIndex == 33 or selectedIndex == 34 or selectedIndex == 64:
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
				selectedIndex == 47 or 
				selectedIndex == 80 or 
				selectedIndex == 81 or 
				selectedIndex == 82
				):
				self.setGUIInfo("table")
				self.helpInfo.setText(self.gHelpInfoF42)
			
			if selectedIndex == 48:
				self.setGUIInfo("side")
				self.helpInfo.setText(self.gHelpInfoF48)

			if selectedIndex == 59 or selectedIndex == 60:
				self.setGUIInfo("decorative front")
				self.helpInfo.setText(self.gHelpInfoF59)

			if selectedIndex == 61:
				self.setGUIInfo("front decoration")
				self.helpInfo.setText(self.gHelpInfoF61)
			
			if selectedIndex == 62:
				self.setGUIInfo("side decoration")
				self.helpInfo.setText(self.gHelpInfoF62)
			
			if selectedIndex == 71 or selectedIndex == 72:
				self.setGUIInfo("drawer hafele")
				self.helpInfo.setText(self.gHelpInfoF30)
			
			if selectedIndex == 73:
				self.setGUIInfo("workspace")
				self.helpInfo.setText(self.gHelpInfoF73)
			
			if selectedIndex == 74 or selectedIndex == 75:
				self.setGUIInfo("back")
				self.helpInfo.setText(self.gHelpInfoF74)

			# ##########################################################################
			# show and hide GUI elements
			# ##########################################################################
			
			# set defaults for furniture
			if (
				selectedIndex == 0 or 
				selectedIndex == 1 or 
				selectedIndex == 10 or
				selectedIndex == 27 or 
				selectedIndex == 28 or 
				selectedIndex == 29 or 
				selectedIndex == 35 or 
				selectedIndex == 36 or 
				selectedIndex == 65 or 
				selectedIndex == 66 or 
				selectedIndex == 67 or 
				selectedIndex == 78 or 
				selectedIndex == 79 or 
				selectedIndex == 84 or 
				selectedIndex == 85 or 
				selectedIndex == 86 or 
				selectedIndex == 87 or 
				selectedIndex == 88 or 
				selectedIndex == 89 
				):
				self.oThickL.show()
				self.oThickE.show()
				self.oThickBackL.show()
				self.oThickBackE.show()
				self.oThickShelfL.show()
				self.oThickShelfE.show()
				self.oThickFrontL.show()
				self.oThickFrontE.show()
				self.oOffsetFrontLL.show()
				self.oOffsetFrontLE.show()
				self.oOffsetFrontRL.show()
				self.oOffsetFrontRE.show()
				self.oOffsetFrontTL.show()
				self.oOffsetFrontTE.show()
				self.oOffsetFrontBL.show()
				self.oOffsetFrontBE.show()
				self.oModulesNumL.hide()
				self.oModulesNumE.hide()
				self.oHeightE.show()
				self.oWidthE.show()
				self.oDepthE.show()
			
			# furniture without fronts
			if (
				selectedIndex == 1 or 
				selectedIndex == 35 or 
				selectedIndex == 36 or 
				selectedIndex == 78 or 
				selectedIndex == 79 or 
				selectedIndex == 86 or 
				selectedIndex == 87 or 
				selectedIndex == 88 or 
				selectedIndex == 89 
				):
				self.oThickFrontL.hide()
				self.oThickFrontE.hide()
				self.oOffsetFrontLL.hide()
				self.oOffsetFrontLE.hide()
				self.oOffsetFrontRL.hide()
				self.oOffsetFrontRE.hide()
				self.oOffsetFrontTL.hide()
				self.oOffsetFrontTE.hide()
				self.oOffsetFrontBL.hide()
				self.oOffsetFrontBE.hide()
			
			# furniture with face frame
			if (
				selectedIndex == 35 or 
				selectedIndex == 36
				):
				self.oThickBackL.hide()
				self.oThickBackE.hide()
				self.oThickShelfL.hide()
				self.oThickShelfE.hide()
			
			if selectedIndex == 65:
				self.oThickShelfL.hide()
				self.oThickShelfE.hide()
				self.oThickFrontL.hide()
				self.oThickFrontE.hide()
				self.oOffsetFrontLL.hide()
				self.oOffsetFrontLE.hide()
				self.oOffsetFrontRL.hide()
				self.oOffsetFrontRE.hide()
				self.oOffsetFrontTL.hide()
				self.oOffsetFrontTE.hide()
				self.oOffsetFrontBL.hide()
				self.oOffsetFrontBE.hide()

			if selectedIndex == 67:
				self.oThickFrontL.hide()
				self.oThickFrontE.hide()
				self.oOffsetFrontLL.hide()
				self.oOffsetFrontLE.hide()
				self.oOffsetFrontRL.hide()
				self.oOffsetFrontRE.hide()
				self.oOffsetFrontTL.hide()
				self.oOffsetFrontTE.hide()
				self.oOffsetFrontBL.hide()
				self.oOffsetFrontBE.hide()
			
			# modular furniture
			if (
				selectedIndex == 10 or 
				selectedIndex == 78 or 
				selectedIndex == 79 or 
				selectedIndex == 84 or 
				selectedIndex == 85 
				):
				self.oModulesNumL.show()
				self.oModulesNumE.show()
			
			# ##########################################################################
			# custom values
			# ##########################################################################
			
			self.oFootThickE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			
			if selectedIndex == 0:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackInsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oThickFrontE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideThickness) )
				self.oOffsetFrontLE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL) )
				self.oOffsetFrontRE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetR) )
				self.oOffsetFrontTE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetT) )
				self.oOffsetFrontBE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB) )
				self.oHeightE.setText( MagicPanels.unit2gui(760) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 1:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackOutsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oHeightE.setText( MagicPanels.unit2gui(760) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 10:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackInsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oThickFrontE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideThickness) )
				self.oOffsetFrontLE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL) )
				self.oOffsetFrontRE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetR) )
				self.oOffsetFrontTE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetT) )
				self.oOffsetFrontBE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB) )
				self.oModulesNumE.setText("3")
				self.oHeightE.setText( MagicPanels.unit2gui(2300) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 20:
				self.oFootThickE.setText(MagicPanels.unit2gui(80))
			
			if selectedIndex == 21:
				self.og10L.setText(translate('magicStart', 'Drawer front overlap:'))
				self.og101E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL))
				self.og102E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB))
			
			if selectedIndex == 22:
				self.og10L.setText(translate('magicStart', 'Drawer front offset:'))
				self.og101E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetL))
				self.og102E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetB))
				
			if selectedIndex == 23:
				self.ofr7E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideThickness))
				self.ofr81E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL))
				self.ofr82E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetR))
				self.ofr83E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetT))
				self.ofr84E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB))
				
			if selectedIndex == 24:
				self.ofr7E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideThickness))
				self.ofr81E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetL))
				self.ofr82E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetR))
				self.ofr83E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetT))
				self.ofr84E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetB))
			
			if selectedIndex == 25:
				self.osh31E.setText(MagicPanels.unit2gui( MagicPanels.gShelfOffsetSides / 2 ))
				self.osh32E.setText(MagicPanels.unit2gui( MagicPanels.gShelfOffsetSides / 2 ))
			
			if selectedIndex == 27:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackOutsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oThickFrontE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideThickness) )
				self.oOffsetFrontLE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL) )
				self.oOffsetFrontRE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetR) )
				self.oOffsetFrontTE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetT) )
				self.oOffsetFrontBE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB) )
				self.oHeightE.setText( MagicPanels.unit2gui(760) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )

			if selectedIndex == 28:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackInsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oThickFrontE.setText( MagicPanels.unit2gui(MagicPanels.gFrontInsideThickness) )
				self.oOffsetFrontLE.setText( MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetL) )
				self.oOffsetFrontRE.setText( MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetR) )
				self.oOffsetFrontTE.setText( MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetT) )
				self.oOffsetFrontBE.setText( MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetB) )
				self.oHeightE.setText( MagicPanels.unit2gui(760) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 29:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackOutsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oThickFrontE.setText( MagicPanels.unit2gui(MagicPanels.gFrontInsideThickness) )
				self.oOffsetFrontLE.setText( MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetL) )
				self.oOffsetFrontRE.setText( MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetR) )
				self.oOffsetFrontTE.setText( MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetT) )
				self.oOffsetFrontBE.setText( MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetB) )
				self.oHeightE.setText( MagicPanels.unit2gui(760) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 30:
				self.ods11L.setText(translate('magicStart', 'Drawer front overlap:'))
				self.ods111E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL))
				self.ods112E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB))
				self.ods113E.setText(MagicPanels.unit2gui(4))
				self.ods41E.setText(MagicPanels.unit2gui(26))
				self.ods31E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideThickness))
				self.ods32E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.ods33E.setText(MagicPanels.unit2gui(3))
			
			if selectedIndex == 31:
				self.ods11L.setText(translate('magicStart', 'Drawer front offset:'))
				self.ods111E.setText(MagicPanels.unit2gui(2 * MagicPanels.gFrontInsideOffsetL))
				self.ods112E.setText(MagicPanels.unit2gui(2 * MagicPanels.gFrontInsideOffsetB))
				self.ods113E.setText(MagicPanels.unit2gui(4))
				self.ods41E.setText(MagicPanels.unit2gui(26))
				self.ods31E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideThickness))
				self.ods32E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.ods33E.setText(MagicPanels.unit2gui(3))
		
			if selectedIndex == 35:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.hide()
				self.oThickShelfE.hide()
				self.oHeightE.setText( MagicPanels.unit2gui(760) )
				self.oWidthE.setText( MagicPanels.unit2gui(900) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 36:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.hide()
				self.oThickShelfE.hide()
				self.oHeightE.setText( MagicPanels.unit2gui(760) )
				self.oWidthE.setText( MagicPanels.unit2gui(900) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 37 or selectedIndex == 38:
				self.ofglass3E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL))
				self.ofglass4E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB))
				self.ofglass3L.setText(translate('magicStart', 'Overlap horizontal:'))
				self.ofglass4L.setText(translate('magicStart', 'Overlap vertical:'))

			if selectedIndex == 39 or selectedIndex == 40:
				self.ofglass3E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetL))
				self.ofglass4E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetB))
				self.ofglass3L.setText(translate('magicStart', 'Offset horizontal:'))
				self.ofglass4L.setText(translate('magicStart', 'Offset vertical:'))
			
			if selectedIndex == 42:
				self.oTableSizeXE.setText(MagicPanels.unit2gui(1050))
				self.oTableSizeYE.setText(MagicPanels.unit2gui(600))
				self.oTableSizeZE.setText(MagicPanels.unit2gui(780))
				self.oTableTopThickE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oTableLegThickE.setText(MagicPanels.unit2gui(60))
				self.oTableTopOffsetE.setText(MagicPanels.unit2gui(35))
				
			if selectedIndex == 43:
				self.oTableSizeXE.setText(MagicPanels.unit2gui(990))
				self.oTableSizeYE.setText(MagicPanels.unit2gui(525))
				self.oTableSizeZE.setText(MagicPanels.unit2gui(430))
				self.oTableTopThickE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oTableLegThickE.setText(MagicPanels.unit2gui(80))
				self.oTableTopOffsetE.setText(MagicPanels.unit2gui(35))

			if selectedIndex == 44:
				self.oTableSizeXE.setText(MagicPanels.unit2gui(1050))
				self.oTableSizeYE.setText(MagicPanels.unit2gui(600))
				self.oTableSizeZE.setText(MagicPanels.unit2gui(780))
				self.oTableTopThickE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oTableLegThickE.setText(MagicPanels.unit2gui(150))
				self.oTableTopOffsetE.setText(MagicPanels.unit2gui(0))
				
			if selectedIndex == 45:
				self.oTableSizeXE.setText(MagicPanels.unit2gui(990))
				self.oTableSizeYE.setText(MagicPanels.unit2gui(525))
				self.oTableSizeZE.setText(MagicPanels.unit2gui(430))
				self.oTableTopThickE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oTableLegThickE.setText(MagicPanels.unit2gui(150))
				self.oTableTopOffsetE.setText(MagicPanels.unit2gui(0))
			
			if selectedIndex == 46:
				self.oTableSizeXE.setText(MagicPanels.unit2gui(1150))
				self.oTableSizeYE.setText(MagicPanels.unit2gui(700))
				self.oTableSizeZE.setText(MagicPanels.unit2gui(780))
				self.oTableTopThickE.setText(MagicPanels.unit2gui(36))
				self.oTableLegThickE.setText(MagicPanels.unit2gui(100))
				self.oTableTopOffsetE.setText(MagicPanels.unit2gui(40))
				
			if selectedIndex == 47:
				self.oTableSizeXE.setText(MagicPanels.unit2gui(1150))
				self.oTableSizeYE.setText(MagicPanels.unit2gui(700))
				self.oTableSizeZE.setText(MagicPanels.unit2gui(450))
				self.oTableTopThickE.setText(MagicPanels.unit2gui(36))
				self.oTableLegThickE.setText(MagicPanels.unit2gui(80))
				self.oTableTopOffsetE.setText(MagicPanels.unit2gui(0))

			if selectedIndex == 59:
				self.odf3E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL))
				self.odf4E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB))
				self.odf3L.setText(translate('magicStart', 'Front overlap horizontal:'))
				self.odf4L.setText(translate('magicStart', 'Front overlap vertical:'))

			if selectedIndex == 60:
				self.odf3E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetL))
				self.odf4E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideOffsetB))
				self.odf3L.setText(translate('magicStart', 'Front offset horizontal:'))
				self.odf4L.setText(translate('magicStart', 'Front offset vertical:'))
			
			if selectedIndex == 65:
				self.oThickE.setText(MagicPanels.unit2gui(19.05))
				self.oThickBackE.setText( MagicPanels.unit2gui(6.35) )
				self.oHeightE.setText(MagicPanels.unit2gui(876.3))
				self.oWidthE.setText(MagicPanels.unit2gui(914.4))
				self.oDepthE.setText(MagicPanels.unit2gui(609.6))
			
			if selectedIndex == 66:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackOutsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(6) )
				self.oThickFrontE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideThickness) )
				self.oOffsetFrontLE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL) )
				self.oOffsetFrontRE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetR) )
				self.oOffsetFrontTE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetT) )
				self.oOffsetFrontBE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB) )
				self.oHeightE.setText( MagicPanels.unit2gui(600) )
				self.oWidthE.setText( MagicPanels.unit2gui(400) )
				self.oDepthE.setText( MagicPanels.unit2gui(321) )

			if selectedIndex == 67:
				self.oThickE.setText(MagicPanels.unit2gui(19.05))
				self.oThickBackE.setText( MagicPanels.unit2gui(6.35) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(19.05) )
				self.oHeightE.setText(MagicPanels.unit2gui(762))
				self.oWidthE.setText(MagicPanels.unit2gui(457.2))
				self.oDepthE.setText(MagicPanels.unit2gui(330.2 - 19.05)) # 13 inch without front
			
			if selectedIndex == 71:
				self.ods11L.setText(translate('magicStart', 'Drawer front overlap:'))
				self.ods111E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL))
				self.ods112E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB))
				self.ods113E.setText(MagicPanels.unit2gui(4))
				self.ods41E.setText(MagicPanels.unit2gui(75))
				self.ods31E.setText(MagicPanels.unit2gui(MagicPanels.gFrontOutsideThickness))
				self.ods32E.setText(MagicPanels.unit2gui(16))
				self.ods33E.setText(MagicPanels.unit2gui(16))
			
			if selectedIndex == 72:
				self.ods11L.setText(translate('magicStart', 'Drawer front offset:'))
				self.ods111E.setText(MagicPanels.unit2gui(2 * MagicPanels.gFrontInsideOffsetL))
				self.ods112E.setText(MagicPanels.unit2gui(2 * MagicPanels.gFrontInsideOffsetB))
				self.ods113E.setText(MagicPanels.unit2gui(4))
				self.ods41E.setText(MagicPanels.unit2gui(75))
				self.ods31E.setText(MagicPanels.unit2gui(MagicPanels.gFrontInsideThickness))
				self.ods32E.setText(MagicPanels.unit2gui(16))
				self.ods33E.setText(MagicPanels.unit2gui(16))
			
			if selectedIndex == 74:
				self.oBackOffsetsL.setText(translate('magicStart', 'Back overlaps:'))
				self.oBackThickE.setText(MagicPanels.unit2gui(3))
				self.oBackOffsets1E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oBackOffsets2E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oBackOffsets3E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oBackOffsets4E.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			
			if selectedIndex == 75:
				self.oBackOffsetsL.setText(translate('magicStart', 'Back offsets:'))
				self.oBackThickE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oBackOffsets1E.setText(MagicPanels.unit2gui(0))
				self.oBackOffsets2E.setText(MagicPanels.unit2gui(0))
				self.oBackOffsets3E.setText(MagicPanels.unit2gui(0))
				self.oBackOffsets4E.setText(MagicPanels.unit2gui(0))
			
			if selectedIndex == 78:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackInsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oModulesNumE.setText("3")
				self.oHeightE.setText( MagicPanels.unit2gui(2300) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 79:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackOutsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oModulesNumE.setText("3")
				self.oHeightE.setText( MagicPanels.unit2gui(2300) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 80 or selectedIndex == 81:
				self.oTableSizeXE.setText(MagicPanels.unit2gui(1000))
				self.oTableSizeYE.setText(MagicPanels.unit2gui(550))
				self.oTableSizeZE.setText(MagicPanels.unit2gui(700))
				self.oTableTopThickE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oTableLegThickE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oTableTopOffsetE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))

			if selectedIndex == 82:
				self.oTableSizeXE.setText(MagicPanels.unit2gui(1200))
				self.oTableSizeYE.setText(MagicPanels.unit2gui(500))
				self.oTableSizeZE.setText(MagicPanels.unit2gui(810))
				self.oTableTopThickE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oTableLegThickE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
				self.oTableTopOffsetE.setText(MagicPanels.unit2gui(MagicPanels.gWoodThickness))
			
			if selectedIndex == 84:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackOutsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oThickFrontE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideThickness) )
				self.oOffsetFrontLE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL) )
				self.oOffsetFrontRE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetR) )
				self.oOffsetFrontTE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetT) )
				self.oOffsetFrontBE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB) )
				self.oModulesNumE.setText("4")
				self.oHeightE.setText( MagicPanels.unit2gui(2300) )
				self.oWidthE.setText( MagicPanels.unit2gui(620) )
				self.oDepthE.setText( MagicPanels.unit2gui(521) )
			
			if selectedIndex == 85:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackOutsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oThickFrontE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideThickness) )
				self.oOffsetFrontLE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetL) )
				self.oOffsetFrontRE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetR) )
				self.oOffsetFrontTE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetT) )
				self.oOffsetFrontBE.setText( MagicPanels.unit2gui(MagicPanels.gFrontOutsideOffsetB) )
				self.oModulesNumE.setText("3")
				self.oHeightE.setText( MagicPanels.unit2gui(2300) )
				self.oWidthE.setText( MagicPanels.unit2gui(620) )
				self.oDepthE.setText( MagicPanels.unit2gui(521) )
			
			if selectedIndex == 86:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackInsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oHeightE.setText( MagicPanels.unit2gui(760) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 87:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackOutsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oHeightE.setText( MagicPanels.unit2gui(760) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 88:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackInsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oHeightE.setText( MagicPanels.unit2gui(760) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
			
			if selectedIndex == 89:
				self.oThickE.setText( MagicPanels.unit2gui(self.gThick) )
				self.oThickBackE.setText( MagicPanels.unit2gui(MagicPanels.gBackOutsideThickness) )
				self.oThickShelfE.setText( MagicPanels.unit2gui(MagicPanels.gShelfThickness) )
				self.oHeightE.setText( MagicPanels.unit2gui(760) )
				self.oWidthE.setText( MagicPanels.unit2gui(500) )
				self.oDepthE.setText( MagicPanels.unit2gui(400) )
				
		# ############################################################################
		def createObject(self):

			if self.gSelectedFurniture == "F0":
				self.createF0()
			
			if self.gSelectedFurniture == "F1":
				self.createF1()
			
			if self.gSelectedFurniture == "F2":
				self.mergeF("Bookcase_002.FCStd")

			if self.gSelectedFurniture == "F3":
				self.mergeF("msf003.FCStd", "magicStart")
			
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
				self.mergeF("msf058.FCStd", "magicStart")

			if self.gSelectedFurniture == "F59" or self.gSelectedFurniture == "F60":
				self.createF59()
			
			if self.gSelectedFurniture == "F61":
				self.createF61()
			
			if self.gSelectedFurniture == "F62":
				self.createF62()
			
			if self.gSelectedFurniture == "F63":
				self.mergeF("Minifix_15_x_45_mm.FCStd", "mount")
			
			if self.gSelectedFurniture == "F64":
				self.createF64()
			
			if self.gSelectedFurniture == "F65":
				self.createF65()
			
			if self.gSelectedFurniture == "F66":
				self.createF66()
			
			if self.gSelectedFurniture == "F67":
				self.createF67()

			if self.gSelectedFurniture == "F68":
				self.mergeF("msf068.FCStd", "magicStart")
			
			if self.gSelectedFurniture == "F69":
				self.mergeF("msf069.FCStd", "magicStart")

			if self.gSelectedFurniture == "F70":
				self.mergeF("msf070.FCStd", "magicStart")
			
			if self.gSelectedFurniture == "F71":
				self.createF71()

			if self.gSelectedFurniture == "F72":
				self.createF72()
			
			if self.gSelectedFurniture == "F73":
				self.createF73()
			
			if self.gSelectedFurniture == "F74" or self.gSelectedFurniture == "F75":
				self.createF74()
			
			if self.gSelectedFurniture == "F76":
				self.mergeF("msf076.FCStd", "magicStart")
			
			if self.gSelectedFurniture == "F77":
				self.mergeF("msf077.FCStd", "magicStart")
			
			if self.gSelectedFurniture == "F78":
				self.createF78()
			
			if self.gSelectedFurniture == "F79":
				self.createF79()

			if self.gSelectedFurniture == "F80":
				self.createF80()
			
			if self.gSelectedFurniture == "F81":
				self.createF81()

			if self.gSelectedFurniture == "F82":
				self.createF82()
			
			if self.gSelectedFurniture == "F83":
				self.mergeF("msf083.FCStd", "magicStart")
			
			if self.gSelectedFurniture == "F84":
				self.createF84()
			
			if self.gSelectedFurniture == "F85":
				self.createF85()
			
			if self.gSelectedFurniture == "F86":
				self.createF86()
			
			if self.gSelectedFurniture == "F87":
				self.createF87()
			
			if self.gSelectedFurniture == "F88":
				self.createF88()
			
			if self.gSelectedFurniture == "F89":
				self.createF89()
			
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
				self.si.move(self.toolSW - 200 - 10, 50)
				self.si.show()

		# ############################################################################
		def getPathToMerge(self, iName, iType="magicStart"):
			
			if iType == "magicStart":
				path = FreeCADGui.activeWorkbench().path
				path = str(os.path.join(path, "Examples"))
				path = str(os.path.join(path, "magicStart"))
				path = str(os.path.join(path, iName))
			
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
			
			if iType == "other":
				path = FreeCADGui.activeWorkbench().path
				path = str(os.path.join(path, "Examples"))
				path = str(os.path.join(path, "Fixture"))
				path = str(os.path.join(path, "Other"))
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
			
			self.resize(self.toolSW + self.helpSW, self.toolSH)
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
		def calculateWorkspace(self):
			
			obj = False
			sub = False
			startX = 0
			startY = 0
			startZ = 0
			
			try:
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

				if sub.ShapeType == "Edge":
					startX = float(sub.CenterOfMass.x)
					startY = float(sub.CenterOfMass.y)
					startZ = float(sub.CenterOfMass.z)
					
				if sub.ShapeType == "Face":
					startX = float(sub.CenterOfMass.x)
					startY = float(sub.CenterOfMass.y)
					startZ = float(sub.CenterOfMass.z)
					
				if sub.ShapeType == "Vertex":
					startX = float(sub.Point.x)
					startY = float(sub.Point.y)
					startZ = float(sub.Point.z)

			except:
				skip = 1
			
			sizeZ = MagicPanels.unit2value(self.oworkspaceZE.text())
			startZ = startZ - sizeZ
			
			if obj != False:
				[[ startX, startY, startZ ]] = MagicPanels.getVerticesPosition([[ startX, startY, startZ ]], obj, "array")
			
			# set values to text fields
			self.oworkspaceSXE.setText(MagicPanels.unit2gui(startX))
			self.oworkspaceSYE.setText(MagicPanels.unit2gui(startY))
			self.oworkspaceSZE.setText(MagicPanels.unit2gui(startZ))

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
				
				woodt = MagicPanels.unit2value(self.oThickE.text())
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

				elif self.gSelectedFurniture == "F86":
					depth = float(obj.Width.Value)
					startY = float(sub.Placement.Base.y)
				
				elif self.gSelectedFurniture == "F87":
					depth = float(obj.Width.Value) + MagicPanels.gBackOutsideThickness
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
			startX = startX + MagicPanels.unit2value(self.oSelectionOffset1E.text())
			startY = startY + MagicPanels.unit2value(self.oSelectionOffset2E.text())
			startZ = startZ + MagicPanels.unit2value(self.oSelectionOffset3E.text())

			# set values to text fields
			self.oStartXE.setText(MagicPanels.unit2gui(startX))
			self.oStartYE.setText(MagicPanels.unit2gui(startY))
			self.oStartZE.setText(MagicPanels.unit2gui(startZ))
			
			if width != 0:
				self.oWidthE.setText(MagicPanels.unit2gui(width))
			
			if height != 0:
				self.oHeightE.setText(MagicPanels.unit2gui(height))
			
			if depth != 0:
				self.oDepthE.setText(MagicPanels.unit2gui(depth))

		# ############################################################################
		def calculateFoot(self):
			
			obj = False
			sub = False
			
			try:
				obj = FreeCADGui.Selection.getSelection()[0]
				sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

			except:
				return
			
			thick = MagicPanels.unit2value(self.oFootThickE.text())
			height = MagicPanels.unit2value(self.oFootSizeZE.text())
			width = 0
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
				startZ = float(sub.CenterOfMass.z) - height
				
			if sub.ShapeType == "Face":
				
				width = float(obj.Length.Value)
				depth = float(obj.Width.Value)
				startX = float(sub.Placement.Base.x)
				startY = float(sub.Placement.Base.y)
				startZ = float(sub.Placement.Base.z) - height

			if sub.ShapeType == "Vertex":
				
				startX = float(sub.X)
				startY = float(sub.Y)
				startZ = float(sub.Z) - height

			# set values to text fields
			self.oFootStartXE.setText(MagicPanels.unit2gui(startX))
			self.oFootStartYE.setText(MagicPanels.unit2gui(startY))
			self.oFootStartZE.setText(MagicPanels.unit2gui(startZ))
			
			if width != 0:
				self.oFootSizeXE.setText(MagicPanels.unit2gui(width))
			
			if depth != 0:
				self.oFootSizeYE.setText(MagicPanels.unit2gui(depth))

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
			self.og2E.setText(MagicPanels.unit2gui(startX))
			self.og3E.setText(MagicPanels.unit2gui(startY))
			self.og4E.setText(MagicPanels.unit2gui(startZ))
			self.og5E.setText(MagicPanels.unit2gui(width))
			self.og6E.setText(MagicPanels.unit2gui(height))
			self.og7E.setText(MagicPanels.unit2gui(depth))

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
			
			thick = MagicPanels.unit2value(self.ofr7E.text())
			
			offL = MagicPanels.unit2value(self.ofr81E.text())
			offR = MagicPanels.unit2value(self.ofr82E.text())
			offT = MagicPanels.unit2value(self.ofr83E.text())
			offB = MagicPanels.unit2value(self.ofr84E.text())
			
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
			self.ofr2E.setText(MagicPanels.unit2gui(startX))
			self.ofr3E.setText(MagicPanels.unit2gui(startY))
			self.ofr4E.setText(MagicPanels.unit2gui(startZ))
			self.ofr5E.setText(MagicPanels.unit2gui(width))
			self.ofr6E.setText(MagicPanels.unit2gui(height))

		# ############################################################################
		def calculateBack(self):
			
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
			gw = float(edge3.CenterOfMass.x) - float(edge4.CenterOfMass.x)
			
			sx = float(edge4.CenterOfMass.x)
			sy = float(edge4.CenterOfMass.y)
			sz = float(edge1.CenterOfMass.z)
			
			thick = MagicPanels.unit2value(self.oBackThickE.text())
			
			offL = MagicPanels.unit2value(self.oBackOffsets1E.text())
			offR = MagicPanels.unit2value(self.oBackOffsets2E.text())
			offT = MagicPanels.unit2value(self.oBackOffsets3E.text())
			offB = MagicPanels.unit2value(self.oBackOffsets4E.text())
			
			# outside
			if self.gSelectedFurniture == "F74":
				width = offL + gw + offR
				height = offB + gh + offT
				startX = sx - offR
				startY = sy
				startZ = sz - offB

			# inside
			if self.gSelectedFurniture == "F75":
				width = gw - offL - offR
				height = gh - offB - offT
				startX = sx + offR
				startY = sy - thick
				startZ = sz + offB
	
			# set values to text fields
			self.oBackSXE.setText(MagicPanels.unit2gui(startX))
			self.oBackSYE.setText(MagicPanels.unit2gui(startY))
			self.oBackSZE.setText(MagicPanels.unit2gui(startZ))
			self.oBackSizeXE.setText(MagicPanels.unit2gui(width))
			self.oBackSizeYE.setText(MagicPanels.unit2gui(height))

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
			
			thick = MagicPanels.unit2value(self.ofglass2E.text())
			overlapH = MagicPanels.unit2value(self.ofglass3E.text())
			overlapV = MagicPanels.unit2value(self.ofglass4E.text())
			
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
			self.ofglass71E.setText(MagicPanels.unit2gui(startX))
			self.ofglass72E.setText(MagicPanels.unit2gui(startY))
			self.ofglass73E.setText(MagicPanels.unit2gui(startZ))
			self.ofglass8E.setText(MagicPanels.unit2gui(barWidth))
			self.ofglass9E.setText(MagicPanels.unit2gui(width))
			self.ofglass10E.setText(MagicPanels.unit2gui(height))

		# ############################################################################
		def calculateDecorativeFront(self):
			
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
			
			thick = MagicPanels.unit2value(self.odf2E.text())
			overlapH = MagicPanels.unit2value(self.odf3E.text())
			overlapV = MagicPanels.unit2value(self.odf4E.text())
			
			# outside
			if self.gSelectedFurniture == "F59":
				
				width = gw + (2 * overlapH)
				height = gh + (2 * overlapV)
			
				startX = gsx - overlapH
				startY = gsy - thick
				startZ = gsz - overlapV

			# inside
			if self.gSelectedFurniture == "F60":
				
				width = gw - (2 * overlapH)
				height = gh - (2 * overlapV)
			
				startX = gsx + overlapH
				startY = gsy
				startZ = gsz + overlapV

			# simple
			if self.gSelectedFurniture == "F59" or self.gSelectedFurniture == "F60":
				barWidth = int(width / 10)

			# set values to text fields
			self.odf71E.setText(MagicPanels.unit2gui(startX))
			self.odf72E.setText(MagicPanels.unit2gui(startY))
			self.odf73E.setText(MagicPanels.unit2gui(startZ))
			self.odf8E.setText(MagicPanels.unit2gui(barWidth))
			self.odf9E.setText(MagicPanels.unit2gui(width))
			self.odf10E.setText(MagicPanels.unit2gui(height))

		# ############################################################################
		def calculateFrontDecoration(self):
			
			obj1 = False
			
			edge1 = False
			edge2 = False
			edge3 = False
			edge4 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
			
			except:
				return

			try:
				edge2 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[1]
				edge3 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[2]
				edge4 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[3]
			
			except:
				skip = 1
			
			if edge1.ShapeType == "Face":
				
				face = edge1
				
				if obj1.isDerivedFrom("Part::Box"):
					edge1 = face.Edges[0]
					edge2 = face.Edges[2]
					edge3 = face.Edges[3]
					edge4 = face.Edges[1]
				
				else:
					edge1 = face.Edges[2]
					edge2 = face.Edges[0]
					edge3 = face.Edges[3]
					edge4 = face.Edges[1]

			gh = abs(float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z))
			gw = abs(float(edge4.CenterOfMass.x) - float(edge3.CenterOfMass.x))
			
			gsx = float(edge3.CenterOfMass.x)
			gsy = float(edge3.CenterOfMass.y)
			gsz = float(edge1.CenterOfMass.z)
			
			barWidth = MagicPanels.unit2value(self.ofdec2E.text())
			barThick = MagicPanels.unit2value(self.ofdec3E.text())
			offsetH = MagicPanels.unit2value(self.ofdecOHE.text())
			offsetV = MagicPanels.unit2value(self.ofdecOVE.text())
			
			width = gw - (2 * offsetH)
			height = gh - (2 * offsetV)
			startX = gsx + offsetH
			startY = gsy - barThick
			startZ = gsz + offsetV

			# set values to text fields
			self.ofdec61E.setText(MagicPanels.unit2gui(startX))
			self.ofdec62E.setText(MagicPanels.unit2gui(startY))
			self.ofdec63E.setText(MagicPanels.unit2gui(startZ))
			self.ofdec7E.setText(MagicPanels.unit2gui(width))
			self.ofdec8E.setText(MagicPanels.unit2gui(height))

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
			
			barThick = MagicPanels.unit2value(self.offrame3E.text())
			offX = MagicPanels.unit2value(self.offrame4E.text())
			offY = MagicPanels.unit2value(self.offrame5E.text())
			
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
			self.offrame71E.setText(MagicPanels.unit2gui(startX))
			self.offrame72E.setText(MagicPanels.unit2gui(startY))
			self.offrame73E.setText(MagicPanels.unit2gui(startZ))
			self.offrame8E.setText(MagicPanels.unit2gui(width))
			self.offrame9E.setText(MagicPanels.unit2gui(height))

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
			
			thick = MagicPanels.unit2value(self.osh1E.text())
			udepth = MagicPanels.unit2value(self.osh2E.text())
			
			offL = MagicPanels.unit2value(self.osh31E.text())
			offR = MagicPanels.unit2value(self.osh32E.text())
			offF = MagicPanels.unit2value(self.osh33E.text())
			offB = MagicPanels.unit2value(self.osh34E.text())
			
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
			self.osh2E.setText(MagicPanels.unit2gui(depth))
			self.osh31E.setText(MagicPanels.unit2gui(offL))
			self.osh32E.setText(MagicPanels.unit2gui(offR))
			self.osh33E.setText(MagicPanels.unit2gui(offF))
			self.osh34E.setText(MagicPanels.unit2gui(offB))
			
			self.osh51E.setText(MagicPanels.unit2gui(startX))
			self.osh52E.setText(MagicPanels.unit2gui(startY))
			self.osh53E.setText(MagicPanels.unit2gui(startZ))
			
			self.osh6E.setText(MagicPanels.unit2gui(width))
			self.osh7E.setText(MagicPanels.unit2gui(depth))

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
			
			thick = MagicPanels.unit2value(self.oshs1E.text())
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			num = int(self.oshs2E.text())
			
			startX = sx + shelfOS
			startY = sy
			startZ = sz
			
			width = gw - (2 * shelfOS)
			depth = gd
			
			offset = (gh - (num * thick)) / (num + 1)
			
			# set values to text fields
			self.oshs41E.setText(MagicPanels.unit2gui(startX))
			self.oshs42E.setText(MagicPanels.unit2gui(startY))
			self.oshs43E.setText(MagicPanels.unit2gui(startZ))

			self.oshs5E.setText(MagicPanels.unit2gui(width))
			self.oshs6E.setText(MagicPanels.unit2gui(depth))
			self.oshs7E.setText(MagicPanels.unit2gui(offset))

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
			
			thick = MagicPanels.unit2value(self.oside1E.text())
			uwidth = MagicPanels.unit2value(self.oside2E.text())
			offL = MagicPanels.unit2value(self.oside31E.text())
			offR = MagicPanels.unit2value(self.oside32E.text())
			offT = MagicPanels.unit2value(self.oside33E.text())
			offB = MagicPanels.unit2value(self.oside34E.text())
			
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
			self.oside2E.setText(MagicPanels.unit2gui(width))
			self.oside31E.setText(MagicPanels.unit2gui(offL))
			self.oside32E.setText(MagicPanels.unit2gui(offR))
			self.oside33E.setText(MagicPanels.unit2gui(offT))
			self.oside34E.setText(MagicPanels.unit2gui(offB))
			
			self.oside51E.setText(MagicPanels.unit2gui(startX))
			self.oside52E.setText(MagicPanels.unit2gui(startY))
			self.oside53E.setText(MagicPanels.unit2gui(startZ))
			
			self.oside6E.setText(MagicPanels.unit2gui(width))
			self.oside7E.setText(MagicPanels.unit2gui(height))

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
				
			
			thick = MagicPanels.unit2value(self.ocs1E.text())
			udepth = MagicPanels.unit2value(self.ocs2E.text())
			
			offTo = MagicPanels.unit2value(self.ocs31E.text())
			offBo = MagicPanels.unit2value(self.ocs32E.text())
			offFr = MagicPanels.unit2value(self.ocs33E.text())
			offBa = MagicPanels.unit2value(self.ocs34E.text())
			
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
			self.ocs2E.setText(MagicPanels.unit2gui(depth))
			self.ocs31E.setText(MagicPanels.unit2gui(offTo))
			self.ocs32E.setText(MagicPanels.unit2gui(offBo))
			self.ocs33E.setText(MagicPanels.unit2gui(offFr))
			self.ocs34E.setText(MagicPanels.unit2gui(offBa))
			
			self.ocs51E.setText(MagicPanels.unit2gui(startX))
			self.ocs52E.setText(MagicPanels.unit2gui(startY))
			self.ocs53E.setText(MagicPanels.unit2gui(startZ))
			
			self.ocs6E.setText(MagicPanels.unit2gui(height))
			self.ocs7E.setText(MagicPanels.unit2gui(depth))

		# ############################################################################
		def calculateSideDecoration(self):
			
			obj1 = False
			
			edge1 = False
			edge2 = False
			edge3 = False
			edge4 = False
			
			try:
				obj1 = FreeCADGui.Selection.getSelection()[0]
				edge1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

			except:
				return

			try:
				edge2 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[1]
				edge3 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[2]
				edge4 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[3]
			
			except:
				skip = 1
			
			if edge1.ShapeType == "Face":
				
				face = edge1
				sink = MagicPanels.getFaceSink(obj1, face)
				
				if obj1.isDerivedFrom("Part::Box"):
					
					if sink == "-":
						edge1 = face.Edges[3]
						edge2 = face.Edges[1]
						edge3 = face.Edges[0]
						edge4 = face.Edges[2]
					else:
						edge1 = face.Edges[3]
						edge2 = face.Edges[1]
						edge3 = face.Edges[2]
						edge4 = face.Edges[0]

				else:
				
					if sink == "-":
						edge1 = face.Edges[2]
						edge2 = face.Edges[0]
						edge3 = face.Edges[3]
						edge4 = face.Edges[1]
					else:
						edge1 = face.Edges[2]
						edge2 = face.Edges[0]
						edge3 = face.Edges[1]
						edge4 = face.Edges[3]
			
			barWidth = MagicPanels.unit2value(self.osdec2E.text())
			barThick = MagicPanels.unit2value(self.osdec3E.text())
			offsetH = MagicPanels.unit2value(self.osdecOHE.text())
			offsetV = MagicPanels.unit2value(self.osdecOVE.text())
			
			self.gSideEdgePlane = MagicPanels.getEdgePlane(obj1, edge1, "clean")
			
			if self.gSideEdgePlane == "Y":
				
				gheight = abs(float(edge2.CenterOfMass.z) - float(edge1.CenterOfMass.z))
				gwidth = float(edge4.CenterOfMass.y) - float(edge3.CenterOfMass.y)
				
				
				if gwidth > 0:
					self.gSideDirection = "+"
				else:
					self.gSideDirection = "-"
					gwidth = abs(gwidth)
				
				width = gwidth - (2 * offsetH)
				height = gheight - (2 * offsetV)
			
				if self.gSideDirection == "+":
					startX = float(edge3.CenterOfMass.x)
					startY = float(edge3.CenterOfMass.y) + offsetH
					startZ = float(edge1.CenterOfMass.z) + offsetV

				if self.gSideDirection == "-":
					startX = float(edge3.CenterOfMass.x) - barThick
					startY = float(edge3.CenterOfMass.y) - offsetH - width
					startZ = float(edge1.CenterOfMass.z) + offsetV
			
			else:
				return

			# set values to text fields
			self.osdec61E.setText(MagicPanels.unit2gui(startX))
			self.osdec62E.setText(MagicPanels.unit2gui(startY))
			self.osdec63E.setText(MagicPanels.unit2gui(startZ))
			self.osdec7E.setText(MagicPanels.unit2gui(width))
			self.osdec8E.setText(MagicPanels.unit2gui(height))

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
			offset = 0 # offset between gaps
			
			width = gw
			height = ( gh - ((num + 1) * offset) ) / num
			depth = gd
			
			# set values to text fields
			self.ods61E.setText(MagicPanels.unit2gui(startX))
			self.ods62E.setText(MagicPanels.unit2gui(startY))
			self.ods63E.setText(MagicPanels.unit2gui(startZ))
			self.ods7E.setText(MagicPanels.unit2gui(width))
			self.ods8E.setText(MagicPanels.unit2gui(height))
			self.ods9E.setText(MagicPanels.unit2gui(depth))

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
				self.oTableStartXE.setText(MagicPanels.unit2gui(startX))
				self.oTableStartYE.setText(MagicPanels.unit2gui(startY))
				self.oTableStartZE.setText(MagicPanels.unit2gui(startZ))

		# ############################################################################
		# actions - draw functions
		# ############################################################################

		# ############################################################################
		def createF0(self):
			
			thick = MagicPanels.unit2value( self.oThickE.text() )
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			thickFront = MagicPanels.unit2value( self.oThickFrontE.text() )
			offsetFrontL = MagicPanels.unit2value( self.oOffsetFrontLE.text() )
			offsetFrontR = MagicPanels.unit2value( self.oOffsetFrontRE.text() )
			offsetFrontT = MagicPanels.unit2value( self.oOffsetFrontTE.text() )
			offsetFrontB = MagicPanels.unit2value( self.oOffsetFrontBE.text() )

			startX = MagicPanels.unit2value( self.oStartXE.text() )
			startY = MagicPanels.unit2value( self.oStartYE.text() )
			startZ = MagicPanels.unit2value( self.oStartZE.text() )
			
			sizeX = MagicPanels.unit2value( self.oWidthE.text() )
			sizeY = MagicPanels.unit2value( self.oDepthE.text() )
			sizeZ = MagicPanels.unit2value( self.oHeightE.text() )
			
			edgeband = MagicPanels.gEdgebandThickness
			if MagicPanels.gEdgebandApply == "everywhere":
				edgebandE = edgeband
			else:
				edgebandE = 0
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = sizeX - (2 * edgeband)
			o1.Height = thick
			o1.Width = sizeY - thickFront - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgeband, startY + thickFront + edgeband, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = thick
			o2.Height = sizeZ - (2 * thick) - (2 * edgebandE)
			o2.Width = sizeY - thickFront - (2 * edgeband)
			pl = FreeCAD.Vector(startX, startY + thickFront + edgeband, startZ + thick + edgebandE)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = thick
			o3.Height = sizeZ - (2 * thick) - (2 * edgebandE)
			o3.Width = sizeY - thickFront - (2 * edgeband)
			pl = FreeCAD.Vector(startX + sizeX - thick, startY + thickFront + edgeband, startZ + thick + edgebandE)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = sizeX - (2 * thick) - (2 * edgebandE)
			o4.Height = sizeZ - (2 * thick) - (2 * edgebandE)
			o4.Width = thickBack
			pl = FreeCAD.Vector(startX + thick + edgebandE, startY + sizeY - thickBack, startZ + thick + edgebandE)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = sizeX - (2 * edgeband)
			o5.Height = thick
			o5.Width = sizeY - thickFront - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgeband, startY + thickFront + edgeband, startZ + sizeZ - thick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o6.Label = translate('magicStart', 'Front')
			o6.Length = sizeX - (2 * thick) + offsetFrontL + offsetFrontR - (2 * edgeband)
			o6.Height = sizeZ - (2 * thick) + offsetFrontB + offsetFrontT - (2 * edgeband)
			o6.Width = thickFront
			px = startX + thick + edgeband - offsetFrontL
			py = startY
			pz = startZ + thick + edgeband - offsetFrontB
			pl = FreeCAD.Vector(px, py, pz)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
			
			# Shelf
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o7.Label = translate('magicStart', 'Shelf')
			o7.Length = sizeX - (2 * thick) - (2 * edgebandE) - (2 * shelfOS)
			o7.Height = thickShelf
			o7.Width = sizeY - thickFront - thickBack - thick - edgeband - edgebandE
			px = startX + thick + edgebandE + shelfOS
			py = startY + thickFront + thick + edgeband
			pz = startZ + (sizeZ / 2) - (thickShelf / 2)
			pl = FreeCAD.Vector(px, py, pz)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5, o6, o7]
			label = "Furniture, Module"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF1(self):
			
			thick = MagicPanels.unit2value( self.oThickE.text() )
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			startX = MagicPanels.unit2value( self.oStartXE.text() )
			startY = MagicPanels.unit2value( self.oStartYE.text() )
			startZ = MagicPanels.unit2value( self.oStartZE.text() )
			
			sizeX = MagicPanels.unit2value( self.oWidthE.text() )
			sizeY = MagicPanels.unit2value( self.oDepthE.text() ) - thickBack
			sizeZ = MagicPanels.unit2value( self.oHeightE.text() )
			
			edgeband = MagicPanels.gEdgebandThickness
			if MagicPanels.gEdgebandApply == "everywhere":
				edgebandE = edgeband
			else:
				edgebandE = 0
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = sizeX - (2 * thick) - (2 * edgebandE)
			o1.Height = thick
			o1.Width = sizeY - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + thick + edgebandE, startY + edgeband, startZ + 100)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = thick
			o2.Height = sizeZ - (2 * edgeband)
			o2.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX, startY + edgeband, startZ + edgeband)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = thick
			o3.Height = sizeZ - (2 * edgeband)
			o3.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX + sizeX - thick, startY + edgeband, startZ + edgeband)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = sizeX
			o4.Height = sizeZ - 100
			o4.Width = thickBack
			pl = FreeCAD.Vector(startX, startY + sizeY, startZ + 100)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			MagicPanels.setColor(o4, 3, (1.0, 1.0, 1.0, 1.0), "color")
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = sizeX - (2 * thick) - (2 * edgebandE)
			o5.Height = thick
			o5.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX + thick + edgebandE, startY + edgeband, startZ + sizeZ - thick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")

			# Shelf
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o6.Label = translate('magicStart', 'Shelf')
			o6.Length = sizeX - (2 * thick) - (2 * edgebandE) - (2 * shelfOS)
			o6.Height = thickShelf
			o6.Width = sizeY - edgeband - edgebandE
			px = startX + thick + edgebandE + shelfOS
			py = startY + edgeband
			pz = startZ + (sizeZ / 2) - (thickShelf / 2)
			o6.Placement = FreeCAD.Placement(FreeCAD.Vector(px, py, pz), self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5, o6]
			label = "Furniture, Module"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF10(self):
			
			thick = MagicPanels.unit2value( self.oThickE.text() )
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			thickFront = MagicPanels.unit2value( self.oThickFrontE.text() )
			offsetFrontL = MagicPanels.unit2value( self.oOffsetFrontLE.text() )
			offsetFrontR = MagicPanels.unit2value( self.oOffsetFrontRE.text() )
			offsetFrontT = MagicPanels.unit2value( self.oOffsetFrontTE.text() )
			offsetFrontB = MagicPanels.unit2value( self.oOffsetFrontBE.text() )
			
			startX = MagicPanels.unit2value( self.oStartXE.text() )
			startY = MagicPanels.unit2value( self.oStartYE.text() )
			startZ = MagicPanels.unit2value( self.oStartZE.text() )
			
			sizeX = MagicPanels.unit2value( self.oWidthE.text() )
			sizeY = MagicPanels.unit2value( self.oDepthE.text() )
			sizeZ = MagicPanels.unit2value( self.oHeightE.text() )
			
			edgeband = MagicPanels.gEdgebandThickness
			if MagicPanels.gEdgebandApply == "everywhere":
				edgebandE = edgeband
			else:
				edgebandE = 0
			
			# calculation
			mNum = int(self.oModulesNumE.text())
			sideZ = ((sizeZ - thick - (mNum * thick)) / mNum)
			
			# #######################
			# Modules
			# #######################
			
			for i in range(mNum):
			
				posZ = (i * sideZ) + (i * thick)
			
				# Floor
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
				o1.Label = translate('magicStart', 'Floor M'+str(i))
				o1.Length = sizeX
				o1.Height = thick
				o1.Width = sizeY - thickFront
				pl = FreeCAD.Vector(startX, startY + thickFront, startZ + posZ)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o1, 0, self.gColor, "color")
				
				# Left Side
				o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
				o2.Label = translate('magicStart', 'Left M'+str(i))
				o2.Length = thick
				o2.Height = sideZ
				o2.Width = sizeY - thickFront
				pl = FreeCAD.Vector(startX, startY + thickFront, startZ + posZ + thick)
				o2.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o2, 0, self.gColor, "color")
				
				# Right Side
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
				o3.Label = translate('magicStart', 'Right M'+str(i))
				o3.Length = thick
				o3.Height = sideZ
				o3.Width = sizeY - thickFront
				pl = FreeCAD.Vector(startX + sizeX - thick, startY + thickFront, startZ + posZ + thick)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o3, 0, self.gColor, "color")
				
				# Back
				o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
				o4.Label = translate('magicStart', 'Back M'+str(i))
				o4.Length = sizeX - (2 * thick)
				o4.Height = sideZ
				o4.Width = thickBack
				pl = FreeCAD.Vector(startX + thick, startY + sizeY - thickBack, startZ + posZ + thick)
				o4.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o4, 0, self.gColor, "color")
				
				# Front
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
				o5.Label = translate('magicStart', 'Front M'+str(i))
				o5.Length = sizeX - (2 * thick) + offsetFrontL + offsetFrontR
				o5.Height = sideZ + offsetFrontB + offsetFrontT
				o5.Width = thickFront
				pl = FreeCAD.Vector(startX + thick - offsetFrontL, startY, startZ + posZ + thick - offsetFrontB)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o5, 0, self.gColor, "color")
				
				# Shelf
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
				o6.Label = translate('magicStart', 'Shelf M'+str(i))
				o6.Length = sizeX - (2 * thick) - (2 * shelfOS)
				o6.Height = thickShelf
				o6.Width = sizeY - thickFront - thickBack - thick
				pZ = ((2 * i) + 1) * ((thick + sideZ) / 2)
				pl = FreeCAD.Vector(startX + thick + shelfOS, startY + thickFront + thick, startZ + pZ)
				o6.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o6, 0, self.gColor, "color")
				
				# create folder
				objects = [o1, o2, o3, o4, o5, o6]
				label = translate('magicStart', 'Module '+str(i))
				container = MagicPanels.createContainer(objects, label, False)

			# #######################
			# Top cover
			# #######################
			
			# final top
			t1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			t1.Label = translate('magicStart', 'Top cover')
			t1.Length = sizeX
			t1.Height = thick
			t1.Width = sizeY - thickFront
			pZ = mNum * (thick + sideZ)
			pl = FreeCAD.Vector(startX, startY + thickFront, startZ + pZ)
			t1.Placement = FreeCAD.Placement(pl, self.gR)
			t1.ViewObject.ShapeColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF16(self):
			
			frontOF = 0
			
			startX = MagicPanels.unit2value(self.oFootStartXE.text())
			startY = MagicPanels.unit2value(self.oFootStartYE.text())
			startZ = MagicPanels.unit2value(self.oFootStartZE.text())
			
			thick = MagicPanels.unit2value(self.oFootThickE.text())
			width = MagicPanels.unit2value(self.oFootSizeXE.text())
			height = MagicPanels.unit2value(self.oFootSizeZE.text())
			depth = MagicPanels.unit2value(self.oFootSizeYE.text()) - frontOF
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(startX, startY, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(startX + width - thick, startY, startZ)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			objects = [o1, o2]
			label = "Container, Foot"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF17(self):
			
			frontOF = 0
			
			startX = MagicPanels.unit2value(self.oFootStartXE.text())
			startY = MagicPanels.unit2value(self.oFootStartYE.text())
			startZ = MagicPanels.unit2value(self.oFootStartZE.text())
			
			thick = MagicPanels.unit2value(self.oFootThickE.text())
			width = MagicPanels.unit2value(self.oFootSizeXE.text())
			height = MagicPanels.unit2value(self.oFootSizeZE.text())
			depth = MagicPanels.unit2value(self.oFootSizeYE.text()) - frontOF
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(startX, startY, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(startX + width - thick, startY, startZ)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootBack")
			o3.Label = translate('magicStart', 'Foot Back')
			o3.Length = width - (2 * thick)
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(startX + thick, startY + depth - thick, startZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Front
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootFront")
			o4.Label = translate('magicStart', 'Foot Front')
			o4.Length = width - (2 * thick)
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(startX + thick, startY, startZ)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4]
			label = "Container, Foot"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF18(self):
			
			frontOF = 0
			
			startX = MagicPanels.unit2value(self.oFootStartXE.text())
			startY = MagicPanels.unit2value(self.oFootStartYE.text())
			startZ = MagicPanels.unit2value(self.oFootStartZE.text())
			
			thick = MagicPanels.unit2value(self.oFootThickE.text())
			width = MagicPanels.unit2value(self.oFootSizeXE.text())
			height = MagicPanels.unit2value(self.oFootSizeZE.text())
			depth = MagicPanels.unit2value(self.oFootSizeYE.text()) - frontOF

			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(startX, startY, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(startX + width - thick, startY, startZ)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootBack")
			o3.Label = translate('magicStart', 'Foot Back')
			o3.Length = width - (2 * thick)
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(startX + thick, startY + depth - thick, startZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Front
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootFront")
			o4.Label = translate('magicStart', 'Foot Front')
			o4.Length = width - (2 * thick)
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(startX + thick, startY, startZ)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Center
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootCenter")
			o5.Label = translate('magicStart', 'Foot Center')
			o5.Length = width - (2 * thick)
			o5.Height = height
			o5.Width = thick
			py = startY + (depth / 2) - (thick / 2)
			pl = FreeCAD.Vector(startX + thick, py, startZ)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5]
			label = "Container, Foot"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF19(self):
			
			frontOF = 0
			
			startX = MagicPanels.unit2value(self.oFootStartXE.text())
			startY = MagicPanels.unit2value(self.oFootStartYE.text())
			startZ = MagicPanels.unit2value(self.oFootStartZE.text())
			
			thick = MagicPanels.unit2value(self.oFootThickE.text())
			width = MagicPanels.unit2value(self.oFootSizeXE.text())
			height = MagicPanels.unit2value(self.oFootSizeZE.text())
			depth = MagicPanels.unit2value(self.oFootSizeYE.text()) - frontOF

			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeft")
			o1.Label = translate('magicStart', 'Foot Left')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(startX, startY, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRight")
			o2.Label = translate('magicStart', 'Foot Right')
			o2.Length = thick
			o2.Height = height
			o2.Width = depth
			pl = FreeCAD.Vector(startX + width - thick, startY, startZ)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootBack")
			o3.Label = translate('magicStart', 'Foot Back')
			o3.Length = width - (2 * thick)
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(startX + thick, startY + depth - thick, startZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Front
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootFront")
			o4.Label = translate('magicStart', 'Foot Front')
			o4.Length = width - (2 * thick)
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(startX + thick, startY + thick, startZ)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4]
			label = "Container, Foot"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF20(self):
			
			frontOF = 0
			
			startX = MagicPanels.unit2value(self.oFootStartXE.text())
			startY = MagicPanels.unit2value(self.oFootStartYE.text())
			startZ = MagicPanels.unit2value(self.oFootStartZE.text())
			
			thick = MagicPanels.unit2value(self.oFootThickE.text())
			width = MagicPanels.unit2value(self.oFootSizeXE.text())
			height = MagicPanels.unit2value(self.oFootSizeZE.text())
			depth = MagicPanels.unit2value(self.oFootSizeYE.text()) - frontOF

			# Left Front
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeftFront")
			o1.Label = translate('magicStart', 'Foot Left Front')
			o1.Length = thick
			o1.Height = height
			o1.Width = thick
			pl = FreeCAD.Vector(startX, startY, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Back
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootLeftBack")
			o2.Label = translate('magicStart', 'Foot Left Back')
			o2.Length = thick
			o2.Height = height
			o2.Width = thick
			pl = FreeCAD.Vector(startX, startY + depth - thick, startZ)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Front
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRightFront")
			o3.Label = translate('magicStart', 'Foot Right Front')
			o3.Length = thick
			o3.Height = height
			o3.Width = thick
			pl = FreeCAD.Vector(startX + width - thick, startY, startZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Right Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FootRightBack")
			o4.Label = translate('magicStart', 'Foot Right Back')
			o4.Length = thick
			o4.Height = height
			o4.Width = thick
			pl = FreeCAD.Vector(startX + width - thick, startY + depth - thick, startZ)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4]
			label = "Container, Foot"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF21(self):
			
			p0X = MagicPanels.unit2value(self.og2E.text())
			p0Y = MagicPanels.unit2value(self.og3E.text())
			p0Z = MagicPanels.unit2value(self.og4E.text())
			
			width = MagicPanels.unit2value(self.og5E.text())
			height = MagicPanels.unit2value(self.og6E.text())
			depth = MagicPanels.unit2value(self.og7E.text())
			
			frontOffsetH = 2 * MagicPanels.unit2value(self.og101E.text())
			frontOffsetV = 2 * MagicPanels.unit2value(self.og102E.text())
			
			thickFront = MagicPanels.unit2value(self.og81E.text())
			thickSides = MagicPanels.unit2value(self.og82E.text())
			thickBottom = MagicPanels.unit2value(self.og83E.text())
			
			sidesOF = MagicPanels.unit2value(self.og91E.text())
			sideOF = sidesOF / 2
			backOF = MagicPanels.unit2value(self.og92E.text())
			topOF = MagicPanels.unit2value(self.og93E.text())
			bottomOF = MagicPanels.unit2value(self.og94E.text())
			
			if self.gSingleDrawerPlane == "X":
			
				if self.gSingleDrawerDirection == "+":

					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = thickSides
					o1.Height = height - bottomOF - topOF - thickBottom
					o1.Width = depth - backOF
					pl = FreeCAD.Vector(p0X + sideOF, p0Y, p0Z + bottomOF + thickBottom)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = thickSides
					o2.Height = height - bottomOF - topOF - thickBottom
					o2.Width = depth - backOF
					pl = FreeCAD.Vector(p0X + width - thickSides - sideOF, p0Y, p0Z + bottomOF + thickBottom)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = width - (2 * thickSides) - sidesOF
					o3.Height = height - bottomOF - topOF - thickBottom
					o3.Width = thickSides
					pl = FreeCAD.Vector(p0X + sideOF + thickSides, p0Y + depth - thickSides - backOF, p0Z + bottomOF + thickBottom)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = width - (2 * thickSides) - sidesOF
					o4.Height = height - bottomOF - topOF - thickBottom
					o4.Width = thickSides
					pl = FreeCAD.Vector(p0X + sideOF + thickSides, p0Y, p0Z + bottomOF + thickBottom)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, (1.0, 1.0, 1.0, 1.0), "color")

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = width - sidesOF
					o5.Height = thickBottom
					o5.Width = depth - backOF
					pl = FreeCAD.Vector(p0X + sideOF, p0Y, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					colors = [ self.gColor, self.gColor, self.gColor, self.gColor, self.gColor, (1.0, 1.0, 1.0, 1.0) ]
					MagicPanels.setColor(o5, 0, colors, "color")

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = width + frontOffsetH
					o6.Height = height + frontOffsetV
					o6.Width = thickFront
					pl = FreeCAD.Vector(p0X - (frontOffsetH / 2), p0Y - thickFront, p0Z - (frontOffsetV / 2))
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o6, 0, self.gColor, "color")

					objects = [o1, o2, o3, o4, o5, o6]
					label = "Container, Drawer"
					container = MagicPanels.createContainer(objects, label, False)
					
					# recompute
					FreeCAD.ActiveDocument.recompute()
			
				if self.gSingleDrawerDirection == "-":

					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = thickSides
					o1.Height = height - bottomOF - topOF - thickBottom
					o1.Width = depth - backOF
					pl = FreeCAD.Vector(p0X - sideOF - thickSides, p0Y - depth + backOF, p0Z + bottomOF + thickBottom)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = thickSides
					o2.Height = height - bottomOF - topOF - thickBottom
					o2.Width = depth - backOF
					pl = FreeCAD.Vector(p0X - width + sideOF, p0Y - depth + backOF, p0Z + bottomOF + thickBottom)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = width - (2 * thickSides) - sidesOF
					o3.Height = height - bottomOF - topOF - thickBottom
					o3.Width = thickSides
					pl = FreeCAD.Vector(p0X - width + sideOF + thickSides, p0Y - depth + backOF, p0Z + bottomOF + thickBottom)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = width - (2 * thickSides) - sidesOF
					o4.Height = height - bottomOF - topOF - thickBottom
					o4.Width = thickSides
					pl = FreeCAD.Vector(p0X - width + sideOF + thickSides, p0Y - thickSides, p0Z + bottomOF + thickBottom)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, (1.0, 1.0, 1.0, 1.0), "color")

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = width - sidesOF
					o5.Height = thickBottom
					o5.Width = depth - backOF
					pl = FreeCAD.Vector(p0X - width + sideOF, p0Y - depth + backOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					colors = [ self.gColor, self.gColor, self.gColor, self.gColor, self.gColor, (1.0, 1.0, 1.0, 1.0) ]
					MagicPanels.setColor(o5, 0, colors, "color")

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = width + frontOffsetH
					o6.Height = height + frontOffsetV
					o6.Width = thickFront
					pl = FreeCAD.Vector(p0X - width - (frontOffsetH / 2), p0Y, p0Z - (frontOffsetV / 2))
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o6, 0, self.gColor, "color")

					objects = [o1, o2, o3, o4, o5, o6]
					label = "Container, Drawer"
					container = MagicPanels.createContainer(objects, label, False)
					
					# recompute
					FreeCAD.ActiveDocument.recompute()

			if self.gSingleDrawerPlane == "Y":
			
				if self.gSingleDrawerDirection == "+":
				
					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = depth - backOF
					o1.Height = height - bottomOF - topOF - thickBottom
					o1.Width = thickSides
					pl = FreeCAD.Vector(p0X, p0Y - sideOF - thickSides, p0Z + bottomOF + thickBottom)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = depth - backOF
					o2.Height = height - bottomOF - topOF - thickBottom
					o2.Width = thickSides
					pl = FreeCAD.Vector(p0X, p0Y - width + sideOF, p0Z + bottomOF + thickBottom)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = thickSides
					o3.Height = height - bottomOF - topOF - thickBottom
					o3.Width = width - (2 * thickSides) - sidesOF
					px = p0X + depth - thickSides - backOF
					py = p0Y - width + sideOF + thickSides
					pz = p0Z + bottomOF + thickBottom
					pl = FreeCAD.Vector(px, py, pz)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = thickSides
					o4.Height = height - bottomOF - topOF - thickBottom
					o4.Width = width - (2 * thickSides) - sidesOF
					pl = FreeCAD.Vector(p0X, p0Y - width + sideOF + thickSides, p0Z + bottomOF + thickBottom)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, (1.0, 1.0, 1.0, 1.0), "color")

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = depth - backOF
					o5.Height = thickBottom
					o5.Width = width - sidesOF
					pl = FreeCAD.Vector(p0X, p0Y - width + sideOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					colors = [ self.gColor, self.gColor, self.gColor, self.gColor, self.gColor, (1.0, 1.0, 1.0, 1.0) ]
					MagicPanels.setColor(o5, 0, colors, "color")

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = thickFront
					o6.Height = height + frontOffsetV
					o6.Width = width + frontOffsetH
					pl = FreeCAD.Vector(p0X - thickFront, p0Y - width - (frontOffsetH / 2), p0Z - (frontOffsetV / 2))
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o6, 0, self.gColor, "color")

					objects = [o1, o2, o3, o4, o5, o6]
					label = "Container, Drawer"
					container = MagicPanels.createContainer(objects, label, False)
					
					# recompute
					FreeCAD.ActiveDocument.recompute()
		
				if self.gSingleDrawerDirection == "-":

					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = depth - backOF
					o1.Height = height - bottomOF - topOF - thickBottom
					o1.Width = thickSides
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF, p0Z + bottomOF + thickBottom)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = depth - backOF
					o2.Height = height - bottomOF - topOF - thickBottom
					o2.Width = thickSides
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + width - sideOF - thickSides, p0Z + bottomOF + thickBottom)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = thickSides
					o3.Height = height - bottomOF - topOF - thickBottom
					o3.Width = width - (2 * thickSides) - sidesOF
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF + thickSides, p0Z + bottomOF + thickBottom)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = thickSides
					o4.Height = height - bottomOF - topOF - thickBottom
					o4.Width = width - (2 * thickSides) - sidesOF
					pl = FreeCAD.Vector(p0X - thickSides, p0Y + sideOF + thickSides, p0Z + bottomOF + thickBottom)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, (1.0, 1.0, 1.0, 1.0), "color")

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = depth - backOF
					o5.Height = thickBottom
					o5.Width = width - sidesOF
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					colors = [ self.gColor, self.gColor, self.gColor, self.gColor, self.gColor, (1.0, 1.0, 1.0, 1.0) ]
					MagicPanels.setColor(o5, 0, colors, "color")

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = thickFront
					o6.Height = height + frontOffsetV
					o6.Width = width + frontOffsetH
					pl = FreeCAD.Vector(p0X, p0Y - (frontOffsetH / 2), p0Z - (frontOffsetV / 2))
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o6, 0, self.gColor, "color")

					objects = [o1, o2, o3, o4, o5, o6]
					label = "Container, Drawer"
					container = MagicPanels.createContainer(objects, label, False)
					
					# recompute
					FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF22(self):
			
			p0X = MagicPanels.unit2value(self.og2E.text())
			p0Y = MagicPanels.unit2value(self.og3E.text())
			p0Z = MagicPanels.unit2value(self.og4E.text())
			
			width = MagicPanels.unit2value(self.og5E.text())
			height = MagicPanels.unit2value(self.og6E.text())
			depth = MagicPanels.unit2value(self.og7E.text())
			
			frontOffsetH = MagicPanels.unit2value(self.og101E.text())
			frontOffsetV = MagicPanels.unit2value(self.og102E.text())
			
			thickFront = MagicPanels.unit2value(self.og81E.text())
			thickSides = MagicPanels.unit2value(self.og82E.text())
			thickBottom = MagicPanels.unit2value(self.og83E.text())
			
			sidesOF = MagicPanels.unit2value(self.og91E.text())
			sideOF = sidesOF / 2
			backOF = MagicPanels.unit2value(self.og92E.text())
			topOF = MagicPanels.unit2value(self.og93E.text())
			bottomOF = MagicPanels.unit2value(self.og94E.text())
			
			if self.gSingleDrawerPlane == "X":
			
				if self.gSingleDrawerDirection == "+":

					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = thickSides
					o1.Height = height - bottomOF - topOF - thickBottom
					o1.Width = depth - backOF - thickFront
					pl = FreeCAD.Vector(p0X + sideOF, p0Y + thickFront, p0Z + bottomOF + thickBottom)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = thickSides
					o2.Height = height - bottomOF - topOF - thickBottom
					o2.Width = depth - backOF - thickFront
					pl = FreeCAD.Vector(p0X + width - thickSides - sideOF, p0Y + thickFront, p0Z + bottomOF + thickBottom)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = width - (2 * thickSides) - sidesOF
					o3.Height = height - bottomOF - topOF - thickBottom
					o3.Width = thickSides
					pl = FreeCAD.Vector(p0X + sideOF + thickSides, p0Y + depth - thickSides - backOF, p0Z + bottomOF + thickBottom)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = width - (2 * thickSides) - sidesOF
					o4.Height = height - bottomOF - topOF - thickBottom
					o4.Width = thickSides
					pl = FreeCAD.Vector(p0X + sideOF + thickSides, p0Y + thickFront, p0Z + bottomOF + thickBottom)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, (1.0, 1.0, 1.0, 1.0), "color")

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = width - sidesOF
					o5.Height = thickBottom
					o5.Width = depth - backOF - thickFront
					pl = FreeCAD.Vector(p0X + sideOF, p0Y + thickFront, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					colors = [ self.gColor, self.gColor, self.gColor, self.gColor, self.gColor, (1.0, 1.0, 1.0, 1.0) ]
					MagicPanels.setColor(o5, 0, colors, "color")

					# Front outside make inside as well
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = width - ( 2 * frontOffsetH )
					o6.Height = height - ( 2 * frontOffsetV )
					o6.Width = thickFront
					pl = FreeCAD.Vector(p0X + frontOffsetH, p0Y, p0Z + frontOffsetV)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o6, 0, self.gColor, "color")

					objects = [o1, o2, o3, o4, o5, o6]
					label = "Container, Drawer"
					container = MagicPanels.createContainer(objects, label, False)
					
					# recompute
					FreeCAD.ActiveDocument.recompute()
			
				if self.gSingleDrawerDirection == "-":

					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = thickSides
					o1.Height = height - bottomOF - topOF - thickBottom
					o1.Width = depth - backOF - thickFront
					pl = FreeCAD.Vector(p0X - sideOF - thickSides, p0Y - depth + backOF, p0Z + bottomOF + thickBottom)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = thickSides
					o2.Height = height - bottomOF - topOF - thickBottom
					o2.Width = depth - backOF - thickFront
					pl = FreeCAD.Vector(p0X - width + sideOF, p0Y - depth + backOF, p0Z + bottomOF + thickBottom)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = width - (2 * thickSides) - sidesOF
					o3.Height = height - bottomOF - topOF - thickBottom
					o3.Width = thickSides
					pl = FreeCAD.Vector(p0X - width + sideOF + thickSides, p0Y - depth + backOF, p0Z + bottomOF + thickBottom)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = width - (2 * thickSides) - sidesOF
					o4.Height = height - bottomOF - topOF - thickBottom
					o4.Width = thickSides
					pl = FreeCAD.Vector(p0X - width + sideOF + thickSides, p0Y - thickSides - thickFront, p0Z + bottomOF + thickBottom)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, (1.0, 1.0, 1.0, 1.0), "color")

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = width - sidesOF
					o5.Height = thickBottom
					o5.Width = depth - backOF - thickFront
					pl = FreeCAD.Vector(p0X - width + sideOF, p0Y - depth + backOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					colors = [ self.gColor, self.gColor, self.gColor, self.gColor, self.gColor, (1.0, 1.0, 1.0, 1.0) ]
					MagicPanels.setColor(o5, 0, colors, "color")

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = width - ( 2 * frontOffsetH )
					o6.Height = height - ( 2 * frontOffsetV )
					o6.Width = thickFront
					pl = FreeCAD.Vector(p0X - width + frontOffsetH, p0Y - thickFront, p0Z + frontOffsetV)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o6, 0, self.gColor, "color")

					objects = [o1, o2, o3, o4, o5, o6]
					label = "Container, Drawer"
					container = MagicPanels.createContainer(objects, label, False)
					
					# recompute
					FreeCAD.ActiveDocument.recompute()

			if self.gSingleDrawerPlane == "Y":
			
				if self.gSingleDrawerDirection == "+":

					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = depth - backOF - thickFront
					o1.Height = height - bottomOF - topOF - thickBottom
					o1.Width = thickSides
					pl = FreeCAD.Vector(p0X + thickFront, p0Y - sideOF - thickSides, p0Z + bottomOF + thickBottom)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = depth - backOF - thickFront
					o2.Height = height - bottomOF - topOF - thickBottom
					o2.Width = thickSides
					pl = FreeCAD.Vector(p0X + thickFront, p0Y - width + sideOF, p0Z + bottomOF + thickBottom)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = thickSides
					o3.Height = height - bottomOF - topOF - thickBottom
					o3.Width = width - (2 * thickSides) - sidesOF
					px = p0X + depth - backOF - thickSides
					py = p0Y - width + sideOF + thickSides
					pz = p0Z + bottomOF + thickBottom
					pl = FreeCAD.Vector(px, py, pz)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = thickSides
					o4.Height = height - bottomOF - topOF - thickBottom
					o4.Width = width - (2 * thickSides) - sidesOF
					pl = FreeCAD.Vector(p0X + thickFront, p0Y - width + sideOF + thickSides, p0Z + bottomOF + thickBottom)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, (1.0, 1.0, 1.0, 1.0), "color")

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = depth - backOF - thickFront
					o5.Height = thickBottom
					o5.Width = width - sidesOF
					pl = FreeCAD.Vector(p0X + thickFront, p0Y - width + sideOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					colors = [ self.gColor, self.gColor, self.gColor, self.gColor, self.gColor, (1.0, 1.0, 1.0, 1.0) ]
					MagicPanels.setColor(o5, 0, colors, "color")

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = thickFront
					o6.Height = height - ( 2 * frontOffsetV )
					o6.Width = width - ( 2 * frontOffsetH )
					pl = FreeCAD.Vector(p0X, p0Y - width + frontOffsetH, p0Z + frontOffsetV)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o6, 0, self.gColor, "color")

					objects = [o1, o2, o3, o4, o5, o6]
					label = "Container, Drawer"
					container = MagicPanels.createContainer(objects, label, False)
					
					# recompute
					FreeCAD.ActiveDocument.recompute()
		
				if self.gSingleDrawerDirection == "-":

					# Left Side
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerLeft")
					o1.Label = translate('magicStart', 'Drawer Left')
					o1.Length = depth - backOF - thickFront
					o1.Height = height - bottomOF - topOF - thickBottom
					o1.Width = thickSides
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF, p0Z + bottomOF + thickBottom)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Right Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerRight")
					o2.Label = translate('magicStart', 'Drawer Right')
					o2.Length = depth - backOF - thickFront
					o2.Height = height - bottomOF - topOF - thickBottom
					o2.Width = thickSides
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + width - sideOF - thickSides, p0Z + bottomOF + thickBottom)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Back
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBack")
					o3.Label = translate('magicStart', 'Drawer Back')
					o3.Length = thickSides
					o3.Height = height - bottomOF - topOF - thickBottom
					o3.Width = width - (2 * thickSides) - sidesOF
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF + thickSides, p0Z + bottomOF + thickBottom)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Front inside
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontInside")
					o4.Label = translate('magicStart', 'Drawer Front Inside')
					o4.Length = thickSides
					o4.Height = height - bottomOF - topOF - thickBottom
					o4.Width = width - (2 * thickSides) - sidesOF
					pl = FreeCAD.Vector(p0X - thickSides - thickFront, p0Y + sideOF + thickSides, p0Z + bottomOF + thickBottom)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, (1.0, 1.0, 1.0, 1.0), "color")

					# HDF bottom
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerBottom")
					o5.Label = translate('magicStart', 'Drawer Bottom HDF')
					o5.Length = depth - backOF - thickFront
					o5.Height = thickBottom
					o5.Width = width - sidesOF
					pl = FreeCAD.Vector(p0X - depth + backOF, p0Y + sideOF, p0Z  + bottomOF)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					colors = [ self.gColor, self.gColor, self.gColor, self.gColor, self.gColor, (1.0, 1.0, 1.0, 1.0) ]
					MagicPanels.setColor(o5, 0, colors, "color")

					# Front outside
					o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DrawerFrontOutside")
					o6.Label = translate('magicStart', 'Drawer Front Outside')
					o6.Length = thickFront
					o6.Height = height - ( 2 * frontOffsetV )
					o6.Width = width - ( 2 * frontOffsetH )
					pl = FreeCAD.Vector(p0X - thickFront, p0Y + frontOffsetH, p0Z + frontOffsetV)
					o6.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o6, 0, self.gColor, "color")

					objects = [o1, o2, o3, o4, o5, o6]
					label = "Container, Drawer"
					container = MagicPanels.createContainer(objects, label, False)
					
					# recompute
					FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF23(self):
			
			p0X = MagicPanels.unit2value(self.ofr2E.text())
			p0Y = MagicPanels.unit2value(self.ofr3E.text())
			p0Z = MagicPanels.unit2value(self.ofr4E.text())
			
			width = MagicPanels.unit2value(self.ofr5E.text())
			height = MagicPanels.unit2value(self.ofr6E.text())
			thick = MagicPanels.unit2value(self.ofr7E.text())
			
			# Front outside
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FrontOutside")
			o1.Label = translate('magicStart', 'Front outside')
			o1.Length = width
			o1.Height = height
			o1.Width = thick
			pl = FreeCAD.Vector(p0X, p0Y, p0Z)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF24(self):

			p0X = MagicPanels.unit2value(self.ofr2E.text())
			p0Y = MagicPanels.unit2value(self.ofr3E.text())
			p0Z = MagicPanels.unit2value(self.ofr4E.text())
			
			width = MagicPanels.unit2value(self.ofr5E.text())
			height = MagicPanels.unit2value(self.ofr6E.text())
			thick = MagicPanels.unit2value(self.ofr7E.text())
			
			# Front outside
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FrontInside")
			o1.Label = translate('magicStart', 'Front inside')
			o1.Length = width
			o1.Height = height
			o1.Width = thick
			pl = FreeCAD.Vector(p0X, p0Y, p0Z)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF25(self):
	
			p0X = MagicPanels.unit2value(self.osh51E.text())
			p0Y = MagicPanels.unit2value(self.osh52E.text())
			p0Z = MagicPanels.unit2value(self.osh53E.text())
			
			width = MagicPanels.unit2value(self.osh6E.text())
			depth = MagicPanels.unit2value(self.osh7E.text())
			thick = MagicPanels.unit2value(self.osh1E.text())
			
			# Front outside
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o1.Label = translate('magicStart', 'Shelf')
			o1.Length = width
			o1.Height = thick
			o1.Width = depth
			pl = FreeCAD.Vector(p0X, p0Y, p0Z)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF26(self):
	
			p0X = MagicPanels.unit2value(self.ocs51E.text())
			p0Y = MagicPanels.unit2value(self.ocs52E.text())
			p0Z = MagicPanels.unit2value(self.ocs53E.text())
			
			height = MagicPanels.unit2value(self.ocs6E.text())
			depth = MagicPanels.unit2value(self.ocs7E.text())
			thick = MagicPanels.unit2value(self.ocs1E.text())
			
			# Side center
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "SideCenter")
			o1.Label = translate('magicStart', 'Side Center')
			o1.Length = thick
			o1.Height = height
			o1.Width = depth
			pl = FreeCAD.Vector(p0X, p0Y, p0Z)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF27(self):
			
			thick = MagicPanels.unit2value( self.oThickE.text() )
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			thickFront = MagicPanels.unit2value( self.oThickFrontE.text() )
			offsetFrontL = MagicPanels.unit2value( self.oOffsetFrontLE.text() )
			offsetFrontR = MagicPanels.unit2value( self.oOffsetFrontRE.text() )
			offsetFrontT = MagicPanels.unit2value( self.oOffsetFrontTE.text() )
			offsetFrontB = MagicPanels.unit2value( self.oOffsetFrontBE.text() )

			startX = MagicPanels.unit2value( self.oStartXE.text() )
			startY = MagicPanels.unit2value( self.oStartYE.text() )
			startZ = MagicPanels.unit2value( self.oStartZE.text() )
			
			sizeX = MagicPanels.unit2value( self.oWidthE.text() )
			sizeY = MagicPanels.unit2value( self.oDepthE.text() )
			sizeZ = MagicPanels.unit2value( self.oHeightE.text() )
			
			edgeband = MagicPanels.gEdgebandThickness
			if MagicPanels.gEdgebandApply == "everywhere":
				edgebandE = edgeband
			else:
				edgebandE = 0
				
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = sizeX - (2 * edgeband)
			o1.Height = thick
			o1.Width = sizeY - thickFront - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgeband, startY + thickFront + edgeband, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = thick
			o2.Height = sizeZ - (2 * thick) - (2 * edgebandE)
			o2.Width = sizeY - thickFront - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX, startY + thickFront + edgeband, startZ + thick + edgebandE)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = thick
			o3.Height = sizeZ - (2 * thick) - (2 * edgebandE)
			o3.Width = sizeY - thickFront - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + sizeX - thick, startY + thickFront + edgeband, startZ + thick + edgebandE)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back HDF
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "BackHDF")
			o4.Label = translate('magicStart', 'Back HDF')
			o4.Length = sizeX
			o4.Height = sizeZ
			o4.Width = thickBack
			pl = FreeCAD.Vector(startX, startY + sizeY - thickBack, startZ)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			MagicPanels.setColor(o4, 3, (1.0, 1.0, 1.0, 1.0), "color")
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = sizeX - (2 * edgeband)
			o5.Height = thick
			o5.Width = sizeY - thickFront - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgeband, startY + thickFront + edgeband, startZ + sizeZ - thick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o6.Label = translate('magicStart', 'Front')
			o6.Length = sizeX - (2 * thick) + offsetFrontL + offsetFrontR - (2 * edgeband)
			o6.Height = sizeZ - (2 * thick) + offsetFrontB + offsetFrontT - (2 * edgeband)
			o6.Width = thickFront
			pl = FreeCAD.Vector(startX + thick + edgeband - offsetFrontL, startY, startZ + thick + edgeband - offsetFrontB)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
			
			# Shelf
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o7.Label = translate('magicStart', 'Shelf')
			o7.Length = sizeX - (2 * thick) - (2 * edgebandE) - (2 * shelfOS)
			o7.Height = thickShelf
			o7.Width = sizeY - thickFront - thickBack - thick - edgeband - edgebandE
			px = startX + thick + edgebandE + shelfOS
			py = startY + thickFront + thick + edgeband
			pz = startZ + (sizeZ / 2) - (thickShelf / 2)
			o7.Placement = FreeCAD.Placement(FreeCAD.Vector(px, py, pz), self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5, o6, o7]
			label = "Furniture, Module"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF28(self):
			
			thick = MagicPanels.unit2value( self.oThickE.text() )
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			thickFront = MagicPanels.unit2value( self.oThickFrontE.text() )
			offsetFrontL = MagicPanels.unit2value( self.oOffsetFrontLE.text() )
			offsetFrontR = MagicPanels.unit2value( self.oOffsetFrontRE.text() )
			offsetFrontT = MagicPanels.unit2value( self.oOffsetFrontTE.text() )
			offsetFrontB = MagicPanels.unit2value( self.oOffsetFrontBE.text() )

			startX = MagicPanels.unit2value( self.oStartXE.text() )
			startY = MagicPanels.unit2value( self.oStartYE.text() )
			startZ = MagicPanels.unit2value( self.oStartZE.text() )
			
			sizeX = MagicPanels.unit2value( self.oWidthE.text() )
			sizeY = MagicPanels.unit2value( self.oDepthE.text() )
			sizeZ = MagicPanels.unit2value( self.oHeightE.text() )
			
			edgeband = MagicPanels.gEdgebandThickness
			if MagicPanels.gEdgebandApply == "everywhere":
				edgebandE = edgeband
			else:
				edgebandE = 0
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = sizeX - (2 * edgeband)
			o1.Height = thick
			o1.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgeband, startY + edgeband, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = thick
			o2.Height = sizeZ - (2 * thick) - (2 * edgebandE)
			o2.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX, startY + edgeband, startZ + thick + edgebandE)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = thick
			o3.Height = sizeZ - (2 * thick) - (2 * edgebandE)
			o3.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX + sizeX - thick, startY + edgeband, startZ + thick + edgebandE)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = sizeX - (2 * thick) - (2 * edgebandE)
			o4.Height = sizeZ - (2 * thick) - (2 * edgebandE)
			o4.Width = thickBack
			pl = FreeCAD.Vector(startX + thick + edgebandE, startY + sizeY - thickBack, startZ + thick + edgebandE)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = sizeX - (2 * edgeband)
			o5.Height = thick
			o5.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgeband, startY + edgeband, startZ + sizeZ - thick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o6.Label = translate('magicStart', 'Front')
			o6.Length = sizeX - (2 * thick) - offsetFrontL - offsetFrontR - (2 * edgeband)
			o6.Height = sizeZ - (2 * thick) - offsetFrontB - offsetFrontT - (2 * edgeband)
			o6.Width = thickFront
			pl = FreeCAD.Vector(startX + thick + edgeband + offsetFrontL, startY, startZ + thick + edgeband + offsetFrontB)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
			
			# Shelf
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o7.Label = translate('magicStart', 'Shelf')
			o7.Length = sizeX - (2 * thick) - (2 * edgebandE) - (2 * shelfOS)
			o7.Height = thickShelf
			o7.Width = sizeY - thickFront - thick - thickBack - edgeband - edgebandE
			px = startX + thick + edgebandE + shelfOS
			py = startY + thickFront + thick + edgeband
			pz = startZ + (sizeZ / 2) - (thickShelf / 2)
			o7.Placement = FreeCAD.Placement(FreeCAD.Vector(px, py, pz), self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5, o6, o7]
			label = "Furniture, Module"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF29(self):
			
			thick = MagicPanels.unit2value( self.oThickE.text() )
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			thickFront = MagicPanels.unit2value( self.oThickFrontE.text() )
			offsetFrontL = MagicPanels.unit2value( self.oOffsetFrontLE.text() )
			offsetFrontR = MagicPanels.unit2value( self.oOffsetFrontRE.text() )
			offsetFrontT = MagicPanels.unit2value( self.oOffsetFrontTE.text() )
			offsetFrontB = MagicPanels.unit2value( self.oOffsetFrontBE.text() )

			startX = MagicPanels.unit2value( self.oStartXE.text() )
			startY = MagicPanels.unit2value( self.oStartYE.text() )
			startZ = MagicPanels.unit2value( self.oStartZE.text() )
			
			sizeX = MagicPanels.unit2value( self.oWidthE.text() )
			sizeY = MagicPanels.unit2value( self.oDepthE.text() )
			sizeZ = MagicPanels.unit2value( self.oHeightE.text() )
			
			edgeband = MagicPanels.gEdgebandThickness
			if MagicPanels.gEdgebandApply == "everywhere":
				edgebandE = edgeband
			else:
				edgebandE = 0
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = sizeX - (2 * edgeband)
			o1.Height = thick
			o1.Width = sizeY - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgeband, startY + edgeband, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = thick
			o2.Height = sizeZ - (2 * thick) - (2 * edgebandE)
			o2.Width = sizeY - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX, startY + edgeband, startZ + thick + edgebandE)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = thick
			o3.Height = sizeZ - (2 * thick) - (2 * edgebandE)
			o3.Width = sizeY - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + sizeX - thick, startY + edgeband, startZ + thick + edgebandE)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back HDF
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = sizeX
			o4.Height = sizeZ
			o4.Width = thickBack
			pl = FreeCAD.Vector(startX, startY + sizeY - thickBack, startZ)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			MagicPanels.setColor(o4, 3, (1.0, 1.0, 1.0, 1.0), "color")
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = sizeX - (2 * edgeband)
			o5.Height = thick
			o5.Width = sizeY - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgeband, startY + edgeband, startZ + sizeZ - thick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o6.Label = translate('magicStart', 'Front')
			o6.Length = sizeX - (2 * thick) - offsetFrontL - offsetFrontR - (2 * edgeband)
			o6.Height = sizeZ - (2 * thick) - offsetFrontB - offsetFrontT - (2 * edgeband)
			o6.Width = thickFront
			pl = FreeCAD.Vector(startX + thick + edgeband + offsetFrontL, startY, startZ + thick + edgeband + offsetFrontB)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
			
			# Shelf
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o7.Label = translate('magicStart', 'Shelf')
			o7.Length = sizeX - (2 * thick) - (2 * edgebandE) - (2 * shelfOS)
			o7.Height = thickShelf
			o7.Width = sizeY - thickFront - thick - thickBack - edgeband -  edgebandE
			px = startX + thick + edgebandE + shelfOS
			py = startY + thickFront + thick + edgeband
			pz = startZ + (sizeZ / 2) - (thickShelf / 2)
			o7.Placement = FreeCAD.Placement(FreeCAD.Vector(px, py, pz), self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5, o6, o7]
			label = "Furniture, Module"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF30(self):
			
			p0X = MagicPanels.unit2value(self.ods61E.text())
			p0Y = MagicPanels.unit2value(self.ods62E.text())
			startZ = MagicPanels.unit2value(self.ods63E.text())
			
			gapX = MagicPanels.unit2value(self.ods7E.text())
			gapZ = MagicPanels.unit2value(self.ods8E.text())
			gapY = MagicPanels.unit2value(self.ods9E.text())
			
			num = int(self.ods2E.text())
			
			offset = 0 # there will be no offset between drawer gaps
			
			frontOffsetH = 2 * MagicPanels.unit2value(self.ods111E.text())
			frontOffsetV = 2 * MagicPanels.unit2value(self.ods112E.text())
			frontOffsetB = MagicPanels.unit2value(self.ods113E.text())
			
			thickFront = MagicPanels.unit2value(self.ods31E.text())
			thickSides = MagicPanels.unit2value(self.ods32E.text())
			thickBottom = MagicPanels.unit2value(self.ods33E.text())
			
			sidesOF = MagicPanels.unit2value(self.ods41E.text())
			sideOF = sidesOF / 2
			backOF = MagicPanels.unit2value(self.ods42E.text())
			topOF = MagicPanels.unit2value(self.ods43E.text())
			bottomOF = MagicPanels.unit2value(self.ods44E.text())
			
			zoffsets = (num - 1) * frontOffsetB
			zspace = (num * gapZ) + frontOffsetV
			frontHeight = (zspace - zoffsets) / num
			
			for i in range(0, num):
			
				p0Z = startZ + (i * (gapZ + offset))
			
				# Left Side
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSLeft")
				o1.Label = translate('magicStart', 'DS ' + str(i+1) + ' Left')
				o1.Length = thickSides
				o1.Height = gapZ - bottomOF - topOF - thickBottom
				o1.Width = gapY - backOF
				pl = FreeCAD.Vector(p0X + sideOF, p0Y, p0Z + bottomOF + thickBottom)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o1, 0, (1.0, 1.0, 1.0, 1.0), "color")
				
				# Right Side
				o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSRight")
				o2.Label = translate('magicStart', 'DS ' + str(i+1) + ' Right')
				o2.Length = thickSides
				o2.Height = gapZ - bottomOF - topOF - thickBottom
				o2.Width = gapY - backOF
				pl = FreeCAD.Vector(p0X + gapX - thickSides - sideOF, p0Y, p0Z + bottomOF + thickBottom)
				o2.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o2, 0, (1.0, 1.0, 1.0, 1.0), "color")
				
				# Back
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBack")
				o3.Label = translate('magicStart', 'DS ' + str(i+1) + ' Back')
				o3.Length = gapX - (2 * thickSides) - sidesOF
				o3.Height = gapZ - bottomOF - topOF - thickBottom
				o3.Width = thickSides
				pl = FreeCAD.Vector(p0X + sideOF + thickSides, p0Y + gapY - thickSides - backOF, p0Z + bottomOF + thickBottom)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
				
				# Front inside
				o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSFrontInside")
				o4.Label = translate('magicStart', 'DS ' + str(i+1) + ' Front Inside')
				o4.Length = gapX - (2 * thickSides) - sidesOF
				o4.Height = gapZ - bottomOF - topOF - thickBottom
				o4.Width = thickSides
				pl = FreeCAD.Vector(p0X + sideOF + thickSides, p0Y, p0Z + bottomOF + thickBottom)
				o4.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o4, 0, (1.0, 1.0, 1.0, 1.0), "color")

				# HDF bottom
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBottom")
				o5.Label = translate('magicStart', 'DS ' + str(i+1) + ' Bottom HDF')
				o5.Length = gapX - sidesOF
				o5.Height = thickBottom
				o5.Width = gapY - backOF
				pl = FreeCAD.Vector(p0X + sideOF, p0Y, p0Z  + bottomOF)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				colors = [ self.gColor, self.gColor, self.gColor, self.gColor, self.gColor, (1.0, 1.0, 1.0, 1.0) ]
				MagicPanels.setColor(o5, 0, colors, "color")

				# Front outside
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSFrontOutside")
				o6.Label = translate('magicStart', 'DS ' + str(i+1) + ' Front Outside')
				o6.Length = gapX + frontOffsetH
				o6.Height = frontHeight
				o6.Width = thickFront
				pz = (startZ - (frontOffsetV / 2)) + (i * (frontHeight + frontOffsetB)) 
				pl = FreeCAD.Vector(p0X - (frontOffsetH / 2), p0Y - thickFront, pz)
				o6.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o6, 0, self.gColor, "color")

				objects = [o1, o2, o3, o4, o5, o6]
				label = "Container, Drawer series " + str(i+1)
				container = MagicPanels.createContainer(objects, label, False)
				
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF31(self):
			
			p0X = MagicPanels.unit2value(self.ods61E.text())
			p0Y = MagicPanels.unit2value(self.ods62E.text())
			startZ = MagicPanels.unit2value(self.ods63E.text())
			
			gapX = MagicPanels.unit2value(self.ods7E.text())
			gapZ = MagicPanels.unit2value(self.ods8E.text())
			gapY = MagicPanels.unit2value(self.ods9E.text())
			
			num = int(self.ods2E.text())
			
			offset = 0 # there will be no offset between drawer gaps

			frontOffsetH = 2 * MagicPanels.unit2value(self.ods111E.text())
			frontOffsetV = 2 * MagicPanels.unit2value(self.ods112E.text())
			frontOffsetB = MagicPanels.unit2value(self.ods113E.text())

			thickFront = MagicPanels.unit2value(self.ods31E.text())
			thickSides = MagicPanels.unit2value(self.ods32E.text())
			thickBottom = MagicPanels.unit2value(self.ods33E.text())
			
			sidesOF = MagicPanels.unit2value(self.ods41E.text())
			sideOF = sidesOF / 2
			backOF = MagicPanels.unit2value(self.ods42E.text())
			topOF = MagicPanels.unit2value(self.ods43E.text())
			bottomOF = MagicPanels.unit2value(self.ods44E.text())
			
			zoffsets = (num - 1) * frontOffsetB
			zspace = (num * gapZ) - frontOffsetV
			frontHeight = (zspace - zoffsets) / num

			for i in range(0, num):
			
				p0Z = startZ + (i * (gapZ + offset))
				
				# Left Side
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSLeft")
				o1.Label = translate('magicStart', 'DS ' + str(i+1) + ' Left')
				o1.Length = thickSides
				o1.Height = gapZ - bottomOF - topOF - thickBottom
				o1.Width = gapY - backOF - thickFront
				pl = FreeCAD.Vector(p0X + sideOF, p0Y + thickFront, p0Z + bottomOF + thickBottom)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o1, 0, (1.0, 1.0, 1.0, 1.0), "color")
				
				# Right Side
				o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSRight")
				o2.Label = translate('magicStart', 'DS ' + str(i+1) + ' Right')
				o2.Length = thickSides
				o2.Height = gapZ - bottomOF - topOF - thickBottom
				o2.Width = gapY - backOF - thickFront
				pl = FreeCAD.Vector(p0X + gapX - sideOF - thickSides, p0Y + thickFront, p0Z + bottomOF + thickBottom)
				o2.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o2, 0, (1.0, 1.0, 1.0, 1.0), "color")
				
				# Back
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBack")
				o3.Label = translate('magicStart', 'DS ' + str(i+1) + ' Back')
				o3.Length = gapX - (2 * thickSides) - sidesOF
				o3.Height = gapZ - bottomOF - topOF - thickBottom
				o3.Width = thickSides
				pl = FreeCAD.Vector(p0X + sideOF + thickSides, p0Y + gapY - backOF - thickSides, p0Z + bottomOF + thickBottom)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
				
				# Front inside
				o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSFrontInside")
				o4.Label = translate('magicStart', 'DS ' + str(i+1) + ' Front Inside')
				o4.Length = gapX - (2 * thickSides) - sidesOF
				o4.Height = gapZ - bottomOF - topOF - thickBottom
				o4.Width = thickSides
				pl = FreeCAD.Vector(p0X + sideOF + thickSides, p0Y + thickFront, p0Z + bottomOF + thickBottom)
				o4.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o4, 0, (1.0, 1.0, 1.0, 1.0), "color")

				# HDF bottom
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBottom")
				o5.Label = translate('magicStart', 'DS ' + str(i+1) + ' Bottom HDF')
				o5.Length = gapX - sidesOF
				o5.Height = thickBottom
				o5.Width = gapY - backOF - thickFront
				pl = FreeCAD.Vector(p0X + sideOF, p0Y + thickFront, p0Z  + bottomOF)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				colors = [ self.gColor, self.gColor, self.gColor, self.gColor, self.gColor, (1.0, 1.0, 1.0, 1.0) ]
				MagicPanels.setColor(o5, 0, colors, "color")

				# Front outside make inside as well
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSFrontOutside")
				o6.Label = translate('magicStart', 'DS ' + str(i+1) + ' Front Outside')
				o6.Length = gapX - frontOffsetH
				o6.Height = frontHeight
				o6.Width = thickFront
				pz = (startZ + (frontOffsetV / 2)) + (i * (frontHeight + frontOffsetB)) 
				pl = FreeCAD.Vector(p0X + (frontOffsetH/2), p0Y, pz)
				o6.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o6, 0, self.gColor, "color")

				objects = [o1, o2, o3, o4, o5, o6]
				label = "Container, Drawer series " + str(i+1)
				container = MagicPanels.createContainer(objects, label, False)
				
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF32(self):
			
			barWidth = MagicPanels.unit2value(self.offrame2E.text())
			barThick = MagicPanels.unit2value(self.offrame3E.text())
			
			FSX = MagicPanels.unit2value(self.offrame71E.text())
			FSY = MagicPanels.unit2value(self.offrame72E.text())
			FSZ = MagicPanels.unit2value(self.offrame73E.text())
			
			FFWidth = MagicPanels.unit2value(self.offrame8E.text())
			FFHeight = MagicPanels.unit2value(self.offrame9E.text())
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFLeft")
			o1.Label = translate('magicStart', 'Face Frame Left')
			o1.Length = barWidth
			o1.Height = FFHeight - (2 * barWidth)
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + barWidth)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFRight")
			o2.Label = translate('magicStart', 'Face Frame Right')
			o2.Length = barWidth
			o2.Height = FFHeight - (2 * barWidth)
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFBottom")
			o3.Label = translate('magicStart', 'Face Frame Bottom')
			o3.Length = FFWidth
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFTop")
			o4.Label = translate('magicStart', 'Face Frame Top')
			o4.Length = FFWidth
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4]
			label = "Container, Face Frame"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF33(self):
			
			barWidth = MagicPanels.unit2value(self.offrame2E.text())
			barThick = MagicPanels.unit2value(self.offrame3E.text())
			
			FSX = MagicPanels.unit2value(self.offrame71E.text())
			FSY = MagicPanels.unit2value(self.offrame72E.text())
			FSZ = MagicPanels.unit2value(self.offrame73E.text())
			
			FFWidth = MagicPanels.unit2value(self.offrame8E.text())
			FFHeight = MagicPanels.unit2value(self.offrame9E.text())
			
			centerFSX = FSX + (FFWidth / 2) - barWidth

			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFLeft")
			o1.Label = translate('magicStart', 'Face Frame Left')
			o1.Length = barWidth
			o1.Height = FFHeight - (2 * barWidth)
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + barWidth)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFRight")
			o2.Label = translate('magicStart', 'Face Frame Right')
			o2.Length = barWidth
			o2.Height = FFHeight - (2 * barWidth)
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFBottom")
			o3.Label = translate('magicStart', 'Face Frame Bottom')
			o3.Length = FFWidth
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFTop")
			o4.Label = translate('magicStart', 'Face Frame Top')
			o4.Length = FFWidth
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Center Side
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFCenter")
			o5.Label = translate('magicStart', 'Face Frame Center')
			o5.Length = 2 * barWidth
			o5.Height = FFHeight - (2 * barWidth)
			o5.Width = barThick
			pl = FreeCAD.Vector(centerFSX, FSY, FSZ + barWidth)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4, o5]
			label = "Container, Face Frame"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF34(self):
			
			barWidth = MagicPanels.unit2value(self.offrame2E.text())
			barThick = MagicPanels.unit2value(self.offrame3E.text())
			
			FSX = MagicPanels.unit2value(self.offrame71E.text())
			FSY = MagicPanels.unit2value(self.offrame72E.text())
			FSZ = MagicPanels.unit2value(self.offrame73E.text())
			
			FFWidth = MagicPanels.unit2value(self.offrame8E.text())
			FFHeight = MagicPanels.unit2value(self.offrame9E.text())
			
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
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFRight")
			o2.Label = translate('magicStart', 'Face Frame Right')
			o2.Length = barWidth
			o2.Height = FFHeight - (2 * barWidth)
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFBottom")
			o3.Label = translate('magicStart', 'Face Frame Bottom')
			o3.Length = FFWidth
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFTop")
			o4.Label = translate('magicStart', 'Face Frame Top')
			o4.Length = FFWidth
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Center Side
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFCenter")
			o5.Label = translate('magicStart', 'Face Frame Center')
			o5.Length = 2 * barWidth
			o5.Height = FFHeight - (2 * barWidth)
			o5.Width = barThick
			pl = FreeCAD.Vector(centerFSX, FSY, FSZ + barWidth)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Horizontal bar
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFHorizontal")
			o6.Label = translate('magicStart', 'Face Frame Horizontal')
			o6.Length = (FFWidth / 2) - barWidth - barWidth
			o6.Height = 2 * barWidth
			o6.Width = barThick
			pl = FreeCAD.Vector(horizontalFSX, FSY, horizontalFSZ)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5, o6]
			label = "Container, Face Frame"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF35(self):
			
			self.gFSX = MagicPanels.unit2value(self.oWidthE.text())
			self.gFSZ = MagicPanels.unit2value(self.oHeightE.text())
			self.gFSY = MagicPanels.unit2value(self.oDepthE.text())
			self.gThick = MagicPanels.unit2value(self.oThickE.text())

			# Face Frame predefined
			
			barWidth = 38
			barThick = 19
			
			# Furniture - settings
			
			sx = MagicPanels.unit2value(self.oStartXE.text())
			sy = MagicPanels.unit2value(self.oStartYE.text()) + barThick
			sz = MagicPanels.unit2value(self.oStartZE.text())
			
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
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back HDF
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX
			o4.Height = self.gFSZ - self.gThick
			o4.Width = 3
			pl = FreeCAD.Vector(sx, sy + depth, sz + self.gThick)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			MagicPanels.setColor(o4, 3, (1.0, 1.0, 1.0, 1.0), "color")
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX - (2 * self.gThick)
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy, sz + self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")

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

			objects = [o1, o2, o3, o4, o5, ff1, ff2, ff3, ff4, ff5, ff6]
			label = "Furniture, Module"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF36(self):
			
			self.gFSX = MagicPanels.unit2value(self.oWidthE.text())
			self.gFSZ = MagicPanels.unit2value(self.oHeightE.text())
			self.gFSY = MagicPanels.unit2value(self.oDepthE.text())
			self.gThick = MagicPanels.unit2value(self.oThickE.text())

			# Face Frame predefined
			
			barWidth = 38
			barThick = 19
			
			# Furniture - settings
			
			sx = MagicPanels.unit2value(self.oStartXE.text())
			sy = MagicPanels.unit2value(self.oStartYE.text()) + barThick
			sz = MagicPanels.unit2value(self.oStartZE.text())
			
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
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ - (2 * self.gThick)
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + self.gThick)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ - (2 * self.gThick)
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz + self.gThick)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back HDF
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX
			o4.Height = self.gFSZ
			o4.Width = 3
			pl = FreeCAD.Vector(sx, sy + depth, sz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			MagicPanels.setColor(o4, 3, (1.0, 1.0, 1.0, 1.0), "color")
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")

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
			
			objects = [o1, o2, o3, o4, o5, ff1, ff2, ff3, ff4, ff5, ff6, ff7]
			label = "Furniture, Module"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF37(self):
			
			barThick = MagicPanels.unit2value(self.ofglass2E.text())
			barWidth = MagicPanels.unit2value(self.ofglass8E.text())
			
			glassThick = MagicPanels.unit2value(self.ofglass5E.text())
			glassSink = 6
			
			FSX = MagicPanels.unit2value(self.ofglass71E.text())
			FSY = MagicPanels.unit2value(self.ofglass72E.text())
			FSZ = MagicPanels.unit2value(self.ofglass73E.text())
			
			FFWidth = MagicPanels.unit2value(self.ofglass9E.text())
			FFHeight = MagicPanels.unit2value(self.ofglass10E.text())
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGLeft")
			o1.Label = translate('magicStart', 'FG Left')
			o1.Length = barWidth
			o1.Height = FFHeight - (2 * barWidth)
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + barWidth)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGRight")
			o2.Label = translate('magicStart', 'FG Right')
			o2.Length = barWidth
			o2.Height = FFHeight - (2 * barWidth)
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGBottom")
			o3.Label = translate('magicStart', 'FG Bottom')
			o3.Length = FFWidth
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGTop")
			o4.Label = translate('magicStart', 'FG Top')
			o4.Length = FFWidth
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o5, 0, 60, "trans", "RGBA")
			
			objects = [o1, o2, o3, o4, o5]
			label = "Container, Front with GLass"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF38(self):
			
			barThick = MagicPanels.unit2value(self.ofglass2E.text())
			barWidth = MagicPanels.unit2value(self.ofglass8E.text())
			
			glassThick = MagicPanels.unit2value(self.ofglass5E.text())
			glassSink = 6
			
			decWidth = int(barWidth/4)
			decThick = int( (barThick - glassThick) / 2 )
			
			FSX = MagicPanels.unit2value(self.ofglass71E.text())
			FSY = MagicPanels.unit2value(self.ofglass72E.text())
			FSZ = MagicPanels.unit2value(self.ofglass73E.text())
			
			FFWidth = MagicPanels.unit2value(self.ofglass9E.text())
			FFHeight = MagicPanels.unit2value(self.ofglass10E.text())
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGLeft")
			o1.Label = translate('magicStart', 'FG Left')
			o1.Length = barWidth
			o1.Height = FFHeight - (2 * barWidth)
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + barWidth)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGRight")
			o2.Label = translate('magicStart', 'FG Right')
			o2.Length = barWidth
			o2.Height = FFHeight - (2 * barWidth)
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ + barWidth)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGBottom")
			o3.Label = translate('magicStart', 'FG Bottom')
			o3.Length = FFWidth
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGTop")
			o4.Label = translate('magicStart', 'FG Top')
			o4.Length = FFWidth
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o5, 0, 60, "trans", "RGBA")
			
			# Vertical decoration
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "FGVertical")
			o6.Label = translate('magicStart', 'FG Vertical')
			o6.Length = decWidth
			o6.Height = FFHeight - (2 * barWidth)
			o6.Width = decThick
			plx = FSX + (FFWidth / 2) - (decWidth / 2)
			pl = FreeCAD.Vector(plx, FSY, FSZ + barWidth)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o7, 0, self.gColor, "color")
		
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
			MagicPanels.setColor(o8, 0, self.gColor, "color")
		
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
			MagicPanels.setColor(o9, 0, self.gColor, "color")
		
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
			MagicPanels.setColor(o10, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4, o5, o6, o7, o8, o9, o10]
			label = "Container, Front with GLass"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF41(self):
	
			thick = MagicPanels.unit2value(self.oshs1E.text())
			num = int(self.oshs2E.text())
			
			p0X = MagicPanels.unit2value(self.oshs41E.text())
			p0Y = MagicPanels.unit2value(self.oshs42E.text())
			p0Z = MagicPanels.unit2value(self.oshs43E.text())
			
			width = MagicPanels.unit2value(self.oshs5E.text())
			depth = MagicPanels.unit2value(self.oshs6E.text())
			offset = MagicPanels.unit2value(self.oshs7E.text())
			
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
				MagicPanels.setColor(o1, 0, self.gColor, "color")
				
				shelvesArr.append(o1)
			
			label = "Container, Shelf Series"
			container = MagicPanels.createContainer(shelvesArr, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF42(self):
			
			width = MagicPanels.unit2value(self.oTableSizeXE.text())
			depth = MagicPanels.unit2value(self.oTableSizeYE.text())
			height = MagicPanels.unit2value(self.oTableSizeZE.text())
			topThick = MagicPanels.unit2value(self.oTableTopThickE.text())
			legThick = MagicPanels.unit2value(self.oTableLegThickE.text())
			offset = MagicPanels.unit2value(self.oTableTopOffsetE.text())
			
			sx = MagicPanels.unit2value(self.oTableStartXE.text())
			sy = MagicPanels.unit2value(self.oTableStartYE.text())
			sz = MagicPanels.unit2value(self.oTableStartZE.text())
			
			# Leg Left Front
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLF")
			o1.Label = translate('magicStart', 'Table Leg LF')
			o1.Length = legThick
			o1.Height = height - topThick
			o1.Width = legThick
			pl = FreeCAD.Vector(sx + offset, sy + offset, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Leg Left Back
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLB")
			o2.Label = translate('magicStart', 'Table Leg LB')
			o2.Length = legThick
			o2.Height = height - topThick
			o2.Width = legThick
			psy = sy + depth - offset - legThick
			pl = FreeCAD.Vector(sx + offset, psy, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Leg Right Front
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLRF")
			o3.Label = translate('magicStart', 'Table Leg RF')
			o3.Length = legThick
			o3.Height = height - topThick
			o3.Width = legThick
			psx = sx + width - offset - legThick
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o6, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o7, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o8, 0, self.gColor, "color")
			
			# Table Top
			o9 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableTop")
			o9.Label = translate('magicStart', 'Table Top')
			o9.Length = width
			o9.Height = topThick
			o9.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + height - topThick)
			o9.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o9, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4, o5, o6, o7, o8, o9]
			label = "Container, Table"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF44(self):
			
			width = MagicPanels.unit2value(self.oTableSizeXE.text())
			depth = MagicPanels.unit2value(self.oTableSizeYE.text())
			height = MagicPanels.unit2value(self.oTableSizeZE.text())
			topThick = MagicPanels.unit2value(self.oTableTopThickE.text())
			legThick = MagicPanels.unit2value(self.oTableLegThickE.text())
			offset = MagicPanels.unit2value(self.oTableTopOffsetE.text())
			
			sx = MagicPanels.unit2value(self.oTableStartXE.text())
			sy = MagicPanels.unit2value(self.oTableStartYE.text())
			sz = MagicPanels.unit2value(self.oTableStartZE.text())
			
			# Leg Left Front
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLF1")
			o1.Label = translate('magicStart', 'Table Leg LF1')
			o1.Length = topThick
			o1.Height = height - topThick
			o1.Width = legThick
			pl = FreeCAD.Vector(sx + offset, sy + offset, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Leg Left Front
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLF2")
			o2.Label = translate('magicStart', 'Table Leg LF2')
			o2.Length = legThick
			o2.Height = height - topThick
			o2.Width = topThick
			pl = FreeCAD.Vector(sx + offset, sy + offset, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Leg Left Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLB1")
			o3.Label = translate('magicStart', 'Table Leg LB1')
			o3.Length = topThick
			o3.Height = height - topThick
			o3.Width = legThick
			psy = sy + depth - offset - legThick
			pl = FreeCAD.Vector(sx + offset, psy, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Leg Left Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLLB2")
			o4.Label = translate('magicStart', 'Table Leg LB2')
			o4.Length = legThick
			o4.Height = height - topThick
			o4.Width = topThick
			psy = sy + depth - offset - topThick
			pl = FreeCAD.Vector(sx + offset, psy, sz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Leg Right Front
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLRF1")
			o5.Label = translate('magicStart', 'Table Leg RF1')
			o5.Length = legThick
			o5.Height = height - topThick
			o5.Width = topThick
			psx = sx + width - offset - legThick
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Leg Right Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLRF2")
			o6.Label = translate('magicStart', 'Table Leg RF2')
			o6.Length = topThick
			o6.Height = height - topThick
			o6.Width = legThick
			psx = sx + width - offset - topThick
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o7, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o8, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o9, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o10, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o11, 0, self.gColor, "color")
			
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
			MagicPanels.setColor(o12, 0, self.gColor, "color")
			
			# Table Top
			o13 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableTop")
			o13.Label = translate('magicStart', 'Table Top')
			o13.Length = width
			o13.Height = topThick
			o13.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz + height - topThick)
			o13.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o13, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4, o5, o6, o7, o8, o9, o10, o11, o12, o13]
			label = "Container, Table"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF46(self):
			
			width = MagicPanels.unit2value(self.oTableSizeXE.text())
			depth = MagicPanels.unit2value(self.oTableSizeYE.text())
			height = MagicPanels.unit2value(self.oTableSizeZE.text())
			topThick = MagicPanels.unit2value(self.oTableTopThickE.text())
			legThick = MagicPanels.unit2value(self.oTableLegThickE.text())
			offset = MagicPanels.unit2value(self.oTableTopOffsetE.text())
			
			sx = MagicPanels.unit2value(self.oTableStartXE.text())
			sy = MagicPanels.unit2value(self.oTableStartYE.text())
			sz = MagicPanels.unit2value(self.oTableStartZE.text())
			
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
			MagicPanels.setColor(o9, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4, o5, o6, o7, o8, o9]
			label = "Container, Table"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF48(self):
	
			p0X = MagicPanels.unit2value(self.oside51E.text())
			p0Y = MagicPanels.unit2value(self.oside52E.text())
			p0Z = MagicPanels.unit2value(self.oside53E.text())
			
			width = MagicPanels.unit2value(self.oside6E.text())
			height = MagicPanels.unit2value(self.oside7E.text())
			thick = MagicPanels.unit2value(self.oside1E.text())
			
			if self.gSideEdgePlane == "X":
				
				# Side
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Side")
				o1.Label = translate('magicStart', 'Side')
				o1.Length = width
				o1.Height = height
				o1.Width = thick
				pl = FreeCAD.Vector(p0X, p0Y, p0Z)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o1, 0, self.gColor, "color")
				
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
				MagicPanels.setColor(o1, 0, self.gColor, "color")
				
				# recompute
				FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF59(self):
			
			barThick = MagicPanels.unit2value(self.odf2E.text())
			barWidth = MagicPanels.unit2value(self.odf8E.text())
			
			innerThick = MagicPanels.unit2value(self.odf5E.text())
			innerSink = 6
			
			FSX = MagicPanels.unit2value(self.odf71E.text())
			FSY = MagicPanels.unit2value(self.odf72E.text())
			FSZ = MagicPanels.unit2value(self.odf73E.text())
			
			FFWidth = MagicPanels.unit2value(self.odf9E.text())
			FFHeight = MagicPanels.unit2value(self.odf10E.text())
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "DFLeft")
			o1.Label = translate('magicStart', 'DF Left')
			o1.Length = barWidth
			o1.Height = FFHeight
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "DFRight")
			o2.Label = translate('magicStart', 'DF Right')
			o2.Length = barWidth
			o2.Height = FFHeight
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DFBottom")
			o3.Label = translate('magicStart', 'DF Bottom')
			o3.Length = FFWidth - (2 * barWidth)
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX + barWidth, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "DFTop")
			o4.Label = translate('magicStart', 'DF Top')
			o4.Length = FFWidth - (2 * barWidth)
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX + barWidth, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Inner
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DFInner")
			o5.Label = translate('magicStart', 'DF Inner')
			o5.Length = FFWidth - (2 * barWidth) + (2 * innerSink)
			o5.Height = FFHeight - (2 * barWidth) + (2 * innerSink)
			o5.Width = innerThick
			plx = FSX + barWidth - innerSink
			ply = FSY + (barThick/2) - (innerThick/2)
			plz = FSZ + barWidth - innerSink
			pl = FreeCAD.Vector(plx, ply, plz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4, o5]
			label = "Container, Decorative front"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF61(self):
			
			barWidth = MagicPanels.unit2value(self.ofdec2E.text())
			barThick = MagicPanels.unit2value(self.ofdec3E.text())
			offsetH = MagicPanels.unit2value(self.ofdecOHE.text())
			offsetV = MagicPanels.unit2value(self.ofdecOVE.text())
			
			FSX = MagicPanels.unit2value(self.ofdec61E.text())
			FSY = MagicPanels.unit2value(self.ofdec62E.text())
			FSZ = MagicPanels.unit2value(self.ofdec63E.text())
			
			FFWidth = MagicPanels.unit2value(self.ofdec7E.text())
			FFHeight = MagicPanels.unit2value(self.ofdec8E.text())
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FDLeft")
			o1.Label = translate('magicStart', 'FD Left')
			o1.Length = barWidth
			o1.Height = FFHeight
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FDRight")
			o2.Label = translate('magicStart', 'FD Right')
			o2.Length = barWidth
			o2.Height = FFHeight
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FDBottom")
			o3.Label = translate('magicStart', 'FD Bottom')
			o3.Length = FFWidth
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FDTop")
			o4.Label = translate('magicStart', 'FD Top')
			o4.Length = FFWidth
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4]
			label = "Container, Front decoration"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

			# ############################################################################
		def createF62(self):
			
			barWidth = MagicPanels.unit2value(self.osdec2E.text())
			barThick = MagicPanels.unit2value(self.osdec3E.text())
			offsetH = MagicPanels.unit2value(self.osdecOHE.text())
			offsetV = MagicPanels.unit2value(self.osdecOVE.text())
			
			FSX = MagicPanels.unit2value(self.osdec61E.text())
			FSY = MagicPanels.unit2value(self.osdec62E.text())
			FSZ = MagicPanels.unit2value(self.osdec63E.text())
			
			FFWidth = MagicPanels.unit2value(self.osdec7E.text())
			FFHeight = MagicPanels.unit2value(self.osdec8E.text())
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "SDLeft")
			o1.Label = translate('magicStart', 'SD Left')
			o1.Length = barThick
			o1.Height = FFHeight
			o1.Width = barWidth
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "SDRight")
			o2.Label = translate('magicStart', 'SD Right')
			o2.Length = barThick
			o2.Height = FFHeight
			o2.Width = barWidth
			pl = FreeCAD.Vector(FSX, FSY + FFWidth - barWidth, FSZ)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "SDBottom")
			o3.Label = translate('magicStart', 'SD Bottom')
			o3.Length = barThick
			o3.Height = barWidth
			o3.Width = FFWidth
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "SDTop")
			o4.Label = translate('magicStart', 'SD Top')
			o4.Length = barThick
			o4.Height = barWidth
			o4.Width = FFWidth
			pl = FreeCAD.Vector(FSX, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4]
			label = "Container, Side decoration"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF64(self):
			
			barWidth = MagicPanels.unit2value(self.offrame2E.text())
			barThick = MagicPanels.unit2value(self.offrame3E.text())
			
			FSX = MagicPanels.unit2value(self.offrame71E.text())
			FSY = MagicPanels.unit2value(self.offrame72E.text())
			FSZ = MagicPanels.unit2value(self.offrame73E.text())
			
			FFWidth = MagicPanels.unit2value(self.offrame8E.text())
			FFHeight = MagicPanels.unit2value(self.offrame9E.text())
			
			centerFSX = FSX + (FFWidth / 2) - barWidth
			horizontalFSX = FSX + (FFWidth / 2) + barWidth
			horizontalFSZ = FSZ + (FFHeight / 2) - barWidth
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFLeft")
			o1.Label = translate('magicStart', 'Face Frame Left')
			o1.Length = barWidth
			o1.Height = FFHeight
			o1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFRight")
			o2.Label = translate('magicStart', 'Face Frame Right')
			o2.Length = barWidth
			o2.Height = FFHeight
			o2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Bottom
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFBottom")
			o3.Label = translate('magicStart', 'Face Frame Bottom')
			o3.Length = FFWidth - (2 * barWidth)
			o3.Height = barWidth
			o3.Width = barThick
			pl = FreeCAD.Vector(FSX + barWidth, FSY, FSZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFTop")
			o4.Label = translate('magicStart', 'Face Frame Top')
			o4.Length = FFWidth- (2 * barWidth)
			o4.Height = barWidth
			o4.Width = barThick
			pl = FreeCAD.Vector(FSX + barWidth, FSY, FSZ + FFHeight - barWidth)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Center Side
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFCenter")
			o5.Label = translate('magicStart', 'Face Frame Center')
			o5.Length = 2 * barWidth
			o5.Height = FFHeight - (2 * barWidth)
			o5.Width = barThick
			pl = FreeCAD.Vector(centerFSX, FSY, FSZ + barWidth)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Horizontal bar
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFHorizontal")
			o6.Label = translate('magicStart', 'Face Frame Horizontal')
			o6.Length = (FFWidth / 2) - barWidth - barWidth
			o6.Height = 2 * barWidth
			o6.Width = barThick
			pl = FreeCAD.Vector(horizontalFSX, FSY, horizontalFSZ)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5, o6]
			label = "Container, Face Frame"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF65(self):
			
			self.gFSX = MagicPanels.unit2value(self.oWidthE.text())
			self.gFSZ = MagicPanels.unit2value(self.oHeightE.text())
			self.gFSY = MagicPanels.unit2value(self.oDepthE.text())
			self.gThick = MagicPanels.unit2value(self.oThickE.text())
			bcthick = MagicPanels.unit2value( self.oThickBackE.text() )
			
			# #################################################################
			# settings
			# #################################################################
			
			barWidth = 50.8                         # face frame bar width
			barThick = 25.4                         # face frame bar thickness
			bfco = 88.9 + 19.05                     # bottom floor cut + offset
			bfflip = 19.05                          # bottom face frame lip
			sfflip = 25.4                           # side face frame lip
			sbsize = 76.2                           # supporters bar size
			
			depth = self.gFSY - bcthick - barThick  # cabinet depth
			FFWidth = self.gFSX + (2 * sfflip)      # face freame width
			FFHeight = self.gFSZ - bfco + bfflip    # face frame height
			
			# start position calculation
			
			sx = MagicPanels.unit2value(self.oStartXE.text())
			sy = MagicPanels.unit2value(self.oStartYE.text()) + barThick
			sz = MagicPanels.unit2value(self.oStartZE.text())
			
			# face frame position calculation

			FSX = sx - sfflip
			FSY = sy - barThick
			FSZ = sz + bfco - bfflip
			
			centerFSX = FSX + (FFWidth / 2) - barWidth
			horizontalFSX = FSX + (FFWidth / 2) + barWidth
			horizontalFSZ = FSZ + (FFHeight / 2) - barWidth
			
			# #####################################################
			# Furniture - draw
			# #####################################################
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX - (2 * self.gThick)
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy, sz + bfco)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX
			o4.Height = self.gFSZ - bfco
			o4.Width = bcthick
			pl = FreeCAD.Vector(sx, sy + depth, sz + bfco)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Support top 1
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "supporter1")
			o5.Label = translate('magicStart', 'ST 1')
			o5.Length = self.gFSX - (2 * self.gThick)
			o5.Height = self.gThick
			o5.Width = sbsize
			pl = FreeCAD.Vector(sx + self.gThick, sy, sz + self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")

			# Support top 2
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "supporter2")
			o6.Label = translate('magicStart', 'ST 2')
			o6.Length = self.gFSX - (2 * self.gThick)
			o6.Height = self.gThick
			o6.Width = sbsize
			pl = FreeCAD.Vector(sx + self.gThick, sy + depth - sbsize, sz + self.gFSZ - self.gThick)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
			
			# Support back 1
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "supporter3")
			o7.Label = translate('magicStart', 'SB 1')
			o7.Length = self.gFSX - (2 * self.gThick)
			o7.Height = sbsize
			o7.Width = self.gThick
			pl = FreeCAD.Vector(sx + self.gThick, sy + depth - self.gThick, sz + self.gFSZ - sbsize - self.gThick)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")

			# Face Frame - draw

			# Left Side
			ff1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFLeft")
			ff1.Label = translate('magicStart', 'FF Left')
			ff1.Length = barWidth
			ff1.Height = FFHeight
			ff1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			ff1.Placement = FreeCAD.Placement(pl, self.gR)
			ff1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			ff2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFRight")
			ff2.Label = translate('magicStart', 'FF Right')
			ff2.Length = barWidth
			ff2.Height = FFHeight
			ff2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidth, FSY, FSZ)
			ff2.Placement = FreeCAD.Placement(pl, self.gR)
			ff2.ViewObject.ShapeColor = self.gColor
			
			# Bottom
			ff3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFBottom")
			ff3.Label = translate('magicStart', 'FF Bottom')
			ff3.Length = FFWidth - (2 * barWidth)
			ff3.Height = barWidth
			ff3.Width = barThick
			pl = FreeCAD.Vector(FSX + barWidth, FSY, FSZ)
			ff3.Placement = FreeCAD.Placement(pl, self.gR)
			ff3.ViewObject.ShapeColor = self.gColor
			
			# Top
			ff4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFTop")
			ff4.Label = translate('magicStart', 'FF Top')
			ff4.Length = FFWidth - (2 * barWidth)
			ff4.Height = barWidth
			ff4.Width = barThick
			pl = FreeCAD.Vector(FSX + barWidth, FSY, FSZ + FFHeight - barWidth)
			ff4.Placement = FreeCAD.Placement(pl, self.gR)
			ff4.ViewObject.ShapeColor = self.gColor
			
			# Center Side
			ff5 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFCenter")
			ff5.Label = translate('magicStart', 'FF Center')
			ff5.Length = 2 * barWidth
			ff5.Height = FFHeight - (2 * barWidth)
			ff5.Width = barThick
			pl = FreeCAD.Vector(centerFSX, FSY, FSZ + barWidth)
			ff5.Placement = FreeCAD.Placement(pl, self.gR)
			ff5.ViewObject.ShapeColor = self.gColor
			
			# Horizontal bar
			ff6 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFHorizontal")
			ff6.Label = translate('magicStart', 'FF Horizontal')
			ff6.Length = (FFWidth / 2) - barWidth - barWidth
			ff6.Height = 2 * barWidth
			ff6.Width = barThick
			pl = FreeCAD.Vector(horizontalFSX, FSY, horizontalFSZ)
			ff6.Placement = FreeCAD.Placement(pl, self.gR)
			ff6.ViewObject.ShapeColor = self.gColor

			objects = [o1, o2, o3, o4, o5, o6, o7, ff1, ff2, ff3, ff4, ff5, ff6]
			label = "Furniture, Module"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF66(self):
			
			thick = MagicPanels.unit2value( self.oThickE.text() )
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			thickFront = MagicPanels.unit2value( self.oThickFrontE.text() )
			offsetFrontL = MagicPanels.unit2value( self.oOffsetFrontLE.text() )
			offsetFrontR = MagicPanels.unit2value( self.oOffsetFrontRE.text() )
			offsetFrontT = MagicPanels.unit2value( self.oOffsetFrontTE.text() )
			offsetFrontB = MagicPanels.unit2value( self.oOffsetFrontBE.text() )

			startX = MagicPanels.unit2value( self.oStartXE.text() )
			startY = MagicPanels.unit2value( self.oStartYE.text() )
			startZ = MagicPanels.unit2value( self.oStartZE.text() )
			
			sizeX = MagicPanels.unit2value( self.oWidthE.text() )
			sizeY = MagicPanels.unit2value( self.oDepthE.text() )
			sizeZ = MagicPanels.unit2value( self.oHeightE.text() )
			
			edgeband = MagicPanels.gEdgebandThickness
			if MagicPanels.gEdgebandApply == "everywhere":
				edgebandE = edgeband
			else:
				edgebandE = 0
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = sizeX - (2 * thick) - (2 * edgebandE)
			o1.Height = thick
			o1.Width = sizeY - thickFront - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + thick + edgebandE, startY + thickFront + edgeband, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			colors = [ (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), 
			 (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0) ]
			MagicPanels.setColor(o1, 0, colors, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = thick
			o2.Height = sizeZ - (2 * edgeband)
			o2.Width = sizeY - thickFront - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX, startY + thickFront + edgeband, startZ + edgeband)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			colors = [ (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), 
			 (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0) ]
			MagicPanels.setColor(o2, 0, colors, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = thick
			o3.Height = sizeZ - (2 * edgeband)
			o3.Width = sizeY - thickFront - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + sizeX - thick, startY + thickFront + edgeband, startZ + edgeband)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			colors = [ (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), 
			 (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0) ]
			MagicPanels.setColor(o3, 0, colors, "color")
			
			# Back HDF
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "BackHDF")
			o4.Label = translate('magicStart', 'Back HDF')
			o4.Length = sizeX
			o4.Height = sizeZ
			o4.Width = thickBack
			pl = FreeCAD.Vector(startX, startY + sizeY - thickBack, startZ)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			MagicPanels.setColor(o4, 3, (1.0, 1.0, 1.0, 1.0), "color")
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = sizeX - (2 * thick) - (2 * edgebandE)
			o5.Height = thick
			o5.Width = sizeY - thickFront - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + thick + edgebandE, startY + thickFront + edgeband, startZ + sizeZ - thick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			colors = [ (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), 
			 (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0) ]
			MagicPanels.setColor(o5, 0, colors, "color")
			
			# Front
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o6.Label = translate('magicStart', 'Front')
			o6.Length = sizeX - (2 * thick) + offsetFrontL + offsetFrontR - (2 * edgeband)
			o6.Height = sizeZ - (2 * thick) + offsetFrontB + offsetFrontT - (2 * edgeband)
			o6.Width = thickFront
			pl = FreeCAD.Vector(startX + thick + edgeband - offsetFrontL, startY, startZ + thick + edgeband - offsetFrontB)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			colors = [ (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), 
			 (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), 
			 (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0) ]
			MagicPanels.setColor(o6, 0, colors, "color")
			
			# Shelf
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o7.Label = translate('magicStart', 'Shelf')
			o7.Length = sizeX - (2 * thick) - (2 * edgebandE) - (2 * shelfOS)
			o7.Height = thickShelf
			o7.Width = sizeY - thickFront - thick - thickBack - edgeband - edgebandE
			px = startX + thick + edgebandE + shelfOS
			py = startY + thickFront + thick + edgeband
			pz = startZ + (sizeZ / 2) - (thickShelf / 2)
			o7.Placement = FreeCAD.Placement(FreeCAD.Vector(px, py, pz), self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")
			MagicPanels.setColor(o7, 3, (1.0, 1.0, 1.0, 1.0), "color")

			objects = [o1, o2, o3, o4, o5, o6, o7]
			label = "Kitchen wall cabinet"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF67(self):
			
			self.gFSX = MagicPanels.unit2value(self.oWidthE.text())
			self.gFSZ = MagicPanels.unit2value(self.oHeightE.text())
			self.gFSY = MagicPanels.unit2value(self.oDepthE.text())
			self.gThick = MagicPanels.unit2value(self.oThickE.text())
			bcthick = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			# #################################################################
			# settings
			# #################################################################
			
			barWidthH = 76.2                        # face frame bar width horizontal
			barWidthV = 50.8                        # face frame bar width vertical
			barThick = 25.4                         # face frame bar thickness
			bfco = 38.1                             # bottom floor offset
			bfflip = bfco                           # bottom face frame lip
			sfflip = 0                              # side face frame lip
			sbsizet = 88.9                          # supporters bar size top
			sbsizeb = bfco                          # supporters bar size bottom
			
			depth = self.gFSY - bcthick - barThick  # cabinet depth
			FFWidth = self.gFSX + (2 * sfflip)      # face freame width
			FFHeight = self.gFSZ - bfco + bfflip    # face frame height
			
			# start position calculation
			
			sx = MagicPanels.unit2value(self.oStartXE.text())
			sy = MagicPanels.unit2value(self.oStartYE.text()) + barThick
			sz = MagicPanels.unit2value(self.oStartZE.text())
			
			# face frame position calculation

			FSX = sx - sfflip
			FSY = sy - barThick
			FSZ = sz + bfco - bfflip
			
			centerFSX = FSX + (FFWidth / 2) - barWidthV
			horizontalFSX = FSX + (FFWidth / 2) + barWidthV
			horizontalFSZ = FSZ + (FFHeight / 2) - barWidthH
			
			# #####################################################
			# Furniture - draw
			# #####################################################
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor')
			o1.Length = self.gFSX - (2 * self.gThick)
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy, sz + bfco)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left')
			o2.Length = self.gThick
			o2.Height = self.gFSZ
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right')
			o3.Length = self.gThick
			o3.Height = self.gFSZ
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back')
			o4.Length = self.gFSX
			o4.Height = self.gFSZ
			o4.Width = bcthick
			pl = FreeCAD.Vector(sx, sy + depth, sz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top')
			o5.Length = self.gFSX - (2 * self.gThick)
			o5.Height = self.gThick
			o5.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy, sz + self.gFSZ - self.gThick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Support top
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "supporter1")
			o6.Label = translate('magicStart', 'ST')
			o6.Length = self.gFSX - (2 * self.gThick)
			o6.Height = sbsizet
			o6.Width = self.gThick
			pl = FreeCAD.Vector(sx + self.gThick, sy + depth - self.gThick, sz + self.gFSZ - sbsizet - self.gThick)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")

			# Support bottom
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "supporter2")
			o7.Label = translate('magicStart', 'SB')
			o7.Length = self.gFSX - (2 * self.gThick)
			o7.Height = sbsizeb
			o7.Width = self.gThick
			pl = FreeCAD.Vector(sx + self.gThick, sy + depth - self.gThick, sz)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")

			# Shelf
			o8 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o8.Label = translate('magicStart', 'Top')
			o8.Length = self.gFSX - (2 * self.gThick) - (2 * shelfOS)
			o8.Height = thickShelf
			o8.Width = depth - self.gThick
			px = sx + self.gThick + shelfOS
			py = sy + self.gThick
			pz = sz + (self.gFSZ  / 2) - (thickShelf / 2)
			o8.Placement = FreeCAD.Placement(FreeCAD.Vector(px, py, pz), self.gR)
			MagicPanels.setColor(o8, 0, self.gColor, "color")

			# Face Frame - draw

			# Left Side
			ff1 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFLeft")
			ff1.Label = translate('magicStart', 'FF Left')
			ff1.Length = barWidthV
			ff1.Height = FFHeight
			ff1.Width = barThick
			pl = FreeCAD.Vector(FSX, FSY, FSZ)
			ff1.Placement = FreeCAD.Placement(pl, self.gR)
			ff1.ViewObject.ShapeColor = self.gColor
			
			# Right Side
			ff2 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFRight")
			ff2.Label = translate('magicStart', 'FF Right')
			ff2.Length = barWidthV
			ff2.Height = FFHeight
			ff2.Width = barThick
			pl = FreeCAD.Vector(FSX + FFWidth - barWidthV, FSY, FSZ)
			ff2.Placement = FreeCAD.Placement(pl, self.gR)
			ff2.ViewObject.ShapeColor = self.gColor
			
			# Bottom
			ff3 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFBottom")
			ff3.Label = translate('magicStart', 'FF Bottom')
			ff3.Length = FFWidth - (2 * barWidthV)
			ff3.Height = barWidthH
			ff3.Width = barThick
			pl = FreeCAD.Vector(FSX + barWidthV, FSY, FSZ)
			ff3.Placement = FreeCAD.Placement(pl, self.gR)
			ff3.ViewObject.ShapeColor = self.gColor
			
			# Top
			ff4 = FreeCAD.ActiveDocument.addObject("Part::Box", "FFTop")
			ff4.Label = translate('magicStart', 'FF Top')
			ff4.Length = FFWidth - (2 * barWidthV)
			ff4.Height = barWidthH
			ff4.Width = barThick
			pl = FreeCAD.Vector(FSX + barWidthV, FSY, FSZ + FFHeight - barWidthH)
			ff4.Placement = FreeCAD.Placement(pl, self.gR)
			ff4.ViewObject.ShapeColor = self.gColor
			
			objects = [o1, o2, o3, o4, o5, o6, o7, o8, ff1, ff2, ff3, ff4]
			label = "Kitchen wall cabinet"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF71(self):
			
			p0X = MagicPanels.unit2value(self.ods61E.text())
			p0Y = MagicPanels.unit2value(self.ods62E.text())
			startZ = MagicPanels.unit2value(self.ods63E.text())
			
			gapX = MagicPanels.unit2value(self.ods7E.text())
			gapZ = MagicPanels.unit2value(self.ods8E.text())
			gapY = MagicPanels.unit2value(self.ods9E.text())
			
			num = int(self.ods2E.text())
			
			offset = 0 # there will be no offset between drawer gaps
			
			frontOffsetH = 2 * MagicPanels.unit2value(self.ods111E.text())
			frontOffsetV = 2 * MagicPanels.unit2value(self.ods112E.text())
			frontOffsetB = MagicPanels.unit2value(self.ods113E.text())
			
			thickFront = MagicPanels.unit2value(self.ods31E.text())
			thickSides = MagicPanels.unit2value(self.ods32E.text())
			thickBottom = MagicPanels.unit2value(self.ods33E.text())
			
			sidesOF = MagicPanels.unit2value(self.ods41E.text())
			sideOF = sidesOF / 2
			backOF = MagicPanels.unit2value(self.ods42E.text())
			topOF = MagicPanels.unit2value(self.ods43E.text())
			bottomOF = MagicPanels.unit2value(self.ods44E.text())
			backSidesOF = MagicPanels.unit2value(self.ods45E.text())
			
			zoffsets = (num - 1) * frontOffsetB
			zspace = (num * gapZ) + frontOffsetV
			frontHeight = (zspace - zoffsets) / num
			
			for i in range(0, num):
			
				p0Z = startZ + (i * (gapZ + offset))
			
				# Back
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBack")
				o3.Label = translate('magicStart', 'DS ' + str(i+1) + ' Back')
				o3.Length = gapX - backSidesOF
				o3.Height = gapZ - bottomOF - topOF - thickBottom
				o3.Width = thickSides
				pl = FreeCAD.Vector(p0X + (backSidesOF/2), p0Y + gapY - thickSides - backOF, p0Z + bottomOF + thickBottom)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
				
				# Bottom
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBottom")
				o5.Label = translate('magicStart', 'DS ' + str(i+1) + ' Bottom HDF')
				o5.Length = gapX - sidesOF
				o5.Height = thickBottom
				o5.Width = gapY - backOF
				pl = FreeCAD.Vector(p0X + sideOF, p0Y, p0Z  + bottomOF)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o5, 0, (1.0, 1.0, 1.0, 1.0), "color")

				# Front outside
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSFrontOutside")
				o6.Label = translate('magicStart', 'DS ' + str(i+1) + ' Front Outside')
				o6.Length = gapX + frontOffsetH
				o6.Height = frontHeight
				o6.Width = thickFront
				pz = (startZ - (frontOffsetV / 2)) + (i * (frontHeight + frontOffsetB)) 
				pl = FreeCAD.Vector(p0X - (frontOffsetH / 2), p0Y - thickFront, pz)
				o6.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o6, 0, self.gColor, "color")

				objects = [o3, o5, o6]
				label = "Container, Drawer series " + str(i+1)
				container = MagicPanels.createContainer(objects, label, False)
				
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF72(self):
			
			p0X = MagicPanels.unit2value(self.ods61E.text())
			p0Y = MagicPanels.unit2value(self.ods62E.text())
			startZ = MagicPanels.unit2value(self.ods63E.text())
			
			gapX = MagicPanels.unit2value(self.ods7E.text())
			gapZ = MagicPanels.unit2value(self.ods8E.text())
			gapY = MagicPanels.unit2value(self.ods9E.text())
			
			num = int(self.ods2E.text())
			
			offset = 0 # there will be no offset between drawer gaps

			frontOffsetH = 2 * MagicPanels.unit2value(self.ods111E.text())
			frontOffsetV = 2 * MagicPanels.unit2value(self.ods112E.text())
			frontOffsetB = MagicPanels.unit2value(self.ods113E.text())

			thickFront = MagicPanels.unit2value(self.ods31E.text())
			thickSides = MagicPanels.unit2value(self.ods32E.text())
			thickBottom = MagicPanels.unit2value(self.ods33E.text())
			
			sidesOF = MagicPanels.unit2value(self.ods41E.text())
			sideOF = sidesOF / 2
			backOF = MagicPanels.unit2value(self.ods42E.text())
			topOF = MagicPanels.unit2value(self.ods43E.text())
			bottomOF = MagicPanels.unit2value(self.ods44E.text())
			backSidesOF = MagicPanels.unit2value(self.ods45E.text())
			
			zoffsets = (num - 1) * frontOffsetB
			zspace = (num * gapZ) - frontOffsetV
			frontHeight = (zspace - zoffsets) / num

			for i in range(0, num):
			
				p0Z = startZ + (i * (gapZ + offset))
				
				# Back
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBack")
				o3.Label = translate('magicStart', 'DS ' + str(i+1) + ' Back')
				o3.Length = gapX - backSidesOF
				o3.Height = gapZ - bottomOF - topOF - thickBottom
				o3.Width = thickSides
				pl = FreeCAD.Vector(p0X + (backSidesOF/2), p0Y + gapY - thickSides - backOF, p0Z + bottomOF + thickBottom)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o3, 0, (1.0, 1.0, 1.0, 1.0), "color")
				
				# Bottom
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSBottom")
				o5.Label = translate('magicStart', 'DS ' + str(i+1) + ' Bottom HDF')
				o5.Length = gapX - sidesOF
				o5.Height = thickBottom
				o5.Width = gapY - backOF - thickFront
				pl = FreeCAD.Vector(p0X + sideOF, p0Y + thickFront, p0Z  + bottomOF)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o5, 0, (1.0, 1.0, 1.0, 1.0), "color")

				# Front outside
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "DSFrontOutside")
				o6.Label = translate('magicStart', 'DS ' + str(i+1) + ' Front Outside')
				o6.Length = gapX - frontOffsetH
				o6.Height = frontHeight
				o6.Width = thickFront
				pz = (startZ + (frontOffsetV / 2)) + (i * (frontHeight + frontOffsetB)) 
				pl = FreeCAD.Vector(p0X + (frontOffsetH/2), p0Y, pz)
				o6.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o6, 0, self.gColor, "color")

				objects = [o3, o5, o6]
				label = "Container, Drawer series " + str(i+1)
				container = MagicPanels.createContainer(objects, label, False)
				
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF73(self):
			
			sizeX = MagicPanels.unit2value(self.oworkspaceXE.text())
			sizeY = MagicPanels.unit2value(self.oworkspaceYE.text())
			sizeZ = MagicPanels.unit2value(self.oworkspaceZE.text())
			
			startX = MagicPanels.unit2value(self.oworkspaceSXE.text())
			startY = MagicPanels.unit2value(self.oworkspaceSYE.text())
			startZ = MagicPanels.unit2value(self.oworkspaceSZE.text())
			
			# Bottom
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "workspace")
			o1.Label = translate('magicStart', 'workspace')
			o1.Length = sizeX
			o1.Height = sizeZ
			o1.Width = sizeY
			pl = FreeCAD.Vector(startX, startY, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, (0.0, 0.0, 0.0, 1.0), "color")
			MagicPanels.setColor(o1, 0, 70, "trans", "RGBA")
			
			if not hasattr(o1, "BOM"):
				info = translate("magicStart", "Allows to skip this workspace in BOM, cut-list report.")
				o1.addProperty("App::PropertyBool", "BOM", "Woodworking", info)
		
			o1.BOM = False

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF74(self):
			
			startX = MagicPanels.unit2value(self.oBackSXE.text())
			startY = MagicPanels.unit2value(self.oBackSYE.text())
			startZ = MagicPanels.unit2value(self.oBackSZE.text())
			
			width = MagicPanels.unit2value(self.oBackSizeXE.text())
			height = MagicPanels.unit2value(self.oBackSizeYE.text())
			thick = MagicPanels.unit2value(self.oBackThickE.text())
			
			# Front outside
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o1.Label = translate('magicStart', 'Back')
			o1.Length = width
			o1.Height = height
			o1.Width = thick
			pl = FreeCAD.Vector(startX, startY, startZ)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")

			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF78(self):
			
			self.gFSX = MagicPanels.unit2value(self.oWidthE.text())
			self.gFSZ = MagicPanels.unit2value(self.oHeightE.text())
			self.gFSY = MagicPanels.unit2value(self.oDepthE.text())
			self.gThick = MagicPanels.unit2value(self.oThickE.text())
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			sx = MagicPanels.unit2value(self.oStartXE.text())
			sy = MagicPanels.unit2value(self.oStartYE.text())
			sz = MagicPanels.unit2value(self.oStartZE.text())
			
			# calculation
			mNum = int(self.oModulesNumE.text())
			sideZ = ((self.gFSZ - self.gThick - (mNum * self.gThick)) / mNum)
			depth = self.gFSY
			
			# #######################
			# Modules
			# #######################
			
			for i in range(mNum):
			
				posZ = (i * sideZ) + (i * self.gThick)
			
				if i == 0:
					# Floor
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
					o1.Label = translate('magicStart', 'Floor') + ' M' + str(i+1)
					o1.Length = self.gFSX - (2 * self.gThick)
					o1.Height = self.gThick
					o1.Width = depth - thickBack
					pl = FreeCAD.Vector(sx + self.gThick, sy, sz + posZ + 100)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, self.gColor, "color")
					
					# Left Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
					o2.Label = translate('magicStart', 'Left') + ' M' + str(i+1)
					o2.Length = self.gThick
					o2.Height = sideZ + self.gThick
					o2.Width = depth
					pl = FreeCAD.Vector(sx, sy, sz + posZ)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, self.gColor, "color")
					
					# Right Side
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
					o3.Label = translate('magicStart', 'Right') + ' M' + str(i+1)
					o3.Length = self.gThick
					o3.Height = sideZ + self.gThick
					o3.Width = depth
					pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz + posZ)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, self.gColor, "color")
				
					# Back
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
					o4.Label = translate('magicStart', 'Back') + ' M' + str(i+1)
					o4.Length = self.gFSX - (2 * self.gThick)
					o4.Height = sideZ - 100 + self.gThick
					o4.Width = thickBack
					pl = FreeCAD.Vector(sx + self.gThick, sy + depth - thickBack, sz + posZ + 100)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, self.gColor, "color")
					
					# Shelf
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
					o5.Label = translate('magicStart', 'Shelf') + ' M' + str(i+1)
					o5.Length = self.gFSX - (2 * self.gThick) - (2 * shelfOS)
					o5.Height = thickShelf
					o5.Width = depth - self.gThick - thickBack
					pZ = ((2 * i) + 1) * ((self.gThick + sideZ) / 2)
					pl = FreeCAD.Vector(sx + self.gThick + shelfOS, sy + self.gThick, sz + pZ)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o5, 0, self.gColor, "color")
				else:
					# Floor
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
					o1.Label = translate('magicStart', 'Floor') + ' M' + str(i+1)
					o1.Length = self.gFSX
					o1.Height = self.gThick
					o1.Width = depth
					pl = FreeCAD.Vector(sx, sy, sz + posZ)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, self.gColor, "color")
				
					# Left Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
					o2.Label = translate('magicStart', 'Left') + ' M' + str(i+1)
					o2.Length = self.gThick
					o2.Height = sideZ
					o2.Width = depth
					pl = FreeCAD.Vector(sx, sy, sz + posZ + self.gThick)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, self.gColor, "color")
					
					# Right Side
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
					o3.Label = translate('magicStart', 'Right') + ' M' + str(i+1)
					o3.Length = self.gThick
					o3.Height = sideZ
					o3.Width = depth
					pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz + posZ + self.gThick)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, self.gColor, "color")
					
					# Back
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
					o4.Label = translate('magicStart', 'Back') + ' M' + str(i+1)
					o4.Length = self.gFSX - (2 * self.gThick)
					o4.Height = sideZ
					o4.Width = thickBack
					pl = FreeCAD.Vector(sx + self.gThick, sy + depth - thickBack, sz + posZ + self.gThick)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, self.gColor, "color")
					
					# Shelf
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
					o5.Label = translate('magicStart', 'Shelf') + ' M' + str(i+1)
					o5.Length = self.gFSX - (2 * self.gThick) - (2 * shelfOS)
					o5.Height = thickShelf
					o5.Width = depth - self.gThick - thickBack
					pZ = ((2 * i) + 1) * ((self.gThick + sideZ) / 2)
					pl = FreeCAD.Vector(sx + self.gThick + shelfOS, sy + self.gThick, sz + pZ)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o5, 0, self.gColor, "color")
					
				# create folder
				objects = [o1, o2, o3, o4, o5]
				label = translate('magicStart', 'Module ') + str(i+1)
				container = MagicPanels.createContainer(objects, label, False)
			
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
			pl = FreeCAD.Vector(sx, sy, sz + pZ)
			t1.Placement = FreeCAD.Placement(pl, self.gR)
			t1.ViewObject.ShapeColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF79(self):
			
			self.gFSX = MagicPanels.unit2value(self.oWidthE.text())
			self.gFSZ = MagicPanels.unit2value(self.oHeightE.text())
			self.gFSY = MagicPanels.unit2value(self.oDepthE.text())
			self.gThick = MagicPanels.unit2value(self.oThickE.text())
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			sx = MagicPanels.unit2value(self.oStartXE.text())
			sy = MagicPanels.unit2value(self.oStartYE.text())
			sz = MagicPanels.unit2value(self.oStartZE.text())
			
			# calculation
			mNum = int(self.oModulesNumE.text())
			sideZ = ((self.gFSZ - self.gThick - (mNum * self.gThick)) / mNum)
			depth = self.gFSY - thickBack
			
			# #######################
			# Modules
			# #######################
			
			for i in range(mNum):
			
				posZ = (i * sideZ) + (i * self.gThick)
			
				if i == 0:
					# Floor
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
					o1.Label = translate('magicStart', 'Floor') + ' M' + str(i+1)
					o1.Length = self.gFSX - (2 * self.gThick)
					o1.Height = self.gThick
					o1.Width = depth
					pl = FreeCAD.Vector(sx + self.gThick, sy, sz + posZ + 100)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, self.gColor, "color")
					
					# Left Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
					o2.Label = translate('magicStart', 'Left') + ' M' + str(i+1)
					o2.Length = self.gThick
					o2.Height = sideZ + self.gThick
					o2.Width = depth
					pl = FreeCAD.Vector(sx, sy, sz + posZ)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, self.gColor, "color")
					
					# Right Side
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
					o3.Label = translate('magicStart', 'Right') + ' M' + str(i+1)
					o3.Length = self.gThick
					o3.Height = sideZ + self.gThick
					o3.Width = depth
					pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz + posZ)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, self.gColor, "color")
				
					# Back
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
					o4.Label = translate('magicStart', 'Back') + ' M' + str(i+1)
					o4.Length = self.gFSX
					o4.Height = sideZ - 100 + (2 * self.gThick)
					o4.Width = thickBack
					pl = FreeCAD.Vector(sx, sy + depth, sz + posZ + 100)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, self.gColor, "color")
					MagicPanels.setColor(o4, 3, (1.0, 1.0, 1.0, 1.0), "color")
					
					# Shelf
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
					o5.Label = translate('magicStart', 'Shelf') + ' M' + str(i+1)
					o5.Length = self.gFSX - (2 * self.gThick) - (2 * shelfOS)
					o5.Height = thickShelf
					o5.Width = depth - self.gThick
					pZ = ((2 * i) + 1) * ((self.gThick + sideZ) / 2)
					pl = FreeCAD.Vector(sx + self.gThick + shelfOS, sy + self.gThick, sz + pZ)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o5, 0, self.gColor, "color")
				else:
					# Floor
					o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
					o1.Label = translate('magicStart', 'Floor') + ' M' + str(i+1)
					o1.Length = self.gFSX
					o1.Height = self.gThick
					o1.Width = depth
					pl = FreeCAD.Vector(sx, sy, sz + posZ)
					o1.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o1, 0, self.gColor, "color")
				
					# Left Side
					o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
					o2.Label = translate('magicStart', 'Left') + ' M' + str(i+1)
					o2.Length = self.gThick
					o2.Height = sideZ
					o2.Width = depth
					pl = FreeCAD.Vector(sx, sy, sz + posZ + self.gThick)
					o2.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o2, 0, self.gColor, "color")
					
					# Right Side
					o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
					o3.Label = translate('magicStart', 'Right') + ' M' + str(i+1)
					o3.Length = self.gThick
					o3.Height = sideZ
					o3.Width = depth
					pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy, sz + posZ + self.gThick)
					o3.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o3, 0, self.gColor, "color")
					
					# Back
					o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
					o4.Label = translate('magicStart', 'Back') + ' M' + str(i+1)
					o4.Length = self.gFSX
					o4.Height = sideZ + self.gThick
					o4.Width = thickBack
					pl = FreeCAD.Vector(sx, sy + depth, sz + posZ + self.gThick)
					o4.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o4, 0, self.gColor, "color")
					MagicPanels.setColor(o4, 3, (1.0, 1.0, 1.0, 1.0), "color")
			
					# Shelf
					o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
					o5.Label = translate('magicStart', 'Shelf') + ' M' + str(i+1)
					o5.Length = self.gFSX - (2 * self.gThick) - (2 * shelfOS)
					o5.Height = thickShelf
					o5.Width = depth - self.gThick
					pZ = ((2 * i) + 1) * ((self.gThick + sideZ) / 2)
					pl = FreeCAD.Vector(sx + self.gThick + shelfOS, sy + self.gThick, sz + pZ)
					o5.Placement = FreeCAD.Placement(pl, self.gR)
					MagicPanels.setColor(o5, 0, self.gColor, "color")
				
				# create folder
				objects = [o1, o2, o3, o4, o5]
				label = translate('magicStart', 'Module ') + str(i+1)
				container = MagicPanels.createContainer(objects, label, False)
			
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
			pl = FreeCAD.Vector(sx, sy, sz + pZ)
			t1.Placement = FreeCAD.Placement(pl, self.gR)
			t1.ViewObject.ShapeColor = self.gColor

			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF80(self):
			
			width = MagicPanels.unit2value(self.oTableSizeXE.text())
			depth = MagicPanels.unit2value(self.oTableSizeYE.text())
			height = MagicPanels.unit2value(self.oTableSizeZE.text())
			topThick = MagicPanels.unit2value(self.oTableTopThickE.text())
			legThick = MagicPanels.unit2value(self.oTableLegThickE.text())
			offset = MagicPanels.unit2value(self.oTableTopOffsetE.text())
			
			sx = MagicPanels.unit2value(self.oTableStartXE.text())
			sy = MagicPanels.unit2value(self.oTableStartYE.text())
			sz = MagicPanels.unit2value(self.oTableStartZE.text())
			
			# Leg Left
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLL")
			o1.Label = translate('magicStart', 'Table Leg Left')
			o1.Length = legThick
			o1.Height = height - topThick
			o1.Width = depth - (2 * offset)
			pl = FreeCAD.Vector(sx + offset, sy + offset, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Leg Middle
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLM")
			o2.Label = translate('magicStart', 'Table Leg Middle')
			o2.Length = legThick
			o2.Height = height - topThick
			o2.Width = depth - (2 * offset)
			psx = sx + width - offset - (2 * legThick) - (4/10 * width)
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Leg Right
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLR")
			o3.Label = translate('magicStart', 'Table Leg Rright')
			o3.Length = legThick
			o3.Height = height - topThick
			o3.Width = depth - (2 * offset)
			psx = sx + width - offset - legThick
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back Left 1
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableBL1")
			o4.Label = translate('magicStart', 'Table Back Left 1')
			o4.Length = width - (2* offset) - (3 * legThick) - (4/10 * width)
			o4.Height = 200
			o4.Width = legThick
			psx = sx + offset + legThick
			psy = sy + depth - offset - legThick
			psz = sz + height - topThick - 200
			pl = FreeCAD.Vector(psx, psy, psz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Back Left 2
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableBL2")
			o5.Label = translate('magicStart', 'Table Back Left 2')
			o5.Length = width - (2* offset) - (3 * legThick) - (4/10 * width)
			o5.Height = 100
			o5.Width = legThick
			psx = sx + offset + legThick
			psy = sy + depth - offset - legThick
			psz = sz + 100
			pl = FreeCAD.Vector(psx, psy, psz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Right Back 1
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableRB1")
			o6.Label = translate('magicStart', 'Table Right Back 1')
			o6.Length = 4/10 * width
			o6.Height = height - topThick
			o6.Width = legThick
			psx = sx + width - offset - legThick - (4/10 * width)
			psy = sy + depth - offset - legThick
			psz = sz
			pl = FreeCAD.Vector(psx, psy, psz)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
			
			# Supporter Front
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSF1")
			o7.Label = translate('magicStart', 'Table SF1')
			o7.Length = 4/10 * width
			o7.Height = 100
			o7.Width = legThick
			psx = sx + width - offset - legThick - (4/10 * width)
			psy = sy + offset + legThick
			psz = sz
			pl = FreeCAD.Vector(psx, psy, psz)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")
			
			# Shelf 1
			o8 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableShelf1")
			o8.Label = translate('magicStart', 'Table Shelf 1')
			o8.Length = 4/10 * width
			o8.Height = legThick
			o8.Width = depth - (2 * offset) - legThick
			psx = sx + width - offset - legThick - (4/10 * width)
			psy = sy + offset
			psz = sz + 100
			pl = FreeCAD.Vector(psx, psy, psz)
			o8.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o8, 0, self.gColor, "color")
			
			# Shelf 2
			o9 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableShelf2")
			o9.Label = translate('magicStart', 'Table Shelf 2')
			o9.Length = 4/10 * width
			o9.Height = legThick
			o9.Width = depth - (2 * offset) - legThick
			psx = sx + width - offset - legThick - (4/10 * width)
			psy = sy + offset
			psz = sz + height - 200
			pl = FreeCAD.Vector(psx, psy, psz)
			o9.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o9, 0, self.gColor, "color")
			
			# Top
			o10 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableTop")
			o10.Label = translate('magicStart', 'Table Top')
			o10.Length = width
			o10.Height = topThick
			o10.Width = depth
			psx = sx
			psy = sy
			psz = sz + height - topThick
			pl = FreeCAD.Vector(psx, psy, psz)
			o10.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o10, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4, o5, o6, o7, o8, o9, o10]
			label = "Container, Table"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF81(self):
			
			width = MagicPanels.unit2value(self.oTableSizeXE.text())
			depth = MagicPanels.unit2value(self.oTableSizeYE.text())
			height = MagicPanels.unit2value(self.oTableSizeZE.text())
			topThick = MagicPanels.unit2value(self.oTableTopThickE.text())
			legThick = MagicPanels.unit2value(self.oTableLegThickE.text())
			offset = MagicPanels.unit2value(self.oTableTopOffsetE.text())
			
			sx = MagicPanels.unit2value(self.oTableStartXE.text())
			sy = MagicPanels.unit2value(self.oTableStartYE.text())
			sz = MagicPanels.unit2value(self.oTableStartZE.text())
			
			# Leg Left
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLL")
			o1.Label = translate('magicStart', 'Table Leg Left')
			o1.Length = legThick
			o1.Height = height - topThick
			o1.Width = depth - (2 * offset)
			pl = FreeCAD.Vector(sx + offset, sy + offset, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Leg Middle
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLM")
			o2.Label = translate('magicStart', 'Table Leg Middle')
			o2.Length = legThick
			o2.Height = height - topThick
			o2.Width = depth - (2 * offset)
			psx = sx + offset + legThick + (4/10 * width)
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Leg Right
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLR")
			o3.Label = translate('magicStart', 'Table Leg Rright')
			o3.Length = legThick
			o3.Height = height - topThick
			o3.Width = depth - (2 * offset)
			psx = sx + width - offset - legThick
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back Right 1
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableBR1")
			o4.Label = translate('magicStart', 'Table Back Right 1')
			o4.Length = width - (2 * offset) - (3 * legThick) - (4/10 * width)
			o4.Height = 200
			o4.Width = legThick
			psx = sx + offset + (2 * legThick) + (4/10 * width)
			psy = sy + depth - offset - legThick
			psz = sz + height - topThick - 200
			pl = FreeCAD.Vector(psx, psy, psz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Back Right 2
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableBR2")
			o5.Label = translate('magicStart', 'Table Back Right 2')
			o5.Length = width - (2 * offset) - (3 * legThick) - (4/10 * width)
			o5.Height = 100
			o5.Width = legThick
			psx = sx + offset + (2 * legThick) + (4/10 * width)
			psy = sy + depth - offset - legThick
			psz = sz + 100
			pl = FreeCAD.Vector(psx, psy, psz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Back Left 1
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableBL1")
			o6.Label = translate('magicStart', 'Table Back Left 1')
			o6.Length = 4/10 * width
			o6.Height = height - topThick
			o6.Width = legThick
			psx = sx + offset + legThick
			psy = sy + depth - offset - legThick
			psz = sz
			pl = FreeCAD.Vector(psx, psy, psz)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
			
			# Supporter Front
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSF1")
			o7.Label = translate('magicStart', 'Table SF1')
			o7.Length = 4/10 * width
			o7.Height = 100
			o7.Width = legThick
			psx = sx + offset + legThick
			psy = sy + offset + legThick
			psz = sz
			pl = FreeCAD.Vector(psx, psy, psz)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")
			
			# Shelf 1
			o8 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableShelf1")
			o8.Label = translate('magicStart', 'Table Shelf 1')
			o8.Length = 4/10 * width
			o8.Height = legThick
			o8.Width = depth - (2 * offset) - legThick
			psx = sx + offset + legThick
			psy = sy + offset
			psz = sz + 100
			pl = FreeCAD.Vector(psx, psy, psz)
			o8.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o8, 0, self.gColor, "color")
			
			# Shelf 2
			o9 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableShelf2")
			o9.Label = translate('magicStart', 'Table Shelf 2')
			o9.Length = 4/10 * width
			o9.Height = legThick
			o9.Width = depth - (2 * offset) - legThick
			psx = sx + offset + legThick
			psy = sy + offset
			psz = sz + height - 200
			pl = FreeCAD.Vector(psx, psy, psz)
			o9.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o9, 0, self.gColor, "color")
			
			# Top
			o10 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableTop")
			o10.Label = translate('magicStart', 'Table Top')
			o10.Length = width
			o10.Height = topThick
			o10.Width = depth
			psx = sx
			psy = sy
			psz = sz + height - topThick
			pl = FreeCAD.Vector(psx, psy, psz)
			o10.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o10, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4, o5, o6, o7, o8, o9, o10]
			label = "Container, Table"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF82(self):
			
			width = MagicPanels.unit2value(self.oTableSizeXE.text())
			depth = MagicPanels.unit2value(self.oTableSizeYE.text())
			height = MagicPanels.unit2value(self.oTableSizeZE.text())
			topThick = MagicPanels.unit2value(self.oTableTopThickE.text())
			legThick = MagicPanels.unit2value(self.oTableLegThickE.text())
			offset = MagicPanels.unit2value(self.oTableTopOffsetE.text())
			
			sx = MagicPanels.unit2value(self.oTableStartXE.text())
			sy = MagicPanels.unit2value(self.oTableStartYE.text())
			sz = MagicPanels.unit2value(self.oTableStartZE.text())
			
			space = 1/4 * ( width - (2 * offset) - (4 * legThick) )
			
			# Leg Left 1
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLL1")
			o1.Label = translate('magicStart', 'Table Leg Left 1')
			o1.Length = legThick
			o1.Height = height - topThick
			o1.Width = depth - (2 * offset)
			pl = FreeCAD.Vector(sx + offset, sy + offset, sz)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Leg Left 2
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLL2")
			o2.Label = translate('magicStart', 'Table Leg Left 2')
			o2.Length = legThick
			o2.Height = height - topThick
			o2.Width = depth - (2 * offset)
			psx = sx + offset + legThick + space
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Leg Right 1
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLR1")
			o3.Label = translate('magicStart', 'Table Leg Right 1')
			o3.Length = legThick
			o3.Height = height - topThick
			o3.Width = depth - (2 * offset)
			psx = sx + width - offset - legThick
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Leg Right 2
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableLR2")
			o4.Label = translate('magicStart', 'Table Leg Right 2')
			o4.Length = legThick
			o4.Height = height - topThick
			o4.Width = depth - (2 * offset)
			psx = sx + width - offset - legThick - space - legThick
			pl = FreeCAD.Vector(psx, sy + offset, sz)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Back Left
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableBL")
			o5.Label = translate('magicStart', 'Table Back Left')
			o5.Length = space
			o5.Height = height - topThick
			o5.Width = legThick
			psx = sx + offset + legThick
			psy = sy + depth - offset - legThick
			psz = sz
			pl = FreeCAD.Vector(psx, psy, psz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Back Right
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableBR")
			o6.Label = translate('magicStart', 'Table Back Right')
			o6.Length = space
			o6.Height = height - topThick
			o6.Width = legThick
			psx = sx + width - offset - legThick - space
			psy = sy + depth - offset - legThick
			psz = sz
			pl = FreeCAD.Vector(psx, psy, psz)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
			
			# Back Middle 1
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableBM1")
			o7.Label = translate('magicStart', 'Table Back Middle 1')
			o7.Length = 2 * space
			o7.Height = 200
			o7.Width = legThick
			psx = sx + offset + legThick + space + legThick
			psy = sy + depth - offset - legThick
			psz = sz + height - topThick - 200
			pl = FreeCAD.Vector(psx, psy, psz)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")
			
			# Back Middle 2
			o8 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableBM2")
			o8.Label = translate('magicStart', 'Table Back Middle 2')
			o8.Length = 2 * space
			o8.Height = 200
			o8.Width = legThick
			psx = sx + offset + legThick + space + legThick
			psy = sy + depth - offset - legThick
			psz = sz + 100
			pl = FreeCAD.Vector(psx, psy, psz)
			o8.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o8, 0, self.gColor, "color")
			
			# Supporter Front Left
			o9 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSFL")
			o9.Label = translate('magicStart', 'Table Support FL')
			o9.Length = space
			o9.Height = 100
			o9.Width = legThick
			psx = sx + offset + legThick
			psy = sy + offset + legThick
			psz = sz
			pl = FreeCAD.Vector(psx, psy, psz)
			o9.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o9, 0, self.gColor, "color")
			
			# Supporter Front Right
			o10 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableSFR")
			o10.Label = translate('magicStart', 'Table Support FR')
			o10.Length = space
			o10.Height = 100
			o10.Width = legThick
			psx = sx + width - offset - legThick - space
			psy = sy + offset + legThick
			psz = sz
			pl = FreeCAD.Vector(psx, psy, psz)
			o10.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o10, 0, self.gColor, "color")
			
			# Shelf Left 1
			o11 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableShelfL1")
			o11.Label = translate('magicStart', 'Table Shelf Left 1')
			o11.Length = space
			o11.Height = legThick
			o11.Width = depth - (2 * offset) - legThick
			psx = sx + offset + legThick
			psy = sy + offset
			psz = sz + 100
			pl = FreeCAD.Vector(psx, psy, psz)
			o11.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o11, 0, self.gColor, "color")
			
			# Shelf Left 2
			o12 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableShelfL2")
			o12.Label = translate('magicStart', 'Table Shelf Left 2')
			o12.Length = space
			o12.Height = legThick
			o12.Width = depth - (2 * offset) - legThick
			psx = sx + offset + legThick
			psy = sy + offset
			psz = sz + height - topThick - 200
			pl = FreeCAD.Vector(psx, psy, psz)
			o12.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o12, 0, self.gColor, "color")
			
			# Shelf Right 1
			o13 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableShelfR1")
			o13.Label = translate('magicStart', 'Table Shelf Right 1')
			o13.Length = space
			o13.Height = legThick
			o13.Width = depth - (2 * offset) - legThick
			psx = sx + width - offset - legThick - space
			psy = sy + offset
			psz = sz + 100
			pl = FreeCAD.Vector(psx, psy, psz)
			o13.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o13, 0, self.gColor, "color")
			
			# Shelf Right 2
			o14 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableShelfR2")
			o14.Label = translate('magicStart', 'Table Shelf Right 2')
			o14.Length = space
			o14.Height = legThick
			o14.Width = depth - (2 * offset) - legThick
			psx = sx + width - offset - legThick - space
			psy = sy + offset
			psz = sz + height - topThick - 200
			pl = FreeCAD.Vector(psx, psy, psz)
			o14.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o14, 0, self.gColor, "color")
			
			# Top
			o15 = FreeCAD.ActiveDocument.addObject("Part::Box", "TableTop")
			o15.Label = translate('magicStart', 'Table Top')
			o15.Length = width
			o15.Height = topThick
			o15.Width = depth
			psx = sx
			psy = sy
			psz = sz + height - topThick
			pl = FreeCAD.Vector(psx, psy, psz)
			o15.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o15, 0, self.gColor, "color")
			
			objects = [o1, o2, o3, o4, o5, o6, o7, o8, o9, o10, o11, o12, o13, o14, o15]
			label = "Container, Table"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF84(self):
			
			self.gFSX = MagicPanels.unit2value(self.oWidthE.text())
			self.gFSZ = MagicPanels.unit2value(self.oHeightE.text())
			self.gFSY = MagicPanels.unit2value(self.oDepthE.text())
			
			self.gThick = MagicPanels.unit2value(self.oThickE.text())
			
			thickFront = MagicPanels.unit2value( self.oThickFrontE.text() )
			offsetFrontL = MagicPanels.unit2value( self.oOffsetFrontLE.text() )
			offsetFrontR = MagicPanels.unit2value( self.oOffsetFrontRE.text() )
			offsetFrontT = MagicPanels.unit2value( self.oOffsetFrontTE.text() )
			offsetFrontB = MagicPanels.unit2value( self.oOffsetFrontBE.text() )
		
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			sx = MagicPanels.unit2value(self.oStartXE.text())
			sy = MagicPanels.unit2value(self.oStartYE.text())
			sz = MagicPanels.unit2value(self.oStartZE.text())
			
			# calculation
			mNum = int(self.oModulesNumE.text())
			topsSize = (mNum - 1) * self.gThick
			
			baseSideZ = 578 # to have eaqual modules size
			modulesSideZ = self.gFSZ - baseSideZ - self.gThick - topsSize

			sideZ = modulesSideZ / (mNum - 1)
			depth = self.gFSY - thickBack - thickFront
			
			# #######################
			# Base
			# #######################
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor') + ' M1'
			o1.Length = self.gFSX - (2 * self.gThick)
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy + thickFront, sz + 100)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left') + ' M1'
			o2.Length = self.gThick
			o2.Height = baseSideZ
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy + thickFront, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right') + ' M1'
			o3.Length = self.gThick
			o3.Height = baseSideZ
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy + thickFront, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
		
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back') + ' M1'
			o4.Length = self.gFSX
			o4.Height = baseSideZ - 100 + self.gThick
			o4.Width = thickBack
			pl = FreeCAD.Vector(sx, sy + depth + thickFront, sz + 100)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			MagicPanels.setColor(o4, 3, (1.0, 1.0, 1.0, 1.0), "color")
			
			# Shelf
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o5.Label = translate('magicStart', 'Shelf') + ' M1'
			o5.Length = self.gFSX - (2 * self.gThick) - (2 * shelfOS)
			o5.Height = thickShelf
			o5.Width = depth - self.gThick
			gap = baseSideZ - 100 - self.gThick
			pZ = 100 + self.gThick + (gap / 2) - (thickShelf / 2)
			pl = FreeCAD.Vector(sx + self.gThick + shelfOS, sy + thickFront + self.gThick, sz + pZ)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")
			
			# Top
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o6.Label = translate('magicStart', 'Top') + ' M1'
			o6.Length = self.gFSX
			o6.Height = self.gThick
			o6.Width = depth
			pl = FreeCAD.Vector(sx, sy + thickFront, sz + baseSideZ)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
		
			# Front
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o7.Label = translate('magicStart', 'Front') + ' M1'
			o7.Length = self.gFSX - (2 * self.gThick) + offsetFrontL + offsetFrontR
			o7.Height = baseSideZ - 100 - self.gThick + offsetFrontB + offsetFrontT
			o7.Width = thickFront
			pl = FreeCAD.Vector(sx + self.gThick - offsetFrontL, sy, sz + 100 + self.gThick - offsetFrontB)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")
			
			# create container
			objects = [o1, o2, o3, o4, o5, o6, o7]
			label = translate('magicStart', 'Module 1')
			container = MagicPanels.createContainer(objects, label, False)
			
			# #######################
			# Modules
			# #######################
			
			for i in range(1, mNum):
			
				posZ = baseSideZ + (i * self.gThick) + ((i - 1) * sideZ)

				# Left Side
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
				o1.Label = translate('magicStart', 'Left') + ' M' + str(i+1)
				o1.Length = self.gThick
				o1.Height = sideZ
				o1.Width = depth
				pl = FreeCAD.Vector(sx, sy + thickFront, sz + posZ)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o1, 0, self.gColor, "color")
				
				# Right Side
				o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
				o2.Label = translate('magicStart', 'Right') + ' M' + str(i+1)
				o2.Length = self.gThick
				o2.Height = sideZ
				o2.Width = depth
				pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy + thickFront, sz + posZ)
				o2.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o2, 0, self.gColor, "color")
				
				# Back
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
				o3.Label = translate('magicStart', 'Back') + ' M' + str(i+1)
				o3.Length = self.gFSX
				o3.Height = sideZ + self.gThick
				o3.Width = thickBack
				pl = FreeCAD.Vector(sx, sy + thickFront + depth, sz + posZ)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o3, 0, self.gColor, "color")
				MagicPanels.setColor(o3, 3, (1.0, 1.0, 1.0, 1.0), "color")
		
				# Shelf
				o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
				o4.Label = translate('magicStart', 'Shelf') + ' M' + str(i+1)
				o4.Length = self.gFSX - (2 * self.gThick) - (2 * shelfOS)
				o4.Height = thickShelf
				o4.Width = depth - self.gThick
				pZ = posZ + (sideZ / 2) - (thickShelf / 2)
				pl = FreeCAD.Vector(sx + self.gThick + shelfOS, sy + thickFront + self.gThick, sz + pZ)
				o4.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o4, 0, self.gColor, "color")
			
				# Top
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
				o5.Label = translate('magicStart', 'Top') + ' M' + str(i+1)
				o5.Length = self.gFSX
				o5.Height = self.gThick
				o5.Width = depth
				pl = FreeCAD.Vector(sx, sy + thickFront, sz + posZ + sideZ)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o5, 0, self.gColor, "color")
				
				# Front
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
				o6.Label = translate('magicStart', 'Front') + ' M1' + str(i+1)
				o6.Length = self.gFSX - (2 * self.gThick) + offsetFrontL + offsetFrontR
				o6.Height = sideZ + offsetFrontB + offsetFrontT
				o6.Width = thickFront
				pl = FreeCAD.Vector(sx + self.gThick - offsetFrontL, sy, sz + posZ - offsetFrontB)
				o6.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o6, 0, self.gColor, "color")
			
				# create container
				objects = [o1, o2, o3, o4, o5, o6]
				label = translate('magicStart', 'Module ') + str(i+1)
				container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF85(self):
			
			self.gFSX = MagicPanels.unit2value(self.oWidthE.text())
			self.gFSZ = MagicPanels.unit2value(self.oHeightE.text())
			self.gFSY = MagicPanels.unit2value(self.oDepthE.text())
			
			self.gThick = MagicPanels.unit2value(self.oThickE.text())
			
			thickFront = MagicPanels.unit2value( self.oThickFrontE.text() )
			offsetFrontL = MagicPanels.unit2value( self.oOffsetFrontLE.text() )
			offsetFrontR = MagicPanels.unit2value( self.oOffsetFrontRE.text() )
			offsetFrontT = MagicPanels.unit2value( self.oOffsetFrontTE.text() )
			offsetFrontB = MagicPanels.unit2value( self.oOffsetFrontBE.text() )
		
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			sx = MagicPanels.unit2value(self.oStartXE.text())
			sy = MagicPanels.unit2value(self.oStartYE.text())
			sz = MagicPanels.unit2value(self.oStartZE.text())
			
			# calculation
			mNum = int(self.oModulesNumE.text())
			topsSize = (mNum - 1) * self.gThick
			
			baseSideZ = 1146 # to have eaqual modules size
			modulesSideZ = self.gFSZ - baseSideZ - self.gThick - topsSize

			sideZ = modulesSideZ / (mNum - 1)
			depth = self.gFSY - thickBack - thickFront
			
			# #######################
			# Base
			# #######################
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor') + ' M1'
			o1.Length = self.gFSX - (2 * self.gThick)
			o1.Height = self.gThick
			o1.Width = depth
			pl = FreeCAD.Vector(sx + self.gThick, sy + thickFront, sz + 100)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left') + ' M1'
			o2.Length = self.gThick
			o2.Height = baseSideZ
			o2.Width = depth
			pl = FreeCAD.Vector(sx, sy + thickFront, sz)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right') + ' M1'
			o3.Length = self.gThick
			o3.Height = baseSideZ
			o3.Width = depth
			pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy + thickFront, sz)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
		
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back') + ' M1'
			o4.Length = self.gFSX
			o4.Height = baseSideZ - 100 + self.gThick
			o4.Width = thickBack
			pl = FreeCAD.Vector(sx, sy + depth + thickFront, sz + 100)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			MagicPanels.setColor(o4, 3, (1.0, 1.0, 1.0, 1.0), "color")
			
			# Top
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o6.Label = translate('magicStart', 'Top') + ' M1'
			o6.Length = self.gFSX
			o6.Height = self.gThick
			o6.Width = depth
			pl = FreeCAD.Vector(sx, sy + thickFront, sz + baseSideZ)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")
		
			# Front
			o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
			o7.Label = translate('magicStart', 'Front') + ' M1'
			o7.Length = self.gFSX - (2 * self.gThick) + offsetFrontL + offsetFrontR
			o7.Height = baseSideZ - 100 - self.gThick + offsetFrontB + offsetFrontT
			o7.Width = thickFront
			pl = FreeCAD.Vector(sx + self.gThick - offsetFrontL, sy, sz + 100 + self.gThick - offsetFrontB)
			o7.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o7, 0, self.gColor, "color")
			
			# create container
			objects = [o1, o2, o3, o4, o6, o7]
			label = translate('magicStart', 'Module 1')
			container = MagicPanels.createContainer(objects, label, False)
			
			# #######################
			# Modules
			# #######################
			
			for i in range(1, mNum):
			
				posZ = baseSideZ + (i * self.gThick) + ((i - 1) * sideZ)

				# Left Side
				o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
				o1.Label = translate('magicStart', 'Left') + ' M' + str(i+1)
				o1.Length = self.gThick
				o1.Height = sideZ
				o1.Width = depth
				pl = FreeCAD.Vector(sx, sy + thickFront, sz + posZ)
				o1.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o1, 0, self.gColor, "color")
				
				# Right Side
				o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
				o2.Label = translate('magicStart', 'Right') + ' M' + str(i+1)
				o2.Length = self.gThick
				o2.Height = sideZ
				o2.Width = depth
				pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy + thickFront, sz + posZ)
				o2.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o2, 0, self.gColor, "color")
				
				# Back
				o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
				o3.Label = translate('magicStart', 'Back') + ' M' + str(i+1)
				o3.Length = self.gFSX
				o3.Height = sideZ + self.gThick
				o3.Width = thickBack
				pl = FreeCAD.Vector(sx, sy + thickFront + depth, sz + posZ)
				o3.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o3, 0, self.gColor, "color")
				MagicPanels.setColor(o3, 3, (1.0, 1.0, 1.0, 1.0), "color")
		
				# Shelf
				o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
				o4.Label = translate('magicStart', 'Shelf') + ' M' + str(i+1)
				o4.Length = self.gFSX - (2 * self.gThick) - (2 * shelfOS)
				o4.Height = thickShelf
				o4.Width = depth - self.gThick
				pZ = posZ + (sideZ / 2) - (thickShelf / 2)
				pl = FreeCAD.Vector(sx + self.gThick + shelfOS, sy + thickFront + self.gThick, sz + pZ)
				o4.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o4, 0, self.gColor, "color")
			
				# Top
				o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
				o5.Label = translate('magicStart', 'Top') + ' M' + str(i+1)
				o5.Length = self.gFSX
				o5.Height = self.gThick
				o5.Width = depth
				pl = FreeCAD.Vector(sx, sy + thickFront, sz + posZ + sideZ)
				o5.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o5, 0, self.gColor, "color")
				
				# Front
				o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
				o6.Label = translate('magicStart', 'Front') + ' M1' + str(i+1)
				o6.Length = self.gFSX - (2 * self.gThick) + offsetFrontL + offsetFrontR
				o6.Height = sideZ + offsetFrontB + offsetFrontT
				o6.Width = thickFront
				pl = FreeCAD.Vector(sx + self.gThick - offsetFrontL, sy, sz + posZ - offsetFrontB)
				o6.Placement = FreeCAD.Placement(pl, self.gR)
				MagicPanels.setColor(o6, 0, self.gColor, "color")
			
				# create container
				objects = [o1, o2, o3, o4, o5, o6]
				label = translate('magicStart', 'Module ') + str(i+1)
				container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF86(self):
			
			thick = MagicPanels.unit2value( self.oThickE.text() )
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			startX = MagicPanels.unit2value( self.oStartXE.text() )
			startY = MagicPanels.unit2value( self.oStartYE.text() )
			startZ = MagicPanels.unit2value( self.oStartZE.text() )
			
			sizeX = MagicPanels.unit2value( self.oWidthE.text() )
			sizeY = MagicPanels.unit2value( self.oDepthE.text() )
			sizeZ = MagicPanels.unit2value( self.oHeightE.text() )
			
			edgeband = MagicPanels.gEdgebandThickness
			if MagicPanels.gEdgebandApply == "everywhere":
				edgebandE = edgeband
			else:
				edgebandE = 0
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o1.Label = translate('magicStart', 'Left M')
			o1.Length = thick
			o1.Height = sizeZ - thick - (2 * edgebandE)
			o1.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX, startY + edgeband, startZ + edgebandE)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o2.Label = translate('magicStart', 'Right M')
			o2.Length = thick
			o2.Height = sizeZ - thick - (2 * edgebandE)
			o2.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX + sizeX - thick, startY + edgeband, startZ + edgebandE)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Back
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o3.Label = translate('magicStart', 'Back M')
			o3.Length = sizeX - (2 * thick) - (2 * edgebandE)
			o3.Height = sizeZ - thick - (2 * edgebandE)
			o3.Width = thickBack
			pl = FreeCAD.Vector(startX + thick + edgebandE, startY + sizeY - thickBack, startZ + edgebandE)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o4.Label = translate('magicStart', 'Top M')
			o4.Length = sizeX - (2 * edgeband)
			o4.Height = thick
			o4.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgeband, startY + edgeband, startZ + sizeZ - thick)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Shelf
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o5.Label = translate('magicStart', 'Shelf M')
			o5.Length = sizeX - (2 * thick) - (2 * edgebandE) - (2 * shelfOS)
			o5.Height = thickShelf
			o5.Width = sizeY - thick - thick - thickBack - edgeband - edgebandE
			px = startX + thick + edgebandE + shelfOS
			py = startY + thick + thick + edgeband
			pz = startZ + (sizeZ / 2) - thickShelf
			pl = FreeCAD.Vector(px, py, pz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5]
			label = "Module"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF87(self):
			
			thick = MagicPanels.unit2value( self.oThickE.text() )
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			startX = MagicPanels.unit2value( self.oStartXE.text() )
			startY = MagicPanels.unit2value( self.oStartYE.text() )
			startZ = MagicPanels.unit2value( self.oStartZE.text() )
			
			sizeX = MagicPanels.unit2value( self.oWidthE.text() )
			sizeY = MagicPanels.unit2value( self.oDepthE.text() )
			sizeZ = MagicPanels.unit2value( self.oHeightE.text() )
			
			edgeband = MagicPanels.gEdgebandThickness
			if MagicPanels.gEdgebandApply == "everywhere":
				edgebandE = edgeband
			else:
				edgebandE = 0
			
			# Left Side
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o1.Label = translate('magicStart', 'Left M')
			o1.Length = thick
			o1.Height = sizeZ - thick - (2 * edgebandE)
			o1.Width = sizeY - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX, startY + edgeband, startZ + edgebandE)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Right Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o2.Label = translate('magicStart', 'Right M')
			o2.Length = thick
			o2.Height = sizeZ - thick - (2 * edgebandE)
			o2.Width = sizeY - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + sizeX - thick, startY + edgeband, startZ + edgebandE)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Back HDF
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o3.Label = translate('magicStart', 'Back M')
			o3.Length = sizeX
			o3.Height = sizeZ
			o3.Width = thickBack
			pl = FreeCAD.Vector(startX, startY + sizeY - thickBack, startZ)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			MagicPanels.setColor(o3, 3, (1.0, 1.0, 1.0, 1.0), "color")
			
			# Top
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o4.Label = translate('magicStart', 'Top M')
			o4.Length = sizeX - (2 * edgeband)
			o4.Height = thick
			o4.Width = sizeY - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgeband, startY + edgeband, startZ + sizeZ - thick)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Shelf
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o5.Label = translate('magicStart', 'Shelf M')
			o5.Length = sizeX - (2 * thick) - (2 * edgebandE) - (2 * shelfOS)
			o5.Height = thickShelf
			o5.Width = sizeY - thick - thick - thickBack - edgeband -  edgebandE
			px = startX + thick + edgebandE + shelfOS
			py = startY + thick + thick + edgeband
			pz = startZ + (sizeZ / 2) - thickShelf
			pl = FreeCAD.Vector(px, py, pz)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5]
			label = "Module"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()

		# ############################################################################
		def createF88(self):
			
			thick = MagicPanels.unit2value( self.oThickE.text() )
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			startX = MagicPanels.unit2value( self.oStartXE.text() )
			startY = MagicPanels.unit2value( self.oStartYE.text() )
			startZ = MagicPanels.unit2value( self.oStartZE.text() )
			
			sizeX = MagicPanels.unit2value( self.oWidthE.text() )
			sizeY = MagicPanels.unit2value( self.oDepthE.text() )
			sizeZ = MagicPanels.unit2value( self.oHeightE.text() )
			
			edgeband = MagicPanels.gEdgebandThickness
			if MagicPanels.gEdgebandApply == "everywhere":
				edgebandE = edgeband
			else:
				edgebandE = 0
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor M')
			o1.Length = sizeX - (2 * thick) - (2 * edgebandE)
			o1.Height = thick
			o1.Width = sizeY - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + thick + edgebandE, startY + edgeband, startZ + 100)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left M')
			o2.Length = thick
			o2.Height = sizeZ - (2 * edgeband) - thick
			o2.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX, startY + edgeband, startZ + edgeband)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right M')
			o3.Length = thick
			o3.Height = sizeZ - (2 * edgeband) - thick
			o3.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX + sizeX - thick, startY + edgeband, startZ + edgeband)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back M')
			o4.Length = sizeX - (2 * thick)
			o4.Height = sizeZ - 100 - thick
			o4.Width = thickBack
			pl = FreeCAD.Vector(startX + thick, startY + sizeY - thickBack, startZ + 100)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top M')
			o5.Length = sizeX - (2 * edgebandE)
			o5.Height = thick
			o5.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgebandE, startY + edgeband, startZ + sizeZ - thick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")

			# Shelf
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o6.Label = translate('magicStart', 'Shelf M')
			o6.Length = sizeX - (2 * thick) - (2 * edgebandE) - (2 * shelfOS)
			o6.Height = thickShelf
			o6.Width = sizeY - thickBack - thick - edgeband - edgebandE
			px = startX + thick + edgebandE + shelfOS
			py = startY + thick + edgeband
			pz = startZ + 100 + ((sizeZ - 100) / 2) - (thickShelf / 2)
			pl = FreeCAD.Vector(px, py, pz)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5, o6]
			label = "Module"
			container = MagicPanels.createContainer(objects, label, False)
			
			# recompute
			FreeCAD.ActiveDocument.recompute()
		
		# ############################################################################
		def createF89(self):
			
			thick = MagicPanels.unit2value( self.oThickE.text() )
			thickBack = MagicPanels.unit2value( self.oThickBackE.text() )
			thickShelf = MagicPanels.unit2value( self.oThickShelfE.text() )
			shelfOS = MagicPanels.gShelfOffsetSides / 2
			
			startX = MagicPanels.unit2value( self.oStartXE.text() )
			startY = MagicPanels.unit2value( self.oStartYE.text() )
			startZ = MagicPanels.unit2value( self.oStartZE.text() )
			
			sizeX = MagicPanels.unit2value( self.oWidthE.text() )
			sizeY = MagicPanels.unit2value( self.oDepthE.text() ) - thickBack
			sizeZ = MagicPanels.unit2value( self.oHeightE.text() )
			
			edgeband = MagicPanels.gEdgebandThickness
			if MagicPanels.gEdgebandApply == "everywhere":
				edgebandE = edgeband
			else:
				edgebandE = 0
			
			# Floor
			o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
			o1.Label = translate('magicStart', 'Floor M')
			o1.Length = sizeX - (2 * thick) - (2 * edgebandE)
			o1.Height = thick
			o1.Width = sizeY - thickBack - (2 * edgeband)
			pl = FreeCAD.Vector(startX + thick + edgebandE, startY + edgeband, startZ + 100)
			o1.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o1, 0, self.gColor, "color")
			
			# Left Side
			o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
			o2.Label = translate('magicStart', 'Left M')
			o2.Length = thick
			o2.Height = sizeZ - (2 * edgeband) - thick
			o2.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX, startY + edgeband, startZ + edgeband)
			o2.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o2, 0, self.gColor, "color")
			
			# Right Side
			o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
			o3.Label = translate('magicStart', 'Right M')
			o3.Length = thick
			o3.Height = sizeZ - (2 * edgeband) - thick
			o3.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX + sizeX - thick, startY + edgeband, startZ + edgeband)
			o3.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o3, 0, self.gColor, "color")
			
			# Back
			o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
			o4.Label = translate('magicStart', 'Back M')
			o4.Length = sizeX
			o4.Height = sizeZ - 100
			o4.Width = thickBack
			pl = FreeCAD.Vector(startX, startY + sizeY, startZ + 100)
			o4.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o4, 0, self.gColor, "color")
			MagicPanels.setColor(o4, 3, (1.0, 1.0, 1.0, 1.0), "color")
			
			# Top
			o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
			o5.Label = translate('magicStart', 'Top M')
			o5.Length = sizeX - (2 * edgebandE)
			o5.Height = thick
			o5.Width = sizeY - (2 * edgeband)
			pl = FreeCAD.Vector(startX + edgebandE, startY + edgeband, startZ + sizeZ - thick)
			o5.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o5, 0, self.gColor, "color")

			# Shelf
			o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
			o6.Label = translate('magicStart', 'Shelf M')
			o6.Length = sizeX - (2 * thick) - (2 * edgebandE) - (2 * shelfOS)
			o6.Height = thickShelf
			o6.Width = sizeY - edgeband - edgebandE
			px = startX + thick + edgebandE + shelfOS
			py = startY + edgeband
			pz = startZ + 100 + ((sizeZ - 100) / 2) - (thickShelf / 2)
			pl = FreeCAD.Vector(px, py, pz)
			o6.Placement = FreeCAD.Placement(pl, self.gR)
			MagicPanels.setColor(o6, 0, self.gColor, "color")

			objects = [o1, o2, o3, o4, o5, o6]
			label = "Module"
			container = MagicPanels.createContainer(objects, label, False)
			
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

