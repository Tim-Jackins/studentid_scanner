# Student ID Scanner

> This repository includes the code and 3d files for my lightweight portable ID scanner.

The acrylic build consists of two parts: one for the holding of cards and one for the camera mount. The webcam should be placed in the mount, as it is shown in solid works, and then plugged into your computer. You can then run the code and scan IDs to your hearts content.

## Table of Contents

- [Background](#background)
  - [Problem](#problem)
  - [Solution](#solution)
- [Install](#install)
  - [Bash](#bash)
  - [Python](#python)
- [Usage](#usage)
  - [Demo](#demo)
  - [Actual](#actual)
- [Questions](#questions)
- [Contribute](#contribute)
- [License](#license)

## Background

### Problem
This project started when I was late to school one day and noticed the arbitarily long amount of time it takes for a student to sign into school. 'Sign in' is currently done using a google form that takes every student about a minute to fill out. This isn't a problem when just a few student show up late; however, our current situation is as follows: let's say 5 (A-E) students show up right at 9:05 and must fill out the form. Each student will add at least 1 minute to their time with student E being disproportionally hit with 5 minutes added to his time, this is unfair. This problem becomes exacerbated when 5 more students show after the first five, potentially allowing a student who arrived at 9:05 actually getting to class at 9:15. 

### Solution
So I thought: "Wow, this is dumb considering we have individual student IDs that could totally be used to sign in, especially because the administration paid for these things." So I threw together a small program capable of snapping photos of IDs and reading useful info (ie name, ID) off of them. I then combined that with a program I had for writing data to google spreadsheets. This device is capable of signing in students in ~4 seconds.

## Install

*Warning*
This process is not for the faint of heart seeing as how this is not a complete project. Feel free to contact me if you have questions about the process.

### Bash

First we need to install the bash modules:

```bash
sudo apt-get install gocr-tk \
  tesseract-ocr \
  libtesseract-dev \
  python3-tk
```

### Python

Next up all the module requirements:

```python
sudo -H pip3 install --trusted-host pypi.python.org -r requirements.txt
```

For any questions about the google spreadsheet api please visit [this tutorial](https://github.com/burnash/gspread)

## Usage

### Demo

A proof of concept menu is available at [/software/menu.py](https://github.com/Tim-Jackins/studentid_scanner/blob/master/software/menu.py). Feel free to check it out, it is scanning photos taken with my phones camera making scanning vastly more simple. It uses pytessaract, a python wrapper for tessaract, to scan photos and regex to find useful data in those photos.

### Actual

A menu is not yet available for the actually code, just call [/software/commands/scan_and_write.py](https://github.com/Tim-Jackins/studentid_scanner/blob/master/software/commands/scan_and_write.py) when a card is loaded into the scanner to scan and write it.

## Questions

Feel free to send me an email if you have any questions about using the code for something interesting.

## Contribute

Feel free to contribute in the following ways:

- [Open an issue!](https://github.com/Tim-Jackins/slackbot-template/issues/new) but please use [the issue template](.github/issue_template.md)
- [Pull Requests](https://github.com/Tim-Jackins/studentid_scanner/compare) are both encouraged and appreciated!
- Please abide by the [code of conduct](docs/CODE_OF_CONDUCT.md).

## License

[GPL-3.0](LICENSE) © Jack Timmins