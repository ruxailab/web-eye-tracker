import plotly.express as px
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_squared_log_error, r2_score
import matplotlib.pyplot as plt

dataset_train_path = '/home/nata-brain/Documents/tcc/web-eye-tracker/public/training/1685126241.2630084natanael/train_data.csv'
dataset_session_path = '/home/nata-brain/Documents/tcc/web-eye-tracker/public/sessions/1685126241.2630084natanael/session_data.csv'

raw_dataset = pd.read_csv(dataset_train_path)
session_dataset = pd.read_csv(dataset_session_path)
dataset_t = raw_dataset
dataset_s = session_dataset.drop(['timestamp'], axis = 1)

def model_for_mouse_x(X, Y1, model):
    print('-----------------MODEL FOR X------------------')
    # split dataset into train and test sets (80/20 where 20 is for test)
    X_train, X_test, Y1_train, Y1_test = train_test_split(X, Y1, test_size=0.2)

    model = model
    model.fit(X_train, Y1_train)

    Y1_pred_train = model.predict(X_train)
    Y1_pred_test = model.predict(X_test)

    Y1_test = normalizeData(Y1_test)
    Y1_pred_test = normalizeData(Y1_pred_test)
    
    print(f'Mean absolute error MAE = {mean_absolute_error(Y1_train, Y1_pred_train)}')
    print(f'Mean squared error MSE = {mean_squared_error(Y1_train, Y1_pred_train)}')
    print(f'Mean squared log error MSLE = {mean_squared_log_error(Y1_train, Y1_pred_train)}')
    print(f'MODEL X SCORE R2 = {model.score(X, Y1)}')
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean absolute error (MAE)", f" {mean_absolute_error(Y1_train, Y1_pred_train)}")
    col2.metric("Mean squared error (MSE)", f" {mean_squared_error(Y1_train, Y1_pred_train)}")
    col3.metric("Mean squared log error (MSLE)", f" {mean_squared_log_error(Y1_train, Y1_pred_train)}")
    col4.metric("MODEL X SCORE R2 ", f" {model.score(X, Y1)}")
    #print(f'TRAIN{Y1_pred_train}')
    #print(f'TEST{Y1_pred_test}')
    return model

def model_for_mouse_y(X, Y2, model):
    print('-----------------MODEL FOR Y------------------')
     # split dataset into train and test sets (80/20 where 20 is for test)
    X_train, X_test, Y2_train, Y2_test = train_test_split(X, Y2, test_size=0.2)

    model = model
    model.fit(X_train, Y2_train)

    Y2_pred_train = model.predict(X_train)
    Y2_pred_test = model.predict(X_test)


    Y2_test = normalizeData(Y2_test)
    Y2_pred_test = normalizeData(Y2_pred_test)

    print(f'Mean absolute error MAE = {mean_absolute_error(Y2_train, Y2_pred_train)}')
    print(f'Mean squared error MSE = {mean_squared_error(Y2_train, Y2_pred_train)}')
    print(f'Mean squared log error MSLE = {mean_squared_log_error(Y2_train, Y2_pred_train)}')
    print(f'MODEL Y SCORE R2 = {model.score(X, Y2)}')

    #print(f'TRAIN{Y2_pred_train}')
    #print(f'TEST{Y2_pred_test}')
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean absolute error (MAE)", f"{mean_absolute_error(Y2_train, Y2_pred_train)}")
    col2.metric("Mean squared error (MSE)", f" {mean_squared_error(Y2_train, Y2_pred_train)}")
    col3.metric("Mean squared log error (MSLE)", f" {mean_squared_log_error(Y2_train, Y2_pred_train)}")
    col4.metric("MODEL Y SCORE R2 ", f" {model.score(X, Y2)}")
    return model

def normalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def train(model):
    # Drop the columns that will be predicted
    X = dataset_t.drop(['timestamp', 'screen_x', 'screen_y'], axis=1)

    Y1 = dataset_t.screen_x
    Y2 = dataset_t.screen_y
    # print('Y1 is the mouse_x column ->', Y1)
    # print('Y2 is the mouse_y column ->', Y2)

    MODEL_X = model_for_mouse_x(X, Y1, model)
    MODEL_Y = model_for_mouse_y(X, Y2, model)

    GAZE_X = MODEL_X.predict(dataset_s)
    GAZE_Y = MODEL_Y.predict(dataset_s)

    GAZE_X = np.abs(GAZE_X)
    GAZE_Y = np.abs(GAZE_Y)

    return GAZE_X, GAZE_Y

def showSaccades(model):
    
    x, y           = train(model)
    datetime       = session_dataset.timestamp
    
    fig_plt, ax = plt.subplots(figsize = (30, 20))

    ax.plot(x, y, 'r*')

    i = 0

    st.pyplot(fig_plt)
    
   

tab1, tab2 = st.tabs(["Dados Brutos", "Dados Processados"])

with tab1:
    st.title("Dados obtidos pela calibração")
    st.dataframe(raw_dataset)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Olho esquerdo")
        df = raw_dataset


        fig_left = px.scatter(
            df,
            x = "left_iris_x",
            y = "left_iris_y",
            color = "left_iris_y",
            color_continuous_scale = "reds",
        )
        
        st.plotly_chart(fig_left, theme="streamlit", use_container_width=True)

    with col2:    
        st.subheader("Olho direito")
        
        fig_right = px.scatter(
            df,
            x = "right_iris_x",
            y = "right_iris_y",
            color = "right_iris_y",
            color_continuous_scale = "reds",
        )

        st.plotly_chart(fig_right, theme="streamlit", use_container_width=True)
        
    fig3 = px.line(raw_dataset, y=["left_iris_x", "left_iris_y", "right_iris_x", "right_iris_y"], title="Left and Right Iris Position")
    st.plotly_chart(fig3,  theme="streamlit", use_container_width=True)

with tab2:
    st.subheader("Sacadas")
    fig_plt, ax = plt.subplots(figsize = (30, 20))

    x           = raw_dataset.left_iris_x
    y           = raw_dataset.left_iris_y
    datetime    = raw_dataset.timestamp

    ax.plot(x, y, 'r*', linestyle = '-')

    i = 0

    for xy in zip(x, y):
        i = i+1
        ax.annotate(f'{i}', xy)
    
    st.pyplot(fig_plt)

    col1, col2 = st.columns(2)
    
    
    st.subheader("Predição Regressão Linear")
    showSaccades(linear_model.LinearRegression())
    
    st.subheader("Predição Regressão Linear Ridge")
    showSaccades(linear_model.Ridge(alpha=.5))
    
    st.subheader("Predição Regressão Linear Ridge com Cross Validation")
    showSaccades(linear_model.RidgeCV(alphas=np.logspace(-6, 6, 13)))
        
    st.subheader("Predição Regressão Linear Lasso")
    showSaccades(linear_model.Lasso(alpha=0.1))