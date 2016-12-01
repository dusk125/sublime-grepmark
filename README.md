# Sublime Grepmark
A Sublime Text 3 plugin that searches a file for a pipe delimited regular expressions and bookmarks all matches.
## Installation
#### Git Clone
First, find out where the packages directory is by going to (Preferences->Browse Packages), use that location in the git clone command.
#### Package Control
Install from Package Control [here](https://packagecontrol.io/packages/Grepmark).
## Usage
Press the key bound to the grepmark command; by default `f1`, type in a query (either string or reqular expression, depending on what your `search_flags` are set to in the [Settings](README.md#Settings)), and hit enter; results will be marked with one of two ways.

1. If you have [BetterBookmarks](https://github.com/dusk125/sublime-betterbookmarks) installed and enabled in the Grepmark settings, the BetterBookmarks layer can be configured in the `better_bookmarks` area of the Grepmark settings file; different layers can have different images configured to represent the mark. You can use Better Bookmarks to cycle through the marks, hide them through a layer change, or save them out to a file.

2. A mark using the default Sublime bookmark caret (greater than sign) will be added to the gutter. You can use the default Sublime commands `next_bookmark` and `prev_bookmark` to cycle through the marks.

**NOTE:** If you enable BetterBookmarks with it being installed, marks will not be added.
## Auto Grep
Greps can be preformed automatically when a file is opened. For example, in the [Settings](README.md#Settings) below, any file with the `.py` extension will have all of its functions marked in the BetterBookmarks `functions` layer. Each file extension can have multiple greps run at load time; each of the greps is individually configurable to allow overloading of the global options of the same name.

**Note:** For `search_flags`, setting the key to anything (even an empty list) will cause the grep to completely ignore the global `search_flags` values.
## Settings
```
{
	"auto_grep":
	{
		// Should marks be added to files with matching extensions based on the configured rules
		"enabled": true,
		// A dictionary of file extensions that contain the auto_grep configuration
		"extensions": 
		{
			"py": 
			[
				{
					// Should this specific search be run
					"enabled": false,
					// A list of patterns to search for
					"pattern_list": ["def.*"],
					// See 'better_bookmarks' in the 'global' section
					"better_bookmarks": 
					{
						"use": true,
						"layer": "functions"
					},
					// See 'ui' in the 'global' section
					"ui": 
					{
						// Should the viewport scroll to the first occurrence
						"goto_first": false,
						// Should all matches become the active selection
						"make_selection": false
					},
					// See 'search_flags' in the 'global' section
					"search_flags": []
				},
			],
		}
	},
	"global":
	{
		"ui": 
		{
			// Should the viewport scroll to the first occurrence
			"goto_first": true,
			// Should all matches become the active selection
			"make_selection": true
		},
		// Search flags:
		//   ignore_case: Searching doesn't care about letter case
		//   literal: Searches using strings instead of regular expressions
		"search_flags": ["ignore_case", "literal"],
		"better_bookmarks":
		{
			// Should Better Bookmarks be used to mark the file
			"use": true,
			// Which Better Bookmarks layer should be marked
			"layer": "bookmarks"
		}
	}
}
```
## License
Copyright (c) 2015 Allen Ray

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
