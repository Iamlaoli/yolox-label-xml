import cv2

# 读取视频文件
video = cv2.VideoCapture(r'C:\Users\Admin\Desktop\video\frame\double_demo.mp4')

# 检查视频是否打开成功
if not video.isOpened():
    print("无法读取视频文件")
    exit()

# 获取视频的帧率和尺寸
fps = int(video.get(cv2.CAP_PROP_FPS))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 设置缩放后的尺寸
new_width = 640
new_height = 480

# 创建输出视频文件名
output_file = 'output_video.mp4'

# 使用循环逐帧处理视频
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (new_width, new_height))

while True:
    # 读取一帧
    ret, frame = video.read()

    # 如果读取失败，跳出循环
    if not ret:
        break

    # 将每一帧缩放并写入输出文件
    out.write(cv2.resize(frame, (new_width, new_height)))

# 释放视频资源并关闭窗口
video.release()
out.release()
cv2.destroyAllWindows()
