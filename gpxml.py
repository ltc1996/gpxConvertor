import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
# from lxml import etree
import os
import xml.etree.ElementTree as etree
import xml.dom.minidom as md


def get_trkpt(xml_file):
    trkpt_lst = []
    with open(xml_file, 'r', encoding='utf-8') as f:
        root = BeautifulSoup(f, 'xml')
        trkpt_lst = root.find_all('trkpt')
    return trkpt_lst


# get_trkpt(xml_path)

def generate_xml(trkpts, xml_file):
    root = etree.Element("gpx")
    root.set("creator", "Garmin Connect")
    root.set("version", "1.1")
    root.set('xsi:schemaLocation', "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/11.xsd")
    root.set("xmlns", "http://www.topografix.com/GPX/1/1")
    root.set("xmlns:ns3", "http://www.garmin.com/xmlschemas/TrackPointExtension/v1")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xmlns:ns2", "http://www.garmin.com/xmlschemas/GpxExtensions/v3")

    metadata = etree.SubElement(root, "metadata")
    link = etree.SubElement(metadata, "link")
    link.set("href", "connect.garmin.com")
    text = etree.SubElement(link, "text")
    text.text = "Garmin Connect"
    trk = etree.SubElement(root, "trk")
    name = etree.SubElement(trk, 'name')
    name.text = "Nanjing Uncategorized"
    type = etree.SubElement(trk, 'type')
    type.text = "uncategorized"
    trkseg = etree.SubElement(trk, 'trkseg')
    for _trkpt in trkpts:
        trkpt = etree.SubElement(trkseg, 'trkpt')
        # lat lon
        geo_d = _trkpt.attrs
        for k in geo_d:
            trkpt.set(k, geo_d[k])
        # ele
        ele_str = _trkpt.contents[1].contents[0]
        ele = etree.SubElement(trkpt, 'ele')
        ele.text = ele_str
        # time
        time_str = _trkpt.contents[3].contents[0]
        time = etree.SubElement(trkpt, 'time')
        time.text = time_str

        # extensions
        extensions = etree.SubElement(trkpt, 'extensions')
        nt = etree.SubElement(extensions, 'ns3:TrackPointExtension')

    # print(etree.tostring(root, pretty_print=True))
    tree = etree.ElementTree(root)

    tree.write(xml_file)
    xml_f = md.parse(xml_file)
    xml_f.writexml(open(xml_file, 'w+'), addindent='    ', newl='\n')


curr = os.getcwd()
test_file = 'test.gpx'
test_path = os.path.join(curr, test_file)

target_file = 'test11.gpx'
target_path = os.path.join(curr, target_file)

trkpts = get_trkpt(test_path)
generate_xml(trkpts, target_path)
