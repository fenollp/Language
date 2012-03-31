#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Usage: ./$0 ‹file utf-8 encoded›

import sys
raw = open(sys.argv[1]).read().decode('utf-8')

import re
lateral = 'jilk'; middle = '-|-' #add escape_regex/1
scheme = re.compile(lateral +"\s+(.+)\s+\-\|\-(?:\s+(.+)\s+\-\|\-)?\s+(.+)\s+"+ lateral)

def recur( raw ): #may be function of scheme someday
  global scheme
  match = scheme.search(raw)  # Greedy or not greedy?
  if not match:  # Cannot apply any longer
    return raw

  (pattern, modifier, replacement) = match.groups()
  pos_start = match.start(); pos_end = match.end()
  raw = raw[:pos_start] +raw[pos_end:]

  flags = 0 #more flags to come
  if modifier == u'-i':
    flags = re.IGNORECASE
  regex = re.compile(pattern, flags)
  raw = re.sub(regex, replacement, raw)

  print raw, "Applied: ", pattern, " --> ", replacement, " / ", modifier
  return recur(raw)  # Keeps applying

print recur(raw)
