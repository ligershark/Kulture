import sublime
import sublime_plugin
import threading
import urllib.request, urllib.parse
import json
import re
import os
import sys
import codecs

SETTINGS_FILE = 'Kulture.sublime-settings'
AC_OPTS = sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS

if sys.version_info >= (3,):
    installed_dir, _ = __name__.split('.')
else:
    installed_dir = os.path.basename(os.getcwd())

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
        # cannont access sublime.packages_path() on init.
        # loading package names on first completion instead

    def on_query_completions(self, view, prefix, locations):
        if(self.cache == None or len(self.cache) <=0):
            packagesFile = os.path.join(sublime.packages_path(), installed_dir,'packagenames.txt')
            self.thread = ReadPackageNamesFromFile(5,packagesFile)
            self.thread.start()
            while(self.thread.is_alive()):
                pass

            response = self.thread.response
            for package in response:
                self.cache.append((package,package))
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

class ReadPackageNamesFromFile(threading.Thread):
    def __init__(self,timeout,filepath):
        self.timeout = timeout
        self.filepath = filepath
        self.response = None
        threading.Thread.__init__(self)

    def run(self):
        allPackageNames = []
        filePath = self.filepath
        print('Kulture: loading package names from: '+filePath)
        with codecs.open(filePath, 'r',encoding='utf8') as f:
            for line in f:
                allPackageNames.append(line.strip())

        self.response = allPackageNames
        return
