try:
	
	import FreeCAD, FreeCADGui

	FreeCADGui.SendMsgToActiveView("ViewFit")
	FreeCADGui.activeDocument().activeView().viewIsometric()

except:

	import FreeCAD
	translate = FreeCAD.Qt.translate
	
	from PySide import QtGui
	from PySide import QtCore
	import MagicPanels
	
	info = ''
	
	info += translate('fitModelInfo', 'Please create model to fit it to the screen. This tool allows to fit model to the screen view and also rotate the model view to the base XY position (0 key press).')
	
	MagicPanels.showInfo("fitModel", info)
