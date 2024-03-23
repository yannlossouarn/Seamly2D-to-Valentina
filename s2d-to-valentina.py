import xml.etree.ElementTree as ET
import shutil
import sys

def transform_xml(file_path):
    # Créer une copie de sauvegarde avec l'extension .s2d.bak
    backup_file_path = file_path + '.s2d.bak'
    shutil.copyfile(file_path, backup_file_path)
    
    # Charger le fichier XML
    tree = ET.parse(file_path)
    root = tree.getroot()
    print("root", root)

    # Parcourir tous les noeuds 'point' et effectuer les transformations demandées


    print("après anytype")
    for point in root.findall('.//point'):
        # Supprimer les attributs lineType="none" et lineType="solidLine"
        if 'lineType' in point.attrib and point.attrib['lineType'] in ['none', 'solidLine']:
            del point.attrib['lineType']

        # Renommer l'attribut showPointName en showLabel
        if 'showPointName' in point.attrib:
            point.attrib['showLabel'] = point.attrib.pop('showPointName')

    for arc in root.findall('.//arc'):
        # Supprimer les attributs lineType="none" et lineType="solidLine"
        if 'penStyle' in arc.attrib and arc.attrib['penStyle'] in ['solidLine']:
            arc.attrib['penStyle'] = 'hair'

    for spline in root.findall('.//spline'):
        # Supprimer les attributs lineType="none" et lineType="solidLine"
        if 'penStyle' in spline.attrib and spline.attrib['penStyle'] in ['solidLine']:
            spline.attrib['penStyle'] = 'hair'

    for line in root.findall('.//line'):
        # Supprimer les attributs lineType="none" et lineType="solidLine"
        if 'lineType' in line.attrib and line.attrib['lineType'] in ['none', 'solidLine']:
            del line.attrib['lineType']

    print("avant anytype")
    for anytype in root.findall('./draw/modeling/*'):
        print(anytype)
        # Supprimer les attributs lineType="none" et lineType="solidLine"
        if 'lineType' in anytype.attrib and anytype.attrib['lineType'] in ['none', 'solidLine']:
            print(anytype, anytype.attrib['lineType'])
            del anytype.attrib['lineType']

    for child in root:
        print(child.tag, child.attrib)

    # Ajouter le nœud <previewCalculations/> entre les nœuds <draw> et <increments>

    draw = root.find('draw')

    increments = root.find('increments')

    print(increments)


    if draw is not None and increments is not None:
        print("draw et increments OK")
        previewCalculations = ET.Element('previewCalculations')
        root.insert(6, previewCalculations)

    # Mettre à jour le contenu textuel du nœud <version> dans <pattern>
    version = root.find('version')
    if version is not None:
        version.text = "0.9.4"

    # Sauvegarder les modifications dans le fichier original en s'assurant qu'il est bien formé
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_file>")
    else:
        file_path = sys.argv[1]
        transform_xml(file_path)
