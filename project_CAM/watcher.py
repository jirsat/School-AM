from time import time

import cv2


class Watcher:
    def __init__(
        self,
        freq = 1,
        HAAR = (0,255,255),
        MT = (0,102,255),
        downscale = 1/2,
    ):
        self._HAAR = HAAR
        self._MT = MT
        self.downscale = downscale
        self.freq = freq
        self._mtcache = None
        self._last_time = 0
        self.h = False
        self.m = False

    def _find_face_haar(self, frame):
        HAARS = [cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml')]
        for c in HAARS:
            d = c.detectMultiScale(
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            )
            found = (len(d) != 0)
            if found:
                for (x, y, w, h) in d:
                    cv2.rectangle(
                        frame, (x, y), (x+w, y+h),
                        self._HAAR, 2
                    )
        return found, frame

    def _find_face_mtcnn(self, image,detector, selected = False):
        found = False
        if time()-self._last_time >= 1/self.freq or selected:
            image_det = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_det = cv2.resize(image_det, None, fx=self.downscale, fy=self.downscale)
            self._mtcache = detector.detect_faces(image_det)
            self._last_time = time()
        for face in self._mtcache:
            if face['confidence'] > 0.8:
                x, y, w, h = [int(i / self.downscale) for i in face['box']]

                found = True
                cv2.rectangle(
                    image, (x, y), (x+w, y+h),
                    self._MT, 2
                )
        return found, image

    def find_face(self, image, detector):
        if self.h:
            found_h, image = self._find_face_haar(image)
        else:
            found_h = False

        if self.m:
            found_m, image = self._find_face_mtcnn(image,detector)
        else:
            found_m = False

        found = found_h or found_m

        return found, image

    def watch_vid(self,vid,fps,detector):
        save = False
        for i in range(len(vid)):
            image = vid[i]
            if self.h:
                found_h, image = self._find_face_haar(image)
            else:
                found_h = False
            T = fps/self.freq
            selected = i % T == 0
            if self.m and selected:
                found_m, image = self._find_face_mtcnn(image,detector,selected)
            else:
                found_m = False
            save = save or found_m or found_h
            if save:
                return True
        return False

        