#!/usr/bin/env python3
import picamera
import numpy as np
import cv2


# using raspberry camera
def capture(width = 320, height =240):
    with picamera.PiCamera() as camera:
        camera.resolution = (width, height)
        camera.framerate = 24
        image = np.empty((height, width, 3), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image = cv2.flip(image, -1)
        return image

def save_image(image, path='image.jpg'):
    cv2.imwrite(path, image)