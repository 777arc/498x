#!/usr/bin/env python

import numpy as np
import adi
import matplotlib.pyplot as plt

sample_rate = 10e6 # Hz
center_freq = 100e6 # Hz
fft_size = 1024
num_samps = 1000000

sdr = adi.Pluto()
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate) # filter width, just set it to the same as sample rate
sdr.rx_lo = int(center_freq) 
sdr.gain_control_mode = "slow_attack" # for automatic gain control

sdr.rx_buffer_size = num_samps # how many samples to get each time we call rx()

samples = sdr.rx() # receive samples off Pluto

# Create Waterfall matrix
num_slices = int(np.floor(num_samps/fft_size))
waterfall = np.zeros((num_slices, fft_size))
for i in range(num_slices):
    waterfall[i,:] = np.log10(np.fft.fftshift(np.abs(np.fft.fft(samples[i*fft_size:(i+1)*fft_size]))**2))

# Plot waterfall
time_per_row = 1.0/sample_rate * fft_size
fmin = (center_freq - sample_rate/2.0)/1e6 # MHz
fmax = (center_freq + sample_rate/2.0)/1e6 # MHz
plt.imshow(waterfall, extent=[fmin, fmax, time_per_row*num_slices, 0], aspect='auto', cmap=plt.get_cmap('jet'))
plt.xlabel('Frequency [MHz]')
plt.ylabel('Time [seconds]')
plt.show()
