from flask import Flask, flash, request, make_response, redirect, url_for
import extract_pdf_data
import json
from pdfminer.pdfparser import PDFSyntaxError
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = './flaskapp/resources/'
ALLOWED_EXTENSIONS = {'pdf',}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('extract_pdf_metadata', pdf_name=filename))
    return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
            '''

@app.route("/extract_pdf_metadata/<pdf_name>", methods=['GET'])
def extract_pdf_metadata(pdf_name):
    if request.method == 'GET':
        # pdf_name = request.args.get("pdf_name")
        pdf_path = UPLOAD_FOLDER + pdf_name
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