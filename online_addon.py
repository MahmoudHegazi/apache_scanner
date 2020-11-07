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





@app.route('/target')
def targeter():
    projectData = []
    # start from Carbs and end with Protein
    info_section1 = []
    info_section1_filtered = []
    thisdict = {'has_number': [], 'has_no_number': [] }
    response = requests.get("https://www.myfitnesspal.com/food/calories/chicken-biriyani-1015500476")
    if response.status_code != 200:
        return "Error fetching page"
        exit()
    else:
        content = response.content
        soup = BeautifulSoup(response.content, 'html.parser')
        # parse the html document
        ju_headers = soup.find_all('h2')
        #for header in ju_headers:
            #if header.text == 'Nutritional Info':
            #    print(str(header)
        #get Nutritional div NutritionalInfoContainer-3XIjH
        nutritional_div = soup.find('div', class_="NutritionalInfoContainer-3XIjH")
        #Nutritional Info

        nutritional_header = soup.find('div', class_="MuiTypography-root MuiTypography-h2 MuiTypography-gutterBottom")
        nutritional_sections = soup.find_all('section', class_="col-1l9Z4")

        #top_3_links = Counter(all_hrefs).most_common(3) return most accured links
        #nutritional_sections = soup.find_all('div', class_="col-1l9Z4")
        # get the sections for our target first
        for  one_section in nutritional_sections:
            projectData.append(one_section.text)

        def listToString(s):
            str1 = " "
            return (str1.join(s))


        string_projectdata = listToString(projectData)
        # get the nutritional_info_list depnd on g in each value
        nutritional_info_list = string_projectdata.split(' g')
        nutritional_info_quots_remove = string_projectdata.split('"')
        #x = listToString(nutritional_info_quots_remove).split(' ', ',')
        for info in range(len(nutritional_info_list)):
            if info == 8:
                info_section1.append(nutritional_info_list[info])
                break
                #return str(info_section1)
            else:
                info_section1.append(nutritional_info_list[info])
        for item in info_section1:
            info_section1_filtered.append(item.replace("'",""))

        # get the first 9 items in the excellsheet
        def num_there(s):
            return any(i.isdigit() for i in s)
        for item in info_section1:
            check_number = num_there(item)
            if check_number:
                #info_sectio1_tuple.append('has_number')
                thisdict["has_number"].append(item)
            else:
                thisdict["has_no_number"].append(item)
                #info_sectio1_tuple.append('has_no_number')


        return str(thisdict)





if __name__ == '__main__':
    app.secret_key = 'AS&S^1234Aoshsheo152h23h5j7ks9-1---3*-s,#k>s'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
