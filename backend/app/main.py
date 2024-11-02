import os
from app.paper import load_paper
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# POST /paper/extract
@app.post("/paper/extract")
async def extract_sections(file: UploadFile = File(...)):
    dir = "uploaded_files"
    os.makedirs(dir, exist_ok=True)  # ディレクトリが存在しない場合は作成する
    file_location = f"{dir}/{file.filename}"

    with open(file_location, "wb") as f:
        f.write(file.file.read())
    paper = load_paper(file_location)

    return paper.to_dict()


# POST /paper/sections/summarize
