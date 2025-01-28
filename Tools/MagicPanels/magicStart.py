import FreeCAD, FreeCADGui
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWidgets import *
import os, sys

import MagicPanels

translate = FreeCAD.Qt.translate

class NumberEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setText("0")
        self.setValidator(QDoubleValidator(0.99, 99.99, 2))
        #self.MaxLength(5)
        #self.Alignment(Qt.AlignRight)



		# ############################################################################
class createF0(object):
    gFSX = 500   # furniture size X (width)
    gFSY = 400   # furniture size Y (depth)
    gFSZ = 760   # furniture size Z (height)
    gThick = 18  # wood thickness

    gColor = (0.9686274528503418, 0.7254902124404907, 0.42352941632270813, 0.0)
    gR = FreeCAD.Rotation(0, 0, 0)

    def __init__(self):
        # draw the description and icon
        self.linfo = QLabel("give me some info")
        self.icon = getIcon("msf000")

        # draw the wood thickness button
        self.lthickness = QLabel("Wood thickness:")
        self.tbThickness = NumberEdit()

        # draw the XYZ offset, but make it horizontal
        self.tbOffsetX = NumberEdit()
        self.tbOffsetY = NumberEdit()
        self.tbOffsetZ = NumberEdit()
        self.HOffset = QHBoxLayout() # horizontal text boxes
        self.HOffset.addWidget(self.tbOffsetX)
        self.HOffset.addWidget(self.tbOffsetY)
        self.HOffset.addWidget(self.tbOffsetZ)

        # calc button
        self.bCalc = QPushButton("calculate furniture")
        #self.bCalc.clicked.connect(self.calculate())

        # draw the Start XYZ (origin?)
        self.tbStartX = NumberEdit()
        self.tbStartY = NumberEdit()
        self.tbStartZ = NumberEdit()
        self.HStart = QHBoxLayout() # horizontal text boxes
        self.HStart.addWidget(self.tbStartX)
        self.HStart.addWidget(self.tbStartY)
        self.HStart.addWidget(self.tbStartZ)

        self.tbWidth = NumberEdit()
        self.tbHeight = NumberEdit()
        self.tbDepth = NumberEdit()


    def draw(self):

        # place the items in the automatic layout
        self.layout = QFormLayout()
        self.layout.addRow(self.linfo, self.icon)
        self.layout.addRow(self.lthickness, self.tbThickness)
        self.layout.addRow(QLabel("Offset XYZ:"), self.HOffset)
        self.layout.addRow(self.bCalc)
        self.layout.addRow(QLabel("Start XYZ:"), self.HStart)
        self.layout.addRow(QLabel("Furniture width"), self.tbWidth)
        self.layout.addRow(QLabel("Furniture height"), self.tbHeight)
        self.layout.addRow(QLabel("Furniture depth"), self.tbDepth)

        return self.layout

    def create(self):
        sx = float(self.tbStartX.text())
        sy = float(self.tbStartY.text())
        sz = float(self.tbStartZ.text())

        depth = self.gFSY - self.gThick

        # Floor
        o1 = FreeCAD.ActiveDocument.addObject("Part::Box", "Floor")
        o1.Label = translate('magicStart', 'Floor')
        o1.Length = self.gFSX
        o1.Height = self.gThick
        o1.Width = depth
        pl = FreeCAD.Vector(sx, sy + self.gThick, sz)
        o1.Placement = FreeCAD.Placement(pl, self.gR)
        o1.ViewObject.ShapeColor = self.gColor

        # Left Side
        o2 = FreeCAD.ActiveDocument.addObject("Part::Box", "Left")
        o2.Label = translate('magicStart', 'Left')
        o2.Length = self.gThick
        o2.Height = self.gFSZ - (2 * self.gThick)
        o2.Width = depth
        pl = FreeCAD.Vector(sx, sy + self.gThick, sz + self.gThick)
        o2.Placement = FreeCAD.Placement(pl, self.gR)
        o2.ViewObject.ShapeColor = self.gColor

        # Right Side
        o3 = FreeCAD.ActiveDocument.addObject("Part::Box", "Right")
        o3.Label = translate('magicStart', 'Right')
        o3.Length = self.gThick
        o3.Height = self.gFSZ - (2 * self.gThick)
        o3.Width = depth
        pl = FreeCAD.Vector(sx + self.gFSX - self.gThick, sy + self.gThick, sz + self.gThick)
        o3.Placement = FreeCAD.Placement(pl, self.gR)
        o3.ViewObject.ShapeColor = self.gColor

        # Back
        o4 = FreeCAD.ActiveDocument.addObject("Part::Box", "Back")
        o4.Label = translate('magicStart', 'Back')
        o4.Length = self.gFSX - (2 * self.gThick)
        o4.Height = self.gFSZ - (2 * self.gThick)
        o4.Width = self.gThick
        pl = FreeCAD.Vector(sx + self.gThick, sy + depth, sz + self.gThick)
        o4.Placement = FreeCAD.Placement(pl, self.gR)
        o4.ViewObject.ShapeColor = self.gColor

        # Top
        o5 = FreeCAD.ActiveDocument.addObject("Part::Box", "Top")
        o5.Label = translate('magicStart', 'Top')
        o5.Length = self.gFSX
        o5.Height = self.gThick
        o5.Width = depth
        pl = FreeCAD.Vector(sx, sy + self.gThick, sz + self.gFSZ - self.gThick)
        o5.Placement = FreeCAD.Placement(pl, self.gR)
        o5.ViewObject.ShapeColor = self.gColor

        # Front
        o6 = FreeCAD.ActiveDocument.addObject("Part::Box", "Front")
        o6.Label = translate('magicStart', 'Front')
        o6.Length = self.gFSX - self.gThick
        o6.Height = self.gFSZ - self.gThick - 4
        o6.Width = self.gThick
        pl = FreeCAD.Vector(sx + (self.gThick / 2), sy, sz + (self.gThick / 2) + 2)
        o6.Placement = FreeCAD.Placement(pl, self.gR)
        o6.ViewObject.ShapeColor = self.gColor

        # Shelf
        o7 = FreeCAD.ActiveDocument.addObject("Part::Box", "Shelf")
        o7.Label = translate('magicStart', 'Shelf')
        o7.Length = self.gFSX - (2 * self.gThick)
        o7.Height = self.gThick
        o7.Width = depth - (3 * self.gThick)
        pl = FreeCAD.Vector(sx + self.gThick, sy + (3 * self.gThick), sz + (self.gFSZ / 2) - (self.gThick / 2))
        o7.Placement = FreeCAD.Placement(pl, self.gR)
        o7.ViewObject.ShapeColor = self.gColor

        container = FreeCAD.ActiveDocument.addObject('App::LinkGroup','FurnitureModule')
        container.setLink([o1, o2, o3, o4, o5, o6, o7])
        container.Label = "Furniture, Module"

        # recompute
        FreeCAD.ActiveDocument.recompute()


    def calculate(self):

        obj = False
        sub = False

        try:
            obj = FreeCADGui.Selection.getSelection()[0]
            sub = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

        except:
            return

        width = 0
        height = 0
        depth = 0
        startX = 0
        startY = 0
        startZ = 0

        if sub.ShapeType == "Edge":

            width = float(sub.Length)

            if float(MagicPanels.touchTypo(sub)[0].X) < float(MagicPanels.touchTypo(sub)[1].X):
                startX = float(MagicPanels.touchTypo(sub)[0].X)
            else:
                startX = float(MagicPanels.touchTypo(sub)[1].X)

            startY = float(sub.CenterOfMass.y)
            startZ = float(sub.CenterOfMass.z)

        if sub.ShapeType == "Face":

            woodt = float(self.tbThickness.text())
            width = float(obj.Length.Value)
            thick = float(obj.Height.Value)

            depth = float(obj.Width.Value) + woodt
            startY = float(sub.Placement.Base.y) - woodt

            startX = float(sub.Placement.Base.x)
            startZ = float(sub.Placement.Base.z) + thick

        if sub.ShapeType == "Vertex":

            startX = float(sub.Point.x)
            startY = float(sub.Point.y)
            startZ = float(sub.Point.z)

        # add offsets
        startX = startX + float(self.tbStartX.text())
        startY = startY + float(self.tbStartY.text())
        startZ = startZ + float(self.tbStartZ.text())

        FreeCADGui.Selection.clearSelection()

        # set values to text fields
        self.tbStartX.setText(str(startX))
        self.tbStartY.setText(str(startY))
        self.tbStartZ.setText(str(startZ))

        if width != 0:
            self.tbWidth.setText(str(width))

        if height != 0:
            self.tbHeight.setText(str(height))

        if depth != 0:
            self.tbDepth.setText(str(depth))



