#!/usr/bin/env -S python 2>/dev/null

__version__ = '0.1'
__author__ = 'Tomáš Jirsa'
__copyright__ = 'Copyright (C) 2021 Tomáš Jirsa'

from multiprocessing import Process
import os
from time import time

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ

import shutup
import cv2
from mtcnn import MTCNN
import tensorflow as tf

from watcher import Watcher

shutup.please()
tf.get_logger().setLevel('ERROR')
#tf.logging.set_verbosity(tf.logging.ERROR)
HAARS = [cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml')]

GRAY = (127,127,127)
HAAR = (0,255,255)
MT = (0,102,255)
FPS = 10

def process_vid(vid,name,watcher):
    detector = MTCNN()
    save = watcher.watch_vid(vid,FPS,detector)
    if save:
        frameSize = vid[0].shape[:2]
        shape = vid[0].shape
        writer = cv2.VideoWriter(f'vids/{name}.avi',cv2.VideoWriter_fourcc(*'XVID'),FPS,frameSize)
        for frame in vid:
            assert frame.shape == shape
            writer.write(frame)
        writer.release()



if __name__ == '__main__':
    try:
        os.mkdir('vids')
    except FileExistsError:
        pass

    cam_i = 0
    known_cam_i = [0]
    cam = cv2.VideoCapture(cam_i)
    font = cv2.FONT_HERSHEY_COMPLEX
    text = ''
    while True:
        ret, frame = cam.read()
        if not ret:
            cam.release()
            cam_i = 0
            cam = cv2.VideoCapture(cam_i)
            if 'errors' in locals():
                errors += 1 
            else:
                errors = 0
            if errors > 3:
                exit('Is camera connected?')
        else:
            cv2.putText(
                frame,
                f'Camera {cam_i}',
                (15, 25),
                font,
                1,(255,0,0)
            )
            cv2.putText(
                frame,
                f'd to select next, a to select previous, s to save',
                (15, frame.shape[0] - 25),
                font,
                0.5,(255,0,0)
            )
            if text != '':
                cv2.putText(
                    frame,
                    text,
                    (15, int(frame.shape[0] / 2)),
                    font,
                    1,(0,0,255)
                )

            cv2.imshow(f'Camera {cam_i}', frame)


            key = cv2.waitKey(1)
            if key == ord('q'):
                cam.release()
                cv2.destroyAllWindows()
                exit("quited")
            elif key == ord('d') or key == ord('a'):
                cv2.destroyAllWindows()
                if key == ord('a'):
                    if cam_i == known_cam_i[0]:
                        text = 'First camera'
                    else:
                        cam_i = known_cam_i[known_cam_i.index(cam_i) - 1]
                if key == ord('d'):
                    if not cam_i == known_cam_i[-1]:
                        cam_i = known_cam_i[known_cam_i.index(cam_i) + 1]
                    else:
                        i = 0
                        while i < 5:
                            cam_i += 1
                            nextcam = cv2.VideoCapture(cam_i)
                            if nextcam.isOpened():
                                ret, _ = nextcam.read()
                            else:
                                ret = True
                            if not ret and nextcam.isOpened():
                                nextcam.release()
                                known_cam_i.append(cam_i)
                                cam.release()
                                cam = cv2.VideoCapture(cam_i)
                                break
                            else:
                                cam_i += 1
                                i += 1
                        text ='No other cameras'
                        cam_i=known_cam_i[-1]
            elif key == ord('s'):
                break

    freq = 0.5
    watcher = Watcher(freq)
    detector = MTCNN()
    while True:
        ret, frame = cam.read()
        if not ret:
            print('Problem with camera, setting to default camera (0)')
            cam.release()
            cam_i = 0
            cam = cv2.VideoCapture(cam_i)
            if 'errors' in locals():
                errors += 1 
            else:
                errors = 0
            if errors > 3:
                exit('Is camera connected?')
        else:
            cv2.putText(
                frame,
                f'Camera {cam_i}',
                (15, 25),
                font,
                1,
                (255,0,0)
            )
            cv2.putText(
                frame,
                f'h to select Haar cascades',
                (15, frame.shape[0] - 50),
                font,
                0.5,
                HAAR if watcher.h else GRAY
            )
            cv2.putText(
                frame,
                f'm to select MTCNN, j to incr. freq., k to decer., {watcher.freq} Hz)',
                (15, frame.shape[0] - 25),
                font,
                0.5,
                MT if watcher.m else GRAY
            )
            cv2.putText(
                frame,
                f's to save',
                (15, frame.shape[0] - 75),
                font,
                0.5,(255,0,0)
            )
            _,frame = watcher.find_face(frame,detector)
            cv2.imshow(f'Camera {cam_i}', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                cam.release()
                cv2.destroyAllWindows()
                exit('quited')
            if key == ord('h'):
                watcher.h = not watcher.h
            if key == ord('m'):
                watcher.m = not watcher.m
            if key == ord('j'):
                watcher.freq = watcher.freq * 2
            if key == ord('k'):
                watcher.freq = watcher.freq / 2
            if key == ord('s'):
                break
    cv2.destroyAllWindows()
    while True:
        length = input('Window length [s]:')
        try:
            length = int(length)
            break
        except:
            print("Can't parse this")

    cam.set(cv2.CAP_PROP_FPS,FPS)
    print("Starting infinite cycle, terminate with ctrl-c")
    current_vid = []
    p = []
    try:
        while True:
            _,frame = cam.read()
            current_vid.append(frame)
            if len(current_vid) == length*FPS:
                p.append(Process(target=process_vid, args=(current_vid,round(time()-length),watcher)))
                p[-1].start()
                current_vid = []
    except KeyboardInterrupt:
        for pi in p:
            pi.join()
        cam.release()





    
    


