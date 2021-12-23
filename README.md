PYTDelivery
===========
Source code of evaluation of "Python for data intensive applications" lecture at MS SIO, CentraleSupélec

This project is a Flask application that provides an API to populate a PDFs DB from ArXiv.org and make their related informations (URI, metadata and content) available for consumption.

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
    
The application database can be populated by batchs from the ArXiv.org API by running requests as follows :

    curl -X POST "http://127.0.0.1:5000/documents/batch_from_arxiv/?cat=cs.ai&start=0&max_results=20"
    
* **"cat" is the category to fetch PDFs into ArXiv.org API**. Here, it is set to cs.ai (Computer Science - Artificial Intelligence).
It is only left for endpoint reutisability purposes : this endpoint does not accept any other category for now
* **"start" is the start index for the ArXiv.org query of their database**. Here, it is set to 0, meaning it will start from the first PDF in base.
To date (December 2021), there are about 41000 to 42000 PDFs stored in their database
* **"max_results" is the maximal number of PDFs to fetch**. The ArXiv.org API user manual discourages to use a max_results value of more than 1000 PDFs.
But here, the liberty is let to the user to fill any other value.

PDFs can also be imported one by one into the application database by providing their URI in the request parameters :

    curl -X POST http://127.0.0.1:5000/documents/?file_uri=http://arxiv.org/pdf/cs/9308101v1

*Note : the file_uri argument has to point onto a PDF !*

It will return a Task ID. The Content and Metadata of the PDF will be extracted and stored into the system's database asynchronously.

Getting the general informations on a previously launched task (processing state, file_uri, metadata, pdf_id, link to content):

    curl http://127.0.0.1:5000/documents/<task_id>/

Getting the PDF metadata :

    curl http://127.0.0.1:5000/documents/<pdf_id>/metadata.json/
    
Getting the PDF content :

    curl http://127.0.0.1:5000/documents/<pdf_id>/content.txt/

Running unit tests
------------------
The tests are defined in tests.py files.
They can be launched from the root directory, by running the following command :

    pytest
    
For more documentation about running tests, please refer to the official documentation : https://docs.pytest.org/en/6.2.x/

