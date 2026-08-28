# Yamaha Motif ES Hardware Measurement Datasets

![All 50 measured EQ response curves overlaid](3beq.jpg)

Real hardware measurements from a 2003 Yamaha Motif ES physical synthesizer
workstation -- signal generated, driven through the hardware, and captured
back, not simulated or datasheet-derived. Intended for audio engineers,
machine learning researchers, and DSP developers focused on hardware
emulation and filter/dynamics modeling.

## Datasets

### [`EQ/`](EQ/) -- 3-Band EQ response curves
50 hardware sweeps of the integrated 3-band Equalizer (Low Shelf, Mid Bell,
High Shelf), 20 Hz - 20,000 Hz, 73 points per sweep. Two flat CSVs (run
metadata + the full frequency-response matrix). See [`EQ/README.md`](EQ/README.md).

### [`Compressor/`](Compressor/) -- Compressor dynamics
7 representative Attack/Release/Threshold/Ratio settings, 90 measurement
points each: attack/release timing, static transfer (threshold/ratio)
behavior, and real time-domain gain-reduction envelope shapes. See
[`Compressor/README.md`](Compressor/README.md).

More effect categories (modulation rate/depth, distortion, lo-fi) may be
added here over time as they're characterized.

## License (CC0 1.0 Universal)
This project is dedicated to the public domain. You are completely free to
use this data for training neural networks, reverse-engineering digital
filters, constructing audio algorithms, or publishing academic work
without any operational restrictions, legal hurdles, or attribution
requirements.
