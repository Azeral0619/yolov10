from ultralytics import YOLOv10

# model = YOLOv10()
# If you want to finetune the model with pretrained weights, you could load the
# pretrained weights like below
# model = YOLOv10('yolov10{n/s/m/b/l/x}.pt')
# model = YOLOv10("yolov10n.pt")
# or
model = YOLOv10("ultralytics/cfg/models/v10/yolov10n.yaml")

model.train(data="mydataset.yaml", epochs=500, batch=16, imgsz=640)
