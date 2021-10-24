import cv2
import numpy as np
import dlib  # Documentation: http://dlib.net/
from math import hypot
import sys
from pathlib import Path

frame = font = None
array_of_positions = []

def setup():
    cap = cv2.VideoCapture(f'{Path().absolute()}/resources/video.mp4')
    # Uses dlib get frontal face detector algorithym
    detector = dlib.get_frontal_face_detector()
    # Gets the shape predictor model
    predictor = dlib.shape_predictor(f'{Path().absolute()}/resources/shape_predictor_68_face_landmarks.dat')
    # font = cv2.FONT_HERSHEY_SIMPLEX
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # change it to grayscale

            # array of detected faces from the frame using the dlib frontal face detector
            faces = detector(gray)

            for face in faces:
                # gets all the landmarks position from the current face that is being analysed
                landmarks = predictor(gray, face)

                # left eye
                left_eye_left_point, left_eye_right_point, left_eye_top_point, left_eye_bottom_point = draw_lines(
                    landmarks, (36, 39, 37, 38, 41, 40))
                left_eye_blinking_ratio = get_blinking_ratio(
                    left_eye_top_point, left_eye_bottom_point, left_eye_left_point, left_eye_right_point)

                # right eye
                right_eye_left_point, right_eye_right_point, right_eye_top_point, right_eye_bottom_point = draw_lines(
                    landmarks, (42, 45, 43, 44, 47, 46))
                right_eye_blinking_ratio = get_blinking_ratio(
                    right_eye_top_point, right_eye_bottom_point, right_eye_left_point, right_eye_right_point)

                # average of blinking ratio to check if person blinked
                is_bliking((left_eye_blinking_ratio + right_eye_blinking_ratio) / 2)

                # gaze detection
                # left eye
                left_eye_gaze_ratio = get_gaze_ratio(
                    landmarks, (36, 37, 38, 39, 40, 41), frame, gray)

                # right eye
                right_eye_gaze_ratio = get_gaze_ratio(
                    landmarks, (42, 45, 43, 44, 47, 46), frame, gray)

                gaze_ratio = (left_eye_gaze_ratio + right_eye_gaze_ratio)/2
                direction = predict_gaze_direction(gaze_ratio)

                # create frame with colors just to help recognize if we got the correct color
                new_frame = np.zeros((500, 500, 3), np.uint8)
                if direction == 'LEFT':
                    array_of_positions.append('left')
                elif direction == 'RIGHT':
                    array_of_positions.append('right')
                else:
                    array_of_positions.append('center')
        else:
            break
          
    cap.release()
    cv2.destroyAllWindows()
    return array_of_positions


def midpoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)


def draw_lines(landmarks, eye_points):
    # draws horizontal and vertical lines on top of the eye to find the center
    left_point = (landmarks.part(
        eye_points[0]).x, landmarks.part(eye_points[0]).y)
    right_point = (landmarks.part(
        eye_points[1]).x, landmarks.part(eye_points[1]).y)

    top_point_middle = midpoint(landmarks.part(
        eye_points[2]), landmarks.part(eye_points[3]))
    bottom_point_middle = midpoint(landmarks.part(
        eye_points[4]), landmarks.part(eye_points[5]))

    return left_point, right_point, top_point_middle, bottom_point_middle


def get_blinking_ratio(top_point_middle, bottom_point_middle, left_point, right_point):
    # discover if eye is blinking by using the lenght of lines and euclidian distance
    vertical_line_length = hypot(
        (top_point_middle[0] - bottom_point_middle[0]), (top_point_middle[1] - bottom_point_middle[1]))
    horizontal_line_length = hypot(
        (left_point[0] - right_point[0]), (left_point[1] - right_point[1]))

    return horizontal_line_length / vertical_line_length


def is_bliking(ratio):
    # usually blinking happends when ratio is more than 6, but it can depend on the eye
    if ratio > 6:
        cv2.putText(frame, "BLINKING", (200, 100), font, 1, (255, 0, 0), 2)
        return True
    return False


def get_gaze_ratio(landmarks, eye_points, frame, gray):
    # region of the eye
    eye_region = np.array([
        (landmarks.part(eye_points[0]).x, landmarks.part(eye_points[0]).y),
        (landmarks.part(eye_points[1]).x, landmarks.part(eye_points[1]).y),
        (landmarks.part(eye_points[2]).x, landmarks.part(eye_points[2]).y),
        (landmarks.part(eye_points[3]).x, landmarks.part(eye_points[3]).y),
        (landmarks.part(eye_points[4]).x, landmarks.part(eye_points[4]).y),
        (landmarks.part(eye_points[5]).x, landmarks.part(eye_points[5]).y),
    ], np.int32)

    heigth, width, _ = frame.shape  # get the dimension of the current frame
    # a black screen of the same size of the frame
    mask = np.zeros((heigth, width), np.uint8)
    cv2.polylines(mask, [eye_region], True, (0, 0, 255), 2)
    cv2.fillPoly(mask, [eye_region], 255)

    # extract the gray eye and process it on the mask
    eye_frame = cv2.bitwise_and(gray, gray, mask=mask)

    # defines the maximum and minimum x and y points around the eye
    min_x = np.min(eye_region[:, 0])
    max_x = np.max(eye_region[:, 0])
    min_y = np.min(eye_region[:, 1])
    max_y = np.max(eye_region[:, 1])

    # extract the points exactly where the minimun and maximum regions
    gray_eye = eye_frame[min_y: max_y, min_x: max_x]

    # creates a threshold to separate the iris and pupil from the white part of the eye
    _, threshold_eye = cv2.threshold(
        gray_eye, 70, 255, cv2.THRESH_BINARY)  # 255 means we are talking about the white part, and 70 I don't know what it is
    heigth, width = threshold_eye.shape

    # check out the the non zeros on both sides of the eye, so we can discover where there are the white points
    left_side_threshold = threshold_eye[0:heigth, 0:int(width/2)]
    left_side_white = cv2.countNonZero(left_side_threshold)

    right_side_threshold = threshold_eye[0:heigth, int(width/2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    try:
        gaze_ratio = left_side_white/right_side_white
    except ZeroDivisionError:
        gaze_ratio = 0

    return gaze_ratio


def predict_gaze_direction(gaze_ratio):
    if gaze_ratio >= 1:
        return 'LEFT'
    elif gaze_ratio <= 0.5:
        return 'RIGHT'
    else:
        return 'CENTER'
