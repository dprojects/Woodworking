import FreeCAD, FreeCADGui
from PySide import QtGui, QtCore

import MagicPanels

translate = FreeCAD.Qt.translate

try:
	
	objects = ""
	
	if len(FreeCADGui.Selection.getSelection()) == 0:
		if len(FreeCAD.ActiveDocument.Objects) == 0:
			raise
		else:
			objects = FreeCAD.ActiveDocument.Objects
	else:
		objects = FreeCADGui.Selection.getSelection()
	
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

	s1 = MagicPanels.getVertexAxisCross(minX, maxX)
	s2 = MagicPanels.getVertexAxisCross(minY, maxY)
	s3 = MagicPanels.getVertexAxisCross(minZ, maxZ)

	mX = round(s1, 2)
	mY = round(s2, 2)
	mZ = round(s3, 2)

	info = ""
	
	info += '<table cellpadding=8>'
	
	info += '<tr><td><b>' + translate('showOccupiedSpace', 'Occupied space along X axis') + ': ' + '</b></td>'
	info += '<td style="text-align:right">' + MagicPanels.unit2gui(mX) + '</td></tr>'
	
	info += '<tr><td><b>' + translate('showOccupiedSpace', 'Occupied space along Y axis') + ': ' + '</b></td>'
	info += '<td style="text-align:right">' + MagicPanels.unit2gui(mY) + '</td></tr>'
	
	info += '<tr><td><b>' + translate('showOccupiedSpace', 'Occupied space along Z axis') + ': ' + '</b></td>'
	info += '<td style="text-align:right">' + MagicPanels.unit2gui(mZ) + '</td></tr>'
	
	info += '</table>'

	info += '<br><br>' + '<b>' + translate('showOccupiedSpace', 'Note') + ':' + '</b>' + ' '
	
	info += translate('showOccupiedSpace', 'They are not dimensions taken from selected objects, they are occupied space in 3D by the selected objects. The values are calculated from raw vertex. You have to be careful because the dimensions are rounded and given in raw form.') + '<br><br>'
	
	info += translate('showOccupiedSpace', 'You can see the difference for all rotated elements. For rotated Cube elements the occupied space in 3D will not be the same as dimensions.') + '<br><br>'
	info += translate('showOccupiedSpace', 'However, this approach might be very useful at furniture designing process. For example you can see how much space in your room will take opened front of the furniture. Normally, all the Pad or Cube elements, should be created according to the XYZ plane, so there will be no difference between the real dimensions and occupied space in 3D.')

	msg = QtGui.QMessageBox()
	msg.setWindowTitle(translate('showOccupiedSpace', 'showOccupiedSpace'))
	msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
	msg.setText(info)
	
	# set theme
	QtCSS = MagicPanels.getTheme(MagicPanels.gTheme)
	if QtCSS == "":
		css = '''
			QLabel {
				padding: 15px;
				margin: 15px 25px 15px 0px;
				color: #000000;
				border-left: 2px solid #C4C4C4;
				border-top: 2px solid #C4C4C4;
				border-right: 2px solid #FFFFFF;
				border-bottom: 2px solid #FFFFFF;
				background-color: qlineargradient( 
					x1: 0, y1: 0, 
					x2: 1, y2: 1,
					stop: 0 #FFFFFF, stop: 1 #C4C4C4
				);
			}
			
		'''
	else:
		css = '''
			QLabel { 
				padding: 15px;
				margin: 15px 25px 15px 0px;
				color: #000000;
			}
		'''
	
	msg.setStyleSheet(QtCSS + css)
	msg.exec_()
	
except:
	
	info = ""

	info += translate('showOccupiedSpace', '<b>Please create document and objects to see occupied space by all elements or select objects to see occupied space only by selected objects. </b><br><br><b>Note:</b> This tool allows you to calculate the overall occupied space in 3D by the selected parts or whole model, if nothing is selected. This approach might be very useful at furniture designing process. For example you can see how much space in your room will take opened front of the furniture or how much space take selected parts of the furniture. Normally, all the `Pad` or `Cube` elements, should be created according to the `XYZ` plane, so there will be no difference between the real dimensions and occupied space in 3D. To select more objects hold left CTRL key during selection.')
	
	MagicPanels.showInfo("showOccupiedSpace", info)
