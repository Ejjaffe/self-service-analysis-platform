"""
CREATE AN END-TO-END CSV UPLOAD AND DOWNLOAD SYSTEM
"""
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import List, Optional
import shutil
from glob import glob
import pandas as pd
import os


# RESPONSE MODELS
class FileColumn(BaseModel):
    colname: str
    colkey: str
    dtype: str

class UploadedFile(BaseModel):
    filename:str
    columns: List[FileColumn]
    filekey:int

class UploadedFiles(BaseModel):
    files: Optional[List[UploadedFile]]

# APP CONFIGURATION
DATA_DIR_NAME = "data"

ORIGINS = [
    "*", # this is pretty insecure and the CORS might have to be removed once auth gets installed. but for my purposes it's okay at the moment.
]

app = FastAPI(title="Self Service Analysis API",description="CSV-based upload/analysis/download.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APP API CALLS
@app.get('/')
def root():
    return {"title":app.title, "description":app.description}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(default="")):
    """
    Takes a csv file uploaded as multipart form data, downloads it.
    """
    newpath = os.path.join(DATA_DIR_NAME, file.filename)

    with open(newpath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
@app.get("/downloadfile/{filename}")
"""
Download a file by it's filename
"""
async def download_file(filename:str):
    file_path = os.path.join(DATA_DIR_NAME, filename)
    
    return FileResponse(path=file_path, filename=filename, media_type='text/csv')

def filecolumns(fname):
    """
    Open a csv with pandas by it's full filename and return a list of FileColumn dicts, which look like this:
        {'colname':'Houses Sold', 'dtype':'int64', 'colkey':'RealatorData.csv4'}
    """
    df = pd.read_csv(fname)
    col_and_dtype = df.dtypes.to_dict()
    format = lambda idx, col, dtype: {'colname':col, 'colkey':fname+str(idx), "dtype":str(dtype)}
    return [format(i,name,dtype) for i, (name, dtype) in enumerate(col_and_dtype.items())]

def uploaded_file(i, fname):
    """
    Return a list of UploadedFile dicts, which look like this:
    {
        'filename': 'RealatorData.csv', 
        'columns':  [ ... {'colname':'Houses Sold', 'dtype':'int64', 'colkey':'RealatorData.csv4'} ... ]
        'filekey': 7
    }
    """
    uf = {}
    uf["filekey"] = i
    uf["filename"] = os.path.basename(fname)
    uf["columns"] = filecolumns(fname)
    return uf

@app.get("/listuploadedfiles/", response_model=UploadedFiles)
def list_files():
    """
    Return uploaded file data as an UploadedFiles object
    """
    search_str = os.path.join(DATA_DIR_NAME, "*.csv")
    csv_list = glob(search_str)
    uf_list = [uploaded_file(i,f) for i,f in enumerate(csv_list)]
    return {"files":uf_list}
