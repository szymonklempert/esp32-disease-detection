import neurokit2 as nk
import numpy as np


def raw_to_dict(data_raw: dict) -> dict:
    data, info = nk.eda_process(data_raw['eda'], sampling_rate=1)

    result = dict()

    eda = data['EDA_Clean']
    result['EDA_mean'] = eda.mean()
    result['EDA_std'] = eda.std()
    result['EDA_min'] = eda.min()
    result['EDA_max'] = eda.max()

    eda_phasic = data['EDA_Phasic']
    result['EDA_phasic_mean'] = eda_phasic.mean()
    result['EDA_phasic_std'] = eda_phasic.std()
    result['EDA_phasic_min'] = eda_phasic.min()
    result['EDA_phasic_max'] = eda_phasic.max()

    eda_tonic = data['EDA_Tonic']
    result['EDA_tonic_mean'] = eda_tonic.mean()
    result['EDA_tonic_std'] = eda_tonic.std()
    result['EDA_tonic_min'] = eda_tonic.min()
    result['EDA_tonic_max'] = eda_tonic.max()

    temp = data_raw['temp']
    temp = np.array(temp)
    result['TEMP_mean'] = temp.mean()
    result['TEMP_std'] = temp.std()
    result['TEMP_min'] = temp.min()
    result['TEMP_max'] = temp.max()
    result['TEMP_slope'] = np.mean(np.gradient(temp))

    result['age'] = data_raw['user_data']['age']
    result['height'] = data_raw['user_data']['height']
    result['weight'] = data_raw['user_data']['weight']
    result['coffee_today_YES'] = data_raw['user_data']['coffee_today_YES']
    result['sport_today_YES'] = data_raw['user_data']['sport_today_YES']
    result['feel_ill_today_YES'] = data_raw['user_data']['feeling_ill_today_YES']
    result['gender'] = data_raw['user_data']['gender']
    result['smoker'] = data_raw['user_data']['smoker']

    return result
