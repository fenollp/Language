#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 

input = ''' ( (pattern) ê (replacement) ) '''

# ① Obliger GlobalScope
# ② Obliger PatternScheme


def split_in_scopes( input ):
  """
  str -> [str,]
  Splits the first level of Scopes
  """
  scopes = []

  c = input + '\n'
  buffer = ''

  n = 0   # n(i)
  nn = n  # n(i-1)
  def change_n( new ):
    global n
    global nn
    nn = n
    n = new

  for i in range(len(c)):
    if c[i] == '(':
      change_n(n + 1)
      if nn != 0:
        buffer += c[i]
    elif c[i] == ')':
      change_n(n - 1)
      if n == 0:
        #print(buffer)#
        scopes.append(buffer)
        buffer = ''
      buffer += c[i]
    else:
      buffer += c[i]
    #print(n)#

  if n < 0:  # Une ')' trouvée, sans paire '(':
    # Le dernier scope est celui en cause
    print("SyntaxError: " \
      "cannot find (Global||local)Scope's ending" '\n' \
      "In: " + scopes[-1] + ')' '\n' \
      "Near " + '-'*(len(scopes[-1]) +4 -5 -1) + '↗' '\n' \
      '\t' "(unmatching left parenthesis)"
    )

  print(scopes)#
  return scopes

# ① Spliter en sous scopes
scopes = split_in_scopes(input)

n = nn = 0
# ② Appliquer les schemes
for scope in scopes:
  c = scope
  for i in range(len(c)):
    pass

