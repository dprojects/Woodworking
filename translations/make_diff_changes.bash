pylupdate5 `find .. -name "*.py"` -ts ./Woodworking_pl_new.ts
/usr/lib/x86_64-linux-gnu/qt5/bin/lrelease ./Woodworking_pl_new.ts
lconvert ./Woodworking_pl_new.qm -o ./Woodworking_pl_new.ts
lconvert ./Woodworking_pl.qm -o ./Woodworking_pl_old.ts
diff ./Woodworking_pl_old.ts ./Woodworking_pl_new.ts > ./Woodworking_pl_diff.ts
