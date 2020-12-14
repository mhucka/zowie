Zowie<img width="10%" align="right" src="https://github.com/mhucka/zowie/raw/main/.graphics/zowie-icon.png">
======

Zowie (_"**Zo**tero link **w**r**i**t**e**r"_) is a command-line program that writes Zotero _select_ links into the PDF files of a Zotero database.  Zowie is written in Python and runs on macOS.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Python](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat-square)](http://shields.io)
[![Latest release](https://img.shields.io/github/v/release/mhucka/zowie.svg?style=flat-square&color=b44e88)](https://github.com/mhucka/zowie/releases)
[![DOI](https://img.shields.io/badge/dynamic/json.svg?label=DOI&style=flat-square&colorA=gray&colorB=navy&query=$.metadata.doi&uri=https://data.caltech.edu/api/record/1709)](https://data.caltech.edu/records/1709)
[![PyPI](https://img.shields.io/pypi/v/zowie.svg?style=flat-square&color=orange)](https://pypi.org/project/zowie/)


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

Enter Zowie (a loose acronym for _"**Zo**tero link **w**r**i**t**e**r"_, and pronounced like [the interjection](https://www.merriam-webster.com/dictionary/zowie)).  Zowie scans through the files in a local Zotero database, looks up the Zotero bibliographic record corresponding to each PDF file found, and writes a [Zotero select link](https://forums.zotero.org/discussion/78053/given-the-pdf-file-of-an-article-how-can-you-find-out-its-uri#latest) into the PDF file and/or certain macOS Finder/Spotlight metadata fields (depending on the user's choice).  A Zotero select link has the form `zotero://select/...` and when opened on macOS, causes the Zotero desktop application to open that item in your database.  Zowie thus makes it possible to go from a PDF file opened in an application other than Zotero (e.g., DEVONthink, Adobe Acrobat), to the Zotero record corresponding to that PDF file.

Zowie uses the Zotero API to discover the user's shared libraries and groups.  This allows it to look up Zotero item URIs for PDFs regardless of whether they belong to the user's personal library or shared libraries, and from there, construct the appropriate Zotero select link for the files.


Installation
------------

The instructions below assume you have a Python 3 interpreter installed on your computer.  Note that the default on macOS at least through 10.14 (Mojave) is Python **2** &ndash; please first install Python version 3 and familiarize yourself with running Python programs on your system before proceeding further.

You should be able to install `zowie` with [`pip`](https://pip.pypa.io/en/stable/installing/) for Python&nbsp;3.  To install `zowie` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```
python3 -m pip install zowie
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `zowie` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/mhucka/zowie.git
```

_If you already installed Zowie once before_, and want to update to the latest version, add `--upgrade` to the end of either command line above.


Usage
-----

For help with usage at any time, run `zowie` with the option `-h`.

The `zowie` command-line program should end up installed in a location where software is normally installed on your computer, if the installation steps described in the previous section proceed successfully.  Running Zowie from a terminal shell then should be as simple as running any other shell command on your system:

```shell
zowie -h
```

If that fails for some reason, you should be able to run Zowie from anywhere using the normal approach for running Python modules:

```shell
python3 -m zowie -h
```


### Credentials for Zotero access

Zowie relies on the [Zotero sync API](https://www.zotero.org/support/dev/web_api/v3/start) to get information about your references. If you do not already have a [Zotero sync account](https://www.zotero.org/support/sync), it will be necessary to create one before going any further.

To use Zowie, you will also need both an API user identifier (also known as the **userID**) and an **API key**.  To find out your Zotero userID and create a new API key, log in to your Zotero account at [Zotero.org](https://www.zotero.org) and visit the [_Feeds/API_ tab of the your _Settings_ page](https://www.zotero.org/settings/keys).  On that page you can find your userID and create a new API key for Zowie.

The first time you run Zowie, it will ask for this information and (unless the `-K` option is given) store it in your macOS keychain so that it does not have to ask for it again on future occasions.  It is also possible to supply the identifier and API key directly on the command line using the `-i` and `-a` options, respectively; the given values will then override any values stored in the keychain and (unless the `-K` option is also given) will be used to update the keychain for the next time.


### Basic usage

Zowie can operate on a folder, or one or more individual PDF files, or a mix of both. Suppose your local Zotero database is located in `~/my-zotero/`. Perhaps the simplest way to run Zowie is the following command:

```shell
zowie ~/Zotero
```

If this is your first run of Zowie, it will ask you for your userID and API key, then search for PDF files recursively under `~/Zotero/`.  For each PDF file found, Zowie will contact the Zotero servers over the network and determine the Zotero select link for the bibliographic entry containing that PDF file. Finally, it will use the default method of recording the link, which is to write it into the macOS Finder comments for the file.  It will also store your Zotero userID and API key into the system keychain so that it does not have to ask for them in the future.

Instead of a folder, you can invoke Zowie on one or more individual files (but be careful to quote pathnames with spaces in them, such as in this example):

```shell
zowie "~/Zotero/storage/26GS7CZL/Smith 2020 Paper.pdf"
```


### Available methods of writing Zotero links

Zowie supports multiple methods of writing the Zotero select link.  The option `-l` will cause Zowie to print a list of all the methods available, then exit.

The option `-m` can be used to select one or more methods when running Zowie.  Write the method names separated with commas without spaces.  For example, the following command will make Zowie write the Zotero select link into the Finder comments as well as the PDF metadata attribute _Subject_:

```shell
zowie -m findercomment,pdfsubject ~/Zotero/storage
```

At this time, the following methods are available:

* **`findercomment`**: (**The default method**.) Writes the Zotero select link into the Finder comments of each file, attempting to preserve other parts of the comments. If Zowie finds an existing Zotero select link in the text of the Finder comments attribute, it only updates the link portion and tries to leave the rest of the comment text untouched. Otherwise, Zowie **only** writes into the comments attribute if either the attribute value is empty or Zowie is given the overwrite (`-o`) option. (Note that updating the link text requires rewriting the entire Finder comments attribute on a given file. Finder comments have a reputation for being easy to get into inconsistent states, so if you have existing Finder comments that you absolutely don't want to lose, it may be safest to avoid this method.)

* **`pdfproducer`**: Writes the Zotero select link into the "Producer" metadata field of each PDF file. If the "Producer" field is not empty on a given file, Zowie looks for an existing Zotero link within the value and updates the link if one is found; otherwise, Zowie leaves the field untouched unless given the overwrite flag (`-o`), in which case, it replaces the entire contents of the field with the Zotero select link.  For some users, the "Producer" field has not utility, and thus can be usefully hijacked for the purpose of storing the Zotero select link. The value is accessible from macOS Preview, Adobe Acrobat, DEVONthink, and presumably any other application that can display the PDF metadata fields.  However, note that some users (archivists, forensics investigators, possibly others) do use the "Producer" field, and overwriting it may be undesirable.

* **`pdfsubject`**: Writes the Zotero select link into the "Subject" metadata field of each PDF file. If the "Subject" field is not empty on a given file, Zowie looks for an existing Zotero link within the value and updates the link if one is found; otherwise, Zowie leaves the field untouched unless given the overwrite flag (`-o`), in which case, it replaces the entire contents of the field with the Zotero select link.  Note that the PDF "Subject" field is not the same as the "Title" field. For some users, the "Subject" field is not used for any purpose and thus can be usefully hijacked for storing the Zotero select link. The value is accessible from macOS Preview, Adobe Acrobat, DEVONthink, and presumably any other application that can display the PDF metadata fields.

* **`wherefrom`**: Writes the Zotero select link to the "Where from" metadata field of each file (the [`com.apple.metadata:kMDItemWhereFroms`](https://developer.apple.com/documentation/coreservices/kmditemwherefroms) extended attribute). This field is displayed as "Where from" in Finder "Get Info" panels; it is typically used by web browsers to store a files download origin. The field is a list. If Zowie finds a Zotero select link as the first item in the list, it updates that value; otherwise, Zowie prepends the Zotero select link to the list of existing values, keeping the other values unless the overwrite option (`-o`) is used. When the overwrite option is used, Zowie deletes the existing list of values and writes only the Zotero select link. Note that if macOS Spotlight indexing is turned on for the volume containing the file, the macOS Finder will display the upated "Where from" values in the Get Info panel of the file; if Spotlight is not turned on, the Get info panel will not be updated, but other applications will still be able to read the updated value.

Note that, depending on the attribute, it is possible that a file has an attribute value that is not visible in the Finder or other applications.  This is especially true for "Where from" values and Finder comments.  The implication is that it may not be apparent when a file has a value for a given attribute, which can lead to confusion if Zowie thinks there is a value and refuses to change it without the `-o` option.


### Filtering by date

If the `-d` option is given, the PDF files will be filtered to use only those whose last-modified date/time stamp is no older than the given date/time description. Valid descriptors are those accepted by the Python dateparser library. Make sure to enclose descriptions within single or double quotes. Examples:

```shell
zowie -d "2 weeks ago" ....
zowie -d "2014-08-29" ....
zowie -d "12 Dec 2014" ....
zowie -d "July 4, 2013" ....
```


### Additional command-line arguments

To make Zowie only print what it would do without actually doing it, use the `-n` "dry run" option.

If given the `-q` option, Zowie will not print its usual informational messages while it is working. It will only print messages for warnings or errors.  By default messages printed by Zowie are also color-coded. If given the option `-C`, Zowie will not color the text of messages it prints. (This latter option is useful when running Zowie within subshells inside other environments such as Emacs.)

If given the `-V` option, this program will print the version and other information, and exit without doing anything else.

If given the `-@` argument, this program will output a detailed trace of what it is doing.  The debug trace will be sent to the given destination, which can be `-` to indicate console output, or a file path to send the output to a file.

When `-@ has` been given, Zowie also installs a signal handler on signal `SIGUSR1` that will drop Zowie into the pdb debugger if the signal is sent to the running process.


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
| `-o`      | `--overwrite`     | Overwrite previous metadata content | Don't write if already present | |
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

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/mhucka/zowie/issues) for this repository.


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

The [vector artwork](https://thenounproject.com/term/tag-exclamation-point/326951/) of an exclamation point circled by a zigzag, used as the icon for this repository, was created by  [Alfredo @ IconsAlfredo.com](https://thenounproject.com/AlfredoCreates/) from the Noun Project.  It is licensed under the Creative Commons [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/) license.

Zowie makes use of numerous open-source packages, without which Zowie could not have been developed.  I want to acknowledge this debt.  In alphabetical order, the packages are:

* [aenum](https://pypi.org/project/aenum/) &ndash; advanced enumerations for Python
* [biplist](https://bitbucket.org/wooster/biplist/src/master/) &ndash; A binary plist parser/writer for Python
* [bun](https://github.com/caltechlibrary/bun) &ndash; a set of basic user interface classes and functions
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
