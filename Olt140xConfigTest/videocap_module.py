# encoding:utf-8 
import time 
import threading 
# from cv2 
import cv2 
import numpy as np 
from PIL import ImageGrab 

class VideoCapThread(threading.Thread): 
    def __init__(self, video_file='record.mp4'): 
        threading.Thread.__init__(self) 
        self.b_record = True 
        self.video = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'),
                                      32, ImageGrab.grab().size) # 幀率為32，可以調節 
        
    def run(self): 
        while self.b_record: 
            im = ImageGrab.grab() 
            imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR) 
            self.video.write(imm) 
        self.video.release() 
        cv2.destroyAllWindows() 
            
    def stop_record(self): 
        self.b_record = False 
        
if __name__ == "__main__": 
    avi_file = 'data/avi_tmp.avi' 
    t1 = VideoCapThread(avi_file) 
    t1.start() 
    time.sleep(10) # 錄製10s 
    t1.stop_record()

# example use:
# avi_file = 'data_tmp2.mp4'
# t1 = videocap.VideoCapThread(avi_file)
# t1.start()

# time.sleep(3)

# t1.stop_record() 