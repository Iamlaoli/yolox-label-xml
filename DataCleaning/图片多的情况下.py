import os
#xml标签文件
my_data_xml=os.listdir(r"D:\datasets\sign\JPEGImages")
my_data_img=os.listdir(r"D:\datasets\sign\Annotations")
result_path = os.path.join(r"D:\datasets\sign\JPEGImage")
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
        # print(j)
        # print(len(img_list_name))
        # print(len(xml_list_name))
        # print(my_data_xml)
        # for src_xml_data in my_data_xml:
        src_xml_path=os.path.join(r"D:\datasets\sign\JPEGImages"+"/",str(j)+".jpg")
            # print(src_xml_path)
        with open(src_xml_path,"rb") as fpr:
            read_word=fpr.read()
            # print(read_word)
            with open(result_path+"/"+str(j)+".jpg", "wb") as fpw:
                fpw.write(read_word)
    else:
        continue
    # if i == len(img_list_name):
    #     break


