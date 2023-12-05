from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_squared_log_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from pathlib import Path
import pandas as pd
import numpy as np


def predict(data):

    df = pd.read_csv(data)
    df = df.drop(['screen_height', 'screen_width'], axis=1)

    X_x = df[['left_iris_x', 'right_iris_x']]
    y_x = df['point_x']

    sc = StandardScaler()
    X_x = sc.fit_transform(X_x)

    X_train_x, X_test_x, y_train_x, y_test_x = train_test_split(
        X_x, y_x, test_size=0.2, random_state=42)

    model_x = linear_model.LinearRegression()
    model_x.fit(X_train_x, y_train_x)
    y_pred_x = model_x.predict(X_test_x)

    X_y = df[['left_iris_y', 'right_iris_y']]
    y_y = df['point_y']

    sc = StandardScaler()
    X_y = sc.fit_transform(X_y)

    X_train_y, X_test_y, y_train_y, y_test_y = train_test_split(
        X_y, y_y, test_size=0.2, random_state=42)

    model = linear_model.LinearRegression()
    model.fit(X_train_y, y_train_y)
    y_pred_y = model.predict(X_test_y)

    y_test_x = np.array(y_test_x)
    y_test_y = np.array(y_test_y)

    true_points = [(y_test_x[i], y_test_y[i]) for i in range(len(y_test_x))]

    error_range = 0.05

    data = {}

    for true_x, true_y in true_points:

        x_within_range = [y_pred_x[j] for j in range(len(y_test_x)) if abs(
            y_test_x[j] - true_x) <= error_range]
        y_within_range = [y_pred_y[j] for j in range(len(y_test_y)) if abs(
            y_test_y[j] - true_y) <= error_range]

        if len(x_within_range) > 1 and len(y_within_range) > 1:

            combined_predictions = x_within_range + y_within_range
            combined_true = [true_x] * len(x_within_range) + \
                [true_y] * len(y_within_range)

            r2_combined = r2_score(combined_true, combined_predictions)

            outer_key = str(true_x)
            inner_key = str(true_y)

            if true_x not in data:
                data[outer_key] = {}

            data[outer_key][inner_key] = {
                'predicted_x': y_pred_x.tolist(),
                'predicted_y': y_pred_y.tolist(),
                'r2_combined': r2_combined.tolist()
            }

    return data


def train_to_validate_calib(calib_csv_file, predict_csv_file):
    dataset_train_path = calib_csv_file
    dataset_predict_path = predict_csv_file

    # Carregue os dados de treinamento a partir do CSV
    data = pd.read_csv(dataset_train_path)

    # Para evitar que retorne valores negativos: Aplicar uma transformação logarítmica aos rótulos (point_x e point_y)
    # data['point_x'] = np.log(data['point_x'])
    # data['point_y'] = np.log(data['point_y'])

    # Separe os recursos (X) e os rótulos (y)
    X = data[['left_iris_x', 'left_iris_y', 'right_iris_x', 'right_iris_y']]
    y = data[['point_x', 'point_y']]

    # Crie e ajuste um modelo de regressão linear
    model = linear_model.LinearRegression()
    model.fit(X, y)

    # Carregue os dados de teste a partir de um novo arquivo CSV
    dados_teste = pd.read_csv(dataset_predict_path)

    # Faça previsões
    previsoes = model.predict(dados_teste)

    # Para evitar que retorne valores negativos: Inverter a transformação logarítmica nas previsões
    # previsoes = np.exp(previsoes)

    # Exiba as previsões
    print("Previsões de point_x e point_y:")
    print(previsoes)
    return previsoes.tolist()


def train_model(session_id):
    # Download dataset
    dataset_train_path = f'{Path().absolute()}/public/training/{session_id}/train_data.csv'
    dataset_session_path = f'{Path().absolute()}/public/sessions/{session_id}/session_data.csv'

    # Importing data from csv
    raw_dataset = pd.read_csv(dataset_train_path)
    session_dataset = pd.read_csv(dataset_session_path)

    train_stats = raw_dataset.describe()
    train_stats = train_stats.transpose()

    dataset_t = raw_dataset
    dataset_s = session_dataset.drop(['timestamp'], axis=1)

    # Drop the columns that will be predicted
    X = dataset_t.drop(['timestamp', 'mouse_x', 'mouse_y'], axis=1)

    Y1 = dataset_t.mouse_x
    Y2 = dataset_t.mouse_y
    # print('Y1 is the mouse_x column ->', Y1)
    # print('Y2 is the mouse_y column ->', Y2)

    MODEL_X = model_for_mouse_x(X, Y1)
    MODEL_Y = model_for_mouse_y(X, Y2)

    GAZE_X = MODEL_X.predict(dataset_s)
    GAZE_Y = MODEL_Y.predict(dataset_s)

    GAZE_X = np.abs(GAZE_X)
    GAZE_Y = np.abs(GAZE_Y)

    return {"x": GAZE_X, "y": GAZE_Y}


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
        f'Mean absolute error MAE = {mean_absolute_error(Y1_test, Y1_pred_test)}')
    print(
        f'Mean squared error MSE = {mean_squared_error(Y1_test, Y1_pred_test)}')
    print(
        f'Mean squared log error MSLE = {mean_squared_log_error(Y1_test, Y1_pred_test)}')
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
        f'Mean absolute error MAE = {mean_absolute_error(Y2_test, Y2_pred_test)}')
    print(
        f'Mean squared error MSE = {mean_squared_error(Y2_test, Y2_pred_test)}')
    print(
        f'Mean squared log error MSLE = {mean_squared_log_error(Y2_test, Y2_pred_test)}')
    print(f'MODEL X SCORE R2 = {model.score(X, Y2)}')

    # print(f'TRAIN{Y2_pred_train}')
    print(f'TEST{Y2_pred_test}')
    return model


def normalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
