from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import cv2
import numpy as np
import pickle
import os

from insightface.app import FaceAnalysis

app = FastAPI()

# templates folder (UI)
templates = Jinja2Templates(directory="templates")

# serve event photos
app.mount("/photos", StaticFiles(directory="photos"), name="photos")

# load model
face_app = FaceAnalysis()
face_app.prepare(ctx_id=0)

# load embeddings
with open("embeddings.pkl", "rb") as f:
    saved_data = pickle.load(f)

# HOME PAGE (UI)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(

request=request,

name="index.html",

)


# SEARCH API
@app.post("/search")
async def search(file: UploadFile = File(...)):

    upload_path = "uploads/selfie.jpg"

    with open(upload_path, "wb") as f:
        f.write(await file.read())

    img = cv2.imread(upload_path)

    faces = face_app.get(img)

    if len(faces) == 0:
        return {"error": "No face found"}

    selfie_embedding = faces[0].embedding

    matches = []

    for item in saved_data:

        distance = np.linalg.norm(
            selfie_embedding - item["embedding"]
        )

        if distance < 25:
            matches.append({
                "image": item["image"],
                "distance": float(distance)
            })

    matches.sort(key=lambda x: x["distance"])

    results = []

    for m in matches[:20]:
        results.append({
            "image": f"/photos/{m['image']}",
            "distance": m["distance"]
        })

    return {"results": results}