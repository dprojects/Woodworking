#!/bin/bash

RELEASE="0.24"
CODES=("pl" "en" "af" "ar" "eu" "bg" "ca" "zh-CN" "zh-TW" "hr" "cs" "nl" "fil" "fi" "fr" "gl" "ka" "de" "el" "hu" "id" "it" "ja" "kab" "ko" "lt" "no" "pt-PT" "pt-BR" "ro" "ru" "sk" "sl" "es-ES" "es-AR" "sv-SE" "tr" "uk" "val-ES" "vi")

for c in ${CODES[@]}; do

	cp "./template_${RELEASE}.ts" "./Woodworking_${c}.ts"

done
