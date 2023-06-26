from ml_model.utils import raw_to_dict
from ml_model.model import Model

def get_stress_level(data: dict) -> str:
    prep_data = raw_to_dict(data)
    model = Model("ml/randomforest.pkl")
    output = model.predict(prep_data)

    return output
