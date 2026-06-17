import cv2
import numpy as np
import pyautogui
import time

# 设置录制的屏幕尺寸和帧率
screen_size = (1920, 1080)
fps = 30.0

# 设置录制的时长（单位：秒）
record_duration = 10

# 创建 VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*"XVID")
output = cv2.VideoWriter("screen_record.avi", fourcc, fps, screen_size)

start_time = time.time()
end_time = start_time + record_duration

while time.time() < end_time:
    # 截取屏幕图像
    img = pyautogui.screenshot()
    
    # 将图像转换为OpenCV格式
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 写入视频文件
    output.write(frame)
    
    # 显示录制的屏幕图像
    cv2.imshow("Screen Recording", frame)
    
    # 按下 'q' 键退出循环
    if cv2.waitKey(1) == ord('q'):
        break

# 释放资源
output.release()
cv2.destroyAllWindows()
