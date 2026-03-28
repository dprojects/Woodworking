#!/bin/bash
# 

pylupdate5 `find .. -name "*.py"` -ts ./template.ts
python3 "./make_AI_translation.py"
/usr/lib/x86_64-linux-gnu/qt5/bin/lrelease "./Woodworking_pl.ts"
