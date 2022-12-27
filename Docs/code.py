# small macro to reload libriaries
# it can be used for library development without restarting FreeCAD

import sys

try:
	del sys.modules["MagicPanels"]
except:
	skip = 1
	
try:
	del sys.modules["MagicPanelsController"]
except:
	skip = 1

try:
	del sys.modules["RouterPatterns"]
except:
	skip = 1
