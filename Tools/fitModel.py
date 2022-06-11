import FreeCADGui

FreeCADGui.SendMsgToActiveView("ViewFit")
FreeCADGui.activeDocument().activeView().viewIsometric()
