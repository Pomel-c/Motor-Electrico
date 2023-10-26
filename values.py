import serial

ser = serial.Serial('COM4', 9600)

while True:
    data = ser.readline().decode().strip()
    voltage = data.split(' ')[0]
    temperature = data.split(' ')[1]
    rpm = data.split(' ')[2]
    corriente = data.split(' ')[3]

    print(f'Voltage: {voltage}V')
    print(f'Temperatura: {temperature}°C')
    print(f'RPM: {rpm}rpm')
    print(f'Corriente: {corriente}A')
    print('------------------')

