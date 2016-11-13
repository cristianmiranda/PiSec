from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'

@app.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)

@app.route('/teclado/<number>')
def teclado(number):
	with open("/home/pi/Desktop/Flask/password","wb") as fo:
		fo.write(number)
        return 'Saved!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
