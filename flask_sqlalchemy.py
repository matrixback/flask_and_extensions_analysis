1�����ã�
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:xxxxxxx@localhost/flask_test��

2������ģ�ͣ�
class User(db.Model):
	__tablename__ = �������������ݿ�����ƣ�Ϊ�˷���ʹ�á�
	id = ....   ��flask_login��ʱ�����Ҫ�С�
	def __str__(self):
		return ��<User %r>�� % self.name
	def __repr__
return ��<User %r>�� % self.name

3��Ϊ�˷��㣬��User�ȷŽ�shell��make_context�С�
def shell_make_context():
	return dict(User=User,....)
manger.add_commad(��shell��, Shell(make_context=shell_make_context))

����2���� %r ����ֱ�ӽ����Ŵ��룬���ټ����š�
>>> a = "%r" % 'matrix'
>>> a
"'matrix'"
>>> type(a)
<class 'str'>
>>> a = "%s" % 'matrix'
>>> a
'matrix'

5��	���õĲ���
db.create_all()
u = User...
u.name=, u.age = 
db.session.add()
db.session.commit
User.query.all()
User.query.filter().first()

6��	��ϵ
�����category_id = db.Column(db.Integer, db.ForeignKey('category.id')
һ�Զࣺ��ϵ����ƿ�������Ϊ�˴�Role��Ҫ�ҳ������Լ��ģ���һ�Զ��ϵ��������һ���ⷽ������ϵ��
��user�Ƿ�����Ҫ������Ҫһ�����������role�����

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')    # ������ģ����ֱ����role���������

    def __repr__(self):
        return "<Role %r" % self.name

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User %r" % self.username

���һ�����ַ�������һ�Զ�ķ���������ƣ����ǿ���ʵ�֣������߽������relationship�ŵ�����ࡣ

һ��һ��ϵ���Ƿ���Ҫ��ϵ��������ʹ�ö��һ�Ĺ�ϵ��ֻҪ��uselist��Ϊfalse��

relationship�ļ�����ϵѡ�
backref: ��������
lazy�����á�����select��ѯʱ���Ȳ���ѯ������ֻ�Ǽ�¼��䣬��������á�
