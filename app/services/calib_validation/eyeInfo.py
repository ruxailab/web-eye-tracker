# from screeninfo import get_monitors
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class EyeInfo:
    def __init__(self,  calib_points=[], dataset='./data.csv', screen_width=0, screen_height=0,  is_right = False, is_left = False,):
            self.is_right = is_right
            self.is_left = is_left
            self.dataset = dataset

            self.right_eye_df = None
            self.left_eye_df = None
            self.prediction_df = None

            self.calib_points = calib_points
            self.calib_df = None


            self.screen_width = screen_width
            self.screen_height = screen_height

            self.palette = [
                'blue', 
                'red',
                'green',
                'yellow',
                'lightgreen',
                'purple',
                'orange',
                'pink',
                'turquoise'
            ]

    def init_eye(self):
        # self.init_screen_resolution()
        self.init_calib_points()
        self.init_points()
        

    # def init_screen_resolution(self):
    #     monitors = get_monitors()
    #     if monitors:
    #         primary_monitor = monitors[0]
    #         self.screen_width = primary_monitor.width 
    #         self.screen_height = primary_monitor.height
    #     else:
    #         self.screen_width = self.screen_width
    #         self.screen_height = self.screen_height

    def init_calib_points(self):
        if self.calib_points:
            post_calib = []
            for point in self.calib_points:
                calibrated_point = {
                    "screen_x": point["x"],
                    "screen_y": point["y"],
                    "order":    point["order"]
                }
                post_calib.append(calibrated_point)
            df = pd.DataFrame(post_calib)
            self.calib_df = df

    def init_points(self):
        try:
            data = pd.read_csv(self.dataset)
            if self.is_right:
                self.prediction_df = data[['screen_x', 'screen_y','right_iris_x', 'right_iris_y']]
            elif self.is_left:
                self.prediction_df = data[['screen_x', 'screen_y','left_iris_x', 'left_iris_y']]
            else:
                self.prediction_df = data[['screen_x', 'screen_y','right_iris_x', 'right_iris_y','left_iris_x', 'left_iris_y']]

        except FileNotFoundError:
            print(f"File {self.dataset} not found.")
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {str(e)}")
    
    def plot(self, datasets, keys_x, keys_y, is_subset, subset_size, lock_plot, eyes_only, ax, display_centroid, colors=[]):
        sns.set(style="whitegrid")
        for i in range(len(datasets)):
            if is_subset:
                for j in range(len(self.calib_points)):
                    start_index = j * subset_size
                    end_index = (j + 1) * subset_size

                    subset_df = datasets[i].iloc[start_index:end_index]
                    x_values = subset_df[keys_x[i]]
                    y_values = subset_df[keys_y[i]]
                    centroid_x = subset_df[keys_x[i]].mean()
                    centroid_y = subset_df[keys_y[i]].mean()
                    
                    distances = np.sqrt((x_values - centroid_x)**2 + (y_values - centroid_y)**2)

                    max_distance = max_distance = np.max(distances)


                    centroid_df = pd.DataFrame({'x': [centroid_x], 'y': [centroid_y]})
                    if not eyes_only:
                        sub_calib_df = self.calib_df.iloc[[j]]
                        sns.scatterplot(data=sub_calib_df, x='screen_x', y='screen_y', marker='*', color=self.palette[j], s=300)
                        if display_centroid:
                            sns.scatterplot(data=centroid_df,x='x', y='y', markers='x',s=max_distance, color=self.palette[j], alpha=0.5)
                            circle = plt.Circle((centroid_x, centroid_y), max_distance, color=self.palette[j], fill=False) 
                            plt.gca().add_patch(circle)


                    sns.scatterplot(data=subset_df, x=keys_x[i], y=keys_y[i], color=self.palette[j], ax=ax, s = 10)
            else:
                sns.scatterplot(data=datasets[i], x=f'{keys_x[i]}', y=f'{keys_y[i]}', color=colors[i], ax=ax)
        if lock_plot:
            plt.xlim(0, self.screen_width)
            plt.ylim(0, self.screen_height)
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.grid(True)