class Lexer:
    def __init__(self, input="", keywords=[], operators=['+', '-', '*', '/']):
        self.keywords = keywords
        self.operators = operators
        self.set_input(input)

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

        # Parentheses
        if cur_char == '(':
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

