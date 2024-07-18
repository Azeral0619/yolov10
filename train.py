from ultralytics import YOLOv10

# model = YOLOv10()
# If you want to finetune the model with pretrained weights, you could load the
# pretrained weights like below
# model = YOLOv10('yolov10{n/s/m/b/l/x}.pt')
model = YOLOv10.from_pretrained("jameslahm/yolov10n")
# or
# model = YOLOv10("ultralytics/cfg/models/v10/yolov10n.yaml")
# model = YOLOv10("runs/detect/train3/weights/last.pt")

model.train(resume=True, data="data/dataset_x.yaml", epochs=500, batch=64, imgsz=640)
