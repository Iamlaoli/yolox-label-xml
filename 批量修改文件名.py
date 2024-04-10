import os.path
import shutil
num = 0 #修改文件名的数量词

#保存图片模块
def moveFiles(path, disdir):  # path为原始路径，disdir是移动的目标目录

    dirlist = os.listdir(path)
    for i in dirlist:
        child = os.path.join('%s/%s' % (path, i))
        if os.path.isfile(child):
            imagename, jpg = os.path.splitext(i)  # 分开文件名和后缀
            shutil.copy(child, os.path.join(disdir, imagename + ".jpg"))#保存格式自己设置
            # 复制后改为原来图片名称
            # 也可以用shutil.move()
            continue
        moveFiles(child, disdir)
#重命名模块
def rename(img_folder):
    for img_name in os.listdir(img_folder):  # os.listdir()： 列出路径下所有的文件
        #os.path.join() 拼接文件路径
        global num
        src = os.path.join(img_folder, img_name)   #src：要修改的目录名
        # dst = os.path.join(img_folder, "J01_" +str(num) + '.jpg') #dst： 修改后的目录名      注意此处str(num)将num转化为字符串,继而拼接
        dst = os.path.join(img_folder, "no_phone_"+str(num)+".jpg") #dst： 修改后的目录名      注意此处str(num)将num转化为字符串,继而拼接
        num= num+1
        os.rename(src, dst) #用dst替代src


def main():
    # for i in range(1,3):
        #要修改文件名的路径
        # img_folder0 = r'F:\model\YOLOX-main\datasets\VOCdevkit\VOC2007\JPEGImages' #图片的文件夹路径    直接放你的文件夹路径即可
    img_folder0 = r'D:\datasets\sign\JPEGImages' #图片的文件夹路径    直接放你的文件夹路径即可
    rename(img_folder0)

        # #保存图片代码
        # disdir = r'F:\model\YOLOX-main\datasets\VOCdevkit\VOC2007\res'  # 移动到目标文件夹
        # moveFiles(img_folder0, disdir)

if __name__=="__main__":
    main()