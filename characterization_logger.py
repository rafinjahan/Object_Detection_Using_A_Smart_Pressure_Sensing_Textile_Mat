import serial
import time
import csv
import sys
import msvcrt

PORT = 'COM4'
BAUD = 115200

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
except Exception as e:
    print("could not connect to arduino")
    sys.exit()

filename = "step_response_test.csv"

weight_map = {
    b'0': 0,    
    b'1': 40,  
    b'2': 140,  
    b'3': 340,  
    b'4': 590   
}

with open(filename, 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["timestamp", "target_weight", "resistance_ohms"])

print("Step Response Test Started.")
print("Use keys 0-4 to set the current total weight.")
print("Press 'q' to stop and save.")

current_weight = 0

while True:
    try:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'q':
                print("Saving and exiting...")
                break
            elif key in weight_map:
                current_weight = weight_map[key]
                print(f"Current weight set to: {current_weight}g")

        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    res = float(line)
                    with open(filename, 'a', newline='') as f:
                        writer = csv.writer(f, delimiter=';')
                        writer.writerow([time.time(), current_weight, res])
                except ValueError:
                    pass
    except KeyboardInterrupt:
        break