# Sublime Grepmark
A Sublime Text 3 plugin that searches a file for a pipe delimited regular expressions and bookmarks all matches.
## Dependency
Grepmark uses another of my plugins [BetterBookmarks](https://github.com/dusk125/sublime-betterbookmarks) to add the bookmarks to the view. Right now, BetterBookmarks needs to be installed along side of Grepmark, otherwise a nasty error message will pop up and Grepmark will not work.
## Installation
#### Git Clone
First, find out where the packages directory is by going to (Preferences->Browse Packages), use that location in the git clone command.
#### Package Control
Coming soon!
## Usage
Press the key bound to the grepmark command; by default `f1`, type in a query, and hit enter. Results will be marked by the standard bookmark caret on the BetterBookmarks 'bookmark' layer.

Another feature is to automatically search and mark a file with a certain file extension and with a certain pattern. This will be explained further in the [Settings](README.md#Settings) section
## KeyBinding
```
[
    {
        "keys": ["f1"],
        "command": "grepmark",
    },
]
```
## Settings
auto_open (true/false): Should Grepmark listen for on_load events.

auto_open_patterns (extension : pattern(s)): Extension to auto-open and what pattern(s) to search for on the on_load event.

auto_open_goto_first (true/false): Should the view be scrolled to the first bookmark after the on_load event is called.

ui_search_goto_first (true/false): Should the view be scrolled to the first bookmark after the user executes the grepmark command.
#### Example
```
{
	"auto_open": true,
	"auto_open_patterns": {
		".md": ["sublime", "bookmark"],
	},
	"auto_open_goto_first": true,
	"ui_search_goto_first": false,
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
