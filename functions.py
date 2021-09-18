import cv2
import face_recognition
import numpy as np
import tkinter as tk
import sqlite3
import pandas as pd
import re
import ast
from os import listdir


def database_connexion():
    try:
        conn = sqlite3.connect("data/database.db")
        print("Opened database successfully")
    except Exception as e:
        print("Error during connection: ", str(e))

    df = pd.read_sql_query("SELECT * FROM black_list", conn)

    conn.close()

    encodings = df['FACE_ENCODING'].tolist()
    known_faces = []
    # transform string list to list
    for encoding in encodings:
        encoding = re.sub('\s+', ',', encoding)
        encoding = np.array(ast.literal_eval(encoding))
        known_faces.append(encoding)
    known_faces_ids = df['ID'].tolist()
    known_faces_firstnames = df['FIRSTNAME'].tolist()
    known_faces_lastnames = df['LASTNAME'].tolist()
    known_faces_nb_problems = df['NB_PROBLEMS'].tolist()
    know_faces_vip = df['VIP'].tolist()
    infos = {
        "ids": known_faces_ids,
        "faces": known_faces,
        "firstnames": known_faces_firstnames,
        "lastnames": known_faces_lastnames,
        "probs": known_faces_nb_problems,
        "vips": know_faces_vip
    }
    return infos


def check_image(pic, infos):
    # load the image with faces
    image = cv2.imread(pic)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_image = image[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    # Initialize face names list
    face_ids = []
    face_firstnames = []
    face_lastnames = []
    face_nb_problems = []
    face_vip = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(infos["faces"], face_encoding, tolerance=0.50)
        firstname = 'Unknown'
        lastname = ''
        face_id = None
        nb_problems = 0
        vip = 0
        # get the distance between know faces and face to compare with
        face_distances = face_recognition.face_distance(infos["faces"], face_encoding)

        # get shorter distance
        best_match_index = np.argmin(face_distances)
        # get name associated with index of best match
        if matches[best_match_index]:
            face_id = infos["ids"][best_match_index]
            firstname = infos["firstnames"][best_match_index]
            lastname = infos["lastnames"][best_match_index]
            nb_problems = infos["probs"][best_match_index]
            vip = infos["vips"][best_match_index]

        face_ids.append(face_id)
        face_firstnames.append(firstname)
        face_lastnames.append(lastname)
        face_nb_problems.append(nb_problems)
        face_vip.append(vip)

    i = 0
    # Label the results
    for (top, right, bottom, left), firstname, lastname, nb_prob in zip(face_locations, face_firstnames, face_lastnames, face_nb_problems):
        if not firstname:
            continue
        sub_pic = image[top:bottom, left:right]
        cv2.imwrite(f"static/saved_pics/sub_image_{i}.jpg", sub_pic)
        # Draw a label with a name below the face
        font = cv2.FONT_HERSHEY_DUPLEX
        name = f"{firstname} {lastname}"
        cv2.putText(image, name, (left + 3, bottom + 20), font, 0.5, (255, 255, 255), 1)
        if nb_prob > 0:
            # Draw a box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
            text = f'number of problems : {nb_prob}'
            cv2.putText(image, text, (left + 3, bottom + 40), font, 0.5, (255, 255, 255), 1)
        elif not firstname == 'Unknown':
            cv2.rectangle(image, (left, top), (right, bottom), (0, 128, 0), 2)
        else:
            # Draw a box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 255), 2)
        i += 1
    cv2.imwrite("static/saved_pics/image_out.jpg", image)
    return face_firstnames, face_lastnames, face_nb_problems, face_vip, face_ids


def create_html_sub_faces():
    text = ""
    files = [f for f in listdir('static/saved_pics') if f.startswith('sub_image_')]
    for file in files:
        text += """
    <div class="row">
        <div class='col-sm-2'>
            <img src="{{ url_for('static', path='saved_pics/""" + file + """') }}" class="img-responsive" alt="processed image">
        </div>
    </div>
    <hr/>"""

    return text


def get_pics():
    files = [f for f in listdir('static/saved_pics') if f.startswith('sub_image_')]
    path = "http://127.0.0.1:8000/static/saved_pics/"
    files = [path + file for file in files]
    return files


def add_to_database(firstname, lastname, problems, picid, vip):
    try:
        conn = sqlite3.connect("data/database.db")
        cursor = conn.cursor()
        print("Opened database successfully")
        face = face_recognition.load_image_file(f"static/saved_pics/sub_image_{picid}.jpg")
        face_encoding = face_recognition.face_encodings(face)[0]
        if vip:
            vip = 1
        else:
            vip = 0

        sqlite3_query = f"""INSERT INTO black_list (FIRSTNAME, LASTNAME, NB_PROBLEMS, FACE_ENCODING, VIP) 
                        VALUES ('{firstname}', '{lastname}',{problems},'{face_encoding}',{vip});
                        """

        results = conn.execute(sqlite3_query)
        conn.commit()
        print("data have been inserted successfuly")
        cursor.close()
    except Exception as e:
        print("Error during connection: ", str(e))
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


def update_database(firstname, lastname, problems, face_id, vip):
    try:
        conn = sqlite3.connect("data/database.db")
        cursor = conn.cursor()
        print("Opened database successfully")

        if vip:
            vip = 1
        else:
            vip = 0

        sqlite3_query = f"""UPDATE black_list 
                        SET FIRSTNAME = '{firstname}',
                        LASTNAME = '{lastname}', 
                        NB_PROBLEMS = {problems}, 
                        VIP = {vip}
                        WHERE ID={face_id};
                        """

        conn.execute(sqlite3_query)
        conn.commit()
        print("data have been updated successfuly")
        cursor.close()
    except Exception as e:
        print("Error during connection: ", str(e))
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


def delete_from_database(delete_id):
    print('in delete')
    try:
        conn = sqlite3.connect("data/database.db")
        cursor = conn.cursor()
        print("Opened database successfully")

        sqlite3_query = f"""DELETE FROM black_list 
                        WHERE ID={delete_id};
                        """

        conn.execute(sqlite3_query)
        conn.commit()
        print("data have been deleted successfuly")
        cursor.close()
    except Exception as e:
        print("Error during connection: ", str(e))
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")