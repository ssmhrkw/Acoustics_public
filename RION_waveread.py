import matplotlib.pyplot as plt
import os
import struct
import wavio

filename = 'ForceHammer (1)'
strWAVFile = filename+'.wav'

fileIn = open(strWAVFile, 'rb')
bufHeader_fmt = fileIn.read(712)

Ch1commonFields = {'ChxValuePerBit':0}
Ch2commonFields = {'ChxValuePerBit':0}
Ch3commonFields = {'ChxValuePerBit':0}
Ch4commonFields = {'ChxValuePerBit':0}

Ch1commonFields['ChxValuePerBit'] = struct.unpack('d', bufHeader_fmt[324:332])[0] 
Ch2commonFields['ChxValuePerBit'] = struct.unpack('d', bufHeader_fmt[438:446])[0] 
Ch3commonFields['ChxValuePerBit'] = struct.unpack('d', bufHeader_fmt[552:560])[0] 
Ch4commonFields['ChxValuePerBit'] = struct.unpack('d', bufHeader_fmt[666:674])[0] 

# wavioで読み込み
w = wavio.read(strWAVFile)
fs = w.rate #Sampling frequencu (Hz)
bit = 8 * w.sampwidth # Bit数
data = w.data.T  # Data -SA-A1を使用しているので4chにしてる

Accelerometer = data[0,:] #加速度ピックアップはCh0で測定した
Forcehammer = data[1,:] #加振ハンマーはCh1で測定した

Accelerometer_normalised_RION = Accelerometer * Ch1commonFields['ChxValuePerBit'] # RION風に正規化 
Forcehammer_normalised_RION = Forcehammer * Ch2commonFields['ChxValuePerBit'] # RION風に正規化 

fig, (axL, axR) = plt.subplots(ncols=2, figsize=(13,4))
axL.plot(Forcehammer_normalised_RION)
axL.set_title('Normalised (RION)')
axL.set_xlabel('Discrete points (-)')
axL.set_ylabel('Force (N)')
axL.grid(True)

axR.plot(Accelerometer_normalised_RION)
axR.set_title('Normalised (RION)')
axR.set_xlabel('Discrete points (-)')
axR.set_ylabel('Acceleration (m/s$^2$)')
axR.grid(True)
