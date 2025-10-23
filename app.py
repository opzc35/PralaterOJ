from click import confirmation_option
from flask import Flask, render_template, request, flash
import json
import os
import sys
from flask_sqlalchemy import SQLAlchemy
import click
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

#前置
app = Flask(__name__)
app.secret_key = 'PralaterOJ-default-secret-key'
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    poisition = db.Column(db.String(10))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.cli.command()
@click.option('--drop', is_flag=True, help="Create after drop.")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
@click.option('--username', prompt=True, help=u'请输入你要增加的管理员的用户名')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help=u'请输入管理员密码')
def admin(username, password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        user.name = username
        user.set_password(password)
    else:
        click.echo(u"没有找到用户，开始重新创建")
        user = User(name=username, poisition='admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo(u"Done.")
try:
    with open('problems.json', 'r', encoding='utf-8') as f:
        problems = json.load(f)
except:
    problems = {}

loginmanager = LoginManager(app)

# 账号处理

@loginmanager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

# Web
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        user = User(name=username, poisition='normal')
        db.session.add(user)
        db.session.commit()
        flash(u"注册成功")
        return render_template('register.html')
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)