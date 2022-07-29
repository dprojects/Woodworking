import FreeCAD, FreeCADGui
import FreeCADGui as Gui

translate = FreeCAD.Qt.translate

try:

	# ############################################################################
	# This part of code has been created by Werner Mayer (wmayer) at forum:
	# https://forum.freecadweb.org/viewtopic.php?p=187448#p187448
	# ############################################################################
	
	from PySide import QtCore
	from PySide import QtGui
	
	class AboutInfo(QtCore.QObject):
		def eventFilter(self, obj, ev):
			if obj.metaObject().className() == "Gui::Dialog::AboutDialog":
				if ev.type() == ev.ChildPolished:
					mo = obj.metaObject()
					index = mo.indexOfMethod("on_copyButton_clicked()")
					if index > 0:
						mo.invokeMethod(obj, "on_copyButton_clicked")
						QtGui.qApp.postEvent(obj, QtGui.QCloseEvent())
	    
			return False
	
	ai=AboutInfo()
	QtGui.qApp.installEventFilter(ai)
	Gui.runCommand("Std_About")
	QtGui.qApp.removeEventFilter(ai)
	
	# ############################################################################
	# added by Darek L below:
	# ############################################################################
	
	def showQtGUI():
		
		class QtMainClass(QtGui.QDialog):
	
			def __init__(self):
				super(QtMainClass, self).__init__()
				self.initUI()
	
			def initUI(self):
				
				# ############################################################################
				# set screen
				# ############################################################################
				
				# tool screen size
				toolSW = 410
				toolSH = 400
				
				# active screen size - FreeCAD main window
				gSW = FreeCADGui.getMainWindow().width()
				gSH = FreeCADGui.getMainWindow().height()

				# tool screen position
				gPW = int( ( gSW - toolSW ) / 2 )
				gPH = int( ( gSH - toolSH ) / 2 )

				# ############################################################################
				# main window
				# ############################################################################
				
				self.result = userCancelled
				self.setGeometry(gPW, gPH, toolSW, toolSH)
				self.setWindowTitle(translate('debugInfo', 'platform details for bug report'))
				self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
	
				# output
				Info = ""
				Info += translate('debugInfo', 'Has been copied to clipboard:')
				Info += "\n"
				
				self.oInfo1 = QtGui.QLabel(Info, self)
				self.oInfo1.move(5, 10)
				
				self.o = QtGui.QTextEdit(self)
				self.o.setMinimumSize(400, 250)
				self.o.setMaximumSize(400, 250)
				self.o.move(5, 40)
				
				self.o.setPlainText("")
				self.o.paste()
	
				Info = ""
				Info += translate('debugInfo', 'Note:')
				Info += "\n\n"
				Info += translate('debugInfo', 'CTRL-V - to paste it at your forum topic')
				Info += "\n\n"
				Info += translate('debugInfo', 'CTRL-A, CTRL-C - to copy again')
				
				self.oInfo2 = QtGui.QLabel(Info, self)
				self.oInfo2.move(5, 300)
	
				# show
				self.show()
				
		userCancelled = "Cancelled"
		userOK = "OK"
		
		form = QtMainClass()
		form.exec_()
		
		if form.result == userCancelled:
			pass
	
	# ###################################################################################################################
	# MAIN
	# ###################################################################################################################
	
	showQtGUI()

except:

	import FreeCAD, FreeCADGui
	from PySide import QtGui
	from PySide import QtCore

	info = ''
	info += translate('debugInfo', 'There is an error during getting debug information.')
	info += '<br>'
	info += translate('debugInfo', 'It probably means')
	info += ' ' + '<span style="color:red;">'
	info += translate('debugInfo', 'Your FreeCAD installation is incorrect.')
	info += '</span>' + '<br><br>'
	info += translate('debugInfo', 'For more details please see:')
	info += ' ' + '<a href="https://github.com/dprojects/Woodworking#certified-platforms">'
	info += translate('debugInfo', 'Woodworking workbench certified platforms.')
	info += '</a>'

	msg = QtGui.QMessageBox()
	msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
	msg.setText(info)
	msg.exec_()
