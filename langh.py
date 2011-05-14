#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 

# input = open('./code.txt').read().decode('utf-8')
input = u''' ( (pattern) ê (replacement) ) '''

# ① Obliger GlobalScope
# ② Obliger PatternScheme


def split_in_scopes( input ):
  """
  str -> [str,]
  Splits the first level of Scopes
  """
  scopes = []

  c = input + u'\n'
  buffer = u''

  n = 0   # n(i)
  nn = n  # n(i-1)
  def change_n( new ):
    "Can't use one-level up variables"
    #global n
    #global nn
    nn = n
    n = new

  for i in range(len(c)):
    if c[i] == u'(':
      #change_n(n + 1)
      nn = n  # n(-1)
      n = n+1 # n(0)
      if nn != 0:
        buffer += c[i]
    elif c[i] == u')':
      #change_n(n - 1)
      nn = n  # n(-1)
      n = n-1 # n(0)
      if n == 0:
        #print(buffer)#
        scopes.append(buffer)
        buffer = u''
      buffer += c[i]
    else:
      buffer += c[i]
    #print(n)#

  if n < 0:  # Une ')' trouvée, sans paire '(':
    # Le dernier scope est celui en cause
    print(u"SyntaxError: " \
      u"cannot find (Global||local)Scope's ending" u'\n' \
      u"In: " + scopes[-1] + u')' u'\n' \
      u"Near " + u'-'*(len(scopes[-1]) +4 -5 -1) + u'↗' u'\n' \
      u'\t' u"(unmatching left parenthesis)"
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

