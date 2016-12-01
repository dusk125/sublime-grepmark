import sublime, sublime_plugin

def Settings():
	return sublime.load_settings('Grepmark.sublime-settings')

def Variable(var, window=None):
	window = window if window else sublime.active_window()
	return sublime.expand_variables(var, window.extract_variables())

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

	def run(self, edit, **args):
		if 'headless' in args:
			self._run(args)
		else:
			selection = self.view.sel()[0]
			if selection:
				self.grep = self.view.substr(selection)

			self.view.window().show_input_panel('Grep for:', self.grep, lambda pattern: self._run({}, pattern), None, None)
	
	def _run(self, args, pattern=None):
		# Extract variables from args
		globals = Settings().get('global')
		ui = args['ui'] if 'ui' in args else globals.get('ui')
		pattern = pattern if pattern else args['pattern']
		goto_first = args['goto_first'] if 'goto_first' in args else ui['goto_first']
		make_selection = args['make_selection'] if 'make_selection' in args else ui['make_selection']
		flags = args['search_flags'] if 'search_flags' in args else globals.get('search_flags', [])

		# Actually find all of the instances of the pattern
		ignore_case = sublime.IGNORECASE if 'ignore_case' in flags else 0
		literal = sublime.LITERAL if 'literal' in flags else 0
		line_regions = self.view.find_all(pattern, ignore_case | literal, None, None)

		# Highlight all of the found items
		if make_selection:
			sel = self.view.sel()
			sel.clear()
			sel.add_all(line_regions)

		# Use BetterBookmarks if we're configured to
		bbsettings = args['better_bookmarks'] if 'better_bookmarks' in args else globals.get('better_bookmarks')
		if bbsettings['use']:
			layer = args['layer'] if 'layer' in args else bbsettings['layer']
			self.view.run_command('better_bookmarks', {'subcommand': 'mark_line', 'line': HashMarks(line_regions), 'layer': layer})
		else:
			self.view.add_regions('bookmarks', line_regions, 'string', 'bookmark', sublime.PERSISTENT | sublime.HIDDEN)

		# Move our view to the first found item
		if goto_first:
			if line_regions:
				self.view.show_at_center(line_regions[0])
			else:
				sublime.status_message('Could not find matches.')

class GrepmarkListener(sublime_plugin.EventListener):
	def on_load_async(self, view):
		settings = Settings().get('auto_grep')
		if settings['enabled']:
			extension = Variable('${file_extension}', view.window())
			extensions = settings['extensions']

			if extension in extensions.keys():
				for pattern_object in extensions[extension]:
					if 'enabled' in pattern_object and pattern_object['enabled']:
						pattern_list = pattern_object['pattern_list']
						if len(pattern_list):
							pattern = pattern_list[0]
							for p in range(1, len(pattern_list)):
								pattern += '|{:s}'.format(pattern_list[p])
							if pattern:
								pattern_object['pattern'] = pattern
								pattern_object['headless'] = True
								view.run_command('grepmark', pattern_object)
