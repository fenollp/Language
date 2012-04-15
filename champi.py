#!/usr/bin/env
#-*- coding: utf-8 -*-

import re

def there_are_rules_in( text ):
  return ( len(find_first_rule( text )) >= 1 )



def apply_first_found_rule( text ):
  (patt, rep) = find_first_rule( text )
  return re.sub( re.escape(patt), rep, text )



def find_first_rule( text ):
  global rule_string

  mask = u' \( \s* ([^' + rule_string + u'\n' + u']+) \s* \) '
  regex = re.compile(mask + u'\s*' + rule_string + u'\s*' + mask, re.S | re.X)
  matches = regex.findall( text )

  return {
    "pattern": matches[0][0].decode('utf-8'),
    "replacement": matches[0][1].decode('utf-8')
  }




iput = '''
    (patt) ê (replacement)
    (patt) y (replacement)
    ( p ) y ( r)

  patt <---
'''.decode('utf-8')

rule_string = u'y'


# Tests
# print find_first_rule(raw)
# print there_are_rules_in(raw)



### Algorithm
raw = iput
while there_are_rules_in( raw ):
  apply_first_found_rule( raw )
print raw
###





