flask_script 

# Manager对象，有个_commands私有字典属性，添加的命令全放在这个字典里。
class Manager(object):

    def __init__(self, app=None, with_default_commands=None, usage=None,
                 help=None, description=None, disable_argcomplete=False):

        self.app = app

        self._commands = dict()
        self._options = list()

        self.usage = usage
        self.help = help if help is not None else usage
        self.description = description if description is not None else usage
        self.disable_argcomplete = disable_argcomplete
        self.with_default_commands = with_default_commands

        self.parent = None


# add_command解决命令name,namespace的问题，并将commad 加入_commands。
# 如果参数有2个，则将第一个参数作为name，否则的话，取出函数的__name__作为_commands用的key。

def add_command(self, *args, **kwargs):
        """
        Adds command to registry.

        :param command: Command instance
        :param name: Name of the command (optional)
        :param namespace: Namespace of the command (optional; pass as kwarg)
        """

        if len(args) == 1:
            command = args[0]
            name = None

        else:
            name, command = args

        if name is None:
            if hasattr(command, 'name'):
                name = command.name

            else:
                name = type(command).__name__.lower()
                name = re.sub(r'command$', '', name)

        if isinstance(command, Manager):
            command.parent = self

        if isinstance(command, type):
            command = command()

        namespace = kwargs.get('namespace')
        if not namespace:
            namespace = getattr(command, 'namespace', None)

        if namespace:
            if namespace not in self._commands:
                self.add_command(namespace, Manager())

            self._commands[namespace]._commands[name] = command

        else:
            self._commands[name] = command



# commad函数是个装饰器，将被装饰的函数，加入_command。
# 模式是：
# @manager.command
# def hello:
#     print(current_app.name)   可以打印current_app.name，说明激活了程序上下文。
#	  print('hello')
# 然后在命令行执行 python manage.py hello
#

def command(self, func):
        """
        Decorator to add a command function to the registry.

        :param func: command function.Arguments depend on the
                     options.

        """

        command = Command(func)
        self.add_command(func.__name__, command)

        return func

# 添加两个默认的命令。
# “shell” 对应 Shell 对象，'server' 对应 Server对象，这两个对象都是Command对象，实现了__call__方法。
def add_default_commands(self):
        """
        Adds the shell and runserver default commands. To override these,
        simply add your own equivalents using add_command or decorators.
        """

        if "shell" not in self._commands:
            self.add_command("shell", Shell())
        if "runserver" not in self._commands:
            self.add_command("runserver", Server())


# Shell 主要有两个作用，其一为创建/得到一个上下文 make_context，在解释器中不用再导入。其二就是执行时，开启一个shell。
# 一般模式是：manager.add_command('shell', Shell(make_context=make_shell_context)), 其中的make_shell_context返回一个字典：
# def make_shell_context():
#     return dict(app=app, db=db)   # 返回的字典是{'app'=app, 'db'=db}


class Shell(Command):
    help = description = 'Runs a Python shell inside Flask application context.'

    def __init__(self, banner=None, make_context=None, use_ipython=True,
                use_bpython=True):

        self.banner = banner or self.banner
        self.use_ipython = use_ipython
        self.use_bpython = use_bpython

        if make_context is None:
            make_context = lambda: dict(app=_request_ctx_stack.top.app)

        self.make_context = make_context

    def get_context(self):
        """
        Returns a dict of context variables added to the shell namespace.
        """
        return self.make_context()

    def run(self, no_ipython, no_bpython):
        """
        Runs the shell.  If no_bpython is False or use_bpython is True, then
        a BPython shell is run (if installed).  Else, if no_ipython is False or
        use_python is True then a IPython shell is run (if installed).
        """

        context = self.get_context()

        if not no_bpython:
            # Try BPython
            try:
                from bpython import embed
                embed(banner=self.banner, locals_=context)
                return
            except ImportError:
                pass

        if not no_ipython:
            # Try IPython
            try:
                try:
                    # 0.10.x
                    from IPython.Shell import IPShellEmbed
                    ipshell = IPShellEmbed(banner=self.banner)
                    ipshell(global_ns=dict(), local_ns=context)
                except ImportError:
                    # 0.12+
                    from IPython import embed
                    embed(banner1=self.banner, user_ns=context)
                return
            except ImportError:
                pass

        # Use basic python shell
        code.interact(self.banner, local=context)


class Server(Command):
    def __init__(self, host='127.0.0.1', port=5000, use_debugger=None,
                 use_reloader=None, threaded=False, processes=1,
                 passthrough_errors=False, **options):

        self.port = port
        self.host = host
        self.use_debugger = use_debugger
        self.use_reloader = use_reloader if use_reloader is not None else use_debugger
        self.server_options = options
        self.threaded = threaded
        self.processes = processes
        self.passthrough_errors = passthrough_errors

    def __call__(self, app, host, port, use_debugger, use_reloader,
               threaded, processes, passthrough_errors):
        # we don't need to run the server in request context
        # so just run it directly
        app.run(host=host,
                port=port,
                debug=use_debugger,
                use_debugger=use_debugger,
                use_reloader=use_reloader,
                threaded=threaded,
                processes=processes,
                passthrough_errors=passthrough_errors,
                **self.server_options)


class Clean(Command):
    "Remove *.pyc and *.pyo files recursively starting at current directory"

class ShowUrls(Command):
    """
        Displays all of the url matching routes for the project
    """


另外，flask_migrate 包自动整理了一个Migrate_command，我们直接添加就可以呢。
manager.add_command('db', MigrateCommand)，在 db 后面可以直接跟一些命令，比如 python hello.py db init。