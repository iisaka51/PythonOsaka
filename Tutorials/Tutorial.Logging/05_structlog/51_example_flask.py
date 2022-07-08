from flask import Flask, render_template
from some_module import some_function

app = Flask(__name__, template_folder='templates')
@app.route('/greeting/<name>')
def index(name):
    name = some_function(name)
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)

