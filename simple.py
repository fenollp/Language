#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Usage: ./$0 ‹file utf-8 encoded› [--options]

import sys
raw = open(sys.argv[1]).read().decode('utf-8')

import re
lateral = 'jilk'; middle = '-|-'
scheme = re.compile(lateral +" \s*(.+)\s* \-\|\-(?: \s*(\-i)\s* \-\|\-)? \s*(.+)\s* "+ lateral)

def apply( raw ):
  match = scheme.search(raw)
  if not match:
    return raw

  (pattern, modifier, replacement) = match.groups()
  #raw = re.sub(regex, '', raw, 1)
  pos_start = match.start(); pos_end = match.end()
  raw = raw[:pos_start] +raw[pos_end:]

  flags = 0
  if modifier == u'-i':
    flags = re.IGNORECASE
  regex = re.compile(pattern, flags)
  raw = re.sub(regex, replacement, raw)

  return raw

print apply(raw)
