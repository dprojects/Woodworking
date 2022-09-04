import FreeCAD, FreeCADGui
from PySide import QtGui

import MagicPanels

translate = FreeCAD.Qt.translate

# ###################################################################################################################
def showCellAlias(index):
		
	r = index.row() + 1
	c = index.column() + 1
	
	key = MagicPanels.sheetGetKey(c, r)
		
	sheet = FreeCADGui.Selection.getSelection()[0]
	alias = str(sheet.getAlias(key))
	
	
	FreeCADGui.Selection.clearSelection()
	FreeCADGui.Selection.addSelection(sheet)
	
	for o in FreeCAD.ActiveDocument.Objects:
		try:
			
			if str(o.ExpressionEngine).find(alias) != -1:
				FreeCADGui.Selection.addSelection(o)
	
		except:
			skip = 1

# ###################################################################################################################
# main
# ###################################################################################################################

try:
	
	# search for active spreadsheet window
	mw = FreeCADGui.getMainWindow()
	mdiarea = mw.findChild(QtGui.QMdiArea)
	subw = mdiarea.subWindowList()

	for o in subw:
		if o.widget().metaObject().className() == "SpreadsheetGui::SheetView":
			sw = o.widget()
			tv = sw.findChild(QtGui.QTableView)

	objects = FreeCADGui.Selection.getSelection()
	
	# if there is no selection deactivate the preview mode
	if len(objects) < 1:
		
		tv.clicked.disconnect()
	
		info = ""
		info += translate('showAlias', '<b>The preview mode has been deactivated. You can turn it on again at any time. </b><br><br>')
		MagicPanels.showInfo("showAlias", info)
	
	else:
		
		# if first object is spreadsheet
		if objects[0].isDerivedFrom("Spreadsheet::Sheet"):

			tv.clicked.connect(showCellAlias)
		
			info = ""
			info += translate('showAlias', '<b>The preview mode has been activated. Select spreadsheet cell with alias to see objects. </b><br><br>')
			MagicPanels.showInfo("showAlias", info)
		
		# if first selected object is not spreadsheet show info how to use it
		else:
			
			raise
		
except:
	
	info = ""
	
	info += translate('showAlias', '<b>To see all objects with alias: <ol><li>First select spreadsheet at objects Tree.</li><li>Click this tool icon to activate the preview mode.</li><li>Click any spreadsheet cell with alias.</li></b><br><br><b>Note:</b> This tool needs to be activated to work. To activate this tool you have to select spreadsheet at objects Tree and click this tool icon. If this tool will be activated you can select any cell with alias to see all objects selected. The selected objects at 3D model will be those that uses the selected alias. Also the objects will be selected at objects Tree. To finish the preview mode, click the tool icon without any selection.')

	MagicPanels.showInfo("showAlias", info)

