import sublime, sublime_plugin

class Grepmark(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.window().show_input_panel("Grep for:", "", lambda s: self.run_with_args(self, self.view, s), None, None)
	
	@staticmethod			
	def run_with_args(self, view, text):
		line_regions = view.find_all(text, sublime.IGNORECASE, None, None)
		start_region = None
		for line_region in line_regions:
			view.sel().clear()
			view.sel().add(line_region)
			if Grepmark.should_bookmark(view, line_region):
				if start_region == None:
					start_region = line_region
				view.run_command('bookmark_line')
		# view.run_command('next_bookmark')
		if start_region != None:
			view.show(start_region)

	@staticmethod
	def should_bookmark(view, region):
		bookmarks = view.get_regions("bookmarks")
		line = view.line(region)

		for bookmark in bookmarks:
			if line.contains(bookmark):
				return False

		return True

class Grepmark_Loader(sublime_plugin.EventListener):
	
	def __init__(self):
		global settings
		settings = sublime.load_settings("grepmark.sublime-settings")

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
						Grepmark.run_with_args(self, view, pattern)
			except KeyError:
				pass
