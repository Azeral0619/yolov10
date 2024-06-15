from ultralytics import YOLOv10

# model = YOLOv10()
# If you want to finetune the model with pretrained weights, you could load the
# pretrained weights like below
# model = YOLOv10('yolov10{n/s/m/b/l/x}.pt')
model = YOLOv10("yolov10s.pt")
# or
# model = YOLOv10.from_pretrained('jameslahm/yolov10{n/s/m/b/l/x}')

model.train(data="mydataset.yaml", epochs=500, batch=16, imgsz=640)
