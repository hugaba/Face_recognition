from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
from functions import *
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.post("/recog_faces/")
async def create_upload_file(request: Request, image: UploadFile = File(...)):
    print('in base function')
    # delete previous files
    for root, dirs, files in os.walk('static/saved_pics'):
        for f in files:
            os.unlink(os.path.join(root, f))

    with open("static/saved_pics/image_in.jpg", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        pic = "static/saved_pics/image_in.jpg"
        db_infos = database_connexion()
        firstnames, lastnames, nb_problems, vips, ids = check_image(pic, db_infos)
        faces = get_pics()
        faces.sort()
        infos = {}
        for index in range(0, len(faces)):
            infos[f'elt{index}'] = {"index": index,
                                    "face": faces[index],
                                    "firstname": firstnames[index],
                                    "lastname": lastnames[index],
                                    "nb_problem": nb_problems[index],
                                    "vip": vips[index],
                                    "face_id": ids[index]}

    return templates.TemplateResponse("response.html",
                                      {"request": request, "infos": infos})  # FileResponse('saved_pics/image_out.jpg')


@app.post("/add_to_database/")
async def create_upload_file(request: Request, firstname: str = Form(...), lastname: str = Form(...),
                             probs: int = Form(...), vip: bool = Form(False), picid: int = Form(...)):
    print('in add function')
    add_to_database(firstname, lastname, probs, picid, vip)
    pic = "static/saved_pics/image_in.jpg"
    db_infos = database_connexion()
    firstnames, lastnames, nb_problems, vips, ids = check_image(pic, db_infos)
    faces = get_pics()
    faces.sort()
    infos = {}
    for index in range(0, len(faces)):
        infos[f'elt{index}'] = {"index": index,
                                "face": faces[index],
                                "firstname": firstnames[index],
                                "lastname": lastnames[index],
                                "nb_problem": nb_problems[index],
                                "vip": vips[index],
                                "face_id": ids[index]}

    return templates.TemplateResponse("response.html", {"request": request, "infos": infos})


@app.post("/update_database/")
async def create_upload_file(request: Request, firstname: str = Form(...), lastname: str = Form(...),
                             probs: int = Form(...), vip: bool = Form(False), face_id: int = Form(...)):
    print('in update function')
    update_database(firstname, lastname, probs, face_id, vip)
    pic = "static/saved_pics/image_in.jpg"
    db_infos = database_connexion()
    firstnames, lastnames, nb_problems, vips, ids = check_image(pic, db_infos)
    faces = get_pics()
    faces.sort()
    infos = {}
    for index in range(0, len(faces)):
        infos[f'elt{index}'] = {"index": index,
                                "face": faces[index],
                                "firstname": firstnames[index],
                                "lastname": lastnames[index],
                                "nb_problem": nb_problems[index],
                                "vip": vips[index],
                                "face_id": ids[index]}

    return templates.TemplateResponse("response.html", {"request": request, "infos": infos})


@app.post("/delete_from_database/")
async def create_upload_file(request: Request, delete_id: int = Form(...)):
    print('in delete function')
    delete_from_database(delete_id)
    pic = "static/saved_pics/image_in.jpg"
    db_infos = database_connexion()
    firstnames, lastnames, nb_problems, vips, ids = check_image(pic, db_infos)
    faces = get_pics()
    faces.sort()
    infos = {}
    for index in range(0, len(faces)):
        infos[f'elt{index}'] = {"index": index,
                                "face": faces[index],
                                "firstname": firstnames[index],
                                "lastname": lastnames[index],
                                "nb_problem": nb_problems[index],
                                "vip": vips[index],
                                "face_id": ids[index]}

    return templates.TemplateResponse("response.html", {"request": request, "infos": infos})
