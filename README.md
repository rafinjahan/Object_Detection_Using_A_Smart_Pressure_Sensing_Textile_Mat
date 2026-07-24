# Object Detection Using a Smart Pressure-Sensing Textile Mat

This repository contains the Python code and dataset for my bachelor thesis. The project uses a 4x4 woven piezoresistive pressure mat to classify everyday kitchen objects. It uses a Random Forest machine learning model to read the pressure footprint and total weight.
I designed a custom printed circuit board using KiCad to upgrade the original breadboard prototype. This custom PCB connects the textile mat directly to the microcontroller and multiplexer for a reliable system. You can see 3D screenshots of the finished board in the images folder.

## Hardware Setup
* 4x4 piezoresistive textile mat
* Seeed Studio XIAO ESP32S3 microcontroller
* CD74HC4051E analog multiplexer

## Software Dependencies
* Python 3
* pandas
* numpy
* scikit-learn
* matplotlib
* pyserial

## Project Structure
* `code/` contains all Python scripts.
* `data/` contains CSV datasets and measurement files.
* `hardware/` contains the KiCad PCB project and Gerber manufacturing files and the 3D model of the PCB.
* `images/` contains generated PNG plots and confusion matrices.
* `thesis/` contains thesis-related files.


## Project Files
* `data/tablecloth_dataset_flattened.csv` contains the recorded dataset of physical placements.
* `code/thesis_project.py` reads serial data and saves new placements to the dataset.
* `code/live_classifier.py` trains the model and shows real time predictions on a heatmap.
* `code/confusin_matrix_result.py` calculates grouped cross validation accuracy and generates the confusion matrix.

## How It Works
The microcontroller scans the 16 sensor nodes on the fabric. Custom data acquisition software stabilizes the analog signals and filters out background noise. The system sends the pressure data to a computer for real time visualization and recording. The Python script reads this data stream and updates a visual heatmap. The system includes a noise limit of 150 ADC units. When the pressure goes above this limit the Random Forest model predicts which object is on the mat.

## Tested Objects
The dataset includes eight different classes.
* Iittala plate empty and full
* Kotikulta Ulappa bowl empty and full
* Arabia Muumi cup empty and full
* 0.33 L Coca-Cola can full
* 1.5 L Sprite bottle full

## Future Work
Future improvements could include increasing the spatial resolution of the textile sensor. Another step is deploying the trained classifier directly on the microcontroller using a TinyML framework to improve user privacy.


## Instructions

The physical setup requires connecting the textile matrix to the microcontroller and multiplexer.

1. Connect the four row pins of the 4x4 piezoresistive textile mat to the digital output pins of the microcontroller.
2. Connect the four column pins of the mat to the analog multiplexer inputs.
3. Ensure the microcontroller and multiplexer share a common ground and a stable 3.3V power supply.
4. Connect the microcontroller to the data collection computer using a USB cable.

## Microcontroller Setup (Arduino IDE)

Before running the Python scripts, you must program the microcontroller and verify it is reading the sensors correctly.

1. Install the Arduino IDE and add support for the Seeed Studio XIAO ESP32S3 board.
2. Open the provided `.ino` file in the Arduino IDE and upload it to the microcontroller.
3. Open the Serial Monitor in the Arduino IDE (set the baud rate to 115200).
4. Apply pressure to different parts of the mat. You should see a stream of numbers appearing in the Serial Monitor. If the output changes when you press the mat, the hardware is working correctly.
5. **Important:** Close the Arduino Serial Monitor before running the Python scripts, otherwise Python will not be able to connect to the serial port.

## Software Installation (Python)

The software pipeline requires Python 3 and several scientific computing libraries.

1. Install Python 3 on the data collection computer.
2. Create a virtual environment to manage the project dependencies.
3. Install the required libraries using the pip package manager.

`pip install pandas numpy scikit-learn matplotlib pyserial`

## Data Collection and Heatmap Visualization

The data collection script reads raw analog values from the serial port and visualizes the spatial pressure distribution.

1. Place the smart textile mat on a flat and rigid surface to ensure consistent pressure readings.
2. Run the data collection script from your terminal using `python data_collection.py`.
3. Observe the real time heatmap interface to verify all 16 sensor nodes respond correctly to physical pressure.
4. Place a test object on the mat and allow the sensor values to stabilize for a few seconds.
5. Press the designated keyboard key to record the current matrix values and the object label into the dataset file named `tablecloth_dataset_flattened.csv`.

## Model Training and Evaluation

The machine learning model uses the collected CSV dataset to train the Random Forest classifier.

1. Verify the dataset file contains sufficient samples for all tested object categories.
2. Run the model evaluation script from the terminal using `python model_evaluation.py`.
3. The script will automatically load the CSV dataset and format the spatial arrays into one dimensional features.
4. The Random Forest algorithm will train on the data and output the grouped cross validation accuracy results.
5. Review the generated confusion matrix image to analyze the classification performance across different objects.
