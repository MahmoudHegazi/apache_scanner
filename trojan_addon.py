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
import time


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


@app.route('/db/json')
def dbjson():
    content = session.query(Page).all()
    return jsonify(Content=[r.serialize for r in content])

#first_child = our_soup.find("body").find("ol")
#print(first_child.findChild())
chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
collecter = []
errors = []

def pages_jumber():
    for side in range(100):
        page = str(side + 1)
        for char in chars:
            character = char
            alink = 'https://www.myfitnesspal.com/food/search?page=' + page + '&search=' + character
            collecter.append(alink)
            newlink = Element(url=alink)
            session.add(newlink)
            session.commit()
            print('Apache_Scanner collecting links ....')

@app.route('/view')
def viewer():
    x = session.query(Page).order_by(asc(Page.id))
    prpject_data = []
    for i in x:
        prpject_data.append(str(i.url))
        print('appending item')
    return str(prpject_data)



@app.route('/target')
def targeter():
    print('Prepear Your Self For Awesome joureny...')
    print('apache_scanner getting ready and appending the links ...')
    print('1')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('go.............')
    pages_jumber()
    link_storage = []

    projectData = []
    # start from Carbs and end with Protein
    info_section1 = []
    info_section1_filtered = []
    thisdict = {'has_number': [], 'has_no_number': [] }
    for ju_page in collecter:
        part_container = []

        ju_link = ju_page
        response = requests.get(ju_link)
        if response.status_code == 500:
            time.sleep(240)
        if response.status_code != 200:
            #return "Error fetching page"
            the_resp = response.status_code
            newpage = Page(name="null", url=ju_link, status=the_resp, public='FALSE', item_type='food',
            jss_description='null',jss_name='null',
            jss_quantity='null',jss_calories='null',jss_carbs='null',
            jss_fat='null',jss_protein='null')
            session.add(newpage)
            session.commit()
            print('Apache_Scanner Found Problem with status_code = ' + str(newpage.status))
            print('Apache_Scanner AI system will wait 60 second before start request..')
            time.sleep(60)
            continue
        else:
            the_resp = response.status_code
            content = response.content
            soup = BeautifulSoup(response.content, 'html.parser')
            # parse the html document
            # get the description jss36
            #Calories: 380 •Carbs: 33g •Fat: 19g •Protein: 21g 3

            # this function take info_string part 3 from each page return dict with key and value for each info
            def ge_info(info_string):
                 info_list = info_string.split('•')
                 new_dict = {}
                 for info in info_list:
                     info_key= str(info.split(': ', 1)[0])
                     info_value = str(info.split(': ', 1)[1]).split(' ')[0]
                     new_dict[info_key] = info_value
                     print('skanner_apache getting Awesome new info  .. ' + str(info_value))
                 return new_dict
            # this function take description_string part 3 from each page return dict with key and value for each description
            def ge_descriptions(descriptions_string):
                 descriptions_list = descriptions.split(', ')
                 new_dict = {}
                 description_key= descriptions_list[0]
                 description_value= descriptions_list[1]
                 new_dict1[description_key] = description_value;
                 print('Got New Awesome Description with value... ' + str(description_value))
                 return new_dict
            ju_info = soup.find_all('div', class_="jss36")
            # get the description jss36 2
            ju_description = soup.find_all('div', class_="jss31")
            # get all parents  (2600) 26000 - 10940 it was stoped at 1094  (10940/10) 1
            ju_link_parent = soup.find('div', class_="main-2ZMcp")

            # get all links from that and names and info from that div
            ju_divs = soup.find('div', class_="main-2ZMcp").find_all('div')
            for onediv in ju_divs:
                part_container.append(onediv)
            for container in part_container:
                if container['class'].startswith('jss'):
                    part_container1 = []
                    ju_conter = container.find_all('div')
                    for i in ju_conter:
                        part_container1.append(i)
                    #part1
                    get_link = part_container1[0].find('a')
                    get_link_text = get_link.text
                    get_link_href = 'https://www.myfitnesspal.com' + str(get_link['href'])
                    #part2
                    get_description = part_container1[1].text
                    descriptions_dict = ge_descriptions(get_description)
                    #part3
                    get_infos = part_container1[2].text
                    info_dict = ge_info(get_infos)

                    # parse descriptions
                    descriptions_names = ''
                    descriptions_quantity = ''
                    Calories_value = ''
                    Carbs_value = ''
                    Fat_value = ''
                    Protein_value = ''
                    for key, value in descriptions_dict.items():                        # item_description or nname in excel Protein
                        descriptions_names = str(key)
                        descriptions_quantity = str(value)
                    for key, value in info_dict.items():
                        if key == 'Calories':
                            Calories_value = str(value)
                        if key == 'Carbs':
                            Carbs_value = str(value)
                        if key == 'Fat':
                            Fat_value = str(value)
                        if key == 'Protein':
                            Protein_value = str(value)
                    print('Apache_Scanner Got a new Container and parsed it ready to scrap..')
                    newpage = Page(name=get_link_text, url=get_link_href, status=the_resp, public='TRUE', item_type='food',
                    jss_description=descriptions_names,jss_name=descriptions_names,
                    jss_quantity=descriptions_quantity,jss_calories=Calories_value,jss_carbs=Carbs_value,
                    jss_fat=Fat_value,jss_protein=Protein_value)
                    session.add(newpage)
                    session.commit()
                    print('Apache_Scanner Successfuly Got link with id ' + str(newpage.id) + ' .')
    return 'Apache_Scanner Conquered The all pages'



if __name__ == '__main__':
    app.secret_key = 'AS&S^1234Aoshsheo152h23h5j7ks9-1---3*-s,#k>s'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
