from ultralytics import YOLOv10
import os

enable_int8 = True
dir = "model"
# Load a model
model = YOLOv10(os.path.join(dir, "best.pt"))  # load an official model

# Export the model
for imgsz in (320, 640):
    model.export(format="onnx", imgsz=imgsz, int8=enable_int8)
    int8_str = "_int8" if enable_int8 else ""
    os.rename(os.path.join(dir, "best.onnx"), os.path.join(dir, f"best_{imgsz}{int8_str}.onnx"))
