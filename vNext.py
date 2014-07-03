import sublime, sublime_plugin, urllib.request, threading, json, jsonschema
# Add jsonschema folder to C:\Program Files\Sublime Text 3 as a temporary workaround
from jsonschema import validate

class ValidateSchemaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        threads = []
        thread = ValidateSchemaApiCall(5, self.view)
        threads.append(thread)
        thread.start()
        # self.output_view = self.window.get_output_panel("textarea")
        # self.window.run_command("show_panel", {"panel": "output.textarea"})
        self.handle_threads(threads)

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

class ValidateSchemaApiCall(threading.Thread):
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

