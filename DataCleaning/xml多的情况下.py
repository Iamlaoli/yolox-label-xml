import os
#xml标签文件
my_data_xml=os.listdir(r"D:\model\YOLOX-main\datasets\VOCdevkit\VOC2007\Annotations")
my_data_img=os.listdir(r"D:\model\YOLOX-main\datasets\VOCdevkit\VOC2007\JPEGImages")
result_path = os.path.join(r"D:\model\YOLOX-main\datasets\VOCdevkit\VOC2007\Annotation")
if not os.path.exists(result_path):
    os.mkdir(result_path)
xml_list_name=[]
img_list_name=[]
for xml_cell in my_data_xml:
    # print(str(xml_cell).split(".",)[0])
    xml_list_name.append((xml_cell).split(".",)[0])
for img_cell in my_data_img:
    # print(str(img_cell).split(".", )[0])
    img_list_name.append((img_cell).split(".", )[0])
# print(len(img_list_name))
# print(len(xml_list_name))
for i,j in enumerate(img_list_name):
    print(j)
    if j in xml_list_name:
        src_xml_path=os.path.join(r"D:\model\YOLOX-main\datasets\VOCdevkit\VOC2007\Annotations"+"/",str(j)+".xml")
        # src_xml_path=os.path.join(r"D:\model\yolox-label-xml-main\c_xml"+"/",str(j)+".xml")
            # print(src_xml_path)
        with open(src_xml_path,"r+",encoding="utf-8") as fpr:
            read_word=fpr.read()
            # print(read_word)
            with open(result_path+"/"+str(j)+".xml", "w+",encoding="utf-8") as fpw:
                fpw.write(read_word)
    else:
        continue
    # if i == len(img_list_name):
    #     break


