# ###################################################################################################################
'''

This showSpaceSelected macro allows to calculate occupied space in 3D by all the selected parts.
Note: This FreeCAD macro is part of Woodworking workbench. However, it can be used as standalone macro.

Author: Darek L (github.com/dprojects)
Latest version: https://github.com/dprojects/Woodworking/blob/master/Tools/showSpaceSelected.py

Certified platform:

OS: Ubuntu 22.04 LTS (XFCE/xubuntu)
Word size of FreeCAD: 64-bit
Version: 0.20.29177 (Git) AppImage
Build type: Release
Branch: (HEAD detached at 0.20)
Hash: 68e337670e227889217652ddac593c93b5e8dc94
Python 3.9.13, Qt 5.12.9, Coin 4.0.0, Vtk 9.1.0, OCC 7.5.3
Locale: English/United States (en_US)
Installed mods: 
  * Woodworking 0.20.29177

https://github.com/dprojects/Woodworking

'''
# ###################################################################################################################


import FreeCAD, FreeCADGui
from PySide import QtGui
from PySide import QtCore

translate = FreeCAD.Qt.translate


# ###################################################################################################################
def switchApproximation(iA, iB):

	if iA >= 0 and iB >= 0 and iB > iA:
		return iB - iA
	if iB >= 0 and iA >= 0 and iA > iB:
		return iA - iB
		
	if iA < 0 and iB >= 0 and iB > iA:
		return abs(iA) + iB
	if iB < 0 and iA >= 0 and iA > iB:
		return abs(iB) + iA

	if iA < 0 and iB <= 0 and iB > iA:
		return abs(iA) - abs(iB)
	if iB < 0 and iA <= 0 and iA > iB:
		return abs(iB) - abs(iA)

	return 0


# ###################################################################################################################
info = ""

try:
	init = 0

	minX = 0
	minY = 0
	minZ = 0

	maxX = 0
	maxY = 0
	maxZ = 0

	mX = 0
	mY = 0
	mZ = 0

	objects = FreeCADGui.Selection.getSelection()

	for o in objects:
		
		try:
			
			vs = getattr(o.Shape, "Vertex"+"es")
			
			for v in vs:
				
				[ x, y, z ] = [ v.X, v.Y, v.Z ]
		
				if init == 0:
					[ minX, minY, minZ ] = [ x, y, z ]
					[ maxX, maxY, maxZ ] = [ x, y, z ]
					init = 1
				
				if x > maxX:
					maxX = x
				
				if y > maxY:
					maxY = y

				if z > maxZ:
					maxZ = z

				if x < minX:
					minX = x

				if y < minY:
					minY = y

				if z < minZ:
					minZ = z

		except:
			skip = 1

	s1 = switchApproximation(minX, maxX)
	s2 = switchApproximation(minY, maxY)
	s3 = switchApproximation(minZ, maxZ)

	mX = round(s1, 2)
	mY = round(s2, 2)
	mZ = round(s3, 2)

	info += translate('showSpaceSelected1', 'Occupied space in 3D by all the selected parts:') + '<br><br>'
	
	info += '<table cellpadding=5 style="background-color:#DDDDFF;">'
	
	info += '<tr><td><b>' + translate('showSpaceSelected2', 'Space along X axis') + ': ' + '</b></td>'
	info += '<td style="text-align:right">' + str(mX) + '</td></tr>'
	
	info += '<tr><td><b>' + translate('showSpaceSelected3', 'Space along Y axis') + ': ' + '</b></td>'
	info += '<td style="text-align:right">' + str(mY) + '</td></tr>'
	
	info += '<tr><td><b>' + translate('showSpaceSelected4', 'Space along Z axis') + ': ' + '</b></td>'
	info += '<td style="text-align:right">' + str(mZ) + '</td></tr>'
	
	info += '</table>'

except:

	if info == "":
		info += translate('showSpaceSelected5', 'Please select parts to calculate occupied space in 3D.')

info += '<br><br>' + '<b>' + translate('showSpaceSelected6', 'Note') + ':' + '</b>' + ' '

info += translate('showSpaceSelected7', 'They are not dimensions taken from selected objects, they are occupied space in 3D by the selected objects. The values are calculated from raw vertex. You have to be careful because the dimensions are rounded and given in raw form.') + '<br><br>'

info += translate('showSpaceSelected8', 'You can see the difference for all rotated elements. For rotated Cube elements the occupied space in 3D will not be the same as dimensions.') + '<br><br>'

info += translate('showSpaceSelected9', 'However, this approach might be very useful at furniture designing process. For example you can see how much space in your room will take opened front of the furniture. Normally, all the Pad or Cube elements, should be created according to the XYZ plane, so there will be no difference between the real dimensions and occupied space in 3D.')

msg = QtGui.QMessageBox()
msg.setWindowTitle(translate('showSpaceSelected10', 'showSpaceSelected'))
msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
msg.setText(info)
msg.exec_()

