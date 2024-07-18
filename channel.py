import torch

# 加载预训练权重
checkpoint = torch.load("runs/detect/train2/weights/best.pt")

# 获取第一个卷积层的权重
state_dict = checkpoint["model"].state_dict()

for name, param in state_dict.items():
    print(f"{name}: {param.size()}")

original_weight = state_dict["model.0.conv.weight"]

# 计算通道维度的平均值
new_weight = original_weight.mean(dim=1, keepdim=True)

# 更新权重
state_dict["model.0.conv.weight"] = new_weight

checkpoint["model"].load_state_dict(state_dict)

# 保存修改后的权重文件
torch.save(checkpoint, "gray_yolov10n.pt")
