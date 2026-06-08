import serial
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import os

script_folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_folder, 'tablecloth_dataset_flattened.csv')
df = pd.read_csv(csv_path, sep=';')

if len(df.columns) == 1:
    df = pd.read_csv(csv_path, sep=',')

df['raw_label'] = df['state'].astype(str) + " " + df['item'].astype(str)
label_mapping = {
    'empty plate': 'Empty Plate',
    'full plate': 'Full Plate',
    'empty bowl': 'Empty Bowl',
    'full bowl': 'Full Bowl',
    'empty muumi_cup_arabia': 'Empty Muumi Cup',
    'full muumi_cup_arabia': 'Full Muumi Cup',
    'full coke_0.33l': 'Full 0.33L Coke',
    'full coke_1.5l': 'Full 1.5L Bottle'
}
df['label'] = df['raw_label'].map(label_mapping).fillna(df['raw_label'])

X = df.loc[:, 'p0':'p15']
y = df['label']

print("Training Random Forest model on all data...")
rf = RandomForestClassifier(random_state=42)
rf.fit(X, y)
print("Model ready.")

PORT = 'COM3'
BAUD = 115200

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
except Exception:
    print(f"Could not connect to {PORT}. Check connection.")
    exit()

plt.ion()
fig, ax = plt.subplots(figsize=(8, 6))
matrix = np.zeros((4, 4))

im = ax.imshow(matrix, cmap='hot', vmin=0, vmax=4095)
plt.colorbar(im)
title_text = ax.set_title("Waiting for data...", fontsize=16, fontweight='bold')

grid_data = []

print("Starting live classification. Press Ctrl+C in terminal to stop.")

while True:
    try:
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()

            if line == "----":
                if len(grid_data) == 4:
                    matrix = np.array(grid_data)
                    im.set_data(matrix)

                    flat_data = matrix.flatten()

                    if np.max(flat_data) < 150:
                        title_text.set_text("Empty Mat")
                        title_text.set_color("black")
                    else:
                        prediction = rf.predict([flat_data])[0]
                        title_text.set_text(f"Prediction {prediction}")
                        title_text.set_color("blue")

                grid_data = []

            elif line != "":
                row = [int(x) for x in line.split('\t') if x != ""]
                if len(row) == 4:
                    grid_data.append(row)

        plt.pause(0.001)

    except KeyboardInterrupt:
        print("\nStopped by user.")
        break
    except Exception:
        pass