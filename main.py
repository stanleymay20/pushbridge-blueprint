from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import zipfile, os, shutil

app = FastAPI()

@app.post("/push-to-github/")
async def push_to_github(file: UploadFile, repo: str = Form(...), token: str = Form(...), username: str = Form(...)):
    try:
        temp_dir = "temp_repo"
        with zipfile.ZipFile(file.file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        os.system(f"cd {temp_dir} && git init")
        os.system(f"cd {temp_dir} && git remote add origin https://{token}@github.com/{username}/{repo}.git")
        os.system(f"cd {temp_dir} && git add .")
        os.system(f'cd {temp_dir} && git commit -m "Pushed via PushBridge"')
        os.system(f"cd {temp_dir} && git push --force origin master")

        shutil.rmtree(temp_dir)
        return JSONResponse(content={"message": "Push successful"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
