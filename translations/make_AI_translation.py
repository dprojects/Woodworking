import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator
import os, sys

def makeTranslation(iTemplate="template.ts", iLang="pl"):
    output_file = f"Woodworking_{iLang}.ts"
    
    words_pl = {
        "disabled": "nieaktywne",
        "Yes": "Tak",
        "No": "Nie",
        "yes": "Tak",
        "no": "Nie",
        "face": "lico",
        "faces": "lica",
        "MagicPanels": "MagiczneFormatki",
        "panel": "formatka",
        "panels": "formatki",
        "edge": "krawędź"  # no comma
    }
    
    words_same = {
        "addExternal": "addExternal",
        "jointTenonCut": "jointTenonCut",
        "magicView": "magicView",
        "panelCopyYZ": "panelCopyYZ",
        "panelMoveZp": "panelMoveZp",
        "routerStraight4": "routerStraight4",
        "addVeneer": "addVeneer",
        "jointTenonDowelP": "jointTenonDowelP",
        "makeBeautiful": "makeBeautiful",
        "panelCopyZX": "panelCopyZX",
        "panelResize1": "panelResize1",
        "scanObjects": "scanObjects",
        "align2Curve": "align2Curve",
        "jointTenonDowel": "jointTenonDowel",
        "makeTransparent": "makeTransparent",
        "panelCopyZY": "panelCopyZY",
        "panelResize2": "panelResize2",
        "selected2Assembly": "selected2Assembly",
        "cornerBlock": "cornerBlock",
        "magicAngle": "magicAngle",
        "mapPosition": "mapPosition",
        "panelCoverXY": "panelCoverXY",
        "panelResize3": "panelResize3",
        "selected2Group": "selected2Group",
        "cornerBrace": "cornerBrace",
        "magicCNC": "magicCNC",
        "multiPocket2": "multiPocket2",
        "panelDefaultXY": "panelDefaultXY",
        "panelResize4": "panelResize4",
        "selected2LinkGroup": "selected2LinkGroup",
        "cutDowels": "cutDowels",
        "magicColors": "magicColors",
        "multiPocket4": "multiPocket4",
        "panelDefaultXZ": "panelDefaultXZ",
        "panelResize5": "panelResize5",
        "selected2Link": "selected2Link",
        "cutTenonDowelsP": "cutTenonDowelsP",
        "magicCorner": "magicCorner",
        "multiPocket": "multiPocket",
        "panelDefaultYX": "panelDefaultYX",
        "panelResize6": "panelResize6",
        "selected2Outside": "selected2Outside",
        "cutTenonDowels": "cutTenonDowels",
        "magicCutLinks": "magicCutLinks",
        "panel2angle45cut": "panel2angle45cut",
        "panelDefaultYZ": "panelDefaultYZ",
        "panelSideLeft": "panelSideLeft",
        "selectVertex": "selectVertex",
        "debugInfo": "debugInfo",
        "magicCut": "magicCut",
        "panel2angle": "panel2angle",
        "panelDefaultZX": "panelDefaultZX",
        "panelSideLeftUP": "panelSideLeftUP",
        "setTextures": "setTextures",
        "drillCounterbores2x": "drillCounterbores2x",
        "magicDowels": "magicDowels",
        "panel2clone": "panel2clone",
        "panelDefaultZY": "panelDefaultZY",
        "panelSideRight": "panelSideRight",
        "sheet2export": "sheet2export",
        "drillCounterbores": "drillCounterbores",
        "magicDriller": "magicDriller",
        "panel2frame": "panel2frame",
        "panelFaceXY": "panelFaceXY",
        "panelSideRightUP": "panelSideRightUP",
        "shelvesEqual": "shelvesEqual",
        "drillCountersinks": "drillCountersinks",
        "magicFixture": "magicFixture",
        "panel2link": "panel2link",
        "panelFaceXZ": "panelFaceXZ",
        "roundCurve": "roundCurve",
        "showAlias": "showAlias",
        "drillHoles": "drillHoles",
        "magicGlue": "magicGlue",
        "panel2pad": "panel2pad",
        "panelFaceYX": "panelFaceYX",
        "routerChamfer2": "routerChamfer2",
        "showConstraints": "showConstraints",
        "edge2dowel": "edge2dowel",
        "magicJoints": "magicJoints",
        "panel2profile": "panel2profile",
        "panelFaceYZ": "panelFaceYZ",
        "routerChamfer4": "routerChamfer4",
        "showMeasurements": "showMeasurements",
        "edge2drillbit": "edge2drillbit",
        "magicKnifeLinks": "magicKnifeLinks",
        "panelBackOut": "panelBackOut",
        "panelFaceZX": "panelFaceZX",
        "routerChamfer": "routerChamfer",
        "showOccupiedSpace": "showOccupiedSpace",
        "eyeHorus": "eyeHorus",
        "magicKnife": "magicKnife",
        "panelBetweenXY": "panelBetweenXY",
        "panelFaceZY": "panelFaceZY",
        "routerCove2": "routerCove2",
        "showPlacement": "showPlacement",
        "eyeRa": "eyeRa",
        "magicManager": "magicManager",
        "panelBetweenXZ": "panelBetweenXZ",
        "panelMove2Anchor": "panelMove2Anchor",
        "routerCove4": "routerCove4",
        "showVertex": "showVertex",
        "fitModel": "fitModel",
        "magicMeasure": "magicMeasure",
        "panelBetweenYX": "panelBetweenYX",
        "panelMove2Center": "panelMove2Center",
        "routerCove": "routerCove",
        "sketch2clone": "sketch2clone", 
        "frontsOpenClose": "frontsOpenClose",
        "magicMove": "magicMove",
        "panelBetweenYZ": "panelBetweenYZ",
        "panelMove2Face": "panelMove2Face",
        "RouterPatterns": "RouterPatterns",
        "sketch2dowel":  "sketch2dowel",
        "getDimensions": "getDimensions",
        "MagicPanelsController": "MagicPanelsController",
        "MagicPanels": "MagicPanels",
        "panelBetweenZX": "panelBetweenZX",
        "panelMoveXm": "panelMoveXm",
        "routerRoundOver2": "routerRoundOver2",
        "sketch2pad": "sketch2pad",
        "grainH": "grainH",
        "panelBetweenZY": "panelBetweenZY",
        "panelMoveXp": "panelMoveXp",
        "routerRoundOver4": "routerRoundOver4",
        "wires2pad": "wires2pad",
        "grainV": "grainV",
        "magicResizer": "magicResizer",
        "panelCopyXY": "panelCopyXY",
        "panelMoveYm": "panelMoveYm",
        "routerRoundOver": "routerRoundOver",
        "grainX": "grainX",
        "magicSettings": "magicSettings",
        "panelCopyXZ": "panelCopyXZ",
        "panelMoveYp": "panelMoveYp",
        "routerStraight2": "routerStraight2",
        "jointMortiseCut": "jointMortiseCut",
        "magicStart": "magicStart",
        "panelCopyYX": "panelCopyYX",
        "panelMoveZm": "panelMoveZm",
        "routerStraight3": "routerStraight3" # no comma
    }
    
    if iLang == "pl":
        words = words_same | words_pl
    else:
        words = words_same
    
    print(f"Starting: {iTemplate} -> {iLang}", flush=True)
    
    try:
        tree = ET.parse(iTemplate)
        root = tree.getroot()
        translator = GoogleTranslator(source='auto', target=iLang)
        
        count = 0
        for message in root.findall('.//message'):
            source = message.find('source')
            translation = message.find('translation')
            
            if source is not None and source.text and translation is not None:
                if not translation.text or translation.get('type') == 'unfinished':
                    original_text = source.text
                    
                    try:
                        if original_text in words:
                            translated_text = words[original_text]
                            print(f" [Replace: ] {original_text} -> {translated_text}", flush=True)
                        else:
                            translated_text = translator.translate(original_text)
                        
                        translation.text = translated_text
                        
                        if 'type' in translation.attrib:
                            del translation.attrib['type']
                            
                        count += 1
                        if count % 10 == 0:
                            print(f"Language: {iLang}, translated: {count} ...", flush=True)
                            
                    except Exception as e:
                        print(f"Error: '{original_text}': {e}", flush=True)

        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"\nDone! Translated: {count}. File: {output_file}", flush=True)

    except Exception as e:
        print(f"Fatal error and kernel panic :-): {e}", flush=True)

if len(sys.argv) > 1:
    makeTranslation("template.ts", sys.argv[1])
else:
    makeTranslation("template.ts", "pl")
    
