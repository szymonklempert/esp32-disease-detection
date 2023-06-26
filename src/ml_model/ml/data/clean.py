import pandas as pd
from features import FEATURES

df = pd.read_csv('merged.csv')

df = df[FEATURES]

# 1 - male, 0 - female
df['gender'] = (df['gender_ male'] == 1).astype(int)
df.drop(['gender_ female', 'gender_ male'], axis=1, inplace=True)

# smoker, 1 - yes, 0 - no
df['smoker'] = (df['smoker_YES'] == 1).astype(int)
df.drop(['smoker_NO', 'smoker_YES'], axis=1, inplace=True)

df.to_csv('merged_cleaned.csv', index=False)
print(df.columns)
