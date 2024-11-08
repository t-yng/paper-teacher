import os
from typing import List
from app.llm.summarize.model import SummarizeLlm
from app.paper import load_paper
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pydantic import BaseModel

app = FastAPI()

# CORS 設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SummarizeSectionRequest(BaseModel):
    language: str
    title: str
    section: str
    summarized_sections: List[str]


@app.post("/papers/extract")
async def extract_sections(file: UploadFile = File(None)):
    if file is None:
        return JSONResponse(
            status_code=422,
            content={"message": "ファイルがアップロードされていません。"},
        )

    dir = "uploaded_files"
    os.makedirs(dir, exist_ok=True)  # ディレクトリが存在しない場合は作成する
    file_location = f"{dir}/{file.filename}"

    with open(file_location, "wb") as f:
        f.write(file.file.read())
    paper = load_paper(file_location)

    return paper.to_dict()


@app.post("/paper/sections/summarize")
def summarize_section(body: SummarizeSectionRequest):
    llm = SummarizeLlm(language=body.language)
    summary = llm.summarize_section(
        title=body.title,
        section=body.section,
        summarized_sections=body.summarized_sections,
    )

    return {"summary": summary}