# ############################################################################
# Global definitions
# ############################################################################

# create a function for generating the new item; then add it to the list
getMenuIndex = {
        translate('magicStart', 'Simple storage ( front outside, back full )'): createF0,
        #	translate('magicStart', 'Simple bookcase ( no front, back HDF )'): createF1,
        #	translate('magicStart', 'Bookcase ( import parametric )'): createF2,
        #	translate('magicStart', 'Simple drawer ( import parametric )'): createF3,
        #	translate('magicStart', 'Simple chair ( import parametric )'): createF4,
        #	translate('magicStart', 'Picture frame ( import parametric )'): createF5,
        #	translate('magicStart', 'Simple table ( import parametric )'): createF6,
        #	translate('magicStart', 'Storage box ( import parametric )'): createF7,
        #	translate('magicStart', 'Dowel 8x35 mm ( import parametric )'): createF8,
        #	translate('magicStart', 'Screw 4x40 mm ( import parametric )'): createF9,
        #	translate('magicStart', 'Modular storage ( front outside, 3 modules )'): createF10,
        #	translate('magicStart', 'Screw 3x20 mm for HDF ( import parametric )'): createF11,
        #	translate('magicStart', 'Screw 5x50 mm ( import parametric )'): createF12,
        #	translate('magicStart', 'Counterbore 2x 5x60 mm ( import parametric )'): createF13,
        #	translate('magicStart', 'Shelf Pin 5x16 mm ( import parametric )'): createF14,
        #	translate('magicStart', 'Angle 40x40x100 mm ( import parametric )'): createF15,
        #	translate('magicStart', 'Foot ( good for cleaning )'): createF16,
        #	translate('magicStart', 'Foot ( standard )'): createF17,
        #	translate('magicStart', 'Foot ( more stable )'): createF18,
        #	translate('magicStart', 'Foot ( decorated )'): createF19,
        #	translate('magicStart', 'Foot ( chair style )'): createF20,
        #	translate('magicStart', 'Drawer with front outside ( fit into the shelf gap)'): createF21,
        #	translate('magicStart', 'Drawer with front inside ( fit into the shelf gap)'): createF22,
        #	translate('magicStart', 'Front outside ( fit into gap )'): createF23,
        #	translate('magicStart', 'Front inside ( fit into gap )'): createF24,
        #	translate('magicStart', 'Shelf ( fit into gap )'): createF25,
        #	translate('magicStart', 'Center side ( fit into gap )'): createF26,
        #	translate('magicStart', 'Simple storage ( front outside, back HDF )'): createF27,
        #	translate('magicStart', 'Simple storage ( front inside, back full )'): createF28,
        #	translate('magicStart', 'Simple storage ( front inside, back HDF )'): createF29,
        #	translate('magicStart', 'Drawer series with front outside ( fit into the shelf gap )'): createF30,
        #	translate('magicStart', 'Drawer series with front inside ( fit into the shelf gap )'): createF31
        }

