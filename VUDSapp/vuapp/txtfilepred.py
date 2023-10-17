from lib2to3.pgen2.pgen import DFAState
import io
import base64
import joblib
import pickle
import pandas as pd
import numpy as np
from tensorflow.python.keras.models import Model, load_model
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pickle
from sksurv.ensemble import RandomSurvivalForest


class NN_by_pressure:
    def __init__(self, txtfile, ebc):
        txtfile2 = txtfile.open("r")
        arr = pd.read_csv(txtfile2, sep="\t")
        self.arr = arr
        self.ebc = ebc

        with open('vuapp/rsf_model_25.pkl', 'rb') as model_file25:
            self.twentyfive_model = pickle.load(model_file25)
        with open('vuapp/rsf_model_50.pkl', 'rb') as model_file_50:
            self.fifty_model = pickle.load(model_file_50)
        with open('vuapp/rsf_model_75.pkl', 'rb') as model_file_75:
            self.model = pickle.load(model_file_75)

            
        self.scaler_25 = joblib.load('vuapp/25scaler.pkl')
        self.scaler_50 = joblib.load('vuapp/50scaler.pkl')
        self.scaler_75 = joblib.load('vuapp/75scaler.pkl')
        self.feventtimes =np.array([  24.33333333,   35.33333333,   64.66666667,   77.33333333,
        86.        ,   93.66666667,  120.33333333,  138.33333333,
        150.66666667,  186.33333333,  208.66666667,  265.66666667,
        311.33333333,  317.        ,  341.        ,  346.        ,
        376.66666667,  474.33333333,  502.33333333,  557.        ,
        581.33333333,  677.33333333,  772.        ,  803.33333333,
        837.66666667,  905.33333333,  938.66666667,  968.        ,
        1007.33333333, 1044.66666667, 1115.33333333, 1165.66666667,
        1361.33333333, 1510.        , 1526.66666667, 1763.66666667])
        print(arr)

    @staticmethod
    def _reshape_to_tensor(df1, mymodel,scale):
        print('AT DF')
        print(df1)
        test_predictions = mymodel.predict(df1)
        new_data_scaled = scale.transform(test_predictions[0].reshape(-1, 1))
        new_data_scaled = new_data_scaled[0][0]
        new_data_scaled = int(np.round(new_data_scaled, 2) * 100)
        new_data_scaled = str(new_data_scaled)
        return new_data_scaled, mymodel

    @staticmethod
    def make_fig(self, pltfig):
        fig = pltfig.get_figure()
        canvas = FigureCanvas(fig)
        buffer = io.BytesIO()
        canvas.print_png(buffer)
        pabd_base_64 = base64.b64encode(buffer.getvalue()).decode()
        return pabd_base_64

    @staticmethod
    def _create_txt_plot(self, df):
        a4_dims = (18.7, 9)
        sns.set(font_scale=2)
        sns.set_style("whitegrid")
        # ig, ax = plt.subplots(figsize=a4_dims)
        pabd = sns.lineplot(x="percent", y="Pdet", data=df, color="r", label="Pdet")
        plt.xlabel("Percent")
        plt.ylabel("Pdet")
        plt.legend()
        pabd_base_64 = self.make_fig(self, pabd)
        return pabd_base_64
    
    @staticmethod
    def _plot_survival_function(self, rsf, X):
        Xplt = rsf.predict_survival_function(X, return_array=True)
        Xplt = (Xplt[0][:36])
        myx = self.feventtimes
        myInt = 365.25
        newArray = myx/myInt
        newArray = newArray.round(0)
        fig = plt.figure(figsize=(6,6))
        sns.set(style="whitegrid")  # Set the style to whitegrid

        plt.title("Survival Analysis",fontsize=20)
        plt.xlabel("Years",fontsize=20)
        plt.ylabel("Survival Probability",fontsize=20)
        plt.yticks(fontsize=16)
        plt.xticks(fontsize=16)
        #plt.plot(newArray,FXpltzerosurv2, color="blue",label="Low Risk Group",linewidth=5.5)
        plt.plot(newArray,Xplt, color="red", label="Survival Probability",linewidth=5.5)
        plt.legend(fontsize=20)
        plt.ylim(ymin=0)
        pabd_base_64 = self.make_fig(self, fig)
        return pabd_base_64
    
    @staticmethod
    def _create_time_txt_plot(self, df):
        sns.set(font_scale=2)
        sns.set_style("whitegrid")
        a4_dims = (8, 4)
        ig, ax = plt.subplots(figsize=a4_dims)
        axplt = sns.lineplot(x="Time", y="Pdet", data=df, color="r", label="Pdet")
        ax2 = plt.twinx()
        sns.lineplot(x="Time", y="VH2O", data=df, ax=ax2, color="b", label="VH2O")
        axplt.xaxis.set_major_locator(ticker.MultipleLocator(2000))
        pabd_base_64 = self.make_fig(self, axplt)
        return pabd_base_64

    def make_predictions(self):
        df = self.arr
        df["percent"] = df["VH2O"] / self.ebc
        df["percent"] = df["percent"].round(2)
        df = df.loc[df["percent"] >= 0.01]  ### Normalizing
        df = df.loc[df["percent"] <= 1.0]
        my_time_plot = self._create_time_txt_plot(self, df=df)
        df = df[["Pdet", "percent"]]


        df = df.groupby(["percent"])["Pdet"].mean().reset_index()
        del df["percent"]
        df1 = df.transpose().reset_index()  ## create array
        del df1["index"]
        dflen = df1.to_numpy()

        if dflen.shape[1] >= 73:
            df1 = df1.iloc[:, :73]
            pred,rsf = self._reshape_to_tensor(df1, self.model,self.scaler_75)

        elif dflen.shape[1] >= 48:
            df1 = df1.iloc[:, :48]
            pred,rsf = self._reshape_to_tensor(df1, self.fifty_model,self.scaler_50)

        elif dflen.shape[1] >= 23:
            df1 = df1.iloc[:, :23]
            pred,rsf = self._reshape_to_tensor(df1, self.twentyfive_model,self.scaler_25)

        else:  ### Error with file or less than 25% filled
            pred = "error"

        #if pred != "error":
         #   predict_class = np.argmax(pred, axis=1)
        #else:
         #   predict_class = "Error"

        #if predict_class == 0:
           # final_pred = "Good Bladder"
        #elif predict_class == 1:
         #   final_pred = "Bad Bladder"
       # elif predict_class == 2:
       #     final_pred = "Ugly Bladder"
        #else:
         #   final_pred = "Error"
        #try:
         #   print(pred.round(2))
        #my_plot = self._create_txt_plot(self, df=df)

        my_plot = self._plot_survival_function(self,rsf,df1)

       # except:
           # pass
        print(pred)

        return (pred, my_plot, my_time_plot)
