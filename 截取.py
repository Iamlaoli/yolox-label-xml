import cv2

# 打开视频文件
video_in = cv2.VideoCapture('D:\model\yolox-label-xml-main\input1.mp4')

# 检查视频是否成功打开
if not video_in.isOpened():
    print('Error: Could not open the video.')
    exit()

# 获取视频的宽度和高度
video_width = int(video_in.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(video_in.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 设置要截取的区域 (例如: 左上角 (50, 50), 右下角 (200, 200))
x1, y1, x2, y2 = 114, 118, 750,560

# 创建一个新的视频写入对象
# video_out = cv2.VideoWriter('output.mp4', video_in.get(cv2.CAP_PROP_FOURCC), video_in.get(cv2.CAP_PROP_FPS),
#                            (x2 - x1, y2 - y1))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 选择视频编解码器
video_out = cv2.VideoWriter('output.mp4', fourcc, 30, (x2 - x1, y2 - y1))  # 30 是帧率，可以根据需要调整
# 循环读取视频的每一帧
while True:
    ret, frame = video_in.read()

    # 如果读取成功，ret 为 True
    if not ret:
        break

        # 截取指定区域的视频帧
    frame = frame[y1:y2, x1:x2]
    cv2.imshow("frame",frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

        # 将截取的区域写入新的视频文件
    video_out.write(frame)

# 释放视频资源
video_in.release()
video_out.release()