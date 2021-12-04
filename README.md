PYTDelivery
===========
Source code of evaluation of "Python for data intensive applications" lecture at MS SIO, CentraleSupélec

This project is a Flask application that :
* provides an API to import a pdf from a URI
* extract its metadata and content asynchronously
* and make them available for consumption by the user

Installing the project on your machine
--------------------------------------
In a terminal, run the following command :

    git clone https://github.com/will-afs/PYTDelivery.git

Make sure to use Python>= 3.7.
You can check your Python version by running :

    python --version

You can use your own virtual environment.
If you are using Visual Studio Code as an IDE, you can find more info on both : 

* https://code.visualstudio.com/docs/python/environments
* https://stackoverflow.com/questions/54106071/how-can-i-set-up-a-virtual-environment-for-python-in-visual-studio-code

Then, make sure to install the necessary Python dependencies in it by running :
    
    pip install -r requirements.txt

Running the Back-End locally on your machine
--------------------------------------------
You should work within the backend directory.

To run the Back-End, you need to run the following command :

    export FLASK_APP=flaskapp
    export FLASK_ENV=development
    flask init-db
    flask run
    
Sending an HTTP request locally to the Back-End
-----------------------------------------------
Considering the Flask application is running and accessible through the following address :

    http://127.0.0.1:5000/
    
And given the PDF of which extracting metadata is accessible through the client working directory, as "PDF_FILE.pdf" ;

The service can be accessed by a client through HTTP requests as follows.

Posting the PDF towards the service file system:

    curl http://127.0.0.1:5000/extract_pdf_metadata/ -d -o PDF_FILE.pdf

*Note : the PDF file will be stored into the flaskapp/resources directory !*

Getting the PDF metadata after having sent it:

    curl http://127.0.0.1:5000/extract_pdf_metadata/?pdf_name=PDF_FILE.pdf
    
Getting the PDF content after having sent it:

    curl http://127.0.0.1:5000/extract_pdf_content/?pdf_name=PDF_FILE.pdf

Running unit tests
------------------
The tests are defined in tests.py files.
They can be launched from the root directory, by running the following command :

    python -m unittest discover -s flaskapp/tests
    
For more documentation about running tests, please refer to the official documentation : https://docs.python.org/3/library/unittest.html

