import pyvisa
import keyboard
import csv
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()
sa = rm.open_resource('GPIB0::1::INSTR')

print("Enter low wavelength (nm)")
wl_low = float(input())

print("Enter high wavelength (nm)")
wl_high = float(input())

if wl_high < wl_low:
    wl_low, wl_high = wl_high, wl_low
wl_low = max(350, min(wl_low, 1749))
wl_high = max(351, min(wl_high, 1750))

span = round(100 * (wl_high - wl_low)) / 100.0
ctr = round(100.0 * (wl_high + wl_low) / 2) / 100.0

print("Enter resolution (nm)")
precision = round(100.0 * float(input())) / 100.0
precision = max(0.05, min(precision, 10))

print("Initializing sweep...")

sa.write("STP")
sa.write("NORMD")
sa.write(f"SPAN{span}")
sa.write(f"CTRWL{ctr}")
sa.write("REFL0.00")
sa.write(f"RESLN{precision}")
sa.write("LSCL10.00")
sa.write("RPT")
sa.write("ACTV0")

print("Sweeping")
print("Press 'q' to end the program")
print("Press 'm' to save the data")

while True:
    if keyboard.is_pressed('m') or keyboard.is_pressed('q'):
        sa.write("STP")
        if keyboard.is_pressed('q'):
            print("Program exiting")
            exit()
        break

sa.write("LDATA R0001-R1001")
response = sa.read().strip()
if not response:
    print("Error: No data received")
    exit()

data_points = response.split(',')
del data_points[0] # Number of requested data points

if len(data_points) != 1001:
    print(f"Warning: Expected 1001 points, received {len(data_points)}")

wavelengths = [(wl_low + i * span / 1000) for i in range(1001)]

csv_filename = "spectrum_data.csv" # REPLACE WITH FILENAME
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Wavelength (nm)", "Absolute Intensity (dBm)"])

    for wl, value in zip(wavelengths, data_points):
        try:
            writer.writerow([wl, float(value)])
        except ValueError:
            print(f"Error parsing value: {value}")

print(f"Data saved to {csv_filename}\n")
print("Would you like to plot the data? (y/n)")

while True:
    if keyboard.is_pressed('n'):
        print("Program exiting")
        exit()
    if keyboard.is_pressed('y'):
        break

data_points = [float(value) for value in data_points]
plt.figure(figsize=(8, 6))
plt.plot(wavelengths, data_points)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Relative Intensity (dBm)")
plt.grid(True)
plt.show()

print("Program exiting")
