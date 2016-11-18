flask_wtf 提供了快速使用的表单类

先看官方例子：

1）定义表单类
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

2）模板中使用
<form method="POST" action="/">
    {{ form.csrf_token }}
    {{ form.name.label }} {{ form.name(size=20) }}
    <input type="submit" value="Go">
</form>


3）视图函数
@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)


再看filed类：
class Field(object):
    """
    Field base class
    """
    errors = tuple()
    process_errors = tuple()
    raw_data = None
    validators = tuple()
    widget = None
    _formfield = True
    _translations = DummyTranslations()
    do_not_call_in_templates = True  # Allow Django 1.4 traversal

    def __new__(cls, *args, **kwargs):
        if '_form' in kwargs and '_name' in kwargs:
            return super(Field, cls).__new__(cls)
        else:
            return UnboundField(cls, *args, **kwargs)

    def __init__(self, label=None, validators=None, filters=tuple(),
                 description='', id=None, default=None, widget=None,
                 render_kw=None, _form=None, _name=None, _prefix='',
                 _translations=None, _meta=None):
        """
        Construct a new field.

        :param label:
            The label of the field.
        :param validators:
            A sequence of validators to call when `validate` is called.
        :param filters:
            A sequence of filters which are run on input data by `process`.
        :param description:
            A description for the field, typically used for help text.
        :param id:
            An id to use for the field. A reasonable default is set by the form,
            and you shouldn't need to set this manually.
        :param default:
            The default value to assign to the field, if no form or object
            input is provided. May be a callable.
        :param widget:
            If provided, overrides the widget used to render the field.
        :param dict render_kw:
            If provided, a dictionary which provides default keywords that
            will be given to the widget at render time.
        :param _form:
            The form holding this field. It is passed by the form itself during
            construction. You should never pass this value yourself.
        :param _name:
            The name of this field, passed by the enclosing form during its
            construction. You should never pass this value yourself.
        :param _prefix:
            The prefix to prepend to the form name of this field, passed by
            the enclosing form during construction.
        :param _translations:
            A translations object providing message translations. Usually
            passed by the enclosing form during construction. See
            :doc:`I18n docs <i18n>` for information on message translations.
        :param _meta:
            If provided, this is the 'meta' instance from the form. You usually
            don't pass this yourself.

        If `_form` and `_name` isn't provided, an :class:`UnboundField` will be
        returned instead. Call its :func:`bind` method with a form instance and
        a name to construct the field.
		"""


1) 因为有errors属性，我们可以直接在模板中用errors，打印出错信息：
{% for error in form.name.errors %}
<span style='color: red'> error </span>
{% endfor %}

2)有 render_kw，我们在定义时或者在模板中可以添加额外的字段，比如
password = PasswordField('Password', validators=[DataRequired(message='provide password')], render_kw=dict(placeholder='can run'))

3)由于Jinja支持宏，所以可以直接写一个宏，后面重复使用，此时要将一些额外信息都放在rend_kw中。
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='mail is incorrect'), Length(1, 64), Email()],\
                        render_kw=dict(placeholder='example@email.com'))
    password = PasswordField('Password', validators=[DataRequired(message='provide password')], \
                             render_kw=dict(placeholder='password'))
    remember_me = BooleanField('Keep me')
    submit = SubmitField('Log In')

模板：
{% macro render_field(field) %}
    <div class="uk-form-row">
        {% for error in field.errors %}
        <span style="color: red;">{{error}}</span>
        {% endfor %}
        <div class="uk-form-label">{{ field.label}}</div>
        <div class="uk-form-controls uk-width-1-3">
            {{ field }}
        </div>
    </div>
{% endmacro %}

然后
{% extends "base.html" %}
{% import 'render_field.html' as macros %}

{% block content %}
	<div class="uk-width-1-1">
        <h1>登录</h1>
        <form method="post" class="uk-form uk-form-stacked">
            {{ form.hidden_tag() }}
            <div class="uk-alert uk-alert-danger uk-hidden"></div>
            {{ macros.render_field(form.email) }}
            {{ macros.render_field(form.password)}}
            {{ macros.render_field(form.remember_me)}}

            <div class="uk-form-row ">
                <input type="submit"  value="Log in" class="uk-button uk-button-primary uk-icon-user">
            </div>
        </form>
    </div>
{% endblock %}

render_field.html 在 templates 文件夹下，flask 能找到。
