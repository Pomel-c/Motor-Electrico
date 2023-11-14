from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_serial import Serial
from eventlet import monkey_patch
import random
import os

# Correr serve online 
# ssh -R 80:localhost:5000 localhost.run
# btunnel http --key JDJhJDEyJEZ3L3dvWGtkWVQ3ZVhsYkVJbFREUE9DYkwwTVJoanhFRlhGRXV2UmE4RDVvVGJvdWtkWE1L --port 5000

monkey_patch()

app = Flask(__name__)
app.config['SERIAL_TIMEOUT'] = 0.2
# Puerto de USB del arduino
# app.config['SERIAL_PORT'] = 'COM4' # Windows
app.config['SERIAL_PORT'] = './dev/cu.usbserial-1410' # MacOs
# Baudios del arduino
app.config['SERIAL_BAUDRATE'] = 9600
app.config['SERIAL_BYTESIZE'] = 8
app.config['SERIAL_PARITY'] = 'N'
app.config['SERIAL_STOPBITS'] = 1
app.config['SECRET_KEY'] = 'secret!'

ser = Serial(app)
socketio = SocketIO(app)

print("Server running...")

# Correr en localhost
print("http://localhost:5000")

@app.route('/')
def index():
    # Motores siendo medidos por el Arduino
    motors = [
        {'id': 1, 'name': 'Motor 1 - Cinta transportadora', 'power': 0.5},
        {'id': 2, 'name': 'Motor 2 - Compresor taller', 'power': 1.0},
        {'id': 3, 'name': 'Motor 3 - Tornillo sin fin', 'power': 1.5},
        {'id': 4, 'name': 'Motor 4', 'power': 2.5}
        # Agrega más motores según sea necesario
    ]
    return render_template('index.html', motors=motors)


@ser.on_message()
def handle_message(medida):
    medida = medida.decode().replace('\r','').replace('\n',' ')
    
    # voltaje = float(medida.split(' ')[0]) * random.uniform(0.5, 5)
    # voltaje = float("{:.2f}".format(voltaje))

    # temperatura = float( medida.split(' ')[1]) * random.uniform(0.1, 10)
    # temperatura = float("{:.2f}".format(temperatura))

    # rpm = float(medida.split(' ')[2]) * random.uniform(0.5, 5)
    # rpm = float("{:.2f}".format(rpm))

    # corriente = float(medida.split(' ')[3]) * random.uniform(0.5, 2.5)
    # corriente = float("{:.2f}".format(corriente))
    
    voltaje = float(medida.split(' ')[0]) * random.uniform(0.5, 5)
    voltaje = float("{:.2f}".format(voltaje))

    temperatura = float( medida.split(' ')[1]) * random.uniform(0.1, 10)
    temperatura = float("{:.2f}".format(temperatura))

    rpm = float(medida.split(' ')[2]) * random.uniform(0.5, 5)
    rpm = float("{:.2f}".format(rpm))

    corriente = float(medida.split(' ')[3]) * random.uniform(0.5, 2.5)
    corriente = float("{:.2f}".format(corriente))

    # Horsepower = Torque x RPM / 5,252.
    # Power = Voltage x Current x Power Factor
    # Torque = Power / 746
    horsepower = (float(voltaje) * float(corriente) * 0.8) / 746
    
    # print(voltaje, temperatura, rpm, corriente, horsepower)

    socketio.emit('data',{'temperatura':temperatura,'voltaje':voltaje,'rpm':rpm,'corriente':corriente, 'horsepower': horsepower})

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/motor_details/<int:motor_id>')
def motor_details(motor_id):
    # Define un diccionario con los detalles de los motores (puedes reemplazar esto con tus datos)
    # Motores con la placa caracteristica
    motors = {
        1: {
            'voltage': '220-240 V',
            'rpm': 1850,
            'current': '2.5 A',
            'frequency': '50 Hz',
            'max_temp': 80,
            'rated_power': 0.5
        },
        2: {
            'voltage': '220-240 V',
            'rpm': 2000,
            'current': '3.0 A',
            'frequency': '60 Hz',
            'max_temp': 90,
            'rated_power': 1.0
        },
        3: {
            'voltage': '220-240 V',
            'rpm': 2600,
            'current': '3.0 A',
            'frequency': '50 Hz',
            'max_temp': 75,
            'rated_power': 1.5
        },
        4: {
            'voltage': '220-240 V',
            'rpm': 1600,
            'current': '2.5 A',
            'frequency': '50 Hz',
            'max_temp': 90,
            'rated_power': 2.5
        }
        # Agrega más motores según sea necesario
    }

    motor_data = motors.get(motor_id, None)

    if motor_data:
        return render_template('motor_details.html', **motor_data)
    else:
        return "Motor not found"

@app.route('/contact', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Aquí podrías procesar los datos del formulario, como enviar correos electrónicos, etc.
        return render_template('contact_success.html', name=name)
    return render_template('contact_form.html')


if __name__ == '__main__':
    socketio.run(app,debug = False)