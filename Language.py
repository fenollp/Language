#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Usage: ./$0 ‹file utf-8 encoded›

import re

def recur( source, schemes, rules=[] ):
  return extract_rules(source, schemes, rules)

def report_applied( raw, pattern, replacement ):
  #print raw
  print u"› Applied: ‘"+ pattern +u"’ ⟼  ‘"+ replacement +u"’"

def apply_rules_found( raw, rules ):
  # Unhappily: no scope consideration; can't discover schemes or rules anymoar…
  #   Thus a discutable way of handeling rules
  i = 0
  for rule in rules:
    pat = rule["pattern"]
    if not re.search(pat, raw):
      i += 1
      continue
    rep = rule["replacement"]
    raw = re.sub(pat, rep, raw)
    report_applied(raw, pat, rep)
  if i == len(rules):
    return raw
  return apply_rules_found(raw, rules)

def extract_rules( raw, schemes, rules ):
  for scheme in schemes:
    match = scheme["regex"].search(raw)
    if not match:
      if schemes[len(schemes)-1] == scheme:
        return apply_rules_found(raw, rules)
      continue
    (pattern, replacement) = match.groups()
    rules.append({"pattern":pattern, "replacement":replacement})
    # Apply once to raw's rest
    raw = raw[:match.start()] + re.sub(pattern, replacement, raw[match.end():])
    report_applied(raw, pattern, replacement)
    return extract_rules(raw, schemes, rules)

def re_escape( string ):
  return string

def new_scheme( middle ):
  lateral = 'jilk'
  return re.compile(lateral +"\s+(.+)\s+"+re_escape(middle)+"\s+(.+)\s+"+ lateral)

schemes = []
schemes.append({"regex":new_scheme('\-\|\-'), "kind":'single-headed'})
schemes.append({"regex":new_scheme('d=xXx=b'), "kind":'double-headed'})

import sys
raw = open(sys.argv[1]).read().decode('utf-8')
print raw
print recur(raw, schemes)

