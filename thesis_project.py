import serial
import numpy as np
import matplotlib.pyplot as plt
import json
import csv
import time
import os

for key in plt.rcParams:
    if key.startswith('keymap.'):
        plt.rcParams[key] = []

script_folder = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_folder, "tablecloth_dataset_flattened.csv")

counts_file = os.path.join(script_folder, "record_counts.json")

try:
    with open(counts_file, 'r') as cf:
        record_counts = json.load(cf)
except Exception:
    record_counts = {}

if not os.path.exists(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["time", "item", "state", "p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13", "p14", "p15"])

PORT = 'COM3' 
BAUD = 115200

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
except Exception:
    print(f"Could not connect to {PORT}. Check connection.")
    exit()

plt.ion()
fig, ax = plt.subplots()
matrix = np.zeros((4, 4))

im = ax.imshow(matrix, cmap='hot', vmin=0, vmax=4095) 
plt.colorbar(im)
plt.title("Textile Pressure Mat (4x4)")

is_recording = False
current_item = ""
current_state = ""
frames_recorded = 0
buffer_data = [] 

TARGET_FRAMES = 1 

def on_key(event):
    global is_recording, current_item, current_state, frames_recorded, buffer_data
    
    key_map = {
        'q': ['bowl', 'empty'],
        'a': ['bowl', 'full'],
        'w': ['plate', 'empty'],
        's': ['plate', 'full'],
        'e': ['muumi_cup_arabia', 'empty'],
        'd': ['muumi_cup_arabia', 'full'],
        'f': ['coke_0.33l', 'full'],
        'g': ['coke_1.5l', 'full']
    }
    
    if event.key in key_map:
        if is_recording:
            print("Already recording... wait a moment.")
            return
            
        current_item = key_map[event.key][0]
        current_state = key_map[event.key][1]
        is_recording = True
        frames_recorded = 0
        buffer_data = [] 
        print(f"\n>>> RECORDING PLACEMENT FOR: {current_state} {current_item}")

fig.canvas.mpl_connect('key_press_event', on_key)

print("Ready. Make sure the heatmap window is active.")
print("Place object, then press its key to record ONE flattened placement.")

grid_data = []

while True:
    try:
        while ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            
            if line == "----":
                if len(grid_data) == 4:
                    matrix = np.array(grid_data)
                    im.set_data(matrix) 
                    
                    if is_recording:
                        flat_matrix = matrix.flatten().tolist()
                        buffer_data.append(flat_matrix)
                        frames_recorded += 1
                        print(".", end="", flush=True)
                        
                    
                        if frames_recorded >= TARGET_FRAMES:
                            is_recording = False
                            
                        
                            flattened_frame = np.mean(buffer_data, axis=0)
                            flattened_frame = np.round(flattened_frame).astype(int)
                            
                            
                            with open(filename, 'a', newline='') as f:
                                writer = csv.writer(f, delimiter=';')
                                row = [time.time(), current_item, current_state] + flattened_frame.tolist()
                                writer.writerow(row)
                           
                            record_counts[current_item] = record_counts.get(current_item, 0) + 1
                            try:
                                with open(counts_file, 'w') as cf:
                                    json.dump(record_counts, cf)
                            except Exception:
                                pass

                            print(f"\n||| PLACEMENT SAVED. {current_item} recorded {record_counts[current_item]} times. Move object to a new spot and press key again.")
                            buffer_data = []
                        
                grid_data = []
                
            elif line != "":
                row = [int(x) for x in line.split('\t') if x != ""]
                if len(row) == 4:
                    grid_data.append(row)
        
        plt.pause(0.001)
                    
    except KeyboardInterrupt:
        print("\nstopped by terminal.")
        break
    except Exception as e:
        pass