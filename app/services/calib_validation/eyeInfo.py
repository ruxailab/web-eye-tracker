import tkinter as tk
import pandas as pd

class EyeInfo:
    def __init__(self,  calib_points=[], dataset='./data.csv', screen_width=0, screen_height=0, k_screen_width = 1872, k_screen_height = 944, is_right = False, is_left = False, is_mean = False):
            self.is_right = is_right
            self.is_left = is_left
            self.is_mean = is_mean
            self.dataset = dataset

            self.right_eye_df = None
            self.left_eye_df = None
            self.prediction_df = None

            self.calib_points = calib_points
            self.calib_df = None


            self.screen_width = screen_width
            self.screen_height = screen_height
            self.k_screen_width = k_screen_width
            self.k_screen_height = k_screen_height

    def init_eye(self):
        self.init_screen_resolution()
        self.init_calib_points()
        self.init_points()
        

    def init_screen_resolution(self):
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.destroy()

    def init_calib_points(self):
        # xf = self.screen_width/self.k_screen_width
        # yf = self.screen_height/self.k_screen_height
        xf = 1
        yf = 1
        if self.calib_points:
            post_calib = []
            for point in self.calib_points:
                calibrated_point = {
                    "screen_x": point["x"]*xf,
                    "screen_y": point["y"]*yf,
                    "order":    point["order"]
                }
                post_calib.append(calibrated_point)
            df = pd.DataFrame(post_calib)
            self.calib_df = df

    def init_points(self):
        try:
            data = pd.read_csv(self.dataset)
            if self.is_right:
                self.right_eye_df = data[['right_iris_x', 'right_iris_y']]
            
            if self.is_left:
                self.left_eye_df = data[['left_iris_x', 'left_iris_y']]

            if self.is_mean:
                self.right_eye_df = data[['right_iris_x', 'right_iris_y']]
                self.left_eye_df = data[['left_iris_x', 'left_iris_y']]
                
            self.prediction_df = data[['screen_x', 'screen_y']]

        except FileNotFoundError:
            print(f"File {self.dataset} not found.")
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {str(e)}")