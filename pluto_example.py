import numpy as np
import adi
import matplotlib.pyplot as plt

sample_rate = 20e6 # Hz
center_freq = 100e6 # Hz
num_samps = 1000000 # number of samples returned per call to rx()


sdr = adi.Pluto('ip:192.168.2.1')
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 70.0 # dB
sdr.rx_lo = int(center_freq)
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samps

samples = sdr.rx() # receive samples off Pluto
print(samples[0:10])

x = samples
fft_size = 2048
num_rows = int(np.floor(len(x)/fft_size))
spectrogram = np.zeros((num_rows, fft_size))
for i in range(num_rows):
    spectrogram[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(x[i*fft_size:(i+1)*fft_size])))**2)


plt.imshow(spectrogram, aspect='auto', extent = [sample_rate/-2/1e6 + center_freq/1e6, sample_rate/2/1e6 + center_freq/1e6, 0, len(x)/sample_rate])
plt.xlabel("Frequency [MHz]")
plt.ylabel("Time [s]")
plt.show()
