import sublime, sublime_plugin

def Settings():
	return sublime.load_settings("Grepmark.sublime-settings")

# In order to use some list functions, python needs to be able to see a sublime.Region as something simpler;
# 	in this case a tuple.
def HashMarks(marks):
	newMarks = []
	for mark in marks:
		newMarks.append((mark.a, mark.b))

	return newMarks

class GrepmarkCommand(sublime_plugin.TextCommand):
	def __init__(self, edit):
		sublime_plugin.TextCommand.__init__(self, edit)
		self.grep = ''
		self.layer = Settings().get('bb_layer', 'bookmarks')

	def run(self, edit, **args):
		selection = self.view.sel()[0]
		if selection:
			self.grep = self.view.substr(selection)
		self.view.window().show_input_panel("Grep for:", self.grep, lambda s: self._run(s), None, None)
	
	def _run(self, text):
		goto_line = Settings().get("ui_search_goto_first", False)

		# Actually find all of the instances of the text
		flaglist = Settings().get('search_flags')
		flags = sublime.IGNORECASE if 'ignore_case' in flaglist else 0 | sublime.LITERAL if 'literal' in flags else 0
		line_regions = self.view.find_all(text, flags, None, None)

		if Settings().get('use_better_bookmarks', False):
			self.view.run_command('better_bookmarks', {'subcommand': 'mark_line', 'line': HashMarks(line_regions), 'layer': self.layer})
		else:
			self.view.add_regions('bookmarks', line_regions, 'string', 'bookmark', sublime.PERSISTENT | sublime.HIDDEN)

		if goto_line:
			if line_regions:
				self.view.run_command("goto_line", {"line": "{:d}".format(view.rowcol(line_regions[0].begin())[0])})
			else:
				sublime.status_message("Could not find matches.")

class GrepmarkLoaderCommand(sublime_plugin.EventListener):
	def on_load(self, view):
		if Settings().get("auto_open"):
			types = Settings().get("auto_open_patterns")
			variables = sublime.active_window().extract_variables()
			extension = sublime.expand_variables("${file_extension}", variables)

			if extension in types:
				patterns = types[extension]
				if len(patterns):
					pattern = patterns[0]
					for p in range(1, len(patterns)):
						pattern += "|{:s}".format(patterns[p])
					if pattern:
						goto_line = Settings().get("auto_open_goto_first")
						GrepmarkCommand.run_with_args(view, pattern, goto_line)
