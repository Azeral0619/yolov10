import os
from ultralytics import YOLOv10

model_dir = "model"
model_list = ["best_320_int8.onnx", "best_320.onnx", "best_640_int8.onnx", "best_640.onnx"]

for model_name in model_list:
    model = YOLOv10(os.path.join(model_dir, model_name), task="detect")
    imgsz = 320 if "320" in model_name else 640
    print(f"val {model_name}")
    model.val(data="data/dataset.yaml", imgsz=imgsz)
