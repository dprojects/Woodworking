pylupdate5 `find . -name "*.py"` -ts translations/Woodworking_pl_new.ts
/usr/lib/x86_64-linux-gnu/qt5/bin/lrelease ./translations/Woodworking_pl_new.ts
lconvert ./translations/Woodworking_pl_new.qm -o ./translations/Woodworking_pl_new.ts
lconvert ./translations/Woodworking_pl.qm -o ./translations/Woodworking_pl_old.ts
diff ./translations/Woodworking_pl_old.ts ./translations/Woodworking_pl_new.ts
