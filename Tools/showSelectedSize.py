# ###################################################################################################################
'''

This showSelectedSize macro allows to calculate the overall dimensions of the selected parts. 
This will show max width, depth and height of the selected elements.

Note: This FreeCAD macro is part of Woodworking workbench. However, it can be used as standalone macro.

Author: Darek L (github.com/dprojects)
Latest version: https://github.com/dprojects/Woodworking/blob/master/Tools/showSelectedSize.py

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

info = ""

try:
	init = 0

	minX = 0
	minY = 0
	minZ = 0

	maxX = 0
	maxY = 0
	maxZ = 0

	mWidth = 0
	mDepth = 0
	mHeight = 0

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

	mWidth = round(s1, 2)
	mDepth = round(s2, 2)
	mHeight = round(s3, 2)

	info += 'Occupied space in 3D by all the selected parts: ' + '<br><br>'
	info += '<table>'
	info += '<tr><td><b>' + 'Width: ' + '</b></td><td style="text-align:right">' + str(mWidth) + '</td></tr>'
	info += '<tr><td><b>' + 'Depth: ' + '</b></td><td style="text-align:right">' + str(mDepth) + '</td></tr>'
	info += '<tr><td><b>' + 'Height: ' + '</b></td><td style="text-align:right">' + str(mHeight) + '</td></tr>'
	info += '</table>'

except:

	if info == "":
		info += "Please select parts to calculate occupied space in 3D."

info += '<br><br>'
info += '<b>Note:</b> '
info += 'They are not dimensions taken from selected objects, they are occupied space in 3D by the selected objects. '
info += 'They values are calculated from raw vertex. You have to be careful because the dimensions are rounded '
info += 'and given in raw form. '
info += '<br><br>'
info += 'You can see the difference for all rotated elements. For rotated Cube elements the occupied space in 3D will '
info += 'not be the same as dimensions. '
info += '<br><br>'
info += 'However, this approach might be very useful at furniture designing process. ' 
info += 'For example you can see how much space in your room will take opened front of the furniture. '
info += 'Normally, all the Pad or Cube elements, should be created according to the XYZ plane, '
info += 'so there will be no difference between the real dimensions and occupied space in 3D. '

msg = QtGui.QMessageBox()
msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
msg.setText(info)
msg.exec_()

