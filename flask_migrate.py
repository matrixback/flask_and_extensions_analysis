这个扩展时迁移数据库的，封装了Alembic。

官方demo:

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


首先需要创建数据库。可以在 shell 中，db.create_all()创建。必须有数据库，才可以变迁成功，否则不会自己创建数据库的。
然后python test.py db init  这个命令会初始化一个版本库，和 git init 一致。此时会建立一个 migrations 文件夹，这个文件夹包含版本控制的脚步。和 git 的.git文件夹一致。
然后每次改变完数据库的结构时，用 python test.py db migrate 探测数据库变化的结构，会将变化脚步写入 migrations文件夹。
然后用 python test.py db upgrade 搬迁到最近的版本。也可以在migrations 文件夹里面查看版本号，直接迁移到某个版本。不过每次migrat时，都产出一个脚本，这个脚本只包含本次的改变，如果你跳跃变迁的话，中间的改动不会变迁到数据库。
可以用downupgrade 返回到某个版本。