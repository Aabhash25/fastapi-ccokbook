import shutil
from fastapi import FastAPI, File, UploadFile

# shutil - used to efficiently copy file objects
File.Uo

app = FastAPI()


@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}
