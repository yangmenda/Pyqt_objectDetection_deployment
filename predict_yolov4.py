
#coding=utf-8 



import cv2

from PIL import Image

import os
from detect.yolov4 import YOLO

def Predict_v4(path_in,mode):


    
    yolo=YOLO()

    
    

    
    if mode==1:
        image = Image.open(path_in)

        dir_save_path="./result"
        r_image,numbers = yolo.detect_image(image,count_indecies=True)

        addr2="predict.jpg"
        path_result=os.path.join(dir_save_path, addr2)
        r_image.save(path_result)

        return path_result,numbers
    if mode==3:


        from tqdm import tqdm
        save_path="./result/dir"
        img_names = os.listdir(path_in)
        for img_name in tqdm(img_names):
            if img_name.lower().endswith(
                    ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                image_path = os.path.join(path_in, img_name)
                image = Image.open(image_path)

                r_image = yolo.detect_image(image,count_indecies=False)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                r_image.save(os.path.join(save_path, img_name), quality=95, subsampling=0)
        return save_path

        
   
            
            

    

    
	

