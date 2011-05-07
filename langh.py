#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Je préfère prévenir, c'est beaucoup plus volumineux que les codes Ocaml, d'une part parce que tout est fait à la main (y compris le lexer, les Genlex et consort c'est de la triche   ), 
#  et d'autre part parce que plutôt que d'interpréter directement le code, j'ai préféré construire un arbre syntaxique, et ensuite l'évaluer. L'avantage c'est que ça permet d'étendre 
#  le langage rapidement, et puis si je suis vraiment motivé (comprendre : j'ai rien à foutre de mes journées), ça peut constituer le front-end d'un compilateur.
# Voilà où le projet en est : on a
#  les opérateurs arithmétiques + - * / ;
#  les opérateurs de comparaison < <= > >= = <> ;
#  les définitions de variables avec (define the_answer 42);
#  les structures if-then-else avec (if ga then bu else zo);
#  une gestion à peu près correcte des erreurs (avec un affichage de où-c'est-qu'-ça-a-foiré™).
# Il n'existe que deux types d'instructions (statement dans le code): les définitions de variables avec define et le reste; toutes les instructions autres que les define renvoient une valeur 
#  (y compris les if-then-else, ça change agréablement du comportement de python), les définitions ne renvoient rien (enfin, qui dit rien en Python dit None).
# L'évaluation est paresseuse (enfin, si je me plante pas sur ce que c'est qu'une évaluation paresseuse). On peut donc écrire (define y x) (define x 3) (y) et paf, 
#  ça fait des chocapics renvoie 3.

# Voilà la grammaire du machin :
#  program         ::= statement_list
#  statement_list  ::= "(" statement ")" statement_list
#                   |  NOTHING
#  statement       ::= assign_stmt
#                   |  expr_stmt
#  assign_stmt     ::= "define" ID expr_stmt
#  expr_stmt       ::= "if" atom "then" atom "else" atom
#                   |  OP atom_list
#                   |  atom
#  atom_list       ::= atom atom_list
#                   |  NOTHING
#  atom            ::= NUM
#                  ::= ID
#                   |  "(" expr_stmt ")"

# Et voilà les 4 fichiers que sont le module des erreurs :

# -- Lexical errors


class PLLexicalError(Exception):
    def __init__(self, value, start_pos, end_pos):
        self.value = value
        self.start_pos = start_pos
        self.end_pos = end_pos


class UnknownOpError(PLLexicalError):
    def __str__(self):
        return "Unknown operator '" + str(self.value) + "'"


class IllicitCharError(PLLexicalError):
    def __str__(self):
        return "Illicit character '" + str(self.value) + "'"


# -- Syntax errors


class PLSyntaxError(Exception):
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg


