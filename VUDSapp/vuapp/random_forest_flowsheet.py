from lib2to3.pgen2.pgen import DFAState
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import joblib


class RandomForestFlowSheet:
    def __init__(self, cleaned_data):
        arr = np.array(
            [
                [
                    cleaned_data["Reflux"],
                    cleaned_data["age_time_of_study"],
                    cleaned_data["pressure_half_ebc"],
                    cleaned_data["pressure_25"],
                    cleaned_data["bladder_shape"],
                    cleaned_data["Leak_Present"],
                    cleaned_data["desd"],
                    cleaned_data["pvr"],
                    cleaned_data["percent_full"],
                    cleaned_data["press_three_four_ebc"],
                ]
            ]
        )
        print(arr)
        self.rf = joblib.load("vuapp/random_forest.joblib")
        my_columns = [
            "reflux",
            "age_time_study",
            "pressure_half_ebc",
            "pressure_25",
            "bladder_shape",
            "leak_present",
            "desd",
            "pvr",
            "percent_full",
            "press_three_four_ebc",
        ]

        self.df = pd.DataFrame(arr, columns=my_columns)
        df1 = self.df
        print(df1)

    def make_predictions(self):
        pred_proba = self.rf.predict_proba(self.df)
        print(pred_proba)
        pred = self.rf.predict(self.df)

        if pred_proba[0][2] >= 0.38:
            pred = 3
        else:
            pred = pred[0]

        if pred == 1:
            fpred = "Good"
        elif pred == 2:
            fpred = "Bad"
        else:
            fpred = "Ugly"

        return fpred
