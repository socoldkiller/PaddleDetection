
import requests
from PIL import Image
from io import BytesIO
import base64
import httpx
import datetime
import sys

URL ="http://127.0.0.1"

def format(n):
     return float("%.2f" % n)


def frame2base64(frame):
    img = Image.fromarray(frame) #将每一帧转为Image
    output_buffer = BytesIO() #创建一个BytesIO
    img.save(output_buffer, format='JPEG') #写入output_buffer
    byte_data = output_buffer.getvalue() #在内存中读取
    base64_data = base64.b64encode(byte_data) #转为BASE64
    return base64_data


class FightWebHook:
    
    def get_rtsp_or_file_video(self):
        argv = sys.argv
        if "--video_file" in argv:
            idx =  argv.index('--video_file')
        elif "--rtsp" in argv:
            idx =  argv.index('--rtsp')
        else:
            assert "video_file or rtsp stream not found"
        
        return argv[idx+1]
    
        
    def __init__(self,endpoint:str) -> None:
        self.endpoint  = endpoint
        self.file_name = self.get_rtsp_or_file_video()
        
    
    def push(self,frame,video_action_score,mot_boxes):
        pictures = frame2base64(frame)
        people = []
        for mot_box in mot_boxes:
            p = {
                "class_id":format(mot_box[1]),
                "score":format(mot_box[2]),
                "x":format(mot_box[3]),
                "y":format(mot_box[4]),
                "w":format(mot_box[5]),
                "h":format(mot_box[6]),
                
            }
            people.append(p)
                
        data = {
            "date":datetime.datetime.now().strftime('%d:%m:%Y %H:%M:%S'),
            "fight_action_score":format(video_action_score),
            "people":people,
            "fight_pictures":pictures,
            "file_name":self.file_name
        }
    
        try:
            res = httpx.post(URL,json=data)
            return res.json()
        except Exception as e:
            return {
                "code":500,
                "data":data,
                "error":e,
                "endpoint":self.endpoint
        } 
        
          
fight_hook = FightWebHook(endpoint=URL)