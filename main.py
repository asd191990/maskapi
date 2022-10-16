from fastapi import FastAPI,UploadFile
from utils.model import Mask2FaceModel
from datetime import datetime
from starlette.responses import FileResponse


app = FastAPI()
model = Mask2FaceModel.load_model('model_epochs-20_batch-64_loss-ssim_l1_loss_20221015_08_23_38.h5')


def process(path):
   try:
      OneImgPath = rf"faces/{path}.png"
      generated_output = model.predict(OneImgPath)  #open img file and predict img
      generated_output.save(rf"outputs/{path}.png") #儲存照片
      return "ok"
   except:
      return "no"

@app.get("/download")
def download(name:str):
   return FileResponse(
            rf"outputs/{name}.png", 
            filename=f"{name}.png", 
        )

@app.post("/upload")
def mask_upload(file:UploadFile):
   img = file.file.read()
   now = datetime.now()
   now_string = datetime.strftime(now, '%Y_%m_%d_%H_%M_%S')

   
   writeImg =  open(rf"faces/{now_string}.png","wb")
   writeImg.write(img)
   writeImg.close()
   print(writeImg)
   if   process(now_string) =="ok":
      return {"url": f"http://127.0.0.1:8000/download?name={now_string}"}
   return {"url": "後端死亡"}


if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)