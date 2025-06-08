# This file set router pattern at given Sketch object

import FreeCAD
import Sketcher, Part

def setRouterPattern(iSketch, iBitSizes, iType):
	
	if iType == "Cove" or iType == "Cove2" or iType == "Cove4":
	
		bit = str(iBitSizes[0]) + " " + "mm"
		
		iSketch.addGeometry(Part.Circle(FreeCAD.Vector(-11.104589, 7.436932, 0), FreeCAD.Vector(0,0,1), 26.433139), False)
		iSketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1)) 
		iSketch.addConstraint(Sketcher.Constraint('Radius', 0, 26.433139))
		iSketch.setDatum(1, FreeCAD.Units.Quantity(bit))

		return iSketch

	if iType == "RoundOver" or iType == "RoundOver2" or iType == "RoundOver4":
		
		bit = str(iBitSizes[0]) + " " + "mm"
		
		iSketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(17.964924,-14.676168,0),FreeCAD.Vector(0,0,1),15.909641),1.709506,3.476161),False)
		iSketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(-19.469606,18.381221,0),FreeCAD.Vector(0,0,1),16.402145),4.613597,6.182640),False)
		iSketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(17.204672,18.981390,0),FreeCAD.Vector(0,0,1),13.708001),3.258160,5.033160),False)
		iSketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(-18.880601,-19.950044,0),FreeCAD.Vector(0,0,1),16.185459),0.050111,1.646764),False)
		iSketch.addConstraint(Sketcher.Constraint('Equal',3,1)) 
		iSketch.addConstraint(Sketcher.Constraint('Equal',1,2)) 
		iSketch.addConstraint(Sketcher.Constraint('Equal',2,0)) 
		iSketch.addConstraint(Sketcher.Constraint('Vertical',0,3,2,3)) 
		iSketch.addConstraint(Sketcher.Constraint('Horizontal',3,3,0,3)) 
		iSketch.addConstraint(Sketcher.Constraint('Vertical',1,3,3,3)) 
		iSketch.addConstraint(Sketcher.Constraint('Horizontal',1,3,2,3)) 
		iSketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		iSketch.addConstraint(Sketcher.Constraint('Coincident',0,1,2,2)) 
		iSketch.addConstraint(Sketcher.Constraint('Coincident',3,1,0,2)) 
		iSketch.addConstraint(Sketcher.Constraint('Coincident',3,2,1,1)) 
		iSketch.addConstraint(Sketcher.Constraint('PointOnObject',1,1,-1)) 
		iSketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-2)) 
		iSketch.addConstraint(Sketcher.Constraint('DistanceY',0,2,-1,1,19.849726)) 
		iSketch.setDatum(13,FreeCAD.Units.Quantity(bit))
		iSketch.addConstraint(Sketcher.Constraint('Vertical',0,3,0,1)) 
		iSketch.addConstraint(Sketcher.Constraint('Horizontal',1,3,1,2)) 

		return iSketch
	
	if iType == "Straight2" or iType == "Straight3" or iType == "Straight4":
		
		bit1 = str(2 * iBitSizes[0]) + " " + "mm"
		bit2 = str(iBitSizes[0]) + " " + "mm"
		
		iSketch.addGeometry(Part.LineSegment(FreeCAD.Vector(-13.867397,19.250723,0),FreeCAD.Vector(26.556583,18.528873,0)),False)
		iSketch.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		iSketch.addGeometry(Part.LineSegment(FreeCAD.Vector(26.556583,19.250723,0),FreeCAD.Vector(25.834734,-12.150050,0)),False)
		iSketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		iSketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
		iSketch.addGeometry(Part.LineSegment(FreeCAD.Vector(26.556583,-12.150050,0),FreeCAD.Vector(-12.784623,-20.812334,0)),False)
		iSketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		iSketch.addGeometry(Part.LineSegment(FreeCAD.Vector(-12.784623,-20.812334,0),FreeCAD.Vector(-14.228333,17.807013,0)),False)
		iSketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		iSketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		iSketch.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		iSketch.addConstraint(Sketcher.Constraint('Equal',1,2)) 
		iSketch.addConstraint(Sketcher.Constraint('Equal',2,3)) 
		iSketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,1,21.849510)) 
		iSketch.setDatum(9,FreeCAD.Units.Quantity(bit2))
		iSketch.addConstraint(Sketcher.Constraint('DistanceX',2,2,-1,1,6.025586)) 
		iSketch.setDatum(10,FreeCAD.Units.Quantity(bit2))
		iSketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,28.280513)) 
		iSketch.setDatum(11,FreeCAD.Units.Quantity(bit1))
 
		return iSketch
	
	if iType == "Chamfer" or iType == "Chamfer2" or iType == "Chamfer4":
		
		import ProfileLib.RegularPolygon
		
		bit = str(iBitSizes[0]) + " " + "mm"
		
		ProfileLib.RegularPolygon.makeRegularPolygon(iSketch,4,FreeCAD.Vector(-5.108387,13.778920,0),FreeCAD.Vector(-3.000101,-11.358306,0),False)
		iSketch.addConstraint(Sketcher.Constraint('Coincident',4,3,-1,1)) 
		iSketch.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-2)) 
		iSketch.addConstraint(Sketcher.Constraint('Radius',4,21.451263)) 
		iSketch.setDatum(13,FreeCAD.Units.Quantity(bit))

		return iSketch
	
	# if nothing to return
	return ""
