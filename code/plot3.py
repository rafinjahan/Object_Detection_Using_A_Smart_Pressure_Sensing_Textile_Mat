import pandas as pd
import matplotlib.pyplot as plt
import os

script_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_folder)
data_folder = os.path.join(project_root, 'data')
images_folder = os.path.join(project_root, 'images')

df = pd.read_csv(os.path.join(data_folder, 'sensitivity_range32.csv'), sep=';')


df = df[df['avg_resistance_ohms'] > 0]
means = df.groupby('weight_grams')['avg_resistance_ohms'].mean().reset_index()
means = means.sort_values('weight_grams')

# 3. Muunna grammat paineeksi (kPa)
# Kaava: P = (m * g) / A -> (m * 0.001 kg * 9.81 m/s^2) / (3.14 cm^2 * 0.0001 m^2)
# Lyhyemmin: (m * 0.0981) / 3.14
area = 3.14
means['pressure_kpa'] = (means['weight_grams'] * 0.0981) / area

r0 = means.iloc[0]['avg_resistance_ohms']
means['rel_change'] = (r0 - means['avg_resistance_ohms']) / r0

working_range = means[means['weight_grams'] <= 800]

plt.figure(figsize=(10, 6))
plt.plot(working_range['pressure_kpa'], working_range['rel_change'], 'r-o', linewidth=2, markersize=8)

plt.title('Working Range (min – max)', fontsize=14)
plt.xlabel('Pressure (kPa)', fontsize=12)
plt.ylabel( '($\Delta R / R_0$)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig(os.path.join(images_folder, 'sensitivity_deltaR_plot.png'), dpi=300, bbox_inches='tight')
plt.show()