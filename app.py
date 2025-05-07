from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/supplies')
def supplies():
    return render_template('supplies.html')

@app.route('/drivers')
def drivers():
    return render_template('drivers.html')

@app.route('/recipients')
def recipients():
    return render_template('recipients.html')

@app.route('/deliveries')
def deliveries():
    return render_template('deliveries.html')

@app.route('/deliveries-supplies')
def deliveries_supplies():
    return render_template('deliveries_supplies.html')

if __name__ == '__main__':
    app.run(port=9313, debug=True)