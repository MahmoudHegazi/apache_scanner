# this awesome solution 

#!/usr/bin/python
from bs4 import BeautifulSoup
from tablib import Dataset
import numpy as np
import excel
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Element, ElementsMeta, Page, Vote
from flask import session as login_session
import string
import excel
# IMPORTS FOR THIS STEP
import httplib2
import json
from flask import make_response
import requests
import pandas as pd
from tablib import Dataset
import numpy as np
import excel
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# IMPORTS FOR THIS STEP
import pprint
import httplib2
import json
import sqlite3
from flask import make_response
import requests


app = Flask(__name__)

APPLICATION_NAME = "skaner"

# Connect to Database and create database session
engine = create_engine('sqlite:///skanner.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



# You need install :
# pip install PyPDF2 - > Read and parse your content pdf
# pip install requests - > request for get the pdf
# pip install BeautifulSoup - > for parse the html and find all url hrf with ".pdf" final
from PyPDF2 import PdfFileReader
import requests
import io
from bs4 import BeautifulSoup
import requests
from collections import Counter






 for side in range(100):
	page = str(side + 1)
	for char in chars:
		character = char
		print('https://www.myfitnesspal.com/food/search?page=' + page + '&search=' + character)
    
    
    
@app.route('/target')
def targeter():
    link_storage = []
    projectData = []
    info_section1 = []
    info_section1_filtered = []
    thisdict = {'has_number': [], 'has_no_number': [] }
    response = requests.get("https://www.myfitnesspal.com/food/search?page=100&search=n")
    if response.status_code != 200:
        return "Error fetching page"
        exit()
    else:
        content = response.content
        soup = BeautifulSoup(response.content, 'html.parser')
        ju_link_parent = soup.find_all('div', class_="jss10")
        for parent in ju_link_parent:
            get_links = parent.find_all('a')
            for i in get_links:
                link_storage.append(i)
