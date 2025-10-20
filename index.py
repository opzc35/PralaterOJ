from flask import Flask, render_template

problems = { "P1001": {"name":"A+B Problem", "id":"P1001", "describe": u"给你两个整数，请你输出他们的和。", "inputformat": u"一行两个整数a和b", "outputformat": u"输出他们的和", "samples": [["1 1", "2"], ["2 2", 4]]}}
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/watch/<pid>')
def watch(pid):
    return render_template('watchproblem.html', problem=problems[pid])

if __name__ == '__main__':
    app.run(debug=True)