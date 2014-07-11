import sublime
import sublime_plugin
import urllib.request
import threading
import json
import os
import sys
import subprocess
import locale
from jsonschema import validate
# Add jsonschema folder to C:\Program Files\Sublime Text 3 as a temporary workaround on Windows
# Add jsonschema folder to /Applications/Sublime\ Text.app/Contents/MacOS/ as a temporary workaround on Mac
# https://pypi.python.org/pypi/jsonschema/2.3.0

if os.name == 'nt':
    plat = 'win'
elif sys.platform == 'darwin':
    plat = 'osx'
else:
    plat = 'linux'


if plat == 'win':
    try:
        import _winreg
    except (ImportError):
        import winreg as _winreg
    from ctypes import windll, create_unicode_buffer

class NotFoundError(Exception):
    pass


if sys.version_info >= (3,):
    installed_dir, _ = __name__.split('.')
else:
    installed_dir = os.path.basename(os.getcwd())


class KTerminalSelector():
    default = None

    @staticmethod
    def get():
        package_dir = os.path.join(sublime.packages_path(), installed_dir)
        default = None

        if plat == 'win':
            if os.path.exists(os.environ['SYSTEMROOT'] +
                    '\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'):
                # This mimics the default powershell colors since calling
                # subprocess.POpen() ends up acting like launching powershell
                # from cmd.exe. Normally the size and color are inherited
                # from cmd.exe, but this creates a custom mapping, and then
                # the LaunchPowerShell.bat file adjusts some other settings.
                key_string = 'Console\\%SystemRoot%_system32_' + \
                    'WindowsPowerShell_v1.0_powershell.exe'
                try:
                    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                        key_string)
                except (WindowsError):
                    key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
                        key_string)
                    _winreg.SetValueEx(key, 'ColorTable05', 0,
                        _winreg.REG_DWORD, 5645313)
                    _winreg.SetValueEx(key, 'ColorTable06', 0,
                        _winreg.REG_DWORD, 15789550)
                default = os.path.join(package_dir, 'PS.bat')
                sublime_terminal_path = os.path.join(sublime.packages_path(), installed_dir)
                # This should turn the path into an 8.3-style path, getting around unicode
                # issues and spaces
                buf = create_unicode_buffer(512)
                if windll.kernel32.GetShortPathNameW(sublime_terminal_path, buf, len(buf)):
                    sublime_terminal_path = buf.value
                os.putenv('sublime_terminal_path', sublime_terminal_path.replace(' ', '` '))
            else :
                default = os.environ['SYSTEMROOT'] + '\\System32\\cmd.exe'

        elif plat == 'osx':
            default = os.path.join(package_dir, 'Terminal.sh')
            if not os.access(default, os.X_OK):
                os.chmod(default, 0o755)

        else:
            ps = 'ps -eo comm | grep -E "gnome-session|ksmserver|' + \
                'xfce4-session" | grep -v grep'
            wm = [x.replace("\n", '') for x in os.popen(ps)]
            if wm:
                if wm[0] == 'gnome-session':
                    default = 'gnome-terminal'
                elif wm[0] == 'xfce4-session':
                    default = 'terminal'
                elif wm[0] == 'ksmserver':
                    default = 'konsole'
            if not default:
                default = 'xterm'

        KTerminalSelector.default = default
        return default
class KTerminalCommand():
    def get_path(self, paths):
        if paths:
            return paths[0]
        elif self.window.active_view():
            return self.window.active_view().file_name()
        elif self.window.folders():
            return self.window.folders()[0]
        else:
            sublime.error_message('Terminal: No place to open terminal to')
            return False

    def run_terminal(self, dir_, parameters):
        try:
            if not dir_:
                raise NotFoundError('The file open in the selected view has ' +
                    'not yet been saved')
            for k, v in enumerate(parameters):
                parameters[k] = v.replace('%CWD%', dir_)
            args = [KTerminalSelector.get()]
            args.extend(parameters)
            encoding = locale.getpreferredencoding(do_setlocale=True)
            if sys.version_info >= (3,):
                cwd = dir_
            else:
                cwd = dir_.encode(encoding)
            print(args)
            subprocess.Popen(args, cwd=cwd)
        except (OSError) as exception:
            print(str(exception))
            sublime.error_message('Terminal: The terminal ' +
                KTerminalSelector.get() + ' was not found')
        except (Exception) as exception:
            sublime.error_message('Terminal: ' + str(exception))


