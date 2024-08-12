import numpy as np
import matplotlib.pyplot as plt

# Create a simple signal with two frequencies
fs = 500  # Sampling rate
t = np.linspace(0, 1, fs, endpoint=False)  # Time vector
f1, f2 = 5, 50  # Frequencies
signal = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)

# Compute the FFT
yf = np.fft.fft(signal)
xf = np.fft.fftfreq(t.size, 1/fs)

# Plot the magnitude spectrum
plt.figure(figsize=(10, 4))
plt.plot(xf, 2.0/fs * np.abs(yf))
plt.title('Frequency Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid()
plt.tight_layout()
plt.show()
