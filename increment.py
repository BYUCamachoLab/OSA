import pyvisa
import keyboard

rm = pyvisa.ResourceManager()
sa = rm.open_resource('GPIB0::1::INSTR')

print("Enter low wavelength (nm)")
wl_low = int(input())

print("Enter high wavelength (nm)")
wl_high = int(input())

if wl_high < wl_low:
    wl_low, wl_high = wl_high, wl_low
wl_low = max(350, min(wl_low, 1749))
wl_high = max(351, min(wl_high, 1750))

breaker = False

print("Press 'q' to end the program")
print("Press 'm' to move to the next wavelength")

for i in range(wl_low, wl_high + 1):
    sa.write("STP")
    sa.write("NORMD")
    sa.write("SPAN2.00")
    sa.write("CTRWL" + str(i))
    sa.write("REFL0.00")
    sa.write("RESLN0.05")
    sa.write("LSCL10.00")
    sa.write("RPT")

    while True:
        if keyboard.is_pressed('m'):
            break
        if keyboard.is_pressed('q'):
            breaker = True
            sa.write("STP")
            break

    if breaker:
        break
