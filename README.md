# Zowie<img width="10%" align="right" src="https://github.com/mhucka/zowie/raw/main/.graphics/zowie-icon.png">

Zowie ("**Zo**tero link **w**r**i**t**e**r") is a command-line program for macOS that writes Zotero _select_ links into the file attachments contained in a Zotero database.

[![License](https://img.shields.io/badge/License-BSD-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Python](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat-square)](http://shields.io)
[![GitHub stars](https://img.shields.io/github/stars/mhucka/zowie.svg?style=flat-square&color=lightgray&label=Stars)](https://github.com/mhucka/zowie/stargazers)
[![Latest release](https://img.shields.io/github/v/release/mhucka/zowie.svg?style=flat-square&color=b44e88&label=Latest%20release)](https://github.com/mhucka/zowie/releases)
[![PyPI](https://img.shields.io/pypi/v/zowie.svg?style=flat-square&color=orange&label=PyPI)](https://pypi.org/project/zowie/)


## Table of contents

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Additional tips](#additional-tips)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgments](#authors-and-acknowledgments)


## Introduction

When using [Zotero](https://zotero.org), you may on occasion want to work with PDF files and other attachment files outside of Zotero.  For example, if you're a [DEVONthink](https://www.devontechnologies.com/apps/devonthink) user, you will at some point discover the power of indexing your local Zotero database from DEVONthink.  However, when viewing or manipulating the attachments from outside of Zotero, you may run into the following problem: when looking at a given file, _how do you find out which Zotero entry it belongs to_?

Enter Zowie (a loose acronym for _"**Zo**tero link **w**r**i**t**e**r"_, and pronounced like [the interjection](https://www.merriam-webster.com/dictionary/zowie)).  Zowie scans through the files on your disk in a local Zotero database, looks up the Zotero bibliographic record corresponding to each file found, and writes a [Zotero select link](https://forums.zotero.org/discussion/78053/given-the-pdf-file-of-an-article-how-can-you-find-out-its-uri#latest) into the file and/or certain macOS Finder/Spotlight metadata fields (depending on the user's choice).  A Zotero select link has the form `zotero://select/...` and when opened on macOS, causes the Zotero desktop application to open that item in your database.  Zowie thus makes it possible to go from a file opened in an application other than Zotero (e.g., DEVONthink, Adobe Acrobat), to the Zotero record corresponding to that file.

Regretfully, Zowie can **only** work with Zotero libraries that use normal/local data storage; **it cannot work when Zotero is configured to use linked attachments**.


## Installation

There are multiple ways of installing Zowie, ranging from downloading a self-contained, single-file, ready-to-run program, to installing it as a typical Python program using `pip`.  Please choose the alternative that suits you and your Mac environment.


### _Alternative 1: downloading the ready-to-run program_

On macOS Catalina (10.15) or later, you can use a ready-to-run version of Zowie that only needs a Python interpreter version 3.8 or higher on your computer. That's the case for macOS 10.15 and later, but before you can use it, you may need to let macOS install some additional software components from Apple. To test it, run the following command in a terminal and **take note of the version of Python** that it prints:
```sh
python3 --version
```
**If this is the first time** you've run `python3` on your system, macOS will either ask you if you want to install certain additional software components, or it may produce an error about 
`xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools) ...`. In either case, the solution is to run the following command in the terminal:
```
xcode-select --install
```
In the pop-up dialog box that this brings up, **click the _Install_ button** and agree to let it install the [Command Line Tools](https://developer.apple.com/library/archive/technotes/tn2339/_index.html) package from Apple.

Next,
1. <img align="right" width="350px" src="https://github.com/mhucka/zowie/raw/develop/.graphics/shiv-releases.png"/>Go to the [latest release on GitHub](https://github.com/mhucka/zowie/releases) and find the **Assets**
2. **Download** the ZIP file whose name contains the version of Python on your computer (which you determined by running `python3 --version` above)
3. **Unzip** the file (if your browser didn't unzip it)
4. **Open the folder** that gets created (it will have a name like `zowie-1.2.0-macos-python3.8`)
5. Look inside for `zowie` and **move it** to a location where you put other command-line programs (such as `/usr/local/bin`). 

If you want to put it in `/usr/local/bin` but that folder does not exist on your computer yet, you can create it by opening a terminal window and running the following command (_prior_ to moving `zowie` into `/usr/local/bin`):

```shell
sudo mkdir /usr/local/bin
```

The following is an example command that you can type in a terminal to move Zowie there:

```shell
sudo mv zowie /usr/local/bin
```


### _Alternative 2: installing Zowie using `pipx`_

You can use [pipx](https://pypa.github.io/pipx/) to install Zowie. Pipx will install it into a separate Python environment that isolates the dependencies needed by Zowie from other Python programs on your system, and yet the resulting `zowie` command wil be executable from any shell &ndash; like any normal program on your computer. If you do not already have `pipx` on your system, it can be installed in a variety of easy ways and it is best to consult [Pipx's installation guide](https://pypa.github.io/pipx/installation/) for instructions. Once you have pipx on your system, you can install Zowie with the following command:
```sh
pipx install zowie
```

Pipx can also let you run Zowie directly using `pipx run zowie`, although in that case, you must always prefix every Zowie command with `pipx run`.  Consult the [documentation for `pipx run`](https://github.com/pypa/pipx#walkthrough-running-an-application-in-a-temporary-virtual-environment) for more information.


### _Alternative 3: installing Zowie using `pip`_

The instructions below assume you have a Python 3 interpreter installed on your computer.  Note that the default on macOS at least through 10.14 (Mojave) is Python **2** &ndash; please first install Python version 3 and familiarize yourself with running Python programs on your system before proceeding further.

You should be able to install `zowie` with [`pip`](https://pip.pypa.io/en/stable/installing/) for Python&nbsp;3.  To install `zowie` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```sh
python3 -m pip install zowie
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `zowie` directly from GitHub:
```sh
python3 -m pip install git+https://github.com/mhucka/zowie.git
```

_If you already installed Zowie once before_, and want to update to the latest version, add `--upgrade` to the end of either command line above.


### _Alternative 4: installing Zowie from sources_

If  you prefer to install Zowie directly from the source code, you can do that too. To get a copy of the files, you can clone the GitHub repository:
```sh
git clone https://github.com/mhucka/zowie
```

Alternatively, you can download the files as a ZIP archive using this link directly from your browser using this link: <https://github.com/mhucka/zowie/archive/refs/heads/main.zip>

Next, after getting a copy of the files,  run `setup.py` inside the code directory:
```sh
cd zowie
python3 setup.py install
```


## Usage

For help with usage at any time, run `zowie` with the option `-h`.

The `zowie` command-line program should end up installed in a location where software is normally installed on your computer, if the installation steps described in the previous section proceeded successfully.  Running Zowie from a terminal shell then should be as simple as running any other shell command on your system:

```shell
zowie -h
```

If you installed it as a Python package, then an alternative method is available to run Zowie from anywhere, namely to use the normal approach for running Python modules:

```shell
python3 -m zowie -h
```


### _Credentials for Zotero access_

Zowie relies on the [Zotero sync API](https://www.zotero.org/support/dev/web_api/v3/start) to get information about your references.  This allows it to look up Zotero item URIs for files regardless of whether they belong to your personal library or shared libraries, and from there, construct the appropriate Zotero select link for the files.  If you do not already have a [Zotero sync account](https://www.zotero.org/support/sync), it will be necessary to create one before going any further.

To use Zowie, you will also need both an API user identifier (also known as the **userID**) and an **API key**.  To find out your Zotero userID and create a new API key, log in to your Zotero account at [Zotero.org](https://www.zotero.org) and visit the [_Feeds/API_ tab of the your _Settings_ page](https://www.zotero.org/settings/keys).  On that page you can find your userID and create a new API key for Zowie.

The first time you run Zowie, it will ask for this information and (unless the `-K` option is given) store it in your macOS keychain so that it does not have to ask for it again on future occasions.  It is also possible to supply the identifier and API key directly on the command line using the `-i` and `-a` options, respectively; the given values will then override any values stored in the keychain and (unless the `-K` option is also given) will be used to update the keychain for the next time.


### _Basic usage_

Zowie can operate on a folder, or one or more individual files, or a mix of both. Suppose your local Zotero database is located in `~/Zotero/`. Perhaps the simplest way to run Zowie is the following command:

```shell
zowie ~/Zotero
```

If this is your first run of Zowie, it will ask you for your userID and API key, then search for files recursively under `~/Zotero/`.  For each file found, Zowie will contact the Zotero servers over the network and determine the Zotero select link for the bibliographic entry containing that file. Finally, it will use the default method of recording the link, which is to write it into the macOS Finder comments for the file.  It will also store your Zotero userID and API key into the system keychain so that it does not have to ask for them in the future.

If you are a user of [DEVONthink](https://www.devontechnologies.com/apps/devonthink), you will probably want to add the `-s` option (see the [explanation below](#special-case-behavior) for the details):

```shell
zowie -s ~/Zotero
```

Instead of a folder, you can also invoke Zowie on one or more individual files (but be careful to put quotes around pathnames with spaces in them, such as in this example):

```shell
zowie -s "~/Zotero/storage/26GS7CZL/Smith 2020 Paper.pdf"
```


### _Available methods of writing Zotero links_

Zowie supports multiple methods of writing the Zotero select link.  The option `-l` will cause Zowie to print a list of all the methods available, then exit.

The option `-m` can be used to select one or more methods when running Zowie.  Write the method names separated with commas without spaces.  For example, the following command will make Zowie write the Zotero select link into the Finder comments as well as the PDF metadata attribute _Subject_:

```shell
zowie -m findercomment,pdfsubject ~/Zotero/storage
```

At this time, the following methods are available:

* **`findercomment`**: (**The default method**.) Writes the Zotero select link into the Finder comments of each file, attempting to preserve other parts of the comments. If Zowie finds an existing Zotero select link in the text of the Finder comments attribute, it only updates the link portion and tries to leave the rest of the comment text untouched. Otherwise, Zowie **only** writes into the comments attribute if either the attribute value is empty or Zowie is given the overwrite (`-o`) option. (Note that updating the link text requires rewriting the entire Finder comments attribute on a given file. Finder comments have a reputation for being easy to get into inconsistent states, so if you have existing Finder comments that you absolutely don't want to lose, it may be safest to avoid this method.)

* **`pdfproducer`**: (Only applicable to PDF files.) Writes the Zotero select link into the "Producer" metadata field of each PDF file. If the "Producer" field is not empty on a given file, Zowie looks for an existing Zotero link within the value and updates the link if one is found; otherwise, Zowie leaves the field untouched unless given the overwrite flag (`-o`), in which case, it replaces the entire contents of the field with the Zotero select link.  For some users, the "Producer" field has not utility, and thus can be usefully hijacked for the purpose of storing the Zotero select link. The value is accessible from macOS Preview, Adobe Acrobat, DEVONthink, and presumably any other application that can display the PDF metadata fields.  However, note that some users (archivists, forensics investigators, possibly others) do use the "Producer" field, and overwriting it may be undesirable.

* **`pdfsubject`**: (Only applicable to PDF files.) Writes the Zotero select link into the "Subject" metadata field of each PDF file. If the "Subject" field is not empty on a given file, Zowie looks for an existing Zotero link within the value and updates the link if one is found; otherwise, Zowie leaves the field untouched unless given the overwrite flag (`-o`), in which case, it replaces the entire contents of the field with the Zotero select link.  Note that the PDF "Subject" field is not the same as the "Title" field. For some users, the "Subject" field is not used for any purpose and thus can be usefully hijacked for storing the Zotero select link. The value is accessible from macOS Preview, Adobe Acrobat, DEVONthink, and presumably any other application that can display the PDF metadata fields.

* **`wherefrom`**: Writes the Zotero select link to the "Where from" metadata field of each file (the [`com.apple.metadata:kMDItemWhereFroms`](https://developer.apple.com/documentation/coreservices/kmditemwherefroms) extended attribute). This field is displayed as "Where from" in Finder "Get Info" panels; it is typically used by web browsers to store a file's download origin. The field is a list. If Zowie finds a Zotero select link as the first item in the list, it updates that value; otherwise, Zowie prepends the Zotero select link to the list of existing values, keeping the other values unless the overwrite option (`-o`) is used. When the overwrite option is used, Zowie deletes the existing list of values and writes only the Zotero select link. Note that if macOS Spotlight indexing is turned on for the volume containing the file, the macOS Finder will display the updated "Where from" values in the Get Info panel of the file; if Spotlight is not turned on, the Get info panel will not be updated, but other applications will still be able to read the updated value.

Note that, depending on the attribute, it is possible that a file has an attribute value that is not visible in the Finder or other applications.  This is especially true for "Where from" values and Finder comments.  The implication is that it may not be apparent when a file has a value for a given attribute, which can lead to confusion if Zowie thinks there is a value and refuses to change it without the `-o` option.


### _Filtering by file type_

By default, Zowie acts on all files it finds on the command line, except for certain files that it always ignores: hidden files and files with extensions `.sqlite`, `.bak`, `.csl`, `.css`, `.js`, `.json`, `.pl`, and a few others.  If the `-m` option is used to select methods that only apply to specific file types, Zowie will examine each file it finds in turn and only apply the methods that match that particular file's type, but it will still consider every file it finds in the directories it scans and apply the methods that are not limited to specific types.

You can use the option `-f` to make Zowie filter the files it finds based on file name extensions.  This is useful if you want it to concentrate only on particular file types and ignore other files it might find while scanning folders. Here is an example (this also using the `-s` option for [reasons given below](#special-case-behavior)):

```shell
zowie -s -f pdf,mp4,mov ~/Zotero
```

will cause it to only work on PDF, MP4, and QuickTime format files.  You can provide multiple file extensions separated by commas, without spaces and without the leading periods.


### _Filtering by date_

If the `-d` option is given, the files will be filtered to use only those whose last-modified date/time stamp is no older than the given date/time description. Valid descriptors are those accepted by the Python dateparser library. Make sure to enclose descriptions within single or double quotes. Examples:

```shell
zowie -d "2 weeks ago" ....
zowie -d "2014-08-29" ....
zowie -d "12 Dec 2014" ....
zowie -d "July 4, 2013" ....
```


### _Special-case behavior_

Although Zowie is not aimed solely at DEVONthink users, its development was motivated by the author's desire to use Zotero with that software.  A complication arose due to an undocumented feature in DEVONthink: [it ignores a Finder comment if it is identical to the value of the "URL" attribute](https://discourse.devontechnologies.com/t/some-finder-comments-not-showing-in-devonthink/66864/30) (which is the name it gives to the `com.apple.metadata:kMDItemWhereFroms` attribute [discussed above](#available-methods-of-writing-zotero-links)).  In practical terms, if you do something like write the Zotero select link into the Finder comment of a file and then have a DEVONthink smart rule copy the value to the URL field, the Finder comment will subsequently [appear blank in DEVONthink](https://discourse.devontechnologies.com/t/some-finder-comments-not-showing-in-devonthink/66864) (even though it exists on the actual file).  This can be unexpected and confusing, and has caught people (including the author of Zowie) unaware.  To compensate, Zowie 1.2 introduced a new option: it can add a trailing space character to the end of the value it writes into the Finder comment when using the `findercomment` method.  Since approaches to copy the Zotero link from the Finder comment to the URL field in DEVONthink will typically strip whitespace around the URL value, the net effect is to make the value in the Finder comment just different enough from the URL field value to prevent DEVONthink from ignoring the Finder comment.  Use the option `-s` to  make Zowie to add the trailing space character.


### _Additional command-line arguments_

To make Zowie only print what it would do without actually doing it, use the `-n` "dry run" option.

If given the `-q` option, Zowie will not print its usual informational messages while it is working. It will only print messages for warnings or errors.  By default, messages printed by Zowie are also color-coded. If given the option `-C`, Zowie will not color the text of messages it prints. (This latter option is useful when running Zowie within subshells inside other environments such as Emacs.)

If given the `-V` option, this program will print the version and other information, and exit without doing anything else.

If given the `-@` argument, this program will output a detailed trace of what it is doing.  The debug trace will be sent to the given destination, which can be `-` to indicate console output, or a file path to send the output to a file.

When `-@` has been given, Zowie also installs a signal handler on signal `SIGUSR1` that will drop Zowie into the pdb debugger if the signal is sent to the running process.


### _Summary of command-line options_

The following table summarizes all the command line options available.

| Short&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   | Long&nbsp;form&nbsp;opt&nbsp;&nbsp;&nbsp;&nbsp; | Meaning | Default |  |
|---------- |-------------------|--------------------------------------|---------|---|
| `-a`_A_   | `--api-key`_A_    | API key to access the Zotero API service | | |
| `-C`      | `--no-color`      | Don't color-code the output | Use colors in the terminal | |
| `-d`      | `--after-date`_D_ | Only act on files modified after date "D" | Act on all files found | |
| `-f`      | `--file-ext`_F_   | Only act on files with extensions in "F" | Act on all files found | ⚑ |
| `-h`      | `--help`          | Display help text and exit | | |
| `-i`      | `--identifier`_I_ | Zotero user ID for API calls | | |
| `-K`      | `--no-keyring`    | Don't use a keyring/keychain | Store login info in keyring | |
| `-l`      | `--list`          | Display known services and exit | | | 
| `-m`      | `--method`_M_     | Select how Zotero select links are written | `findercomment` | |
| `-n`      | `--dry-run`       | Say what would be done, but don't do it | Do it | | 
| `-o`      | `--overwrite`     | Overwrite previous metadata content | Don't write if already present | |
| `-q`      | `--quiet`         | Don't print messages while working | Be chatty while working | |
| `-s`      | `--space`         | Append trailing space to Finder comments | Don't add a space | ★ |
| `-V`      | `--version`       | Display program version info and exit | | |
| `-@`_OUT_ | `--debug`_OUT_    | Debugging mode; write trace to _OUT_ | Normal mode | ⬥ |

⚑ &nbsp; Certain files are always ignored: hidden files, macOS aliases, and files with extensions `.sqlite`, `.sqlite-journal`, `.bak`, `.csl`, `.css`, `.js`, `.json`, `.pl`, and `.config_resp`.<br>
⬥ &nbsp; To write to the console, use the character `-` as the value of _OUT_; otherwise, _OUT_ must be the name of a file where the output should be written.<br>
★ &nbsp; See the explanation in the section on [special-case behavior](#special-case-behavior).


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


## Known issues and limitations

The following is a list of currently-known issues and limitations:

* Zowie can only work when Zotero is set to use direct data storage; i.e., where attached files are stored in Zotero.  It **cannot work if you use [linked attachments](https://www.zotero.org/support/preferences/advanced#files_and_folders)**, that is, if you set _Linked Attachment Base Directory_ in your Zotero Preferences' _Advanced_ → _Files and Folders_ panel.

* If you use [DEVONthink](https://www.devontechnologies.com/apps/devonthink) in a scheme in which you index your Zotero folder and use Zowie to write the Zotero select link into the Finder comments of files, beware of the following situation. If you use a DEVONthink smart rule to copy the comment string into the "URL" field, DEVONthink will (after reindexing the file) suddenly display an _empty_ Finder comment, even though the comment is still there. This is due to a [deliberate behavior in DEVONthink](https://discourse.devontechnologies.com/t/some-finder-comments-not-showing-in-devonthink/66864/30) and not a problem with Zowie, as discussed in the [section on special-case behavior](#special-case-behavior). Using the `-s` option will avoid this, but at the cost of adding an extra character to the Finder comment, so make sure to account for the added space character in any scripts or other actions you take on the Finder comment.

* [DEVONthink](https://www.devontechnologies.com/apps/devonthink) bases the "URL" value of a file on the file's [`com.apple.metadata:kMDItemWhereFroms`](https://developer.apple.com/documentation/coreservices/kmditemwherefroms) extended attribute.  The original hope behind Zowie was to make it write Zotero select links directly into that attribute value. Unfortunately, it turns out that if a file has already been indexed by DEVONthink, then [it will _not_ detect any changes to the `com.apple.metadata:kMDItemWhereFroms` attribute](https://discourse.devontechnologies.com/t/some-finder-comments-not-showing-in-devonthink/66864/38) made by an external program. Thus, if you index your Zotero folder within DEVONthink, you cannot use Zowie's `wherefroms` method to update the "URL" field directly. You are advised instead to use Zowie's `findercomment` method (the default) in combination with smart rules in DEVONthink, as discussed in [the wiki](https://github.com/mhucka/zowie/wiki/Example:-using-Zowie-with-DEVONthink). I share your frustration.

* For reasons I have not had time to investigate, the binary version of `zowie` takes a very long time to start up on macOS 10.15 (Catalina) and 11.1 (Big Sur).  On my test system inside a virtual machine running on a fast iMac, it takes 10 seconds or more before the first output from `zowie` appears.


## Additional tips

In the [wiki associated with the Zowie project in GitHub](https://github.com/mhucka/zowie/wiki), I have started writing some notes about how I personally use Zowie to combine Zotero with DEVONthink.


## Getting help

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/mhucka/zowie/issues) for this repository.


## Contributing

I would be happy to receive your help and participation if you are interested.  Everyone is asked to read and respect the [code of conduct](CONDUCT.md) when participating in this project.  Development generally takes place on the `development` branch.


## License

This software is Copyright (C) 2020&ndash;2023, by Michael Hucka and the California Institute of Technology (Pasadena, California, USA).  This software is freely distributed under a 3-clause BSD type license.  Please see the [LICENSE](LICENSE) file for more information.


## Acknowledgments

This work is a personal project developed by the author, using computing facilities and other resources of the [California Institute of Technology Library](https://www.library.caltech.edu).

The [vector artwork](https://thenounproject.com/term/tag-exclamation-point/326951/) of an exclamation point circled by a zigzag, used as the icon for this repository, was created by  [Alfredo @ IconsAlfredo.com](https://thenounproject.com/AlfredoCreates/) from the Noun Project.  It is licensed under the Creative Commons [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/) license.

Zowie makes use of numerous open-source packages, without which Zowie could not have been developed.  I want to acknowledge this debt.  In alphabetical order, the packages are:

* [aenum](https://pypi.org/project/aenum/) &ndash; advanced enumerations for Python
* [biplist](https://bitbucket.org/wooster/biplist/src/master/) &ndash; A binary plist parser/writer for Python
* [boltons](https://github.com/mahmoud/boltons/) &ndash; package of miscellaneous Python utilities
* [bun](https://github.com/caltechlibrary/bun) &ndash; a set of basic user interface classes and functions
* [CommonPy](https://github.com/caltechlibrary/commonpy) &ndash; a collection of commonly-useful Python functions
* [fastnumbers](https://github.com/SethMMorton/fastnumbers) &ndash; number testing and conversion functions
* [ipdb](https://github.com/gotcha/ipdb) &ndash; the IPython debugger
* [keyring](https://github.com/jaraco/keyring) &ndash; access the system keyring service from Python
* [pdfrw](https://github.com/pmaupin/pdfrw) &ndash; a pure Python library for reading and writing PDFs
* [plac](http://micheles.github.io/plac/) &ndash; a command line argument parser
* [py-applescript](https://pypi.org/project/py-applescript/) &ndash; a Python interface to AppleScript
* [PyInstaller](http://www.pyinstaller.org) &ndash; a packaging program that creates standalone applications from Python programs
* [pyobjc](https://github.com/ronaldoussoren/pyobjc) &ndash; Python &rlhar; Objective-C and macOS frameworks bridge
* [pyxattr](https://github.com/iustin/pyxattr) &ndash; access extended file attributes from Python
* [pyzotero](https://github.com/urschrei/pyzotero) &ndash; a Python API client for Zotero
* [setuptools](https://github.com/pypa/setuptools) &ndash; library for `setup.py`
* [Shiv](https://github.com/linkedin/shiv) &ndash; command-line utility for creating self-contained Python zipapps
* [Sidetrack](https://github.com/caltechlibrary/sidetrack) &ndash; simple debug logging/tracing package
* [wheel](https://pypi.org/project/wheel/) &ndash; setuptools extension for building wheels

The [developers of DEVONthink](https://www.devontechnologies.com/about), especially Jim Neumann and Christian Grunenberg, quickly and consistently replied to my many questions on the [DEVONtechnologies forums](https://discourse.devontechnologies.com).
