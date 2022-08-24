#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : app.py
# Author             : Cazeho
# Date created       : 24/08/2022
# Repository         : https://github.com/Cazeho/eduscore



import streamlit as st 
import pdfplumber
import re

import requests as rq
import mechanize

from io import BytesIO


st.title("Calculer votre Moyenne Générale")

st.success("Compatible uniquement avec les relevés de notes de l'université de Nice Sophia-Antipolis")

def get_moy_by_matter():
    pass

def get_moy(file):
    pattern=r"\d+(?:\.?\d{3}) \(coeff \d+(?:\.?\d{4})\)"
    data=[]
    with pdfplumber.open(file) as pdf:
        pages = pdf.pages
        for page_nr, pg in enumerate(pages, 1):
            text = pg.extract_text()
            for row in text.split('\n'):
                x = re.findall(pattern, row)
                if x:
                    data.append(x)
    flat = []
    for xs in data:
        for x in xs:
            flat.append(x)
    notes=[]
    coeff=[]
    for i in flat:
        h=i.replace("(coeff ","").replace(")","")
        d=h.split(" ")
        notes.append(float(d[0]))
        coeff.append(float(d[1]))
    k=0
    for i,j in zip(notes,coeff):
        k=i*j + k
    moy=k / len(coeff)
    return moy

######################

def web_pdf(username,password):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
    br.open("https://login.unice.fr/login?service=https%3A%2F%2Fintracursus.unice.fr%2Fic%2Fdlogin%2Fcas.php")
    br.select_form(nr=0)
    br.form['username'] = username
    br.form['password'] = password
    br.submit()
    res=br.open("https://intracursus.unice.fr/ic/etudiant/ic-notes-presences.php")
    pdf=res.read()
    return pdf
    
    


def get_name(f):
    with pdfplumber.open(f) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        for row in text.split('\n'):
            if row.startswith('Relevé des notes et absences de'):
                res = row.split()[6:8]
    return res

st.subheader("Uploader votre relevée de note directement")
uploaded_data = st.file_uploader(
        "Drag and Drop or Click to Upload", type=["pdf"], accept_multiple_files=False
    )
if uploaded_data is None:
    name=""
    moy=""
else:
    f= uploaded_data
    name=get_name(f)[1]+" "+get_name(f)[0]
    moy=get_moy(f)
    moy="{:.2F}".format(moy)

st.subheader("Ou en Remote")

with st.form(key='remote'):
    st.write("Credential de votre compte Unice")
    nav1,nav2 = st.columns([2,1])
    with nav1:
        u=st.text_input("username")
    with nav2:
        p=st.text_input("password",type="password")
    submit = st.form_submit_button(label='Remote')


    
    

if submit:
    b = web_pdf(u,p)
    b=BytesIO(b)
    name= get_name(b)[1]+" "+get_name(b)[0]
    moy=get_moy(b)
    moy="{:.2F}".format(moy)
    
st.subheader("Nom: "+name)

st.subheader("Moyenne générale: "+str(moy))


st.info("Version 1.0 , un problème ? reporter le sur https://github.com/Cazeho/eduscore/issues")
