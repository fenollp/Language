#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Put your code into 'input'
#   I'll try not to use RegEx. It'll be hard!

input = '''( ((pattern) ê (replacement)) (ê) )'''

# ① Obliger GlobalScope
# ② Obliger PatternScheme


class LanghException(Exception):
  """
  Langh's most basic Exception.
  """
  def __init__( self,  w ):
    self.reason = w
    print(self)
  def __str__( self ):
    return self.__class__.__name__ + ': ' + self.reason

class LanghError(LanghException):
  """
  Langh's Error. It stops compilation.
  """
  def __init__( self,  w ):
    LanghException.__init__(self, w)
    from sys import exit
    exit(1)

class LanghWarning(LanghException):
  """
  Langh's Warning. Compilation continues.
  """
  pass

class SyntaxError(LanghError):
  pass
class GrammarError(LanghError):
  pass



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
    "Can't use one-level up variables"
    #global n
    #global nn
    nn = n
    n = new

  try:
    for i in range(len(c)):
      if c[i] == '(':
        #change_n(n + 1)
        nn = n  # n(-1)
        n = n+1 # n(0)
        if nn != 0:
          buffer += c[i]

      elif c[i] == ')':
        #change_n(n - 1)
        nn = n  # n(-1)
        n = n-1 # n(0)
        if n == 0:
          #print(buffer)#
          scopes.append(buffer)
          buffer = ''
        buffer += c[i]

      else:
        buffer += c[i]

      #print(n)#


    if len(scopes) == 0:
      raise GrammarError(
        "you didn't mind to embed your code in the GlobalScope, didn't you?")

    if n < 0:  # Une ')' trouvée, sans paire '(':
      # Le dernier scope est celui en cause
      raise SyntaxError(
        "cannot find (Global||local)Scope's ending" '\n' \
        "In: " + scopes[len(scopes) -1] + ')' '\n' \
        "Near " + '-'*(len("In: ") + len(scopes[len(scopes) -1]) -len("Near ") 
          -len(')')) + '↗' '\n' \
        '\t' "(unmatching left parenthesis)"
      )

  except LanghException as e:
    pass

  print(scopes)#
  return scopes

# ① Spliter en sous scopes
scopes = split_in_scopes(input)

n = nn = 0
# ② Appliquer les schemes
for scope in scopes:
  split_in_scopes(scope)
  c = scope
  for i in range(len(c)):
    pass

