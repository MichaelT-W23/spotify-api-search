from flask import Flask, render_template
from routes import routes_blueprint

app = Flask(__name__)

app.register_blueprint(routes_blueprint)

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)