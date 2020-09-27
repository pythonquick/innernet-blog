---
title: "ag - the silver searcher"
date: 2020-01-20
section: aaa
category:
- terminal
tags:
- terminal
- vim
slug: ag-the-silver-searcher
---

[Ag](https://geoff.greer.fm/ag/) is an open-source command line search tool similar to grep, just much faster.

This page is a list of some notes and tips for common searches.

## Case-sensitive search

When searching for a pattern that is all lowercase, Ag will search case-insensitively.

For example:

    :::Bash
    ag elixir

This will match both "elixir" and "Elixir" in files in the current directory or deeper.

To search case-sensitively, add the `-s` option:

    :::Bash
    ag elixir -s

This will only match occurrences of "elixir" but not "Elixir".

When the search term uses mixed case, Ag will automatically search case-sensitively.
This is referred to as "smart case"

    :::Bash
    ag Elixir

This will match both "Elixir" but not "elixir".

## Regular Expressions

This section is a collection of some useful regular expressions used in the search pattern.
The search pattern can include regex searches, but often need many escape characters,
e.g. `\\b` to match a word-boundary, instead of `\b`.
To avoid excessive escape characters, it's easier to surround the pattern in quotes by default.

#### Find lines starting with "init(), but indented by at least one white-space character":

    :::Bash
    ag "^\s+init\(\)"

#### Find whole word "row" match:

    :::Bash
    ag "\brow\b"

#### Find blank lines:

    :::Bash
    ag "^$"

#### Find locations with 2 or more consecutive blank lines:
    :::Bash
    ag "^\n{2,}"

#### Same as before, but "blank" lines may include whitespace:
    :::Bash
    ag "^(\s*\n){2,}"

#### Find lines ending with `',`
    :::Bash
    ag "',$"

#### Find lines starting with "import Route":
    :::Bash
    ag "^import Route"

#### Find match "height" if it's preceded by either "max" or "avail":
    :::Bash
    ag "(max|avail)height"

#### Find all 3 or 4 digit numbers:
    :::Bash
    ag "\b\d{3,4}\b"

#### Find all 24-character words:
    :::Bash
    ag "\b\w{24}\b"

#### find all date format strings in quotes, e.g. "YYYY-MM-DD":
    :::Bash
    ag "['\"][ymd-]{4,12}['\"]"

## Search within specific file types or file patterns

It is often useful to restrict searches to certain file types to reduce the list of matches. 
For example adding `--js` will only search for javascript files with the '.js' file extension.
Run `ag --list-file-types` to see available file types.

To restrict the search to specific files, either list the files after the search pattern
or use the `-G` switch to match the file name. For example, to search only Ruby files
where the file name ends with "_controller.rb", find lines that assign a new
Service instance:

    :::Bash
    ag "= \w+Service\.new\b" -G _controller\.rb

Or, within Ruby files, find lines that assign a new class instance:

    :::Bash
    ag "= \w*\.new\b" --ruby

## Literal match

If you want to search a pattern that contains special regex characters, but you
want to treat those characters as part of a regex, use the `Q` option, which means
"literal match".

For example, find occurrences of "height()" literally:

    :::Bash
    ag "height()" -Q

