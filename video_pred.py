# Ultralytics YOLO 🚀, AGPL-3.0 license
import cv2
import numpy as np
from ultralytics import YOLOv10

# 初始化YOLOv8模型

mdl = 'runs/detect/train/weights/best.pt'
#设置自己训练好的模型路径
model = YOLOv10(mdl, task='detect')
# 读取视频文件
cap = cv2.VideoCapture(0)
# 逐帧进行预测
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
   # 对每一帧进行预测。并设置置信度阈值为0.8，需要其他参数，可直接在后面加
    results = model(frame,False,conf=0.2)
    conf = True
   # 绘制预测结果
    for result in results:
        # 绘制矩形框
        for box in result.boxes:
            xyxy = box.xyxy.squeeze().tolist()
            x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            c, conf, id = int(box.cls), float(box.conf) if conf else None, None if box.id is None else int(box.id.item())
            name = ('' if id is None else f'id:{id} ') + result.names[c]
            label =name
            confidence =conf
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label}: {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    #或者使用下行代码绘制所有结果
    #res=results[0].plot(conf=False)
   # 显示预测结果
    cv2.imshow("Predictions", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 释放资源并关闭窗口
cap.release()
cv2.destroyAllWindows()