# ############################################################################
# Qt Main
# ############################################################################

def showQtGUI():

    class QtMainClass(QDialog):

        # ############################################################################
        # globals
        # ############################################################################


        # ############################################################################
        # init
        # ############################################################################

        def __init__(self):
            super(QtMainClass, self).__init__()
            # set the default furniture selection
            self.selectedFurniture = createF0()
            self.initUI()

        def setFurniture(self, furniture):
            self.selectedFurniture = getMenuIndex[furniture]
            self.update()

        def initUI(self):

            # ############################################################################
            # set screen
            # ############################################################################

            # tool screen size
            toolSW = 450
            toolSH = 550

            # active screen size - FreeCAD main window
            gSW = FreeCADGui.getMainWindow().width()
            gSH = FreeCADGui.getMainWindow().height()

            # active screen size (FreeCAD main window)
            gSW = FreeCADGui.getMainWindow().width()
            gSH = FreeCADGui.getMainWindow().height()

            # tool screen position
            gPW = 0 + 50
            gPH = int( gSH - toolSH ) - 30

            # ############################################################################
            # main window
            # ############################################################################

            self.result = userCancelled
            self.setGeometry(gPW, gPH, toolSW, toolSH)
            self.setWindowTitle(translate('magicStart', 'magicStart'))
            self.setWindowFlags(Qt.WindowStaysOnTopHint)

            # ############################################################################
            # options - selection
            # ############################################################################


            self.layout = QFormLayout()

            # grab list from the menu dictionary
            self.sModeList = getMenuIndex.keys()
            self.sMode = QComboBox(self)
            self.sMode.addItems(self.sModeList)
            self.sMode.setCurrentIndex(0)
            # set object draw call to the event handler for object selection
            # this means that when the user selects from the list, this event
            # will update the internal member that references the specific
            # furniture object. This is critical as it changes what we draw
            # next.
            self.sMode.activated[str].connect(self.setFurniture)
            self.layout.addRow(self.sMode)

            # draw the selected furniture object
            self.layout.addRow(self.selectedFurniture.draw())
            #self.layout.addStretch()

            # setup the create button to use the selected furniture
            self.bCreate = QPushButton(translate('magicStart', 'create'))
            self.bCreate.clicked.connect(self.selectedFurniture.create());

            # add button to layout
            self.layout.addRow(self.bCreate)
            self.setLayout(self.layout)
            self.show()

    # ############################################################################
    # final settings
    # ############################################################################

    userCancelled = "Cancelled"
    userOK = "OK"

    form = QtMainClass()
    form.exec_()




# ############################################################################
def getIcon(iName):

    path = FreeCADGui.activeWorkbench().path
    iconPath = str(os.path.join(path, "Icons"))
    f = os.path.join(iconPath, iName+".png")

    if os.path.exists(f):
        filename = f
        icon = '<img src="'+ filename + '" width="200" height="200" align="right">'
        return QLabel(icon)
# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################

