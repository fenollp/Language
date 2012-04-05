#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Usage: ./$0 ‹file utf-8 encoded›.langh

# Input a file, see how your rules are applied (only once)

import re
lateral = 'jilk'; middle = '-|-'
scheme = re.compile(lateral +"\s+(.+)\s+\-\|\-\s+(.+)\s+"+ lateral)


def recur( raw ):
  global scheme
  match = scheme.search(raw)  # Greedy or not greedy?
  # ie: the sad limitation of this implementation, regex
  if not match:
    # Cannot apply any longer
    return raw

  (pattern, replacement) = match.groups()
  raw = raw[:match.start()] + re.sub(pattern, replacement, raw[match.end():])
  print raw
  print u"› Applied: ‘"+ pattern +u"’ ⟼  ‘"+ replacement +u"’"

  return recur(raw)


import sys
raw = open(sys.argv[1]).read().decode('utf-8')
print raw
recur(raw)

