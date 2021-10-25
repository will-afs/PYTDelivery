PYTDelivery
===========
Source code of evaluation of "Python for data intensive applications" lecture at MS SIO, CentraleSupélec

This project is a Flask application that :
* provides an API that reads an uploaded pdf
* extract its metadata
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

    export FLASK_APP=flaskapp/app
    export FLASK_ENV=development
    python -m flask
    
Sending an HTTP request locally to the Back-End
-----------------------------------------------
Considering the Flask application is running and accessible through the following address :

    http://127.0.0.1:5000/
    
And given the PDF of which extracting its metadata is accessible through the following path : ~/pdf_name.pdf

The service can be accessed by a client through HTTP requests as follows :

    curl http://127.0.0.1:5000/ -o PDFPATH
    
Running unit tests
------------------
The tests are defined in tests.py files.
They can be launched from the root directory, by running the following command :

    python -m unittest discover -s flaskapp/tests
    
For more documentation about running tests, please refer to the official documentation : https://docs.python.org/3/library/unittest.html

