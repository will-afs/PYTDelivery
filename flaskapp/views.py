import json
import urllib

from flask import Blueprint, Flask, g, make_response, request
from pdfminer.pdfparser import PDFSyntaxError
from werkzeug.utils import secure_filename

from flaskapp.core.extract_pdf_uris_from_atom_feed import extract_pdf_uris_from_atom_feed
from flaskapp.core.extract_pdf_data import extract_data_from_pdf_uri
from flaskapp.db.db import create_pdf, fill_pdf, get_db, get_pdf, get_pdf_id

bp = Blueprint("core", __name__, url_prefix="/")

from timeit import default_timer as timer
from time import time
import statistics, os


app = Flask(__name__)

@bp.route("/documents/populate_db_from_arxiv_api/", methods=["POST"])
def populate_db_from_arxiv_api():
    if request.method == "POST":
        # This argument is left for reutisability purpose, but its value is constrained for now
        category = request.args["cat"]
        if category != 'cs.ai':
            status = 400
            data = {"message":"Expected 'cs.ai' value for argument 'cat'"}
        else:
            start = int(request.args["start"])
            max_results = int(request.args["max_results"])
            if max_results <= 1000:
                # Gather PDF URIs
                url = "https://export.arxiv.org/api/"
                query = "query?search_query=cat:{}&start={}&max_results={}&sortBy=lastUpdatedDate&sortOrder=ascending".format(
                                                                                                                                category,
                                                                                                                                start,
                                                                                                                                max_results
                                                                                                                            )
                uri = url+query
                try:                                                                  
                    response = urllib.request.urlopen(uri)
                except urllib.error.HTTPError:
                    status = 400
                    data = {"message":"Could not access the provided URI. Maybe check the requests parameters?"}
                pdf_uris = extract_pdf_uris_from_atom_feed(feed = response.read())
                if len(pdf_uris) != 0:
                    # Setup measurement variables for service performance statistics
                    number_of_pdf_extracted = max_results
                    pdf_timers = []
                    global_start = timer()
                    db = get_db() # Fetch DB cursor
                    db_elapsed_time = timer() - global_start
                    db_size_begin = os.path.getsize(os.getcwd() + '/instance/flaskapp.sqlite')
                    # Start extracting process
                    for pdf_uri in pdf_uris:
                        try:
                            start_current_pdf = timer()
                            pdf_id = create_pdf(db_cursor=db, file_uri=pdf_uri)
                        except:
                            number_of_pdf_extracted += -1
                        else:
                            try:
                                metadata, content = extract_data_from_pdf_uri(pdf_uri)
                            except TypeError:
                                number_of_pdf_extracted += -1
                            else:
                                metadata = json.dumps(metadata)
                                fill_pdf(
                                    db_cursor=db, pdf_id=pdf_id, metadata=metadata, content=content
                                )
                                pdf_elapsed_time = timer() - start_current_pdf
                                pdf_timers.append(pdf_elapsed_time)
                                print("Elapsed {} seconds for this PDF".format(pdf_elapsed_time))
                            # To respect arxiv.org API constraint of 3s between each request
                            if timer() - start_current_pdf < 3:
                                time.sleep(4 - (timer() - start_current_pdf))
                    global_elapsed_time = sum(pdf_timers) + db_elapsed_time
                    db_size_end = os.path.getsize(os.getcwd() + '/instance/flaskapp.sqlite')
                    status = 200
                    data = {
                        "message": "Successfully retrieved, extracted, and stored in local DB {} PDFs metadata and content. {} were already in database".format(
                                                                                                                                                                    number_of_pdf_extracted,
                                                                                                                                                                    max_results-number_of_pdf_extracted
                                                                                                                                                                ),
                        "total elapsed time (s)": str(global_elapsed_time),
                        "max time by pdf (s)": str(max(pdf_timers)),
                        "stddev in total time by pdf (s)": str(statistics.stdev(pdf_timers)),
                        "number of pdf of more than 3s in total time (s)": str(sum(map(lambda x : x>3, pdf_timers))),
                        "mean time by pdf (s)": str(statistics.mean(pdf_timers)),
                        "total db size (Mo)": str((db_size_end - db_size_begin)/1000),
                        "mean size taken by a pdf (Mo)": str(((db_size_end - db_size_begin)/number_of_pdf_extracted)/1000),
                    }
                else:
                    status = 200
                    data = {"message":"No PDF to extract from ArXiv.org API for this set of arguments"}
            else:
                status = 400
                data = {"message":"Argument 'max_result' can not exceed 1000 to prevent performance issues into ArXiv.org backend"}
        response = make_response(data, status)
        return response

