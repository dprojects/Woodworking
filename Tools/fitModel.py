try:
	
	import FreeCADGui

	FreeCADGui.SendMsgToActiveView("ViewFit")
	FreeCADGui.activeDocument().activeView().viewIsometric()

except:

	info = "Please create active document and model to fit it to the screen."
	
	from PySide import QtGui
	from PySide import QtCore
	
	msg = QtGui.QMessageBox()
	msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
	msg.setText(info)
	msg.exec_()
