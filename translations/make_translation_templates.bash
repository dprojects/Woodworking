#!/bin/bash

mkdir -p ./templates
pylupdate5 `find .. -name "*.py"` -ts ./templates/template.ts

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
    "Portuguese (Brazilian)" "pt-BR" "pt"
    "Romanian" "ro" "ro"
    "Russian" "ru" "ru"
    "Serbian" "sr" "sr"
    "Serbian (Latin)" "sr-CS" "sr"
    "Slovak" "sk" "sk"
    "Slovenian" "sl" "sl"
    "Spanish" "es-ES" "es"
    "Spanish (Argentina)" "es-AR" "es"
    "Swedish" "sv-SE" "sv"
    "Turkish" "tr" "tr"
    "Ukrainian" "uk" "uk"
    "Vietnamese" "vi" "vi"
)

for ((i=0; i<${#DATA[@]}; i+=3)); do
    
    freecad_name="${DATA[i]}"
    freecad_code="${DATA[i+1]}"
    ai_code="${DATA[i+2]}"

	cp "./templates/template.ts" "./templates/Woodworking_${freecad_code}.ts"

done