class UnknownIdError(PLSyntaxError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Unknown identifier '" + self.name + "'"


# Lexer :


import string

# Some utility lists
_end_char = '\0'
_digits = list(string.digits)
_letters = list(string.letters)
_whitespace = list(string.whitespace)
_opchars = ['+', '-', '*', '/', '<', '>', '=',]


# The token types
ID = 'an identifier'
KEYWD = 'a keyword'
NUM = 'a number'
OP = 'an operator'
LPAREN = 'a left parenthesis'
RPAREN = 'a right parenthesis'
END = 'the end'

class Lexer:
    def __init__(self, input="", keywords=[], operators=['+', '-', '*', '/']):
        self.keywords = keywords
        self.operators = operators
        self.set_input(input)

    def set_input(self, input):
        self.pos = 0
        self.start_pos = 0
        self.pos_max = len(input)
        self.input = input + _end_char
        self.current_token = self.read_next_token()

    # Return the token being read and scan the next.
    def get_token(self):
        current_token = self.current_token
        self.current_token = self.read_next_token()
        return current_token

    # Return the token being read without scanning the next. That is, several
    # successive calls to 'peek()' will give the same result, while successive
    # calls to 'get_token()' would give three different results (the three next
    # tokens).
    def peek(self):
        return self.current_token

    # Scan the next token and return it.
    def read_next_token(self):
        self.last_start_pos = self.start_pos
        self.last_pos = self.pos

        # Skip _whitespace
        while self.input[self.pos] in _whitespace:
            self.pos += 1

        # Remember the start position of the token being read for debugging
        self.start_pos = self.pos
        cur_char = self.input[self.pos] # The current characterbeing read

        # If we are reading an identifier or a keyword
        if cur_char in _letters:
            result = ''
            while self.input[self.pos] in _letters + _digits + ['_']:
                result += self.input[self.pos]
                self.pos += 1
            
            # Check whether what was read is a keyword
            if result in self.keywords:
                return Token(KEYWD, result)
            else:
                return Token(ID, result)

        # If we are reading a number (positive or negative)
        elif cur_char in _digits + ['-', '+']:
            result = ''
            
            # We first have to check that if we read a '+' or '-', it is
            # followed by a digit to ensure it was a unary operator and not a
            # binary one
            if cur_char in ['+', '-'] and not self.input[self.pos+1] in _digits:
                self.pos += 1
                return Token(OP, cur_char)
            else:
                result += cur_char
                self.pos += 1

            while self.input[self.pos] in _digits:
                result += self.input[self.pos]
                self.pos += 1

            return Token(NUM, int(result))

        # If we are reading an operator
        elif cur_char in _opchars:
            result = ''
            while self.input[self.pos] in _opchars:
                result += self.input[self.pos]
                self.pos += 1

            if result in self.operators:
                return Token(OP, result)
            else:
                raise UnknownOpError(result, self.start_pos, self.pos)

        # Parentheses
        elif cur_char == '(':
            self.pos += 1
            return Token(LPAREN)
        elif cur_char == ')':
            self.pos += 1
            return Token(RPAREN)
                
        # The end of the input
        elif cur_char == _end_char:
            return Token(END)
        
        # Woops, that's not legal
        else:
            raise IllicitCharError(cur_char, self.start_pos, self.pos)


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value



# Arbres syntaxiques :


# Map an operator name to a function
op_dict = {
        '+':    lambda x,y: x + y,
        '-':    lambda x,y: x - y,
        '*':    lambda x,y: x * y,
        '/':    lambda x,y: x / y,
        '<':    lambda x,y: x < y,
        '<=':   lambda x,y: x <= y,
        '>':    lambda x,y: x > y,
        '>=':   lambda x,y: x >= y,
        '=':    lambda x,y: x == y,
        '<>':   lambda x,y: x != y
        }

# A generic syntax tree node.
# The __str__ part is there for debugging purposes.
class PLNode():
    def __str__(self):
        return '<(%s)>' % self.__class__.__name__


class AssignStmt(PLNode):
    def __init__(self, target, ast, context):
        self.target = target
        self.ast = ast
        self.context = context

    def eval(self):
        self.context.assign(target=self.target, ast=self.ast)


class IfThenElse(PLNode):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def eval(self):
        if self.condition.eval():
            return self.then_block.eval()
        else:
            return self.else_block.eval()


class Id(PLNode):
    def __init__(self, name, context):
        self.name = name
        self.context = context

    def eval(self):
        return self.context.fetch(target=self.name)


class Op(PLNode):

    def __init__(self, name, operands):
        self.name = name
        self.operands = operands

    def eval(self):
        if len(self.operands) != 2:
            msg = "Wrong number of arguments. Operator " + self.name +\
            " expected 2 arguments but got %d" % len(self.operands)
            raise PLSyntaxError(msg)
        func = op_dict[self.name]
        arg1 = self.operands[0].eval()
        arg2 = self.operands[1].eval()
        return func(arg1, arg2)


class Atom(PLNode):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class Num(Atom): pass



# Parser proprement dit :


import sys

# For debugging only. When 'pass' is replaced by 'print msg', it prints the
# list of the names of the productions that are matched.
def dump(msg):
    pass#print msg#pass


class Parser:
    def __init__(self, keywords=[], operators=['+','-','*','/']):
        self.input = input
        self.lexer = Lexer(keywords=keywords, operators=operators)
        self.global_context = Context(father=None)
        self.results = None
    
    # Parse the input into an abstract syntax tree
    def parse(self, input=""):
        self.input = input
        try:
            self.lexer.set_input(self.input)
            self.results = self.statement_list
        except PLLexicalError as e:
            print "(!) Lexical error (%d-%d): %s." \
                    % (self.lexer.last_start_pos, self.lexer.last_pos, e)
        except PLSyntaxError as e:
            print "(!) Syntax error (%d-%d): %s." \
                    % (self.lexer.last_start_pos, self.lexer.last_pos, e)
        except: raise

    def report_error(self, name_error, msg_error):
        start = self.lexer.last_start_pos
        stop = self.lexer.last_pos - 1
        print "(!) %s:" % (name_error)
        print "    %s" % self.input
        print "    %s^%s" % (" " * (start), "^" * (stop-start))
        print "    %s." % msg_error

    # A generator that returns the evaluations of the successive statements
    def eval(self):
        try:
            for result in self.results():
                yield result
        except PLSyntaxError as e:
            self.report_error("Syntax error", e)
        except: raise

    # Check that the current token is of the expected type. If it is, return
    # the value of the token; if a value was provided, check that the value of
    # the token is what we expected.
    def match(self, expected_type, expected_value=None):
        token = self.lexer.get_token()
        if token.type == expected_type:
            if expected_value == None or \
                (expected_value != None and token.value == expected_value):
                return token.value
            else:
                raise PLSyntaxError("I expected '%s' but got '%s'" %
                        (expected_value, token.value))
        else:
            raise PLSyntaxError("I expected %s but got %s" % 
                    (expected_type, token.type))

    # -- The functions correponding to productions in the grammar
        
    def statement_list(self):
        dump('statement_list')
        while self.lexer.peek().type == LPAREN:
            self.lexer.get_token()
            statement = self.statement()
            self.match(RPAREN)
            yield statement.eval()

    def statement(self):
        dump('statement')
        token = self.lexer.peek()
        
        # assign_stmt
        if token.type == KEYWD and token.value == "define":
            self.match(KEYWD)
            dump('assign_stmt')
            target = self.match(ID)
            ast = self.atom()
            return AssignStmt(target=target, ast=ast,
                    context=self.global_context)

        # expr_stmt
        else: return self.expr_stmt()

    def expr_stmt(self):
        dump('expr_stmt')
        token = self.lexer.peek()
        
        # if-then-else expression
        if token.type == KEYWD and token.value == "if":
            dump('if_stmt')
            self.match(KEYWD)
            condition = self.atom()
            self.match(KEYWD, "then")
            then_block = self.expr_stmt()
            self.match(KEYWD, "else")
            else_block = self.expr_stmt()
            return IfThenElse(condition=condition, then_block=then_block,
                    else_block=else_block)
        
        # An operation
        if token.type == OP:
            operator = self.match(OP)
            operands = self.atom_list()
            return Op(name=operator, operands=operands)
            
        # atom
        else: return self.atom()

    def atom_list(self):
        dump('atom_list')
        atoms = []

        # Get as much atoms as possible
        while self.lexer.peek().type in [NUM, ID, LPAREN]:
            atoms.append(self.atom())

        return atoms

    def atom(self):
        dump('atom')
        token = self.lexer.get_token()
        dump(token.type)

        # A number
        if token.type == NUM:
            return Num(value=token.value)
        
        # An identifier
        elif token.type == ID:
            return Id(name=token.value, context=self.global_context)

        # ( expr_stmt )
        elif token.type == LPAREN:
            result = self.expr_stmt()
            self.match(RPAREN)
            return result

        else:
            raise PLSyntaxError("I did not expect %s" % token.type)


# A context acts as a dictionary that maps an identifier to a syntax tree. Not
# that useful for now, but it will be when the keyword 'let' is introduced.
class Context():

    def __init__(self, father):
        # 'father' is the context of which 'self' is a sub-context; that is,
        # the father is a broader context.
        # father == None for the global context
        self.father = father
        

    # Assign a syntax tree to a name
    def assign(self, target, ast):
        return setattr(self, target, ast)

    # Get the tree associated to a name, searching from the current context
    # outwards
    def fetch(self, target):
        if hasattr(self, target):   # If the name is defined in this context
            return getattr(self, target).eval()
        elif self.father != None:   # If this is not the global context
            return self.father.fetch(target)
        else:               
            raise UnknownIdError(target)

# A very simple interface: the string that the parser should parse is given as
# a command line argument.
if __name__ == '__main__':
    try:
        parser = Parser(
                keywords=['define', 'if', 'then', 'else'],
                operators=['+', '-', '*', '/', '<', '<=', '>', '>=', '=', '<>']
                )
        parser.parse(input=' '.join(sys.argv[1:]))
        for result in parser.eval():
            print ":", result
    except PLSyntaxError as e: exit()
    except: raise


# Voili voilou.
# PS : un petit code de test:
#  $ ./parse.py "(define y (/ x 10)) (define x (- 0 -20)) (if 0 then (+ x (* y 2)) else (+ (* x y) 2))"
# Édité le 23/09/2009 à 01:59:14 par Bad_Wolf
