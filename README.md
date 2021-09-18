# Face_recognition

lien vers le rapport écrit : [rapport](https://docs.google.com/document/d/1jC87cg68rni0Pxgu-vXMxU5FHK6CnuA5/edit?usp=sharing&ouid=115739380341365217109&rtpof=true&sd=true)

# Content

data folder: contain database.db with database informations

dataset: contain pictures to test the program (some faces registered in database)

static/saved_pics: temporary file where the analaysed pics are stored  for the analysis

templates: contain html templates

functions.py: python functions used to analyse images or write into database

main.py: python file with paths

requirements.txt: requirements to make the virtual environment

# Getting started

## Prerequisite:

### Create your virtual environment

Open the folder in which you import the github files

Open a terminal and create a new virtual environment : python3 -m venv env

Install the required libraries: pip3 install -r requirements.txt

## Start program:

open a terminal in the main folder

activate your virtual environment with the command line: source venv/bin/activate

start the api with the command line: uvicorn main:app --reload

go on this url: http://127.0.0.1:8000

- You can load an image to analyse and click on the submit button
- Pic is going to be analysed and the faces on the pic will be listed below the initial pic with:
  - Unknown faces will be yellow
  - Known faces without problem will be green
  - Known faces with problems will be red
- You will have the possibility to add unknown faces to database or Update/Delete known faces
