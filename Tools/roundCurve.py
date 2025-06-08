import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

try:

	selection = FreeCADGui.Selection.getSelection()

	if len(selection) < 1:
		raise

	defaultAngularDeflection = 28.50
	defaultDeviation = 0.50

	for curve in selection:

		if curve.ViewObject.AngularDeflection == defaultAngularDeflection:
			curve.ViewObject.AngularDeflection = 1.0
		else:
			curve.ViewObject.AngularDeflection = defaultAngularDeflection

		if curve.ViewObject.Deviation == defaultDeviation:
			curve.ViewObject.Deviation = 0.25
		else:
			curve.ViewObject.Deviation = defaultDeviation
		
	FreeCAD.ActiveDocument.recompute()

except:
	
	info = ""

	info += translate('roundCurve', '<b>Select curved objects to improve rendering. </b><br><br><b>Note:</b> This tool allows to improve curve visibility. It makes the curve to look more rounded. Normally, circle Sketch is rendering from straight line segments. If you want to align panel to the curve manually this might be problem to hit exactly the point you want at curve. This tool may help for more precised alignment. If you select the curve and click this tool again the curve will back to default settings. To select more object hold left CTRL key during selection.')
	
	MagicPanels.showInfo("roundCurve", info)

