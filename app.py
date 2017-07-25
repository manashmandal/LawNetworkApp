from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html', title="Homepage")

@app.route('/extend')
def extend():
    return render_template('extend.html', title='Extension')


if __name__ == '__main__':
    app.run(debug=True)

