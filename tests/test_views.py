import configparser
import json

from flaskapp.db.db import create_pdf, fill_pdf, get_db, get_pdf_id

config = configparser.ConfigParser()
TESTS_DIRECTORY = "./tests"
config.read(TESTS_DIRECTORY + "/setup.cfg")

DATA_FILE_PATH = config["PATHS"]["DATA_FILE_PATH"]
PDF_DATA_FILE_NAME = config["PATHS"]["PDF_DATA_FILE_NAME"]
PDF_CONTENT_REFERENCE = config["PATHS"]["PDF_CONTENT_REFERENCE"]
PDF_METADATA_REFERENCE = config["PATHS"]["PDF_METADATA_REFERENCE"]
WRONG_PDF_URI = config["PATHS"]["WRONG_PDF_URI"]
NOT_FOUND_PDF_URI = config["PATHS"]["NOT_FOUND_PDF_URI"]
NOT_PDF_URI = config["PATHS"]["NOT_PDF_URI"]
PDF_URI = config["PATHS"]["PDF_URI"]

def populate_db_from_arxiv_api_success(client, app):
    response = client.post(
        "/documents/populate_db_from_arxiv_api/", query_string={"cat": 'cs.ai', "start":"0", "max_results":"2"}, follow_redirects=True
    )
    assert response.status == "200 OK"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert response_data_as_json["message"] == "Successfully retrieved, extracted, and stored in local DB 2 PDFs metadata and content. 0 were already in database"
    
    # Assert the PDFs have been added into the database
    with app.app_context():
        n_instances = get_db().execute(
            "SELECT COUNT(*) FROM pdf"
        )
        assert n_instances == 2
    
    # But does not seem necessary to check the instances content in DB

def populate_db_from_arxiv_api_cat_not_csai_fail(client, app):
    response = client.post(
        "/documents/populate_db_from_arxiv_api/", query_string={"cat": 'vdf', "start":"0", "max_results":"2"}, follow_redirects=True
    )
    assert response.status == "400 BAD REQUEST"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert response_data_as_json["message"] == "Expected 'cs.ai' value for argument 'cat'"
    
def populate_db_from_arxiv_api_wrong_arguments_value_fail(client, app):
    response = client.post(
        "/documents/populate_db_from_arxiv_api/", query_string={"cat": 'vdf', "start":"-9", "max_results":"-72"}, follow_redirects=True
    )
    assert response.status == "400 BAD REQUEST"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert response_data_as_json["message"] == "Could not access the provided URI. Maybe check the requests parameters?"

def populate_db_from_arxiv_api_query_out_of_range_success(client, app):
    response = client.post(
        "/documents/populate_db_from_arxiv_api/", query_string={"cat": 'vdf', "start":"50000000", "max_results":"1000"}, follow_redirects=True
    )
    assert response.status == "200 OK"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert response_data_as_json["message"] == "No PDF to extract from ArXiv.org API for this set of arguments"

def populate_db_from_arxiv_api_max_results_out_of_range_fail(client, app):
    response = client.post(
        "/documents/populate_db_from_arxiv_api/", query_string={"cat": 'vdf', "start":"0", "max_results":"1001"}, follow_redirects=True
    )
    assert response.status == "400 BAD REQUEST"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert response_data_as_json["message"] == "Argument 'max_result' can not exceed 1000 to prevent performance issues into ArXiv.org backend"

# *********** extract_pdf_metadata_and_content_from_uri test cases ***********

def test_extract_pdf_metadata_and_content_from_uri_success(client, app):
    response = client.post(
        "/documents/", query_string={"file_uri": PDF_URI}, follow_redirects=True
    )
    assert response.status == "200 OK"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert response_data_as_json["message"] == "Uploaded PDF successfully"
    assert response_data_as_json["pdf_id"] == "1"

    # Assert the PDF has been added into the database
    with app.app_context():
        assert get_pdf_id(get_db(), PDF_URI) is not None


