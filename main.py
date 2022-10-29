from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from utils.model import Mask2FaceModel
from datetime import datetime
from starlette.responses import FileResponse
import os
from fastapi.responses import StreamingResponse

app = FastAPI()

origins = [
    "https://yuakatl.github.io",
    "https://yuakatl.github.io:8080",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = Mask2FaceModel.load_model(
    'model_epochs-20_batch-64_loss-ssim_l1_loss_20221015_08_23_38.h5')


def process(path):
    try:
        OneImgPath = rf"faces/{path}.png"
        # open img file and predict img
        generated_output = model.predict(OneImgPath)
        generated_output.save(rf"outputs/{path}.png")  # 儲存照片
        return "ok"
    except:
        return "no"



@app.get("/download/{original_name}")
def download(original_name: str):
    print("iiiiiiii")
    type = original_name.split(".")[-1]
    def iterfile():
        with open(rf"outputs/{original_name}", "rb") as file_like:
            yield from file_like

    return StreamingResponse(
        iterfile(),media_type=f"image/{type}"
    )


@app.get("/download")
def download(original_name: str):
    print("iiiiiiii")
    type = original_name.split(".")[-1]
    def iterfile():
        with open(rf"outputs/{original_name}", "rb") as file_like:
            yield from file_like

    return StreamingResponse(
        iterfile(),media_type=f"image/{type}"
    )

import random

@app.post("/upload")
def mask_upload(file: UploadFile):
    img = file.file.read()
    now = datetime.now()
    now_string = datetime.strftime(now, '%Y_%m_%d_%H_%M_%S')  + "_"+str(random.randrange(10, 51))

    writeImg = open(rf"faces/{now_string}.png", "wb")
    writeImg.write(img)
    writeImg.close()
    print(writeImg)
    if process(now_string) == "ok":
        return {"url":now_string+".png"}
    return {"url": "後端死亡"}


@app.get("/")
async def main():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host="0.0.0.0",
                port=int(os.environ.get("PORT", 8080)), reload=True, debug=True)
