from flask import Flask, request, make_response
import extract_pdf_data
import json
from pdfminer.pdfparser import PDFSyntaxError


app = Flask(__name__)

@app.route("/extract_pdf_metadata/<pdf_name>", methods=['GET'])
def extract_pdf_metadata(pdf_name):
    # pdf_name = request.args.get("pdf_name")
    pdf_path = './flaskapp/resources/' + pdf_name
    try :
        metadata_as_dict = extract_pdf_data.extract_pdf_metadata(pdf_path=pdf_path)
        message = metadata_as_dict
        status = 200
    except FileNotFoundError:
        message = "File not found"
        status = 404
    except PDFSyntaxError:
        message = "The file is not a PDF"
        status = 405    
    response = make_response(message, status)
    return response

# @app.route("/upload_pdf/", methods=['POST'])
# def upload_pdf():
#     pdf_name = request.args.get("pdf_name")
#     pdf_path = './flaskapp/resources/' + pdf_name
#     metadata_as_dict = extract_pdf_data.extract_pdf_metadata(pdf_path=pdf_path)
#     metadata_as_str = json.dumps(metadata_as_dict)
#     return metadata_as_dict