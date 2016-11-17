�����չʱǨ�����ݿ�ģ���װ��Alembic��

�ٷ�demo:

from flask import  Flask, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello world'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_ctx():
    return dict(db=db, app=app)

manager.add_command('shell', Shell(make_context=make_shell_ctx))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    age = db.Column(db.String(20))
    weight = db.Column(db.Integer)

if __name__ == '__main__':
    manager.run()


������Ҫ�������ݿ⡣������ shell �У�db.create_all()���������������ݿ⣬�ſ��Ա�Ǩ�ɹ������򲻻��Լ��������ݿ�ġ�
Ȼ��python test.py db init  ���������ʼ��һ���汾�⣬�� git init һ�¡���ʱ�Ὠ��һ�� migrations �ļ��У�����ļ��а����汾���ƵĽŲ����� git ��.git�ļ���һ�¡�
Ȼ��ÿ�θı������ݿ�Ľṹʱ���� python test.py db migrate ̽�����ݿ�仯�Ľṹ���Ὣ�仯�Ų�д�� migrations�ļ��С�
Ȼ���� python test.py db upgrade ��Ǩ������İ汾��Ҳ������migrations �ļ�������鿴�汾�ţ�ֱ��Ǩ�Ƶ�ĳ���汾������ÿ��migratʱ��������һ���ű�������ű�ֻ�������εĸı䣬�������Ծ��Ǩ�Ļ����м�ĸĶ������Ǩ�����ݿ⡣
������downupgrade ���ص�ĳ���汾��