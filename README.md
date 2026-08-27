# Yamaha Motif ES 3-Band EQ Curves Dataset

This repository contains a comprehensive CSV dataset mapping the response curves of the hardware 3-band Equalizer from a 2003 Yamaha Motif ES workstation. 

This data is intended for audio engineers, DSP developers, and anyone interested in hardware modeling or filter analysis.

## 📦 Dataset Specifications
* **Hardware Source:** Yamaha Motif ES Physical Unit
* **File Format:** `.csv` (Comma-Separated Values)
* **Total Dataset Size:** 50 distinct hardware sweep runs
* **Target:** 3-Band Hardware EQ 

## 🔍 Data Structure & Dictionary
The dataset includes 50 distinct test runs capturing variations across the Low, Mid, and High EQ bands. 

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Run_ID` | Integer / String | Identifier for the specific test run (1 to 50) |
| `Frequency` | Float | Frequency value in Hertz (Hz) |
| `Gain` | Float | Measured gain response in decibels (dB) |
| `[Column 4]` | [Type] | [e.g., Phase response in degrees, Q-factor, or hardware settings] |

## ⚖️ License (CC0 1.0 Universal)
This dataset is dedicated to the public domain. You are completely free to use this data for training machine learning models, building VST/AU audio plugins, hardware modeling, or academic research without any restriction or attribution requirements.
