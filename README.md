# Yamaha Motif ES 3-Band EQ Curves Dataset

This repository contains a comprehensive CSV dataset mapping the hardware response curves of the integrated 3-band Equalizer on a 2003 Yamaha Motif ES physical synthesizer workstation. 

This data is intended for audio engineers, machine learning researchers, and digital signal processing (DSP) developers focused on hardware emulation and filter modeling.

## 📦 Dataset Specifications
* **Hardware Source:** Yamaha Motif ES Physical Unit
* **File Format:** `.csv` (Comma-Separated Values)
* **Total Sweeps:** 50 distinct hardware runs
* **Frequency Range:** 20 Hz to 20,000 Hz
* **Data Resolution:** 73 measured discrete points per run

## 🔍 File Layout & Data Structure
The dataset file uses a dual-section architecture to couple hardware test configurations with the raw frequency matrix.

### Section 1: Run Metadata Manifest
The file begins with a metadata index describing the hardware parameters used for each of the 50 runs.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Label` | String | Unique run identifier linking metadata to the sweep column |
| `Band` | Integer | Active equalizer band (`1` = Low, `2` = Mid, `3` = High) |
| `Shape` | String | EQ filter topology type (`Bell`, `Low Shelf`, `High Shelf`) |
| `Target Freq (Hz)`| Integer | Target center/corner frequency assigned on the hardware interface |
| `Gain (dB)` | Integer | Active hardware gain setting applied during the run (ranging from -12 to +12) |
| `Q` | Float | Filter Quality factor width setting (ranges from 0.1 to 12.0) |
| `Points` | Integer | Total frequency sampling steps captured per run (`73`) |
| `Captured At` | ISO-8601 Timestamp | Exact execution date and time of the physical sweep capture |

### Section 2: Frequency Sweep Matrix
Immediately following the manifest, the data changes into a matrix block. 

* **Row Index:** The first column (`Frequency (Hz)`) represents the independent variable, moving from 20 Hz to 20,000 Hz across 73 sampling steps.
* **Feature Columns:** The remaining 50 columns are named exactly after the metadata `Label` fields. Each column represents a target sweep containing the real-world measured output variation value in decibels (dB).

## ⚖️ License (CC0 1.0 Universal)
This project is dedicated to the public domain. You are completely free to use this data for training neural networks, reverse-engineering digital filters, constructing audio algorithms, or publishing academic work without any operational restrictions, legal hurdles, or attribution requirements.

## 🛠️ Python Usage Example

Since the CSV contains an interleaved layout (a metadata manifest block followed by the data matrix array), use the script below to parse and isolate both sections cleanly using `pandas` and plot a quick visual sweep.

```python
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the raw file
file_path = "your_dataset_file.csv"

# 2. Extract the Metadata Manifest (Rows 0 to 49)
# Reads the first 50 runs of text-based hardware configuration parameters
metadata_df = pd.read_csv(file_path, nrows=50)

# 3. Extract the Filter Data Matrix (Rows 51 onwards)
# Skips the manifest block to read the raw 73-point frequency response array
data_matrix_df = pd.read_csv(file_path, skiprows=51)

# Review the clean structures
print("--- Metadata Sample ---")
print(metadata_df.head(3))
print("\n--- Data Matrix Sample ---")
print(data_matrix_df.head(3))

# 4. Optional: Quick Validation Plot
# Plots the frequency sweeps for the low shelf, mid bell, and high shelf filters
plt.figure(figsize=(10, 6))
for column in data_matrix_df.columns[1:]: # Skip 'Frequency (Hz)' column
    plt.semilogx(data_matrix_df['Frequency (Hz)'], data_matrix_df[column], alpha=0.5)

plt.title('Yamaha Motif ES Integrated 3-Band EQ Response Sweeps')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Measured Output Response (dB)')
plt.grid(True, which="both", ls="-")
plt.show()
```
