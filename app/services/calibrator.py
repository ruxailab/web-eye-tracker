import cv2
from app.eye_tracker.gaze_tracking import GazeTracking
import csv
from pathlib import Path
import json

GAZE_POINTS = []

def start_calib(mouse_events_str, webcam_url, folder):
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(f'{Path().absolute()}\\public\\videos\\'+webcam_url)
    index = 0

    if (webcam.isOpened()== False):
          print("Error opening video stream or file")

    mouse_events = json.loads(mouse_events_str)
    print(f'lenght -> {len(mouse_events)}')
    
    while webcam.isOpened():
        # We get a new frame from the webcam
        ret, frame = webcam.read()

        if ret:
            cv2.namedWindow("calib", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(
                "calib", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            # We send this frame to GazeTracking to analyze it
            gaze.refresh(frame)

            frame = gaze.annotated_frame()

            left_pupil = gaze.pupil_left_coords()

            # save calib points
            left_eye = gaze.eye_left
            cv2.imwrite(f'./training/{folder}/eyes/eye'+str(index)+'.jpg',left_eye.frame)
            add_gaze_point(left_pupil, 'eye'+str(index)+'.jpg', mouse_events[index])
            index+=1
        else:
            break
    webcam.release()
    
    # create csv with the relation between the mouse position and pupil
    gen_train_dataset(folder)
    return

def add_gaze_point(left_pupil, img, gaze_point):
    if(left_pupil is not None):
        left_pupil = {
            "pupil_x" : left_pupil[0],
            "pupil_y" : left_pupil[1],
            "img": img,
            "mouse_x": gaze_point['x'],
            "mouse_y": gaze_point['y'],
        }

        GAZE_POINTS.append(left_pupil)

def gen_train_dataset(folder):
    csv_file = f'./public/training/{folder}/train_data.csv'
    csv_columns = ['pupil_x','pupil_y','img', 'mouse_x', 'mouse_y']
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in GAZE_POINTS:
                writer.writerow(data)
    except IOError:
        print("I/O error")
