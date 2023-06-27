import pickle
import numpy as np
import pandas as pd


def dict_to_df(data):
    return pd.DataFrame(data, index=[0])


class Model:
    re = {0 : 'amusement', 1: 'baseline', 2: 'stress'}
    def __init__(self, model_str: str):
        self.model = pickle.load(open(model_str, 'rb'))

    def predict(self, data) -> str:
        return self.re[self.model.predict(dict_to_df(data))[0]]

    def predict_proba(self, data) -> str:
        return str(self.model.predict_proba(np.array(data).reshape(1, -1))[0][1])

