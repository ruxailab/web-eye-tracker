from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_squared_log_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from pathlib import Path
import pandas as pd
import numpy as np


def predict(data, test_data):

    df = pd.read_csv(data)
    df = df.drop(['screen_height', 'screen_width'], axis=1)

    df_test = pd.read_csv(test_data)
    df_test = df_test.drop(['screen_height', 'screen_width'], axis=1)

    X_train_x = df[['left_iris_x', 'right_iris_x']]
    y_train_x = df['point_x']

    sc = StandardScaler()
    X_train_x = sc.fit_transform(X_train_x)

    X_test_x = df_test[['left_iris_x', 'right_iris_x']]
    y_test_x = df_test['point_x']

    sc = StandardScaler()
    X_test_x = sc.fit_transform(X_test_x)

    model_x = linear_model.LinearRegression()
    model_x.fit(X_train_x, y_train_x)
    y_pred_x = model_x.predict(X_test_x)

    X_train_y = df[['left_iris_y', 'right_iris_y']]
    y_train_y = df['point_y']

    sc = StandardScaler()
    X_train_y = sc.fit_transform(X_train_y)

    X_test_y = df_test[['left_iris_y', 'right_iris_y']]
    y_test_y = df_test['point_y']

    sc = StandardScaler()
    X_test_y = sc.fit_transform(X_test_y)

    model = linear_model.LinearRegression()
    model.fit(X_train_y, y_train_y)
    y_pred_y = model.predict(X_test_y)

    data = {'True X': y_test_x, 'Predicted X': y_pred_x,
            'True Y': y_test_y, 'Predicted Y': y_pred_y}

    df_data = pd.DataFrame(data)
    df_data['True XY'] = list(zip(df_data['True X'], df_data['True Y']))

    def func_precision_x(group): return np.sqrt(
        np.sum(np.square([group['Predicted X'], group['True X']])))

    def func_presicion_y(group): return np.sqrt(
        np.sum(np.square([group['Predicted Y'], group['True Y']])))

    precision_x = df_data.groupby('True XY').apply(func_precision_x)
    precision_y = df_data.groupby('True XY').apply(func_presicion_y)

    precision_xy = (precision_x + precision_y) / 2
    precision_xy = precision_xy / np.mean(precision_xy)

    def func_accuracy_x(group): return np.sqrt(
        np.sum(np.square([group['True X'] - group['Predicted X']])))

    def func_accuracy_y(group): return np.sqrt(
        np.sum(np.square([group['True Y'] - group['Predicted Y']])))

    accuracy_x = df_data.groupby('True XY').apply(func_accuracy_x)
    accuracy_y = df_data.groupby('True XY').apply(func_accuracy_y)

    accuracy_xy = (accuracy_x + accuracy_y) / 2
    accuracy_xy = accuracy_xy / np.mean(accuracy_xy)

    data = {}

    for index, row in df_data.iterrows():

        outer_key = str(row['True X'])
        inner_key = str(row['True Y'])

        if outer_key not in data:
            data[outer_key] = {}

        data[outer_key][inner_key] = {
            'predicted_x': df_data[(df_data['True X'] == row['True X']) & (df_data['True Y'] == row['True Y'])]['Predicted X'].values.tolist(),
            'predicted_y': df_data[(df_data['True X'] == row['True X']) & (df_data['True Y'] == row['True Y'])]['Predicted Y'].values.tolist(),
            'PrecisionSD': precision_xy[(row['True X'], row['True Y'])],
            'Accuracy': accuracy_xy[(row['True X'], row['True Y'])]
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
