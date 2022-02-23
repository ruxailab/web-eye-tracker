import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
from pathlib import Path


def train_model(session_id):
    # Download dataset
    dataset_train_path = f'{Path().absolute()}/public/training/{session_id}/train_data.csv'
    dataset_session_path = f'{Path().absolute()}/public/sessions/{session_id}/session_data.csv'

    # Importing data from csv
    raw_dataset = pd.read_csv(dataset_train_path)
    session_dataset = pd.read_csv(dataset_session_path)

    train_stats = raw_dataset.describe()
    train_stats = train_stats.transpose()

    dataset = raw_dataset

    # Delete columns that won't be used in model
    moment_in_time_col = session_dataset.pop('moment_in_time')
    print(moment_in_time_col)
    MOMENT_IN_TIME = moment_in_time_col.values

    # Drop the columns that will be predicted
    X = dataset.drop(['mouse_x', 'mouse_y'], axis=1)

    Y1 = dataset.mouse_x
    Y2 = dataset.mouse_y
    # print('Y1 is the mouse_x column ->', Y1)
    # print('Y2 is the mouse_y column ->', Y2)

    MODEL_X = model_for_mouse_x(X, Y1)
    MODEL_Y = model_for_mouse_y(X, Y2)

    GAZE_X = MODEL_X.predict(session_dataset)
    GAZE_Y = MODEL_Y.predict(session_dataset)

    GAZE_X = np.abs(GAZE_X)
    GAZE_Y = np.abs(GAZE_Y)

    return {"x": GAZE_X, "y": GAZE_Y, "moment_in_time": MOMENT_IN_TIME}


def model_for_mouse_x(X, Y1):
    print('-----------------MODEL FOR X------------------')
    # split dataset into train and test sets (80/20 where 20 is for test)
    X_train, X_test, Y1_train, Y1_test = train_test_split(X, Y1, test_size=0.2)

    model = linear_model.LinearRegression()
    model.fit(X_train, Y1_train)

    Y1_pred_train = model.predict(X_train)
    Y1_pred_test = model.predict(X_test)

    Y1_test = normalizeData(Y1_test)
    Y1_pred_test = normalizeData(Y1_pred_test)

    print(
        f'Mean squared error MSE = {mean_squared_error(Y1_test, Y1_pred_test)}')
    print(f'MODEL X SCORE R2 = {model.score(X, Y1)}')

    # print(f'TRAIN{Y1_pred_train}')
    # print(f'TEST{Y1_pred_test}')
    return model


def model_for_mouse_y(X, Y2):
    print('-----------------MODEL FOR Y------------------')
    # split dataset into train and test sets (80/20 where 20 is for test)
    X_train, X_test, Y2_train, Y2_test = train_test_split(X, Y2, test_size=0.2)

    model = linear_model.LinearRegression()
    model.fit(X_train, Y2_train)

    Y2_pred_train = model.predict(X_train)
    Y2_pred_test = model.predict(X_test)

    Y2_test = normalizeData(Y2_test)
    Y2_pred_test = normalizeData(Y2_pred_test)

    print(
        f'Mean squared error MSE = {mean_squared_error(Y2_test, Y2_pred_test)}')
    print(f'MODEL Y SCORE R2 = {model.score(X, Y2)}')

    # print(f'TRAIN{Y2_pred_train}')
    # print(f'TEST{Y2_pred_test}')
    return model


def normalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
