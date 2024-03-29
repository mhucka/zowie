# Change log for Zowie

## ★ Version 1.3.0 ★

This release fixes issues #13 and #18, updates the required version of some dependencies, and changes the minimum version of Python to version 3.8.

Detailed changes:
* Fix issue #13: filtering by date using the `-d` option is broken.
* Fix issue #18: installations using `pipx` failed.
* Updated versions of dependencies in `requirements.txt`.
* Added `requirements-dev.txt`.
* Improved `codemeta.json`.
* Updated `Makefile` and `setup.py` to use versions developed for other projects.
* Updated copyright year in various files.


## ★ Version 1.2.0 ★

* Add new `-s` option. Please see the section on [special-case behavior](https://github.com/mhucka/zowie#special-case-behavior) for an explanation.
* Fix issue #9: version incompatibility with Sidetrack version 2.0 package.
* Use lazy imports of Python packages for faster application startup.
* Add script to create zipapp version of Zowie.
* Overhaul Makefile.
* Update versions of all Python packages dependencies, and make `requirements.txt` pin the exact version of the packages used at release time.
* Update `LICENSE` file, which had the wrong license text!


## ★ Version 1.1.2 ★

* Add missing dependency to `requirements.txt`
* Mention Zowie can't work with Zotero installations that use the linked attachment file method.


## ★ Version 1.1.1 ★

* Fix for issue #4, caused by not checking that a path has been provided on the command line.


## ★ Version 1.1.0 ★

* Zowie now operates on all types of files by default, not just PDF files. 
* Zowie has a new command-line option: `-f`, to allow you to filter files by their extensions and limit its operation to specific file types instead of all files, if you wish.
* A ready-to-run binary executable for macOS is now available for downloading from GitHub.


## ★ Version 1.0.6 ★

This update limits the parts of the [PyObjC](https://pypi.org/project/pyobjc/) package that are required in `requirements.txt`, to improve installation time as well as avoid a conflict between `pyobjc-framework-PubSub` and the Python [PyPubSub](https://pypi.org/project/PyPubSub/) package used by [Bun](https://pypi.org/project/bun/).


## ★ Version 1.0.5 ★

Fixed issue #1: PDF files that have no parent records are not necessarily an error. Print warnings, not errors, for those cases.


## ★ Version 1.0.4 ★

* Fixed issue #2: errors about database lookups were unclear about which file was involved.
* Added info to installation instructions about using `--upgrade` option to `pip`.
* Fixed some minor code errors that had few, if any, external implications.
* Made some very minor documentation changes and elaborations.
* Started adding unit tests.
* Made other minor internal fixes and changes.


## ★ Version 1.0.3 ★

This release fixes a missing Python package import in some code files, and also protects more print statements against file names that contain `{` and/or `}` characters.  (The latter have special meaning to some Python constructs.)


## ★ Version 1.0.2 ★

This release fixes an important bug in regular expressions used to replace existing Zotero select links inside Finder comments and PDF Subject and Producer fields. It also includes some internal cleanup for some Pylint issues (a cleanup process that is not finished).


## ★ Version 1.0.1 ★

This release fixes a bug in the installation configuration that caused the shell interface script (`zowie`) to fail to be installed.


## ★ Version 1.0.0 ★

This is the first public release of a completed version of Zowie.

Zowie (a loose acronym of _"**Z**otero link **w**r**i**t**e**r"_) is a command-line program that scans through the files in a local Zotero database, looks up the Zotero bibliographic record corresponding to each PDF file found, and writes a [Zotero select link](https://forums.zotero.org/discussion/78053/given-the-pdf-file-of-an-article-how-can-you-find-out-its-uri#latest) into the PDF file and/or certain macOS Finder/Spotlight metadata fields (depending on the user's choice).  A Zotero select link has the form `zotero://select/...` and when opened on macOS, causes the Zotero desktop application to open that item in your database.  Zowie thus makes it possible to go from a PDF file opened in an application other than Zotero (e.g., DEVONthink, Adobe Acrobat), to the Zotero record corresponding to that PDF file.

Zowie is written in Python and is primarily aimed at macOS users.
