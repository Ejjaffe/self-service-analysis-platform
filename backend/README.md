# Back-End
Code relating to the back-end / server side code.

To create the conda environment, run:

```
conda create -n ssap -c conda-forge -c anaconda fastapi python-multipart pandas numpy pydantic uvicorn starlette
```

To run the app, open up the conda environment, cd to this directory, and run:
```
uvicorn api:app --reload
```
