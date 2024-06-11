# Translations

Please see translation repository at: [github.com/dprojects/Woodworking-translations](https://github.com/dprojects/Woodworking-translations)

# Development

You can create your own `Woodworking` workbench translation with the following steps:

* Generate `.ts` file. At `Xubuntu 22.04 LTS` in `Woodworking` directory:
	
	```
	pylupdate5 `find . -name "*.py"` -ts translations/pyfiles.ts
	```
	
* Rename `pyfiles.ts` e.g.:

	```
	mv ./translations/pyfiles.ts ./translations/Woodworking_pl.ts
	```
	
	**Note:** Replace `pl` with your language code.
	
* Make translations of the `.ts` file. You can also use editor for that.

	* For example this entry below:
	```
	<source>Step 2. Custom CSS rules for each cell (edit or add):</source>
	<translation type="unfinished"></translation>
	```
	* should be replaced with:
	```
	<source>Step 2. Custom CSS rules for each cell (edit or add):</source>
	<translation>Krok 2. Własne ustawienia CSS dla komórki:</translation>
	```

* Generate `.qm` files:
	
	```
	sudo apt-get install qttools5-dev-tools
	/usr/lib/x86_64-linux-gnu/qt5/bin/lrelease ./translations/Woodworking_pl.ts
	```

* Set your language at FreeCAD preferences.
