#!/usr/bin/env Python
# coding=utf-8

from flask import Flask, render_template, request, redirect, url_for, make_response, abort
# 正则表达匹配
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from flask.ext.script import Manager

from os import path


import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 建立一个转化器类
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
# 将转换器中的第一个参数付给正则表达式
        self.regex = items[0]


app = Flask(__name__)
# 把这个转换器的新加到app
app.url_map.converters['regex'] = RegexConverter

manager = Manager(app)

@app.route('/')
def index():
    response = make_response(render_template('index.html', title='welcome'))

    response.set_cookie('username','')

    return response

@app.route('/services')
def services():
    return 'Service'

@app.route('/about')
def about():
    return 'About'

# @app.route('/user/<int:user_id>')
# def user(user_id):
#     return 'User %s' % user_id
# 应用该转换器3个字符
@app.route('/user/<regex("[a-z]{3}"):user_id>')
def user(user_id):
    return 'User %s' % user_id

# 如果url不写自动补上'/'
# 匹配是有规则的
@app.route('/projects/')
@app.route('/our-works/')
def projects():
    return 'The project page'

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    else:
        username = request.args['username']
    return render_template('login.html', method=request.method)

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath, 'static/uploads', secure_filename(f.filename))
        # 检查该文件名
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('upload.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# 自动刷新
@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)

if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)
