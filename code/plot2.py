import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

script_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_folder)
data_folder = os.path.join(project_root, 'data')
images_folder = os.path.join(project_root, 'images')

df = pd.read_csv(os.path.join(data_folder, 'step_response_test.csv'), sep=';')

df['time_rel'] = df['timestamp'] - df['timestamp'].iloc[0]

cutoff_val = 6000
df_clean = df[df['resistance_ohms'] < cutoff_val].copy()

diameter_cm = 2.0
radius_m = (diameter_cm / 2.0) / 100.0
area_m2 = np.pi * (radius_m ** 2)
gravity = 9.81

df_clean['mass_kg'] = df_clean['target_weight'] / 1000.0
df_clean['force_n'] = df_clean['mass_kg'] * gravity
df_clean['pressure_pa'] = df_clean['force_n'] / area_m2
df_clean['pressure_kpa'] = df_clean['pressure_pa'] / 1000.0

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(df_clean['time_rel'], df_clean['resistance_ohms'], 'b-', label='Resistance (Ohms)', alpha=0.8)
ax1.set_xlabel('Time (s)', fontsize=12)
ax1.set_ylabel('Resistance (Ohms)', color='b', fontsize=12)
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True, linestyle='--', alpha=0.6)

ax2 = ax1.twinx()
ax2.step(df_clean['time_rel'], df_clean['pressure_kpa'], 'r--', where='post', label='Applied Pressure (kPa)', alpha=0.6)
ax2.set_ylabel('Applied Pressure (kPa)', color='r', fontsize=12)
ax2.set_ylim(-0.5, 35)
ax2.tick_params(axis='y', labelcolor='r')

plt.title('Sensor Staircase Response', fontsize=14)
fig.tight_layout()

plt.savefig(os.path.join(images_folder, 'staircase_plot_puhdistettu.png'), dpi=300)
print("Plot saved as staircase_plot_puhdistettu.png")