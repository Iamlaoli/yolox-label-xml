#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.
import os
import time
from loguru import logger
import cv2
# https://blog.csdn.net/ssunshining/article/details/125031735
import torch
import sys
sys.path.append(r"../YOLOX-main")
from yolox.data.datasets import VOC_CLASSES
from yolox.data.data_augment import ValTransform
from yolox.data.datasets import COCO_CLASSES
from yolox.exp import get_exp
from yolox.utils import fuse_model, get_model_info, postprocess, vis
from PyQt5 import QtCore, QtGui, QtWidgets
IMAGE_EXT = [".jpg", ".jpeg", ".webp", ".bmp", ".png"]
def get_image_list(path):
    image_names = []
    for maindir, subdir, file_name_list in os.walk(path):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            ext = os.path.splitext(apath)[1]
            if ext in IMAGE_EXT:
                image_names.append(apath)
    return image_names

class Predictor(object):
    def __init__(
        self,
        model,
        exp,
        cls_names=VOC_CLASSES,
        trt_file=None,
        decoder=None,
        device="cpu",
        fp16=False,
        legacy=False,
        classes=None
    ):
        self.model = model
        self.cls_names = cls_names
        self.decoder = decoder
        self.num_classes = exp.num_classes
        self.confthre = exp.test_conf
        self.nmsthre = exp.nmsthre
        self.test_size = exp.test_size
        self.device = device
        self.fp16 = fp16
        self.preproc = ValTransform(legacy=legacy)
        self.classes=classes
        if trt_file is not None:
            from torch2trt import TRTModule

            model_trt = TRTModule()
            model_trt.load_state_dict(torch.load(trt_file))

            x = torch.ones(1, 3, exp.test_size[0], exp.test_size[1]).cuda()
            self.model(x)
            self.model = model_trt

    def inference(self, img):
        img_info = {"id": 0}
        if isinstance(img, str):
            img_info["file_name"] = os.path.basename(img)
            img = cv2.imread(img)
        else:
            img_info["file_name"] = None

        height, width = img.shape[:2]
        img_info["height"] = height
        img_info["width"] = width
        img_info["raw_img"] = img

        ratio = min(self.test_size[0] / img.shape[0], self.test_size[1] / img.shape[1])
        img_info["ratio"] = ratio

        img, _ = self.preproc(img, None, self.test_size)
        img = torch.from_numpy(img).unsqueeze(0)
        img = img.float()
        if self.device == "gpu":
            img = img.cuda()
            if self.fp16:
                img = img.half()  # to FP16
        with torch.no_grad():
            t0 = time.time()
            outputs = self.model(img)
            if self.decoder is not None:
                outputs = self.decoder(outputs, dtype=outputs.type())
            outputs = postprocess(
                outputs, self.num_classes, self.confthre,
                self.nmsthre, class_agnostic=True
            )
        return outputs, img_info
    def visual(self, output, img_info, cls_conf=0.35):
        ratio = img_info["ratio"]
        img = img_info["raw_img"]
        if output is None:
            return img
        output = output.cpu()

        bboxes = output[:, 0:4]

        # preprocessing: resize
        bboxes /= ratio

        cls = output[:, 6]
        # print(output.shape)
        scores = output[:, 4] * output[:, 5]

        vis_res,out_boxes = vis(img, bboxes, scores, cls, cls_conf,self.cls_names,self.classes)
        return out_boxes

def image_demo(predictor, vis_folder, image_name, current_time, save_result):

    outputs, img_info = predictor.inference(image_name)
    out_boxes= predictor.visual(outputs[0], img_info, predictor.confthre)
    return  out_boxes

def imageflow_demo(predictor, vis_folder, current_time, args,label_show_camera,close,c_text):
    if args.camid =='0':
        args.camid=0
    cap = cv2.VideoCapture(args.path if args.demo == "video" else args.camid)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    fps = cap.get(cv2.CAP_PROP_FPS)
    if args.save_result:
        save_folder = os.path.join(
            vis_folder, time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
        )
        os.makedirs(save_folder, exist_ok=True)
        # if args.demo == "video":
        #     save_path = os.path.join(save_folder, os.path.basename(args.path))
        # else:
        save_path =os.path.join(save_folder, "camara{}.mp4".format(args.index))
        # logger.info(f"video save_path is {save_path}")
        vid_writer = cv2.VideoWriter(
            save_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (int(width), int(height))
        )
    i=0
    while True:
        ret_val, frame = cap.read()
        i+=1
        if ret_val:
            if close is None:
                break
            if c_text =="关闭相机":
                break
            if i%5==0:
                outputs, img_info = predictor.inference(frame)
                result_frame = predictor.visual(outputs[0], img_info, predictor.confthre)
                # cv2.imshow("{}".format(args.index), result_frame)
                time1 = time.time()
                out_path = args.img_save_path
                if not os.path.exists(out_path):
                    os.makedirs(out_path)
                if outputs != [None]:
                    fileMame = str(time1) + ".jpg"
                    cv2.imwrite(out_path + "/" + fileMame, result_frame)
                if args.save_result:
                    vid_writer.write(result_frame)

                show = cv2.resize(result_frame, (300, 300))  # 把读到的帧的大小重新设置为 640x480
                show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
                showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
                QtWidgets.QApplication.processEvents()
                label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
                # del result_frame
            # else:
            #     show = cv2.resize(frame, (500, 500))  # 把读到的帧的大小重新设置为 640x480
            #     show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
            #     showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
            #                              QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            #     QtWidgets.QApplication.processEvents()
            #     label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
            #     del frame
                # cv2.imshow("{}".format(args.index),frame)
            # cv2.imshow("{}".format(args.index), frame)
            # fps = cam.cap.get(cv2.CAP_PROP_FPS)
            # time.sleep(1 / fps)  # fps = 20hz
            cv2.waitKey(1)
            # if ch == 27 or ch == ord("q") or ch == ord("Q"):
            #     break
        # else:
        #     break


def main(exp, args,image):
    if not args.experiment_name:
        args.experiment_name = exp.exp_name
    file_name = os.path.join(exp.output_dir, args.experiment_name)
    os.makedirs(file_name, exist_ok=True)
    vis_folder = None
    if args.trt:
        args.device = "gpu"
    if args.conf is not None:
        exp.test_conf = args.conf
    if args.nms is not None:
        exp.nmsthre = args.nms
    if args.tsize is not None:
        exp.test_size = (args.tsize, args.tsize)
    model = exp.get_model()
    if args.device == "gpu":
        model.cuda()
        if args.fp16:
            model.half()  # to FP16
    model.eval()

    if not args.trt:
        if args.ckpt is None:
            ckpt_file = os.path.join(file_name, "best_ckpt.pth")
        else:
            ckpt_file = args.ckpt
        ckpt = torch.load(ckpt_file, map_location="cpu")
        # load the model state dict
        model.load_state_dict(ckpt["model"])

    if args.fuse:
        model = fuse_model(model)

    if args.trt:
        assert not args.fuse, "TensorRT model is not support model fusing!"
        trt_file = os.path.join(file_name, "model_trt.pth")
        assert os.path.exists(
            trt_file
        ), "TensorRT model is not found!\n Run python3 tools/trt.py first!"
        model.head.decode_in_inference = False
        decoder = model.head.decode_outputs
    else:
        trt_file = None
        decoder = None

    predictor = Predictor(
        model, exp, VOC_CLASSES, trt_file, decoder,
        args.device, args.fp16, args.legacy,args.classes
    )
    current_time = time.localtime()
    out_boxes=image_demo(predictor, vis_folder, image, current_time, args.save_result)
    return  out_boxes