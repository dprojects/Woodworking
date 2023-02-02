import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:
	FreeCADGui.SendMsgToActiveView("ViewFit")
	FreeCADGui.ActiveDocument.ActiveView.viewIsometric()

except:

	info = translate('fitModelInfo', 'Please create model to fit it to the screen. This tool allows to fit model to the screen view and also rotate the model view to the base XY position (0 key press).')
	
	MagicPanels.showInfo("fitModel", info)
