from flask import Flask, render_template
import json

try:
    with open('problems.json', 'r', encoding='utf-8') as f:
        problems = json.load(f)
except:
    problems = {}
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/problem/<pid>')
def problem(pid):
    if pid == 'list':
        return render_template('problemlist.html', problems=problems)
    return render_template('watchproblem.html', problem=problems[pid])

if __name__ == '__main__':
    app.run(debug=True)