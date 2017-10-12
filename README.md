# GamrAPI

Gamr is a Like/Dislike style app, used in the course CMPUT401 at the University of Alberta.  The application was developed by Diego Serrano during the Fall of 2017.

## Installation 

First clone the application code into any directory on your disk (preferably, not using spaces in the folder structure)
```sh
$ git clone https://github.com/dfserrano/GamrAPI.git
$ cd GamrAPI
```

Install virtualenv with pip
```sh
$ sudo pip install virtualenv
```

Create a new virtualenv and activate it
```sh
$ virtualenv venv
$ source venv/bin/activate
```

Install the required libraries: flask-restplus, Flask-SQLAlchemy, and flask-cors
```sh
pip install flask-restplus
pip install Flask-SQLAlchemy
pip install -U flask-cors
```

Make sure the current working directory is on your PYTHONPATH:
```sh
export PYTHONPATH=.:$PYTHONPATH
```

Start the app
```sh
python gamr/app.py
```

If you just want to test the app, then type this instead
```sh
python -m unittest discover
```

## References
These resources were used for the creation of this app:

Flask: http://flask.pocoo.org/

Flask-restplus: http://flask-restplus.readthedocs.io/en/stable/

Flask-CORS: https://pypi.python.org/pypi/Flask-Cors

Useful tutorial: http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/

