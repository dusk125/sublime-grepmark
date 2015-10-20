import sublime, sublime_plugin

try:
	from BetterBookmarks.BetterBookmarks import BBFunctions
except ImportError:
	sublime.error_message("Could not load dependency BetterBookmarks, make sure it's installed.")

def Settings():
	return sublime.load_settings("Grepmark.sublime-settings")

class GrepmarkCommand(sublime_plugin.TextCommand):
	def __init__(self, edit):
		sublime_plugin.TextCommand.__init__(self, edit)

	def run(self, edit):
		goto_line = Settings().get("ui_search_goto_first", False)
		self.view.window().show_input_panel("Grep for:", self.view.substr(self.view.sel()[0]), lambda s: self.run_with_args(self, self.view, s, goto_line), None, None)
	
	@staticmethod			
	def run_with_args(self, view, text, goto_line):
		line_regions = view.find_all(text, sublime.IGNORECASE, None, None)
		for line_region in line_regions:
			sel = view.sel()
			sel.clear()
			sel.add(line_region)
			
			bb = BBFunctions.get_bb_file()
			if bb.should_bookmark(line_region):
				bb.change_to_layer("bookmarks")
				bb.add_mark(line_region)

			if goto_line:
				regions = bb.marks["bookmarks"]
				if regions:
					view.run_command("goto_line", {"line": "{:d}".format(
						view.rowcol(regions[0].begin())[0])})
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
						GrepmarkCommand.run_with_args(self, view, pattern, goto_line)
