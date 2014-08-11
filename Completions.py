import sublime
import sublime_plugin
import threading
import urllib.request, urllib.parse
import json
import re

SETTINGS_FILE = 'Kulture.sublime-settings'
AC_OPTS = sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS

class KKultureComplete (sublime_plugin.TextCommand):
    def run(self, edit, action = None, **args):
        print("DOT_COMPLETE:::::Code Reached")
        self.view.insert(edit, self.view.sel()[0].begin(), args['key'])
        self.view.run_command('auto_complete')
        return True

class KKultureCompletion( sublime_plugin.EventListener):
    def __init__(self):
        self.result = {}
        self.cache = []
        self.thread = RetrievePackageNames(5)
        self.thread.start()
        while(self.thread.is_alive()):
            pass
        response = self.thread.response
        for package in response:
            t = (package['Id'],package['Id'])
            # if t not in self.result:
            regex = r'([-a-zA-Z0-9\.]+)\/([-a-zA-Z0-9\.]+)$'
            match = re.search(regex, package['__metadata']['media_src'])
            try:
                if (match.group(1),match.group(1)) not in self.cache:
                    self.cache.append((match.group(1), match.group(1)))
                try:
                    self.result[match.group(1)].append((match.group(2), match.group(2)))
                except KeyError as e:
                    self.result[match.group(1)] = []
                    self.result[match.group(1)].append((match.group(2), match.group(2)))
            except AttributeError as e:
                pass

    def on_query_completions(self, view, prefix, locations):
        pos = locations[0]
        scopes = view.scope_name(pos).split()
        if "source.json" not in scopes:
            return []
        else:
            doc = view.substr(sublime.Region(0,view.size()))

            whitespaces = 0;
            for index, char in enumerate(doc[0:pos]):
                if char == '\n' or char == '\r' or char == ' ' or char == '\t':
                    whitespaces += 1

            doc = doc.replace('\n', '').replace('\r','').replace(' ', '').replace('\t', '')
            pos = pos - whitespaces

            depth = -1
            tokens = []
            token_regex = re.compile(r'"([-a-zA-Z0-9+]+)":{')

            for index, char in enumerate(doc):
                if char == '{':
                    depth += 1
                    token_regex = r'"([-a-zA-Z0-9+]+)":{$'
                    match = re.search(token_regex, doc[0:index+1])
                    try:
                        tokens.append(match.group(1))
                    except AttributeError as e:
                        pass
                if char == '}':
                    depth -= 1
                    try:
                        tokens.pop()
                    except IndexError as e:
                        pass
                if index==pos:
                    if (depth == 1 and tokens[0] == 'dependencies'):
                        # Version number
                        version_regex = r'(?:,|{|\[])"([-a-zA-Z0-9.*]+)":"[-a-zA-Z0-9.*]*$'
                        try:
                            package_name = re.search(version_regex, doc[0:index]).group(1)
                            return (self.result[package_name], AC_OPTS)
                        except AttributeError as e:
                            pass
                        except KeyError as e:
                            # TODO: Not in cache. Make HTTP request to feth completions on that package
                            return AC_OPTS
                        # Package name
                        return (self.cache, AC_OPTS)
                    elif depth == 0:
                        # In future, get completions dynamically from http://schemastore.org/schemas/json/project
                        # Replace word completions with snippets
                        return ([('version', 'version" : "$1"'),
                                    ('dependencies', 'dependencies" : {\n\t"$1": "$2"\n}'),
                                    ('commands', 'commands" : {\n\t"$1": "$2"\n}'),
                                    ('configurations', 'configurations" : {\n\t"$1": {}\n}'),
                                    ('compilationOptions', 'compilationOptions'),
                                    ('frameworks', 'frameworks" : {\n\t"$1": "$2"\n}'),
                                    ('description', 'description" : "$1"'),
                                    ('authors', 'authors" : [\n\t"$1"\n]'),
                                    ('code', 'code" : {\n\t"$1": "$2"\n}'),
                                    ('shared', 'shared" : {\n\t"$1": "$2"\n}'),
                                    ('exclude', 'exclude" : {\n\t"$1": "$2"\n}'),
                                    ('preprocess', 'preprocess" : {\n\t"$1": "$2"\n}'),
                                    ('resources', 'resources')
                                ], AC_OPTS)
                    else:
                        break

            return AC_OPTS


class RetrievePackageNames(threading.Thread):
    def __init__(self,timeout):
        self.timeout = timeout
        self.response = None
        threading.Thread.__init__(self)

    def run(self):
        try:
            request = urllib.request.Request("https://www.myget.org/F/aspnetrelease/api/v2/Packages()?"
                + "$select=Id&"
                + "$format=json&"
                + "orderby=DownloadCount&"
                + "$top=100",
                headers={"User-Agent": "Sublime"})
            http_file = urllib.request.urlopen(request, timeout=self.timeout)
            self.response = json.loads(http_file.read().decode('utf-8'))['d']
            return
        except (urllib.request.HTTPError) as e:
            self.message = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
        except (urllib.request.URLError) as e:
            self.message = '%s: URL error %s contacting API' % (__name__, str(e.reason))
        self.response = False
        return