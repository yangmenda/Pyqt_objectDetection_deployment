import cv2

def get_info(path):
    src=cv2.imread(path)
    img_shape=src.shape
    width=img_shape[1]
    height=img_shape[0]
    channels=img_shape[2]
    width_s=str(width)
    height_s=str(height)
    channels_s=str(channels)
    return width_s,height_s,channels_s