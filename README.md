# sast-parser

[![Docker](https://github.com/pcfens/sast-parser/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/pcfens/sast-parser/actions/workflows/main.yml)

A simple tool to make understanding GitLab SAST reports a little bit
easier.

## Installation

```bash
pip install -r requirements.txt
```

## Building

```bash
docker build -t sast-parser .
```

## Running

### From source

```bash
usage: parse-sast.py [-h] [--only-severities ONLY_SEVERITIES]
                     [--jsonpath-filter JSONPATH_FILTER]
                     files [files ...]
```

### From docker

```bash
docker run --rm -it -v "$(pwd):/reports" sast-parser [-h] [--only-severities ONLY_SEVERITIES]
                     [--jsonpath-filter JSONPATH_FILTER]
                     files [files ...]
```

You can the create an alias to make it easier to run:

```bash
alias sast-parser="docker run --rm -it -v \"$(pwd):/reports\" sast-parser"
```