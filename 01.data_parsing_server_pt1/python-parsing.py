import json
import tomli
import yaml
import xml.etree.ElementTree as ET

toml_file = "/Users/kaitsvetkov/System_Integration/System_Integration/02.Text-based_Data_Formats/me.toml"
xml_file = "/Users/kaitsvetkov/System_Integration/System_Integration/02.Text-based_Data_Formats/me.xml"
yaml_file = "/Users/kaitsvetkov/System_Integration/System_Integration/02.Text-based_Data_Formats/me.yaml"


def read_toml(filepath):
    with open(filepath, "rb") as f:
        return tomli.load(f)


def read_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    xml_dict = {
        child.tag: child.text
        if len(child) == 0
        else [subchild.text for subchild in child]
        for child in root
    }
    return xml_dict


def read_yaml(filepath):
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


toml_content = read_toml(toml_file)
xml_content = read_xml(xml_file)
yaml_content = read_yaml(yaml_file)

print(f"TOML: {json.dumps(toml_content, separators=(',', ':'))}")
print(f"XML: {json.dumps(xml_content, separators=(',', ':'))}")
print(f"YAML: {json.dumps(yaml_content, separators=(',', ':'))}")
