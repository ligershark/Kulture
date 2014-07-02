import sublime, sublime_plugin, urllib.request, threading

class TestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        print("test")
    # def is_enabled(self):
    #     if (window.active_view().settings().get('syntax')=='Packages/JavaScript/JSON.tmLanguage'):
    #         return True
    #     return False

class ValidateSchemaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print ("Test")
        threads = []
        thread = ValidateSchemaApiCall(5)
        threads.append(thread)
        thread.start()


class ValidateSchemaApiCall(threading.Thread):
    def __init__(self, timeout):
        self.timeout = timeout
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        try:
            request = urllib.request.Request("http://schemastore.org/schemas/json/project.json",
                headers={"User-Agent": "Sublime"})
            http_file = urllib.request.urlopen(request, timeout=self.timeout)
            self.result = http_file.read()
            print (self.result.decode('utf-8'))
            return

        except (urllib.request.HTTPError) as e:
            err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
        except (urllib.request.URLError) as e:
            err = '%s: URL error %s contacting API' % (__name__, str(e.reason))

        #sublime.error_message(err)
        self.result = False