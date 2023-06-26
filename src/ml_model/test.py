from neurokit2.eda.eda_simulate import eda_simulate
from neurokit2.eda.eda_process import eda_process, eda_plot
import matplotlib.pyplot as plt

eda = eda_simulate()

signals, info = eda_process(eda)
# plt.figure()
# eda_plot(signals)
# plt.show()

print(signals['EDA_Phasic'].min())
print(signals['EDA_Phasic'].max())
print(signals['EDA_Phasic'].mean())
print(signals['EDA_Phasic'].std())
print('\n')
print(signals["EDA_Raw"].mean())
print(signals["EDA_Clean"].mean())
print(signals.keys())





