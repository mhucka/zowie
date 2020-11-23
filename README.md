Zuppa
======

Zuppa (_"**Z**otero **U**RI **P**DF **P**rop**er**ty" **A**nnotator_) is a command-line program that writes Zotero item URIs into the PDF files of a Zotero database.  Zuppa is written in Python and runs on macOS.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Latest release](https://img.shields.io/github/v/release/mhucka/zupper.svg?style=flat-square&color=b44e88)](https://github.com/mhucka/zupper/releases)


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#authors-and-acknowledgments)


Introduction
------------

When using [Zotero](https://zotero.org), you may on occasion want to work with the PDF files from outside of Zotero.  For example, if you're a [DEVONthink](https://www.devontechnologies.com/apps/devonthink) user, you will at some point discover the power of indexing your local Zotero database from DEVONthink.  However, when viewing or manipulating the PDF files from outside of Zotero, you may run into the following problem: when looking at a given PDF file, _how do you find out which Zotero entry it belongs to_?

Enter Zuppa (a loose acronym for _"**Z**otero **U**RI **P**DF **P**rop**er**ty **A**nnotator"_).  Zuppa looks through the files in a local Zotero for Mac database, looks up the URIs for each PDF file found, and writes the URIs into (depending on the user's choice) the PDF file and/or an extended attribute used for macOS Finder/Spotlight comments.


Installation
------------
 
[_..Forthcoming..._]


Usage
-----

[_..Forthcoming..._]

`com.apple.metadata:kMDItemFinderComment`


Known issues and limitations
----------------------------

[_..Forthcoming..._]


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

Copyright (c) 2020 by Michael Hucka and the California Institute of
Technology.


Acknowledgments
---------------

This work is a personal project developed by the author, using computing facilities and other resources of the [California Institute of Technology Library](https://www.library.caltech.edu).