class KOpenTerminalCommand(sublime_plugin.WindowCommand, KTerminalCommand):
    def run(self, paths=[], parameters=None):
        path = self.get_path(paths)
        if not path:
            return

        if parameters == None:
            settings = sublime.load_settings('Terminal.sublime-settings')
            parameters = settings.get('parameters')

        if not parameters:
            parameters = []

        if os.path.isfile(path):
            path = os.path.dirname(path)
        self.run_terminal(path, parameters)

class KRunCommand(sublime_plugin.WindowCommand):

    def run(self):
        if (plat == 'win'):
            file_name = self.window.folders()[0] + '\\project.json'
        else:
            file_name = self.window.folders()[0] + '/project.json'
        try:
            json_file = json.load(open(file_name))
        except IOError:
            print("project.json not found")
            return
        self.commands = []
        try:
            json_commands = json_file['commands']
            for command in json_commands:
                self.commands.append('k ' + command)
        except LookupError:
            pass
        self.commands.append('k build')
        self.commands.append('kpm restore')
        self.commands.append('kpm pack')
        self.window.show_quick_panel(self.commands, self.commandlist)
    def commandlist(self, position):
        if (position > -1):
            self.window.run_command('k_open_terminal', {'parameters':[self.commands[position]]})
            i = 0;
        else:
            return

class KValidateSchemaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        threads = []
        thread = ValidateSchemaApiCall(5, self.view)
        threads.append(thread)
        thread.start()
        # self.output_view = self.window.get_output_panel("textarea")
        # self.window.run_command("show_panel", {"panel": "output.textarea"})
        self.handle_threads(threads)

    def is_enabled(self):
        # Handle case with no file name
        if (self.view.file_name() == None):
            return False
        if (plat == 'win'):
            return (self.view.file_name().split('\\')[-1] == 'project.json')
        else:
            return (self.view.file_name().split('/')[-1] == 'project.json')

    def handle_threads(self, threads, offset=0, i=0, dir=1):
        message = "JSON Schema successfully validated"
        next_threads = []
        for thread in threads:
            if thread.is_alive():
                next_threads.append(thread)
                continue
            if thread.result == False:
                message = thread.message
                continue
        threads = next_threads

        if len(threads):
            # This animates a little activity indicator in the status area
            before = i % 8
            after = (7) - before
            if not after:
                dir = -1
            if not before:
                dir = 1
            i += dir
            self.view.set_status('validate_schema', 'Validating [%s=%s]' % \
                (' ' * before, ' ' * after))
         
            sublime.set_timeout(lambda: self.handle_threads(threads,
                offset, i, dir), 100)
            return

        self.view.erase_status("validate_schema")
        sublime.status_message(message)

class KValidateSchemaApiCall(threading.Thread):
    def __init__(self, timeout, view):
        self.message = "JSON Schema successfully validated"
        self.timeout = timeout
        self.result = None
        self.view = view
        threading.Thread.__init__(self)

    def run(self):
        try:
            request = urllib.request.Request("http://schemastore.org/schemas/json/project.json",
                headers={"User-Agent": "Sublime"})
            http_file = urllib.request.urlopen(request, timeout=self.timeout)
            self.result = http_file.read().decode('utf-8')
            try:
                schema = json.loads(self.result)
                content = json.loads(self.view.substr(sublime.Region(0, self.view.size())))
            except ValueError as e:
                self.result = False
                self.message = "Not a valid JSON file"
                return
            try:
                validate(content, schema)
            except jsonschema.exceptions.ValidationError as e:
                self.result = False
                self.message = "JSON schema validation failed"
            return

        except (urllib.request.HTTPError) as e:
            self.message = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
        except (urllib.request.URLError) as e:
            self.message = '%s: URL error %s contacting API' % (__name__, str(e.reason))
        self.result = False
        return

class KTestCommand(sublime_plugin.WindowCommand):
    def run(self):
        print('hi')
        return

class RetrievePackageNames(threading.Thread):
    def __init__(self,timeout):
        self.timeout = timeout
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        try:
            request = urllib.request.Request("https://www.myget.org/F/aspnetrelease/api/v2/Packages()?$select=Id&$format=json&orderby=DownloadCount&$top=100",
                headers={"User-Agent": "Sublime"})
            http_file = urllib.request.urlopen(request, timeout=self.timeout)
            self.result = []
            response = json.loads(http_file.read().decode('utf-8'))['d']
            for package in response:
                self.result.append(package['Id'])
            print(self.result)
            return
        except (urllib.request.HTTPError) as e:
            self.message = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
        except (urllib.request.URLError) as e:
            self.message = '%s: URL error %s contacting API' % (__name__, str(e.reason))
        self.result = False
        return
