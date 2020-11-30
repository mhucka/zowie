Zuppa<img width="10%" align="right" src="https://github.com/mhucka/zuppa/raw/main/.graphics/zuppa-icon.png">
======

Zuppa (_"**Z**otero **U**RI **P**DF **P**rop**er**ty **A**nnotator"_) is a command-line program that writes Zotero item URIs into the PDF files of a Zotero database.  Zuppa is written in Python and runs on macOS.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Latest release](https://img.shields.io/github/v/release/mhucka/zupper.svg?style=flat-square&color=b44e88)](https://github.com/mhucka/zupper/releases)


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#authors-and-acknowledgments)


Introduction
------------

When using [Zotero](https://zotero.org), you may on occasion want to work with the PDF files from outside of Zotero.  For example, if you're a [DEVONthink](https://www.devontechnologies.com/apps/devonthink) user, you will at some point discover the power of indexing your local Zotero database from DEVONthink.  However, when viewing or manipulating the PDF files from outside of Zotero, you may run into the following problem: when looking at a given PDF file, _how do you find out which Zotero entry it belongs to_?

Enter Zuppa (a loose acronym for _"**Z**otero **U**RI **P**DF **P**rop**er**ty **A**nnotator"_).  Zuppa scans through the files in a local Zotero database, looks up the Zotero bibliographic record corresponding to each PDF file found, and writes a [Zotero "select" link](https://forums.zotero.org/discussion/78053/given-the-pdf-file-of-an-article-how-can-you-find-out-its-uri#latest) into (depending on the user's choice) the PDF file and/or certain macOS Finder/Spotlight metadata fields.  A Zotero select link has the form `zotero://select/...` and when opened on macOS, causes the Zotero desktop application to open that item in your database.  Zuppa thus makes it possible to go from a PDF file opened in an application other than Zotero (e.g., DEVONthink, Adobe Acrobat), to the Zotero record corresponding to that PDF file.

Zuppa uses the Zotero API to discover the user's shared libraries and groups.  This allows it to look up Zotero URIs for PDFs regardless of whether they belong to the user's personal library or shared libraries.


Installation
------------
 
[_..Forthcoming..._]


Usage
-----

For help with usage at any time, run `zuppa` with the option `-h`.

The `zuppa` command-line program should end up installed in a location where software is normally installed on your computer, if the installation steps described in the previous section proceed successfully.  Running Zuppa from a terminal shell then should be as simple as running any other shell command on your system:

```shell
zuppa -h
```

If that fails for some reason, you should be able to run Zuppa from anywhere using the normal approach for running Python modules:

```shell
python3 -m zuppa -h
```

### Credentials for Zotero access

Zuppa needs to know the user's personal library identifier (also known as the _userID_) and a Zotero API key. By default, it tries to get this information from the user's keychain. If the values do not exist in the keychain from a previous run, Zuppa will ask the user, and (unless the `-K` option is given) store the values in the user's keychain so that it does not have to ask again in the future. It is also possible to supply the identifier and API key on the command line using the `-i` and `-a` options, respectively; the given values will then override the values stored in the keychain (unless the `-K` option is also given). This is also how you can replace previously-stored values: use `-i` and `-a` (without `-K`) and the new values will override the stored values.

To find out your Zotero userID and create an API key, log in to your Zotero account at Zotero.org and visit [https://www.zotero.org/settings/keys](https://www.zotero.org/settings/keys).


### Basic usage

Zuppa can operate on a folder, or one or more individual PDF files, or a mix of both. Suppose your local Zotero database is located in `~/my-zotero/`. Perhaps the simplest way to run Zuppa is the following command:

```shell
zuppa ~/my-zotero
```

If this is your first run of Zuppa, it will ask you for your userID and API key, then search for PDF files recursively under `~/my-zotero/`.  For each PDF file found, Zuppa will contact the Zotero servers over the network and determine the item URI for the bibliographic entry containing that PDF file. Finally, it will use the default method of recording the Zotero link, which is to write it into the macOS Finder comments for the file.  It will also store your Zotero userID and API key into the system keychain so that it does not have to ask for them in the future.

Instead of a folder, you can invoke zuppa on one or more individual files (but be careful to quote pathnames with spaces in them, such as in this example):

```shell
zuppa "~/my-zotero/storage/26GS7CZL/Smith 2020 Paper.pdf"
```

### Available methods of writing Zotero links

Zuppa supports multiple methods of writing the Zotero select link.  The option `-l` will cause Zuppa to print a list of all the methods available, then exit. The default method is to write it to the Finder comments, which are displayed in the Finder's "Get Info" panel for a file.

The option `-m` can be used to select one or more methods when running Zuppa. Write the method names separated with commas without spaces. For example,

```shell
zuppa -m findercomment,pdfsubject ~/my-zotero/storage
```

will make Zuppa write the Zotero select link into the Finder comments as well as the PDF metadata attribute _Subject_.

At this time, the following methods are available:

*  **`findercomment`**: prepends the Zotero item URI to the Finder comments for the file. Zuppa tries to be careful how it does this: if it finds a Zotero URI as the first thing in the comments, it replaces that URI instead of prepending a new one. However, Finder comments are notorious for being easy to damage or lose, so beware that Zuppa may irretrievably corrupt any existing Finder comments on the file.

*  **`wherefrom`**: prepends the Zotero item URI to the "Where from" metadata field of a file (the [`com.apple.metadata:kMDItemWhereFroms`](https://developer.apple.com/documentation/coreservices/kmditemwherefroms) extended attribute).  This field is displayed as "Where from" in Finder "Get Info" panels.  It is typically used by web browsers to store a file's download origin. If macOS Spotlight indexing is turned on for the volume containing the file, the macOS Finder will display the upated "Where from" values in the Get Info panel of the file; if Spotlight is not turned on, the Get info panel will not be updated, but commands such as `xattr` will correctly show changes to the value. This metadata field is a list; thus, that it is possible to add a value without losing previous values.

*  **`pdfsubject`**: rewrites the _Subject_ metadata field in the PDF file. This is not the same as the _Title_ field.  For some users, the _Subject_ field is not used for any purpose and thus can be usefully hijacked for storing the Zotero item URI. This makes the value accessible from macOS Preview, Adobe Acrobat, DEVONthink, and presumably any other application that can read the PDF metadata fields.

*  **`pdfproducer`**: rewrites the _Producer_ metadata field in the PDF file. For some users, this field has not utility, and thus can be usefully hijacked for the purpose of storing the Zotero item URI. This makes the value accessible from macOS Preview, Adobe Acrobat, DEVONthink, and presumably any other application that can read the PDF metadata fields. However, note that some users (archivists, forensics investigators, possibly others) do use the _Producer_ field, and overwriting it may be undesirable.

### Filtering by date

If the `-d` option is given, the PDF files will be filtered to use only those whose last-modified date/time stamp is no older than the given date/time description. Valid descriptors are those accepted by the Python dateparser library. Make sure to enclose descriptions within single or double quotes. Examples:

```shell
zuppa -d "2 weeks ago" ....
zuppa -d "2014-08-29" ....
zuppa -d "12 Dec 2014" ....
zuppa -d "July 4, 2013" ....
```

### Additional command-line arguments

To make Zuppa only print what it would do without actually doing it, use the `-n` "dry run" option.

If given the `-q` option, Zuppa will not print its usual informational messages while it is working. It will only print messages for warnings or errors.  By default messages printed by Zuppa are also color-coded. If given the option `-C`, Zuppa will not color the text of messages it prints. (This latter option is useful when running Zuppa within subshells inside other environments such as Emacs.)

If given the `-V` option, this program will print the version and other information, and exit without doing anything else.

If given the `-@` argument, this program will output a detailed trace of what it is doing.  The debug trace will be sent to the given destination, which can be `-` to indicate console output, or a file path to send the output to a file.

When `-@ has` been given, Zuppa also installs a signal handler on signal `SIGUSR1` that will drop Zuppa into the pdb debugger if the signal is sent to the running process.


### _Summary of command-line options_

The following table summarizes all the command line options available.

| Short&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   | Long&nbsp;form&nbsp;opt&nbsp;&nbsp;&nbsp;&nbsp; | Meaning | Default |  |
|---------- |-------------------|--------------------------------------|---------|---|
| `-a`_A_   | `--api-key`_A_    | API key to access the Zotero API service | | |
| `-C`      | `--no-color`      | Don't color-code the output | Use colors in the terminal | | |
| `-d`      | `--after-date`_D_ | Only act on files modified after date "D" | Act on all PDF files found | |
| `-h`      | `--help`          | Display help text and exit | | |
| `-i`      | `--identifer`_I_  | Zotero user ID for API calls | | |
| `-K`      | `--no-keyring`    | Don't use a keyring/keychain | Store login info in keyring | |
| `-l`      | `--list`          | Display known services and exit | | | 
| `-m`      | `--method`_M_     | Control how Zotero select links are stored | `findercomment` | |
| `-n`      | `--dry-run`       | Report what would be done but don't do it | Do it | | 
| `-q`      | `--quiet`         | Don't print messages while working | Be chatty while working |
| `-V`      | `--version`       | Display program version info and exit | | |
| `-@`_OUT_ | `--debug`_OUT_    | Debugging mode; write trace to _OUT_ | Normal mode | ⬥ |

⬥ &nbsp; To write to the console, use the character `-` as the value of _OUT_; otherwise, _OUT_ must be the name of a file where the output should be written.


### _Return values_

This program exits with a return code of 0 if no problems are encountered.  It returns a nonzero value otherwise. The following table lists the possible return values:

| Code | Meaning                                                  |
|:----:|----------------------------------------------------------|
| 0    | success &ndash; program completed normally               |
| 1    | the user interrupted the program's execution             |
| 2    | encountered a bad or missing value for an option         |
| 3    | no network detected &ndash; cannot proceed               |
| 4    | file error &ndash; encountered a problem with a file     |
| 5    | server error &ndash; encountered a problem with a server |
| 6    | an exception or fatal error occurred                     |


Getting help
------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/mhucka/zuppa/issues) for this repository.


Contributing
------------

I would be happy to receive your help and participation if you are interested.  Everyone is asked to read and respect the [code of conduct](CONDUCT.md) when participating in this project.  Development generally takes place on the `development` branch.


License
-------

This software is Copyright (C) 2020, by Michael Hucka and the California Institute of Technology (Pasadena, California, USA).  This software is freely distributed under a 3-clause BSD type license.  Please see the [LICENSE](LICENSE) file for more information.


Authors and history
---------------------------

Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.


Acknowledgments
---------------

This work is a personal project developed by the author, using computing facilities and other resources of the [California Institute of Technology Library](https://www.library.caltech.edu).

The [vector artwork](https://thenounproject.com/search/?q=soup&i=3124151) of a quiche, used as the icon for this repository, was created by [ghufronagustian](https://thenounproject.com/ghufronagustian/) from the Noun Project.  It is licensed under the Creative Commons [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/) license.

Zuppa makes use of numerous open-source packages, without which Zuppa could not have been developed.  I want to acknowledge this debt.  In alphabetical order, the packages are:

* [aenum](https://pypi.org/project/aenum/) &ndash; advanced enumerations for Python
* [biplist](https://bitbucket.org/wooster/biplist/src/master/) &ndash; A binary plist parser/writer for Python
* [bun](https://github.com/caltechlibrary/bun) &nash; a set of basic user interface classes and functions
* [commonpy](https://github.com/caltechlibrary/commonpy) &ndash; a collection of commonly-useful Python functions
* [ipdb](https://github.com/gotcha/ipdb) &ndash; the IPython debugger
* [keyring](https://github.com/jaraco/keyring) &ndash; access the system keyring service from Python
* [pdfrw](https://github.com/pmaupin/pdfrw) &ndash; a pure Python library for reading and writing PDFs
* [plac](http://micheles.github.io/plac/) &ndash; a command line argument parser
* [py-applescript](https://pypi.org/project/py-applescript/) &ndash; a Python interface to AppleScript
* [pyzotero](https://github.com/urschrei/pyzotero) &ndash; a Python API client for Zotero
* [pyxattr](https://github.com/iustin/pyxattr) &ndash; access extended file attributes from Python
* [setuptools](https://github.com/pypa/setuptools) &ndash; library for `setup.py`
* [sidetrack](https://github.com/caltechlibrary/sidetrack) &ndash; simple debug logging/tracing package
* [wheel](https://pypi.org/project/wheel/) &ndash; setuptools extension for building wheels

The [developers of DEVONthink](https://www.devontechnologies.com/about), especially Jim Neumann and Christian Grunenberg, quickly and consistently replied to my many questions on the [DEVONtechnologies forums](https://discourse.devontechnologies.com).
