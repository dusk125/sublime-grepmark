import sublime, sublime_plugin

global settings
settings = sublime.load_settings("grepmark.sublime-settings")

class GrepmarkCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		goto_line = settings.get("ui_search_goto_first", False)
		self.view.window().show_input_panel("Grep for:", "", lambda s: self.run_with_args(self, self.view, s, goto_line), None, None)
	
	@staticmethod			
	def run_with_args(self, view, text, goto_line):
		line_regions = view.find_all(text, sublime.IGNORECASE, None, None)
		for line_region in line_regions:
			view.sel().clear()
			view.sel().add(line_region)
			if Grepmark.should_bookmark(view, line_region):
				view.run_command('bookmark_line')

			if goto_line:
				regions = view.get_regions("bookmarks")
				view.run_command("goto_line", {"line": "{:d}".format(
					view.rowcol(regions[0].begin())[0])})

	@staticmethod
	def should_bookmark(view, region):
		bookmarks = view.get_regions("bookmarks")
		line = view.line(region)

		for bookmark in bookmarks:
			if line.contains(bookmark):
				return False

		return True

class GrepmarkLoaderCommand(sublime_plugin.EventListener):
	
	def on_load(self, view):
		if settings.get("auto_open"):
			types = settings.get("auto_open_patterns", [])
			variables = view.window().extract_variables()
			extension = sublime.expand_variables("${file_extension}", variables)

			try:
				patterns = types[extension]
				if len(patterns):
					pattern = patterns[0]
					for p in range(1, len(patterns)):
						pattern += "|{:s}".format(patterns[p])
					if pattern:
						goto_line = settings.get("auto_open_goto_first", True)
						Grepmark.run_with_args(self, view, pattern, goto_line)

			except KeyError:
				pass
