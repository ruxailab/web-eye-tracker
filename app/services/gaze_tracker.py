import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd
from pathlib import Path

def train_model(session_id):
    # Download dataset
    dataset_train_path = f'{Path().absolute()}\\public\\training\\{session_id}\\train_data.csv'
    dataset_session_path = f'{Path().absolute()}\\public\\sessions\\{session_id}\\session_data.csv'

    # Importing data from csv
    raw_dataset = pd.read_csv(dataset_train_path)
    session_dataset = pd.read_csv(dataset_session_path)

    train_stats = raw_dataset.describe()
    train_stats = train_stats.transpose()

    dataset = raw_dataset

    # Drop the columns that will be predicted
    X = dataset.drop(['mouse_x', 'mouse_y'], axis=1)

    Y1 = dataset.mouse_x
    Y2 = dataset.mouse_y
    print('Y1 is the mouse_x column ->', Y1)
    print('Y2 is the mouse_y column ->', Y2)

    MODEL_X = model_for_mouse_x(X, Y1)
    MODEL_Y = model_for_mouse_y(X, Y2)

    GAZE_X = MODEL_X.predict(session_dataset)
    GAZE_Y = MODEL_Y.predict(session_dataset)

    return {"x": GAZE_X,"y": GAZE_Y}


def model_for_mouse_x(X, Y1):
    print('-----------------MODEL FOR X------------------')
    # split dataset into train and test sets (80/20 where 20 is for test)
    X_train, X_test, Y1_train, Y1_test = train_test_split(X, Y1, test_size=0.2)
    X_train, X_test, Y1_train, Y1_test = train_test_split(X, Y1, test_size=0.2)

    model = linear_model.LinearRegression()
    model.fit(X_train, Y1_train)

    Y1_pred_train = model.predict(X_train)
    Y1_pred_test = model.predict(X_test)
    
    yintercept = model.intercept_
    left_iris_x = model.coef_[0]
    left_iris_y = model.coef_[1]
    right_iris_x = model.coef_[2]
    right_iris_y = model.coef_[3]
    print(f'MOUSE_X = {yintercept}')
    print(f'LEFT_IRIS_X = {left_iris_x}')
    print(f'LEFT_IRIS_y = {left_iris_y}')
    print(f'RIGHT_IRIS_X = {right_iris_x}')
    print(f'RIGHT_IRIS_Y = {right_iris_y}')

    print(f'TRAIN{Y1_pred_train}')
    print(f'TEST{Y1_pred_test}')
    return model

def model_for_mouse_y(X, Y2):
    print('-----------------MODEL FOR Y------------------')
     # split dataset into train and test sets (80/20 where 20 is for test)
    X_train, X_test, Y2_train, Y2_test = train_test_split(X, Y2, test_size=0.2)
    X_train, X_test, Y2_train, Y2_test = train_test_split(X, Y2, test_size=0.2)

    model = linear_model.LinearRegression()
    model.fit(X_train, Y2_train)

    Y2_pred_train = model.predict(X_train)
    Y2_pred_test = model.predict(X_test)
    
    yintercept = model.intercept_
    left_iris_x = model.coef_[0]
    left_iris_y = model.coef_[1]
    right_iris_x = model.coef_[2]
    right_iris_y = model.coef_[3]
    print(f'MOUSE_X = {yintercept}')
    print(f'LEFT_IRIS_X = {left_iris_x}')
    print(f'LEFT_IRIS_y = {left_iris_y}')
    print(f'RIGHT_IRIS_X = {right_iris_x}')
    print(f'RIGHT_IRIS_Y = {right_iris_y}')

    print(f'TRAIN{Y2_pred_train}')
    print(f'TEST{Y2_pred_test}')
    return model