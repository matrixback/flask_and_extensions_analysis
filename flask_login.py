# coding: utf-8
flask_login 扩展的工作原理

先看官方网站的demo：

import flask
import flask_login

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'SUPER SECRET STRING'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'foo@bar.tld': {'pw': 'secret'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('eamil')
    if email not in users:
        return

    user = User()
    user.id = email

    user.is_authenticated = (request.form['pw'] == users[email]['pw'])

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
                <form method='post' action='login'>
                    <input type='text' name='email' id='email' placehold='email'></input>
                    <input type='password' name='pw' id='pw' palcehold='password'></input>
                    <input type='submit' value='submit'></input>
                </form>
                '''
    email = flask.request.form['email']
    if flask.request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: '+flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return "Logged out"


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

if __name__ == '__main__':
    app.run(debug=True)



工作原理：
登录函数 login_user 中只在session中设置一个user_id,然后在需要时，根据 user_id 加载用户。

为了灵活性，flask_login将指定user_id的任务交给了我们。
我们需要在用户模型中实现4个函数，is_active, is_authenticated, is_anonymous, get_id。
为了方便，flask_login的UserMixIN 提供了默认实现。
其中最重要的是 get_id,其代码为：
def get_id(self):
        try:
            return text_type(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

即我们的用户模型，必须要有 id 属性。有了这个id属性，login_user 就会根据这个id，产生一个cookie，保存在客户端。
login_user的代码为：
def login_user(user, remember=False, force=False, fresh=True):
    if not force and not user.is_active:
        return False

    user_id = getattr(user, current_app.login_manager.id_attribute)()
    session['user_id'] = user_id
    session['_fresh'] = fresh
    session['_id'] = _create_identifier()

    if remember:
        session['remember'] = 'set'

    _request_ctx_stack.top.user = user
    user_logged_in.send(current_app._get_current_object(), user=_get_user())
    return True

其中 user_id = getattr(user, current_app.login_manager.id_attribute)()，追踪过去，就是user_id = get_id()
通过get_id 和 login_user,我们实现了登录用户。

另外一个就是加载用户，flask_login 只能从request的session中取出id,我们需要实现一个回调函数，用这个id，得到一个user对象。一般为：
@login_manager.user_load
def user_load(user_id):
    return User.get(int(user_id))

