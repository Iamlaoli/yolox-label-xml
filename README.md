# yolox-label-xml

### 使用yolox实现的一个预标注程序

1. 将预训练好的权重放入models/weights中，修改demo.py文件中的（.pth）--ckpt参数；

2. 在demo。py中配置需要标注的图片路径和要保存xml路径；

3. 修改 exps\example\yolox_voc\yolox_voc.py类别个数；

4. 修改 yolox\data\datasets\voc_classes.py 种类名称；

5. 修改 yolox\exp\yolox_base.py 类别个数；

6. demo.py 中 def make_parser() 参数可根据实际情况调试；

7. 运行demo.py文件生成xml标签；

8. 使用labelimg进行微调；

本项目基于yolox推理进行修改,仿照yolov5-label-xml-main进行编写；



### 配置说明：

yolox版本，需要的torch环境：torch  >=1.7.0
