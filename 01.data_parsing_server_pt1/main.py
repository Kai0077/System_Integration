from fastapi import FastAPI
import json
import tomli
import yaml
import xml.etree.ElementTree as ET


toml_file = "/Users/kaitsvetkov/System_Integration/System_Integration/02.Text-based_Data_Formats/me.toml"
xml_file = "/Users/kaitsvetkov/System_Integration/System_Integration/02.Text-based_Data_Formats/me.xml"
yaml_file = "/Users/kaitsvetkov/System_Integration/System_Integration/02.Text-based_Data_Formats/me.yaml"




app = FastAPI()


@app.get("/")
def root():
    

     


@app.get("/greet")
def greet():
    return {"message": f"Hello there "}
