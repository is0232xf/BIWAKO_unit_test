import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file = "result.csv"

data = pd.read_csv(file, skipinitialspace=True)
# comvert csv data to a list format data
strength = np.array(data['strength'].values.tolist())
mp_4TD = np.array(data['mean peak(4thruster)'].values.tolist())
mc_4TD = np.array(data['mean const(4thruster)'].values.tolist())
mp_Dia = np.array(data['mean peak(diagonal)'].values.tolist())
mc_Dia = np.array(data['mean const(diagonal)'].values.tolist())
mp_Omni = np.array(data['mean peak(push)'].values.tolist())
mc_Omni = np.array(data['mean const(push)'].values.tolist())

app_mp_4TD = [0.085, 1.35, 1.5499999999999998, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1, 5.1]
app_mp_Dia = [0.085, 0.81, 0.88, 2.810000000000001, 2.83, 2.83, 2.83, 2.83, 2.83, 2.83, 2.83]
app_mp_Omni = [0.085, 0.82, 1.02, 2.730000000000001, 2.81, 2.81, 2.81, 2.81, 2.81, 2.81, 2.81]

app_mc_4TD = [0.1, 0.11930000000000007, 0.4592000000000003, 1.37, 1.37, 1.37, 1.37, 1.37, 1.37, 1.37, 1.37]
app_mc_Dia = [0.1, 0.10360000000000001, 0.2664000000000001, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74]
app_mc_Omni = [0.09, 0.114, 0.30200000000000005, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78]

plt.plot(strength, mc_4TD, color='red', alpha=0.3, linestyle='--')
plt.plot(strength, mc_Dia, color='blue', alpha=0.3, linestyle='--')
plt.plot(strength, mc_Omni, color='green', alpha=0.3, linestyle='--')
plt.plot(strength, app_mc_4TD, color='red', label='4TD')
plt.plot(strength, app_mc_Dia, color='blue', label='Diagonal')
plt.plot(strength, app_mc_Omni, color='green', label='Omni-directional')
plt.xlabel('Thrust strength [%]')
plt.ylabel('Current [A]')
plt.xlim(0, 100)
plt.ylim(0, 3)
plt.xticks(strength)
plt.legend()
plt.grid()
plt.show()
