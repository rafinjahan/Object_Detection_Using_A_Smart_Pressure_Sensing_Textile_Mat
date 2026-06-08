I wrote a README file for your project. You can copy and paste this text directly into GitHub.

Smart Textile Object Detection
This repository contains the Python code and dataset for my bachelor thesis. The project uses a 4x4 woven piezoresistive pressure mat to classify everyday kitchen objects. It uses a Random Forest machine learning model to read the pressure footprint and total weight.

Hardware Setup
4x4 piezoresistive textile mat

Seeed Studio XIAO ESP32S3 microcontroller

CD74HC4051E analog multiplexer

Software Dependencies
Python 3

pandas

numpy

scikit-learn

matplotlib

pyserial

Project Files
tablecloth_dataset_flattened.csv contains the recorded dataset of 800 physical placements.

data_collection.py reads serial data and saves new placements to the dataset.

live_classifier.py trains the model and shows real time predictions on a heatmap.

model_evaluation.py calculates the cross validation accuracy and generates the confusion matrix.

How It Works
The microcontroller scans the 16 sensor nodes on the fabric. It sends the raw analog values to the computer over a USB connection. The Python script reads this data stream and updates a visual heatmap. The system includes a noise limit of 150 ADC units. When the pressure goes above this limit the Random Forest model predicts which object is on the mat.

Tested Objects
The dataset includes eight different classes.

Iittala Plate empty and full

Kotikulta Bowl empty and full

Arabia Muumi cup empty and full

0.33 L Coca-Cola can full

1.5 L Sprite bottle full
