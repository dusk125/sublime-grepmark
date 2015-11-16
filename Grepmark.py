import sublime, sublime_plugin

def plugin_loaded():
	global BBFunctions
	try:
		from BetterBookmarks.BetterBookmarks import BBFunctions
	except ImportError:
		sublime.error_message("Could not load dependency BetterBookmarks, make sure it's installed.")

def Settings():
	return sublime.load_settings("Grepmark.sublime-settings")

class GrepmarkCommand(sublime_plugin.TextCommand):
	def __init__(self, edit):
		sublime_plugin.TextCommand.__init__(self, edit)
		self.grep = ''

	def run(self, edit):
		goto_line = Settings().get("ui_search_goto_first", False)
		selection = self.view.sel()[0]
		if selection:
			self.grep = self.view.substr(selection)
		sublime.active_window().show_input_panel("Grep for:", self.grep, lambda s: self.run_with_args(self.view, s, goto_line), None, None)
	
	@staticmethod			
	def run_with_args(view, text, goto_line, layer='bookmarks'):
		flaglist = Settings().get('search_flags')
		flags = 0 if 'ignore_case' in flaglist else sublime.IGNORECASE | 0 if 'literal' in flags else sublime.LITERAL
		line_regions = view.find_all(text, flags, None, None)
		for line_region in line_regions:
			sel = view.sel()
			sel.clear()
			sel.add(line_region)
			
			bb = BBFunctions.get_bb_file()
			if bb.should_bookmark(line_region):
				if not bb.has_layer(layer):
					print("Not marking; layer {:s} does not exist.".format(layer))
					break
				bb.add_mark(line_region, layer)

			if goto_line:
				regions = bb.marks[layer]
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
						GrepmarkCommand.run_with_args(view, pattern, goto_line)