def test_extract_pdf_metadata_and_content_not_pdf_fail(client, app):
    response = client.post(
        "/documents/", query_string={"file_uri": NOT_PDF_URI}, follow_redirects=True
    )
    assert response.status == "400 BAD REQUEST"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert (
        response_data_as_json["message"]
        == "The content pointed by the provided URI does not seem to be a PDF"
    )


def test_extract_pdf_metadata_and_content_no_uri_fail(client, app):
    response = client.post("/documents/", follow_redirects=True)
    assert response.status == "400 BAD REQUEST"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert (
        response_data_as_json["message"] == "Please provide an URI pointing to a file"
    )


def test_extract_pdf_metadata_and_content_wrong_uri_fail(client, app):
    response = client.post(
        "/documents/", query_string={"file_uri": WRONG_PDF_URI}, follow_redirects=True
    )
    assert response.status == "400 BAD REQUEST"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert response_data_as_json["message"] == "Wrong URI format"


# *********** get_pdf_metadata test cases ***********


def test_get_pdf_metadata_success(client, app):
    # Import reference metadata
    with open(
        DATA_FILE_PATH + PDF_METADATA_REFERENCE, "r"
    ) as pdf_metadata_reference_file:
        reference_metadata = json.load(pdf_metadata_reference_file)
    # Add PDF instance into database
    with app.app_context():
        pdf_id = create_pdf(get_db(), PDF_URI)
        fill_pdf(get_db(), pdf_id, json.dumps(reference_metadata), "dummy content")
    # Now, test the view
    response = client.get(
        "/documents/{}/metadata.json/".format(pdf_id),
    )
    assert response.status == "200 OK"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert (
        response_data_as_json["message"]
        == "Successfully retrieved PDF metadata in database"
    )
    assert response_data_as_json["metadata"] == reference_metadata


def test_get_pdf_metadata_not_in_base_success(client, app):
    response = client.get(
        "/documents/{}/metadata.json/".format(10),
    )
    assert response.status == "404 NOT FOUND"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert response_data_as_json["message"] == "No PDF with such ID in database"


def test_get_pdf_metadata_wrong_pdf_id_format_fail(client, app):
    response = client.get(
        "/documents/{}/metadata.json/".format(-1),
    )
    assert response.status == "404 NOT FOUND"  # Managed by Flask routing service


# TODO : should test whether PDF is in base but metadata is empty

# *********** get_pdf_content test cases ***********


def test_get_pdf_content_success(client, app):
    # Import reference content
    with open(
        DATA_FILE_PATH + PDF_CONTENT_REFERENCE, "r"
    ) as pdf_content_reference_file:
        reference_content = pdf_content_reference_file.read()
    # Add PDF instance into database
    with app.app_context():
        pdf_id = create_pdf(get_db(), PDF_URI)
        fill_pdf(get_db(), pdf_id, '{"dummy key":"dummy value"}', reference_content)
    # Now, test the view
    response = client.get(
        "/documents/{}/content.txt/".format(pdf_id),
    )
    assert response.status == "200 OK"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert (
        response_data_as_json["message"]
        == "Successfully retrieved PDF content in database"
    )
    assert response_data_as_json["content"] == reference_content


def test_get_pdf_content_not_in_base_success(client, app):
    response = client.get(
        "/documents/{}/content.txt/".format(10),
    )
    assert response.status == "404 NOT FOUND"
    response_data_as_json = json.loads(response.data.decode("utf-8").replace("\n", ""))
    assert response_data_as_json["message"] == "No PDF with such ID in database"


def test_get_pdf_content_wrong_pdf_id_format_fail(client, app):
    response = client.get(
        "/documents/{}/content.txt/".format(-1),
    )
    assert response.status == "404 NOT FOUND"  # Managed by Flask routing service


# TODO : should test whether PDF is in base but content is empty
