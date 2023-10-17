from flask import Flask, render_template
from flask import Flask, render_template, request

app = Flask(__name__)

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


@app.route('/motor_details/<int:motor_id>')
def motor_details(motor_id):
    # Define un diccionario con los detalles de los motores (puedes reemplazar esto con tus datos)
    # Motores con la placa caracteristica
    motors = {
        1: {
            'voltage': '220-240 V',
            'rpm': 1500,
            'current': '2.5 A',
            'frequency': '50 Hz',
            'max_temp': 80,
            'rated_power': 0.5
        },
        2: {
            'voltage': '240-250 V',
            'rpm': 1800,
            'current': '3.0 A',
            'frequency': '60 Hz',
            'max_temp': 90,
            'rated_power': 0.75
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
    app.run(debug=True)
