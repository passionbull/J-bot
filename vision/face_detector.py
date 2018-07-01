#!/usr/bin/env python3
import dlib

predictor_model =  'models/shape_predictor_68_face_landmarks.dat'
recognition_model = 'models/dlib_face_recognition_resnet_model_v1.dat'

# get face detector in dlib
detector = dlib.get_frontal_face_detector()
face_pose_predictor = dlib.shape_predictor(predictor_model)
face_recognition_model = dlib.face_recognition_model_v1(recognition_model)


import time
import picamera
import numpy as np
import cv2

image = None
print("start face detection")

# using raspberry camera
def camera_capture(width = 320, height =240):
    with picamera.PiCamera() as camera:
        camera.resolution = (width, height)
        camera.framerate = 24
        image = np.empty((height, width, 3), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image = cv2.flip(image, -1)
        return image

def save_image(image, path='image.jpg'):
    cv2.imwrite(path, image)

def main():
    old_faces = []
    while True:
        image = camera_capture()
        if image == None:
            break
        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        faces = detector(image, 1)
        if len(old_faces) < len(faces):
            old_faces = []
            for face in faces:
                tracker = dlib.correlation_tracker()
                tracker.start_track(image, face)
                old_faces.append(tracker)
        else:
            for i, tracker in enumerate(old_faces):
                quality = tracker.update(image)
                if quality > 7:
                    pos = tracker.get_position()
                    pos = dlib.rectangle(
                        int(pos.left()),
                        int(pos.top()),
                        int(pos.right()),
                        int(pos.bottom()),
                    )
                    cv2.rectangle(image, (pos.left(), pos.top()), (pos.right(), pos.bottom()),
                                  (100, 200, 100))
                    print("detect face")
                    cv2.imwrite("image.jpg", image)
                else:
                    old_faces.pop(i)

        # cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()

