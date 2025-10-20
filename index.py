from flask import Flask, render_template, request, flash
import json

try:
    with open('problems.json', 'r', encoding='utf-8') as f:
        problems = json.load(f)
except:
    problems = {}

app = Flask(__name__)
app.secret_key = 'PralaterOJ-default-secret-key'  # 添加secret_key以支持flash消息

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/problem/<pid>')
def problem(pid):
    if pid == 'list':
        return render_template('problemlist.html', problems=problems)
    return render_template('watchproblem.html', problem=problems[pid])

@app.route('/newproblem', methods=['GET', 'POST'])
def newproblem():
    if request.method == 'POST':
        problemid = request.form['pid']
        problemname = request.form['title']
        problemdesc = request.form['content']
        probleminfo = request.form['inputformat']
        problemoufo = request.form['outputformat']
        problemsai1 = request.form['sampleinput1']
        problemsao1 = request.form['sampleoutput1']

        # 修复添加题目到字典的逻辑
        problems[problemid] = {
            "name": problemname,
            'id': problemid,
            'describe': problemdesc,
            'inputformat': probleminfo,
            'outputformat': problemoufo,
            'samples': [[problemsai1, problemsao1]]
        }

        with open('problems.json', 'w', encoding='utf-8') as f:
            json.dump(problems, f, ensure_ascii=False, indent=4)

        flash("problem added successfully")
        return render_template('newproblem.html')
    return render_template('newproblem.html')

if __name__ == '__main__':
    app.run(debug=True)