@bp.route("/documents/", methods=["POST"])
def extract_pdf_metadata_and_content_from_uri():
    """API endpoint to extract metadata and content of a PDF accessible from a URI

    Requires to specify the URI of the PDF into the request parameters
    """
    if request.method == "POST":
        if "file_uri" in request.args:
            file_uri = request.args["file_uri"]
            try:
                db = get_db()
                pdf_id = get_pdf_id(db, file_uri)
                if (
                    pdf_id is not None
                ):  # Check whether PDF matching URI already exists into DB
                    pdf = get_pdf(db, pdf_id)
                    status = 200
                    data = {
                        "message": "PDF matching the provided URI is already in base",
                        "pdf_id": str(pdf["id"]),
                    }
                else:
                    # Create new row for the PDF
                    pdf_id = create_pdf(db_cursor=db, file_uri=file_uri)
                    # TODO : launch a new task to asynchronously set row fields in db
                    metadata, content = extract_data_from_pdf_uri(file_uri)
                    metadata = json.dumps(metadata)
                    fill_pdf(
                        db_cursor=db, pdf_id=pdf_id, metadata=metadata, content=content
                    )
                    status = 200
                    data = {
                        "message": "Uploaded PDF successfully",
                        "pdf_id": str(pdf_id),
                    }
            except PDFSyntaxError:
                status = 400
                data = {
                    "message": "The content pointed by the provided URI does not seem to be a PDF"
                }
            except ValueError:
                status = 400
                data = {"message": "Wrong URI format"}
            except urllib.error.HTTPError:
                status = 400
                data = {"message": "Could not access the provided URI"}
            except Exception as err:
                status = 500
                data = {"message": "Internal server error"}
        else:
            status = 400
            data = {"message": "Please provide an URI pointing to a file"}
    else:
        status = 405
        data = {"message": "Method now allowed"}
    response = make_response(data, status)
    return response


@bp.route("/documents/<int:pdf_id>/metadata.json/", methods=["GET"])
def get_pdf_metadata(pdf_id: int):
    """API endpoint to get PDF metadata from database, under json format

    Requires to specify the ID of the PDF in database
    """
    if request.method == "GET":
        # Assuming at this step, routing has been done and thus <pdf_id> is not None
        if type(pdf_id) is int:
            pdf = get_pdf(get_db(), pdf_id)
            if pdf is None:
                status = 404
                data = {"message": "No PDF with such ID in database"}
            else:
                status = 200
                data = {
                    "message": "Successfully retrieved PDF metadata in database",
                    "metadata": pdf["metadata"],
                }
        else:
            status = 400
            data = {
                "message": "Bad value for <pdf_id> in request URL. Expected a positive Integer",
            }
        response = make_response(data, status)
        return response


@bp.route("/documents/<int:pdf_id>/content.txt/", methods=["GET"])
def get_pdf_content(pdf_id: int):
    """API endpoint to get PDF content from database, as a .txt file

    Requires to specify the ID of the PDF in database
    """
    if request.method == "GET":
        # Assuming at this step, routing has been done and thus <pdf_id> is not None
        if type(pdf_id) is int:
            pdf = get_pdf(get_db(), pdf_id)
            if pdf is None:
                status = 404
                data = {"message": "No PDF with such ID in database"}
            else:
                status = 200
                data = {
                    "message": "Successfully retrieved PDF content in database",
                    "content": pdf["content"],
                }
        else:
            status = 400
            data = {
                "message": "Bad value for <pdf_id> in request URL. Expected a positive Integer",
            }
        response = make_response(data, status)
        return response
