Change log for Zowie
====================

Version 1.0.2
--------------

This release fixes an important bug in regular expressions used to replace existing Zotero select links inside Finder comments and PDF Subject and Producer fields. It also includes some internal cleanup for some Pylint issues (a cleanup process that is not finished).


Version 1.0.1
--------------

This release fixes a bug in the installation configuration that caused the shell interface script (`zowie`) to fail to be installed.


Version 1.0.0
--------------

This is the first public release of a completed version of Zowie.

Zowie (a loose acronym of _"**Z**otero link **w**r**i**t**e**r"_) is a command-line program that scans through the files in a local Zotero database, looks up the Zotero bibliographic record corresponding to each PDF file found, and writes a [Zotero select link](https://forums.zotero.org/discussion/78053/given-the-pdf-file-of-an-article-how-can-you-find-out-its-uri#latest) into the PDF file and/or certain macOS Finder/Spotlight metadata fields (depending on the user's choice).  A Zotero select link has the form `zotero://select/...` and when opened on macOS, causes the Zotero desktop application to open that item in your database.  Zowie thus makes it possible to go from a PDF file opened in an application other than Zotero (e.g., DEVONthink, Adobe Acrobat), to the Zotero record corresponding to that PDF file.

Zowie is written in Python and is primarily aimed at macOS users.
