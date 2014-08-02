import sublime
import sublime_plugin
import threading
import urllib.request
import json
import re

# class Loading():
#     def __init__(self, view, status_message, display_message, callback):
#         self.view = view
#         self.i = 0
#         self.dir = 1
#         self.status_message = status_message
#         self.display_message = display_message
#         self.callback = callback
#     def increment(self):
#         before = self.i % 8
#         after = (7) - before
#         if not after:
#             self.dir = -1
#         if not before:
#             self.dir = 1
#         self.i += self.dir
#         self.view.set_status(self.status_message, " [%s=%s]" % \
#                 (" " * before, " " * after))
#         sublime.set_timeout(lambda: self.callback(), 100)
#     def clear(self):
#         self.view.erase_status(self.status_message)
#         pass

AC_OPTS = sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS

class KKultureCompletion( sublime_plugin.EventListener):
    def __init__(self):
        request = urllib.request.Request("https://www.myget.org/F/aspnetrelease/api/v2/Packages()?$select=Id&$format=json&orderby=DownloadCount&$top=100",
            headers={"User-Agent": "Sublime"})
        http_file = urllib.request.urlopen(request)
        self.result = {}
        self.cache = []
        response = json.loads(http_file.read().decode('utf-8'))['d']
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
        print("KULTURE::::Done caching")
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
                        version_regex = r'(?:,|{)"([-a-zA-Z0-9.*]+)":"[-a-zA-Z0-9.*]*$'
                        try:
                            package_name = re.search(version_regex, doc[0:index]).group(1)
                            return self.result[package_name]
                        except AttributeError as e:
                            pass
                        except KeyError as e:
                            return []
                        # Package name
                        return self.cache
                    break
            return (self.result['EntityFramework'], AC_OPTS)



# class RetrievePackageNames(threading.Thread):
#     def __init__(self,timeout):
#         self.timeout = timeout
#         self.result = None
#         threading.Thread.__init__(self)

#     def run(self):
#         try:
#             request = urllib.request.Request("https://www.myget.org/F/aspnetrelease/api/v2/Packages()?$select=Id&$format=json&orderby=DownloadCount&$top=10",
#                 headers={"User-Agent": "Sublime"})
#             http_file = urllib.request.urlopen(request, timeout=self.timeout)
#             self.result = []
#             response = json.loads(http_file.read().decode('utf-8'))['d']
#             for package in response:
#                 self.result.append(package['Id'])
#             print(self.result)
#             return
#         except (urllib.request.HTTPError) as e:
#             self.message = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
#         except (urllib.request.URLError) as e:
#             self.message = '%s: URL error %s contacting API' % (__name__, str(e.reason))
#         self.result = False
#         return