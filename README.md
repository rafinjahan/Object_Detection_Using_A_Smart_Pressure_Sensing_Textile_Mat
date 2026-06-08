# Object Detection Using a Smart Pressure-Sensing Textile Mat

[cite_start]This repository contains the Python code and dataset for my bachelor thesis[cite: 4, 11]. [cite_start]The project uses a 4x4 woven piezoresistive pressure mat to classify everyday kitchen objects[cite: 17, 19]. [cite_start]It uses a Random Forest machine learning model to read the pressure footprint and total weight[cite: 31, 33].

## Hardware Setup
* [cite_start]4x4 piezoresistive textile mat [cite: 20]
* [cite_start]Seeed Studio XIAO ESP32S3 microcontroller [cite: 21]
* [cite_start]CD74HC4051E analog multiplexer [cite: 21]

## Software Dependencies
* Python 3
* pandas
* numpy
* scikit-learn
* matplotlib
* pyserial

## Project Files
* [cite_start]tablecloth_dataset_flattened.csv contains the recorded dataset of 800 physical placements[cite: 346].
* data_collection.py reads serial data and saves new placements to the dataset.
* live_classifier.py trains the model and shows real time predictions on a heatmap.
* [cite_start]model_evaluation.py calculates the cross validation accuracy and generates the confusion matrix[cite: 511, 584].

## How It Works
[cite_start]The microcontroller scans the 16 sensor nodes on the fabric[cite: 45]. [cite_start]Custom data acquisition software stabilizes the analog signals and filters out background noise[cite: 22]. [cite_start]The system sends the pressure data to a computer for real time visualization and recording[cite: 23]. The Python script reads this data stream and updates a visual heatmap. [cite_start]The system includes a noise limit of 150 ADC units[cite: 369]. [cite_start]When the pressure goes above this limit the Random Forest model predicts which object is on the mat[cite: 387].

## Tested Objects
[cite_start]The dataset includes eight different classes[cite: 30].
* [cite_start]Iittala plate empty and full [cite: 124, 125]
* [cite_start]Kotikulta Ulappa bowl empty and full [cite: 124, 125]
* [cite_start]Arabia Muumi cup empty and full [cite: 124, 125]
* [cite_start]0.33 L Coca-Cola can full [cite: 124, 127]
* [cite_start]1.5 L Sprite bottle full [cite: 124, 127]

## Future Work
[cite_start]Future improvements could include increasing the spatial resolution of the textile sensor[cite: 693]. [cite_start]Another step is deploying the trained classifier directly on the microcontroller using a TinyML framework to improve user privacy[cite: 695].
