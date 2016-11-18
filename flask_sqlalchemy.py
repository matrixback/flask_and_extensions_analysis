1）配置：
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:xxxxxxx@localhost/flask_test’

2）创建模型：
class User(db.Model):
	__tablename__ = ‘’’’，数据库的名称，为了方便使用。
	id = ....   用flask_login的时候必须要有。
	def __str__(self):
		return ‘<User %r>’ % self.name
	def __repr__
return ‘<User %r>’ % self.name

3）为了方便，将User等放进shell的make_context中。
def shell_make_context():
	return dict(User=User,....)
manger.add_commad(‘shell’, Shell(make_context=shell_make_context))

上面2）用 %r 可以直接将引号代入，不再加引号。
>>> a = "%r" % 'matrix'
>>> a
"'matrix'"
>>> type(a)
<class 'str'>
>>> a = "%s" % 'matrix'
>>> a
'matrix'

5）	常用的操作
db.create_all()
u = User...
u.name=, u.age = 
db.session.add()
db.session.commit
User.query.all()
User.query.filter().first()

6）	关系
外键：category_id = db.Column(db.Integer, db.ForeignKey('category.id')
一对多：关系的设计看需求，因为此处Role需要找出引用自己的，是一对多关系，所以在一的这方创建关系。
而user那方不需要，它需要一个外键，引用role这个表。

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')    # 可以在模型中直接用role引用这个。

    def __repr__(self):
        return "<Role %r" % self.name

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User %r" % self.username

多对一：两种方案，用一对多的方案（反设计，但是可以实现），或者将外键和relationship放到多这侧。

一对一关系：是否需要关系？？可以使用多对一的关系，只要将uselist设为false。

relationship的几个关系选项：
backref: 反向引用
lazy：常用。利用select查询时，先不查询出来，只是记录语句，这个很有用。
