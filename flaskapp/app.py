from flask import Flask, request
import extract_pdf_data
import json


app = Flask(__name__)

@app.route("/extract_pdf_metadata/", methods=['GET'])
def extract_pdf_metadata():
    pdf_name = request.args.get("pdf_name")
    pdf_path = './flaskapp/resources/' + pdf_name
    metadata_as_dict = extract_pdf_data.extract_pdf_metadata(pdf_path=pdf_path)
    metadata_as_str = json.dumps(metadata_as_dict)
    return metadata_as_dict