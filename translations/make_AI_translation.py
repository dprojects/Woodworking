import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator
import os, sys
import html

# #############################################################################################################
# words
# #############################################################################################################

# this will keep the names
words_same = {
    "Assembly4": 0,
    "addExternal": 1,
    "jointTenonCut": 2,
    "magicView": 3,
    "panelCopyYZ": 4,
    "panelMoveZp": 5,
    "routerStraight4": 6,
    "addVeneer": 7,
    "jointTenonDowelP": 8,
    "makeBeautiful": 9,
    "panelCopyZX": 10,
    "panelResize1": 11,
    "scanObjects": 12,
    "align2Curve": 13,
    "jointTenonDowel": 14,
    "makeTransparent": 15,
    "panelCopyZY": 16,
    "panelResize2": 17,
    "selected2Assembly": 18,
    "cornerBlock": 19,
    "magicAngle": 20,
    "mapPosition": 21,
    "panelCoverXY": 22,
    "panelResize3": 23,
    "selected2Group": 24,
    "cornerBrace": 25,
    "magicCNC": 26,
    "multiPocket2": 27,
    "panelDefaultXY": 28,
    "panelResize4": 29,
    "selected2LinkGroup": 30,
    "cutDowels": 31,
    "magicColors": 32,
    "multiPocket4": 33,
    "panelDefaultXZ": 34,
    "panelResize5": 35,
    "selected2Link": 36,
    "cutTenonDowelsP": 37,
    "magicCorner": 38,
    "multiPocket": 39,
    "panelDefaultYX": 40,
    "panelResize6": 41,
    "selected2Outside": 42,
    "cutTenonDowels": 43,
    "magicCutLinks": 44,
    "panel2angle45cut": 45,
    "panelDefaultYZ": 46,
    "panelSideLeft": 47,
    "selectVertex": 48,
    "debugInfo": 49,
    "magicCut": 50,
    "panel2angle": 51,
    "panelDefaultZX": 52,
    "panelSideLeftUP": 53,
    "setTextures": 54,
    "drillCounterbores2x": 55,
    "magicDowels": 56,
    "panel2clone": 57,
    "panelDefaultZY": 58,
    "panelSideRight": 59,
    "sheet2export": 60,
    "drillCounterbores": 61,
    "magicDriller": 62,
    "panel2frame": 63,
    "panelFaceXY": 64,
    "panelSideRightUP": 65,
    "shelvesEqual": 66,
    "drillCountersinks": 67,
    "magicFixture": 68,
    "panel2link": 69,
    "panelFaceXZ": 70,
    "roundCurve": 71,
    "showAlias": 72,
    "drillHoles": 73,
    "magicGlue": 74,
    "panel2pad": 75,
    "panelFaceYX": 76,
    "routerChamfer2": 77,
    "showConstraints": 78,
    "edge2dowel": 79,
    "magicJoints": 80,
    "panel2profile": 81,
    "panelFaceYZ": 82,
    "routerChamfer4": 83,
    "showMeasurements": 84,
    "edge2drillbit": 85,
    "magicKnifeLinks": 86,
    "panelBackOut": 87,
    "panelFaceZX": 88,
    "routerChamfer": 89,
    "showOccupiedSpace": 90,
    "eyeHorus": 91,
    "magicKnife": 92,
    "panelBetweenXY": 93,
    "panelFaceZY": 94,
    "routerCove2": 95,
    "showPlacement": 96,
    "eyeRa": 97,
    "magicManager": 98,
    "panelBetweenXZ": 99,
    "panelMove2Anchor": 100,
    "routerCove4": 101,
    "showVertex": 102,
    "fitModel": 103,
    "magicMeasure": 104,
    "panelBetweenYX": 105,
    "panelMove2Center": 106,
    "routerCove": 107,
    "sketch2clone": 108,
    "frontsOpenClose": 109,
    "magicMove": 110,
    "panelBetweenYZ": 111,
    "panelMove2Face": 112,
    "RouterPatterns": 113,
    "sketch2dowel": 114,
    "getDimensions": 115,
    "MagicPanelsController": 116,
    "MagicPanels": 117,
    "panelBetweenZX": 118,
    "panelMoveXm": 119,
    "routerRoundOver2": 120,
    "sketch2pad": 121,
    "grainH": 122,
    "panelBetweenZY": 123,
    "panelMoveXp": 124,
    "routerRoundOver4": 125,
    "wires2pad": 126,
    "grainV": 127,
    "magicResizer": 128,
    "panelCopyXY": 129,
    "panelMoveYm": 130,
    "routerRoundOver": 131,
    "grainX": 132,
    "magicSettings": 133,
    "panelCopyXZ": 134,
    "panelMoveYp": 135,
    "routerStraight2": 136,
    "jointMortiseCut": 137,
    "magicStart": 138,
    "panelCopyYX": 139,
    "panelMoveZm": 140,
    "routerStraight3": 141 # no comma
}

# #############################################################################################################
# functions
# #############################################################################################################

# #############################################################################################################
def makeTranslation(iTemplate="template.ts", iLang="pl", iDebug="yes"):
    output_file = f"Woodworking_{iLang}.ts"
    
    print(f"Starting: {iTemplate} -> {iLang}", flush=True)
    
    try:
        tree = ET.parse(iTemplate)
        root = tree.getroot()
        translator = GoogleTranslator(source='auto', target=iLang)
        
        count = 0
        for message in root.findall('.//message'):
            source = message.find('source')
            translation = message.find('translation')
            keep, keepWord, keepID = False, "", ""

            if source is not None and source.text and translation is not None:
                if not translation.text or translation.get('type') == 'unfinished':
                    
                    text_source = source.text.strip()
                    
                    for w in words_same:
                        if w in text_source:
                            keep = True
                            keepWord = w
                            keepID = "[" + str(words_same[keepWord]) + "]"
                            text_source = text_source.replace(keepWord, keepID)
                            if iDebug == "yes":
                                print(f" [Keep: ] {keepWord} -> {keepID}", flush=True)
                    
                    try:
                        import time
                        max_attempts = 5
                        for i in range(max_attempts):
                            text_translated = translator.translate(text_source)
                            text_translated = html.unescape(text_translated)
                            if "Error 500" not in text_translated:
                                break
                            else:
                                if i < max_attempts - 1:
                                    wait_seconds = (i + 1) * 120
                                    print(f" [sleep: ] Error 500. Try {i+1}/3. Wait {wait_seconds} seconds...")
                                    time.sleep(wait_seconds)
                                else:
                                    print(f" [sleep: ] No success after {max_attempts}.", flush=True)
                                
                    except Exception as e:
                        print(f"Error: '{text_source}': {e}", flush=True)
                    
                    if keep == True:
                        text_translated = text_translated.replace(keepID, keepWord)
                        if iDebug == "yes":
                            print(f" [Keep back: ] {keepID} -> {keepWord}", flush=True)
                                
                    translation.text = text_translated
                    if iDebug == "yes":
                        print(f" [Translated debug: ] {text_translated}", flush=True)
                    
                    if 'type' in translation.attrib:
                        del translation.attrib['type']
                        
                    count += 1
                    if count % 10 == 0:
                        print(f"Language: {iLang}, translated: {count} ...", flush=True)
                            
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"\nDone! Translated: {count}. File: {output_file}", flush=True)

    except Exception as e:
        print(f"Fatal error and kernel panic :-): {e}", flush=True)

# #############################################################################################################
# main
# #############################################################################################################

if len(sys.argv) > 1:
    makeTranslation("template.ts", sys.argv[1], "no")
else:
    makeTranslation("template.ts", "pl", "yes")
    
