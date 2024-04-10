import cv2
import argparse
import inference
from lxml.etree import Element, SubElement, tostring
from yolox import exp
import os
from yolox.data.datasets import VOC_CLASSES
def make_parser():
    parser = argparse.ArgumentParser("YOLOX Demo!")
    parser.add_argument(
        "--demo",  help="demo type, eg. image, video and webcam"
    )
    parser.add_argument("-expn", "--experiment-name", type=str, default=None)
    parser.add_argument("-n", "--name", type=str, default=None, help="model name")
    parser.add_argument(
        "--path", help="path to images or video"
    )
    parser.add_argument(
        "--save_result",
        action="store_true",
        help="whether to save the inference result of image/video",
    )
    # exp file
    parser.add_argument(
        "-f",
        "--exp_file",
        default="./exps\example\yolox_voc\yolox_voc.py",
        type=str,
        help="please input your experiment description file",
    )
    parser.add_argument("-c", "--ckpt", default=r"D:\model\YOLOX-main\weights\x_s\best_ckpt_0105_fire_95.pth", type=str, help="ckpt for eval")#所用到的模型位置
    parser.add_argument(
        "--device",
        default="gpu",
        type=str,
        help="device to run our model, can either be cpu or gpu",
    )
    parser.add_argument("--conf", default=0.3, type=float, help="test conf")
    parser.add_argument("--nms", default=0.45, type=float, help="test nms threshold")
    parser.add_argument("--tsize", default=640, type=int, help="test img size")
    parser.add_argument(
        "--fp16",
        dest="fp16",
        default=False,
        action="store_true",
        help="Adopting mix precision evaluating.",
    )
    parser.add_argument(
        "--legacy",
        dest="legacy",
        default=False,
        action="store_true",
        help="To be compatible with older versions",
    )
    parser.add_argument(
        "--fuse",
        dest="fuse",
        default=False,
        action="store_true",
        help="Fuse conv and bn for testing.",
    )
    parser.add_argument(
        "--trt",
        dest="trt",
        default=False,
        action="store_true",
        help="Using TensorRT model for testing.",
    )
    parser.add_argument(
        "--classes",
        default=("other"),#需要标注的类别
        # default=VOC_CLASSES,#需要标注的类别
        type=str,
        help="show classes",
    )
    return parser
def create_xml(list_xml,list_images,xml_path):
    """
    创建xml文件，依次写入xml文件必备关键字
    :param list_xml:   txt文件中的box
    :param list_images:   图片信息，xml中需要写入WHC
    :return:
    """
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'Images'
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = str(list_images[3])
    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(list_images[1])
    node_height = SubElement(node_size, 'height')
    node_height.text = str(list_images[0])
    node_depth = SubElement(node_size, 'depth')
    node_depth.text = str(list_images[2])

    if len(list_xml)>=1:        # 循环写入box
        for list_ in list_xml:
            node_object = SubElement(node_root, 'object')
            node_name = SubElement(node_object, 'name')
            # if str(list_[4]) == "person":                # 根据条件筛选需要标注的标签,例如这里只标记person这类，不符合则直接跳过
            #     node_name.text = str(list_[4])
            # else:
            #     continue
            node_name.text = str(list_[4])
            node_pose = SubElement(node_object, 'pose')
            node_pose.text = '0'
            node_name.text = str(list_[4])
            node_truncated = SubElement(node_object, 'truncated')
            node_truncated.text = '0'
            node_name.text = str(list_[4])
            node_difficult = SubElement(node_object, 'difficult')
            node_difficult.text = '0'
            node_bndbox = SubElement(node_object, 'bndbox')
            node_xmin = SubElement(node_bndbox, 'xmin')
            node_xmin.text = str(list_[0])
            node_ymin = SubElement(node_bndbox, 'ymin')
            node_ymin.text = str(list_[1])
            node_xmax = SubElement(node_bndbox, 'xmax')
            node_xmax.text = str(list_[2])
            node_ymax = SubElement(node_bndbox, 'ymax')
            node_ymax.text = str(list_[3])

    xml = tostring(node_root, pretty_print=True)   # 格式化显示，该换行的换行

    file_name = list_images[3].split(".")[0]
    filename = xml_path+"/{}.xml".format(file_name)

    f = open(filename, "wb")
    f.write(xml)
    f.close()


if __name__ == '__main__':

    args = make_parser().parse_args()
    args.path = r"D:\model\YOLOX-main\datasets\VOCdevkit\VOC2007\fire_wb\JPEGImages" #图片路径
    xml_path = r"D:\model\YOLOX-main\datasets\VOCdevkit\VOC2007\fire_wb\Annotations"# xml标注保存路径
    if not os.path.exists(xml_path):
        os.makedirs(xml_path,exist_ok=True)
    args.conf=0.5
    args.nms=0.45
    args.tsize=640
    exp = exp.get_exp(args.exp_file, args.name)
    for name in os.listdir(args.path):
        print(name)
        image = cv2.imread(os.path.join(args.path,name))
        try:
            list_image = (image.shape[0],image.shape[1],image.shape[2],name)             # 图片的宽高等信息
        except:
            continue
        out_boxes= inference.main(exp, args,image)
        if isinstance(out_boxes, list):
            create_xml(out_boxes, list_image, xml_path)
        else:
            continue



             # 生成标注的xml文件