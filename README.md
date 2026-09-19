Event Photo Face Search 

This project was requested by an event organizer who wanted an easier way for guests to find photos of themselves after an event.

Users can upload a selfie, and the app searches through the event photos to find images containing a similar face.

How It Works

-Upload a selfie
-Detect the face using InsightFace
-Compare it with saved face embeddings
-Display the closest matching event photos
-Built With
-FastAPI
-Python
-OpenCV
-InsightFace
-NumPy
-Jinja2

Run
uvicorn main:app --reload

Then open http://127.0.0.1:8000.
