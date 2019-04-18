
''' Program make a simple calculator that can add, subtract, multiply and divide using functions '''

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/calculate', methods = ['POST'])

def calculate():
    choice = request.form['operation']
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    if choice == '1':
        result = num1 + num2

    elif choice == '2':
        result = num1 - num2

    elif choice == '3':
        result = num1 * num2

    elif choice == '4':
        result = num1 / num2
    else:
        result = "Invalid input"
    return render_template("index.html", result = result)

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
