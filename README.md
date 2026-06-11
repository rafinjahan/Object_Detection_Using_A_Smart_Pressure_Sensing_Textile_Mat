# Object Detection Using a Smart Pressure-Sensing Textile Mat

This repository contains the Python code and dataset for my bachelor thesis. The project uses a 4x4 woven piezoresistive pressure mat to classify everyday kitchen objects. It uses a Random Forest machine learning model to read the pressure footprint and total weight.

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
