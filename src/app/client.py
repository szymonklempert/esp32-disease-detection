from ml_model.utils import raw_to_dict
from ml_model.model import Model

path_mac = "src/ml_model/ml/randomForest.pkl"
path_windows = "ml_model/ml/randomForest.pkl"


def get_stress_level(data: dict) -> str:
    prep_data = raw_to_dict(data)
    model = Model(path_windows)
    output = model.predict(prep_data)

    return output
