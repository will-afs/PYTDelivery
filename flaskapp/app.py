from flask import Flask

app = Flask(__name__)

@app.route("/extract_pdf_metadata", methods=['GET'])
def extract_pdf_metadata():
    return "<p>Hello, World!</p>"