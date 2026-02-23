#!/bin/bash
# 
# watch -t -n 1 "tail -n 15 ./current_status.log"

# ################################################################################################################################
# supported by AI
# ################################################################################################################################

# {'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy', 'Assamese': 'as', 'Aymara': 'ay', 'Azerbaijani': 'az', 'Bambara': 'bm', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bhojpuri': 'bho', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca', 'Cebuano': 'ceb', 'Chichewa': 'ny', 'Chinese Simplified': 'zh-CN', 'Chinese Traditional': 'zh-TW', 'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dhivehi': 'dv', 'Dogri': 'doi', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Ewe': 'ee', 'Filipino': 'tl', 'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Guarani': 'gn', 'Gujarati': 'gu', 'Haitian creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'iw', 'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Ilocano': 'ilo', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jw', 'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Kinyarwanda': 'rw', 'Konkani': 'gom', 'Korean': 'ko', 'Krio': 'kri', 'Kurdish Kurmanji': 'ku', 'Kurdish Sorani': 'ckb', 'Kyrgyz': 'ky', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lingala': 'ln', 'Lithuanian': 'lt', 'Luganda': 'lg', 'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Maithili': 'mai', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr', 'Meiteilon Manipuri': 'mni-Mtei', 'Mizo': 'lus', 'Mongolian': 'mn', 'Myanmar': 'my', 'Nepali': 'ne', 'Norwegian': 'no', 'Odia Oriya': 'or', 'Oromo': 'om', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt', 'Punjabi': 'pa', 'Quechua': 'qu', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm', 'Sanskrit': 'sa', 'Scots Gaelic': 'gd', 'Sepedi': 'nso', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw', 'Swedish': 'sv', 'Tajik': 'tg', 'Tamil': 'ta', 'Tatar': 'tt', 'Telugu': 'te', 'Thai': 'th', 'Tigrinya': 'ti', 'Tsonga': 'ts', 'Turkish': 'tr', 'Turkmen': 'tk', 'Twi': 'ak', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uyghur': 'ug', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'}

# ################################################################################################################################
# supported by FreeCAD: FreeCADGui.supportedLocales()
# ################################################################################################################################

# {'English': 'en', 'Afrikaans': 'af', 'Arabic': 'ar', 'Basque': 'eu', 'Belarusian': 'be', 'Bulgarian': 'bg', 'Catalan': 'ca', 'Chinese (Simplified)': 'zh-CN', 'Chinese (Traditional)': 'zh-TW', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'Filipino': 'fil', 'Finnish': 'fi', 'French': 'fr', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Hungarian': 'hu', 'Indonesian': 'id', 'Italian': 'it', 'Japanese': 'ja', 'Kabyle': 'kab', 'Korean': 'ko', 'Lithuanian': 'lt', 'Malay': 'ms', 'Norwegian': 'no', 'Polish': 'pl', 'Portuguese': 'pt-PT', 'Portuguese (Brazilian)': 'pt-BR', 'Romanian': 'ro', 'Russian': 'ru', 'Serbian': 'sr', 'Serbian (Latin)': 'sr-CS', 'Slovak': 'sk', 'Slovenian': 'sl', 'Spanish': 'es-ES', 'Spanish (Argentina)': 'es-AR', 'Swedish': 'sv-SE', 'Turkish': 'tr', 'Ukrainian': 'uk', 'Valencian': 'val-ES', 'Vietnamese': 'vi'}

# ################################################################################################################################
DATA=(
    "Afrikaans" "af" "af"
    "Arabic" "ar" "ar"
    "Basque" "eu" "eu"
    "Belarusian" "be" "be"
    "Bulgarian" "bg" "bg"
    "Catalan" "ca" "ca"
    "Chinese (Simplified)" "zh-CN" "zh-CN"
    "Chinese (Traditional)" "zh-TW" "zh-TW"
    "Croatian" "hr" "hr"
    "Czech" "cs" "cs"
    "Danish" "da" "da"
    "Dutch" "nl" "nl"
    # "English" "en" "en"
    "Filipino" "fil" "tl"
    "Finnish" "fi" "fi"
    "French" "fr" "fr"
    "Galician" "gl" "gl"
    "Georgian" "ka" "ka"
    "German" "de" "de"
    "Greek" "el" "el"
    "Hungarian" "hu" "hu"
    "Indonesian" "id" "id"
    "Italian" "it" "it"
    "Japanese" "ja" "ja"
    "Korean" "ko" "ko"
    "Lithuanian" "lt" "lt"
    "Malay" "ms" "ms"
    "Norwegian" "no" "no"
    "Polish" "pl" "pl"
    "Portuguese" "pt-PT" "pt"
    # "Portuguese (Brazilian)" "pt-BR" "pt"
    "Romanian" "ro" "ro"
    "Russian" "ru" "ru"
    "Serbian" "sr" "sr"
    # "Serbian (Latin)" "sr-CS" "sr"
    "Slovak" "sk" "sk"
    "Slovenian" "sl" "sl"
    "Spanish" "es-ES" "es"
    # "Spanish (Argentina)" "es-AR" "es"
    "Swedish" "sv-SE" "sv"
    "Turkish" "tr" "tr"
    # "Ukrainian" "uk" "uk"
    "Vietnamese" "vi" "vi"
)

# ################################################################################################################################
mkdir -p ./translated

for ((i=0; i<${#DATA[@]}; i+=3)); do
    
    freecad_name="${DATA[i]}"
    freecad_code="${DATA[i+1]}"
    ai_code="${DATA[i+2]}"

	if [ -f "./translated/Woodworking_${freecad_code}.ts" ]; then
		echo -e "Translation .ts file for: [ ${freecad_name} | ${freecad_code} ] => [ ${ai_code} ] already exists, skipped."
	else
		echo -n "Creating translation for: [ ${freecad_name} | ${freecad_code} ] => [ ${ai_code} ] ..."
		python3 "./make_AI_translation.py" "${ai_code}" >> "./current_status.log" 2>&1
		mv "./Woodworking_${ai_code}.ts" "./translated/Woodworking_${freecad_code}.ts"
		echo "done."
		sleep 2
	fi
	
	if [ -f "./translated/Woodworking_${freecad_code}.qm" ]; then
		echo -e "Translation .qm file for: [ ${freecad_name} | ${freecad_code} ] => [ ${ai_code} ] already exists, skipped."
	else
		# echo -n "Compiling .qm for: [ ${freecad_name} | ${freecad_code} ] => [ ${ai_code} ] ... "
		# /usr/lib/x86_64-linux-gnu/qt5/bin/lrelease "./translated/Woodworking_${freecad_code}.ts" -silent >> "./current_status.log" 2>&1
		# echo "done."
		/usr/lib/x86_64-linux-gnu/qt5/bin/lrelease "./translated/Woodworking_${freecad_code}.ts"
	fi
	
done
