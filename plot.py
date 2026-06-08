import pandas as pd
import matplotlib.pyplot as plt


df_sens = pd.read_csv('sensitivity_range32.csv', sep=';')
df_sens = df_sens[df_sens['weight_grams'] < 1000]

means = df_sens.groupby('weight_grams')['avg_resistance_ohms'].mean().reset_index()
means['pressure_kpa'] = means['weight_grams'] * 0.03124

df_resp = pd.read_csv('response_time_400g.csv', sep=';')
df_resp['time_ms'] = (df_resp['timestamp'] - df_resp['timestamp'].iloc[0]) * 1000

df_rec = pd.read_csv('recovery_time_400g.csv', sep=';')
df_rec['time_ms'] = (df_rec['timestamp'] - df_rec['timestamp'].iloc[0]) * 1000


plt.figure(figsize=(10, 6))
plt.plot(means['pressure_kpa'], means['avg_resistance_ohms'], 'b-o', linewidth=2)
plt.title('Sensor Sensitivity: Resistance vs Pressure', fontsize=14)
plt.xlabel('Pressure (kPa)', fontsize=12)
plt.ylabel('Resistance (Ohms)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('sensitivity_plot.png', dpi=300)


plt.figure(figsize=(10, 6))
plt.plot(df_resp['time_ms'], df_resp['resistance_ohms'], 'r-', linewidth=1.5)
plt.title('Response Time: High-Speed Loading (400g)', fontsize=14)
plt.xlabel('Time (ms)', fontsize=12)
plt.ylabel('Resistance (Ohms)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('response_plot.png', dpi=300)

plt.figure(figsize=(10, 6))
plt.plot(df_rec['time_ms'], df_rec['resistance_ohms'], 'g-', linewidth=1.5)
plt.title('Recovery Time: High-Speed Unloading (400g)', fontsize=14)
plt.xlabel('Time (ms)', fontsize=12)
plt.ylabel('Resistance (Ohms)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('recovery_plot.png', dpi=300)

print("Kaikki kuvaajat generoitu ja tallennettu kansioon.")