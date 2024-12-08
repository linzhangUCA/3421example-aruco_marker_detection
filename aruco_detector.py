import cv2 as cv
from picamera2 import Picamera2
import numpy as np

# SETUP
cam = Picamera2()
config = cam.create_still_configuration(
    main={"format": 'RGB888', "size": (400, 300)}, 
    controls={"FrameDurationLimits": (50000, 50000)},
)
cam.configure(config)
cam.start()
aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_50) # aruco dictionary
aruco_params = cv.aruco.DetectorParameters_create()

# LOOP
while True:
    im = cam.capture_array()
    # im_resize = cv.resize(im_rgb, (400, 300))
    corners, ids, reject_candidates = cv.aruco.detectMarkers(
        # im_resize,
        im,
        aruco_dict,
        parameters=aruco_params,
    )
    if ids is not None:  # if marker is detected
        top_left_coords = corners[0][0][0].astype(int)
        bot_right_coords = corners[0][0][2].astype(int)
        im = cv.rectangle(im, top_left_coords, bot_right_coords, (0, 255, 0), 2)
    cv.imshow("Camera", im)
    if cv.waitKey(1) == ord('q'):  # press q to exit
        break
cv.destroyAllWindows()
