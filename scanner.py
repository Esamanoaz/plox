from tokentype import TokenType
from token import Token
from lox import Lox

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        self.digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.token_strings = {
            '(': lambda c: TokenType.LEFT_PAREN,
            ')': lambda c: TokenType.RIGHT_PAREN,
            '{': lambda c: TokenType.LEFT_BRACE,
            '}': lambda c: TokenType.RIGHT_BRACE,
            ',': lambda c: TokenType.COMMA,
            '.': lambda c: TokenType.DOT,
            '-': lambda c: TokenType.MINUS,
            '+': lambda c: TokenType.PLUS,
            ';': lambda c: TokenType.SEMICOLON,
            '*': lambda c: TokenType.STAR,
            '!': lambda c: TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG,
            '=': lambda c: TokenType.EQUAL_EQUAL if self._match('=') else TokenType.BANG,
            '<': lambda c: TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS,
            '>': lambda c: TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER,
            '/': lambda c: self._slash_logic(),
            # Ignore whitespace
            ' ': lambda c: None,
            '\r': lambda c: None,
            '\t': lambda c: None,
            '\n': lambda c: self._advance_line(),
            '"': lambda c: self._string_logic(),
        }

    '''
    Scans the source and returns a token list -> self.tokens
    '''
    def scan_tokens(self):
        while not self._is_at_end():
            # We are at the beggining of the next lexeme
            start = self.current
            self._scan_token()
        
        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens
    

    '''
    Scans the next character and finds out what TokenType it is

    Then adds it to self.tokens
    '''
    def _scan_token(self):
        c = self._advance() # c = next character
        if c in self.token_strings:
            if self._is_digit(c):
                self._number_logic()
            else:
                c = self.token_strings[c](c) # get key c and return value c (which is a lambda returning the correct token)
                if c is not None:
                    self._add_token(c)
        elif self._is_digit(c): 
            self._number_logic()
        else:
            Lox.error(self.line, 'Unexpected character.')
    

    def _slash_logic(self):
        if self._match('/'): # if the next char is also '/':
            # A comment goes until the end of the line
            while (self._peek() != '\n') and not self._is_at_end(): 
                self._advance()
        else:
            self._add_token(TokenType.SLASH)
    

    def _string_logic(self):
        while (self._peek() != '"') and not self._is_at_end():
            if self._peek() == '\n': # Strings are multiline, so when we hit a newline, line++
                self.line += 1 
            self._advance()
        
        if self._is_at_end():
            Lox.error(self.line, 'Unterminated string.')
            return None
        
        # The closing "
        self._advance()

        # Get the string's content and trim the surrounding quotes
        value = self.source[self.start+1:self.current-1]
        self._add_token(TokenType.STRING, value)
    

    def _number_logic(self):
        while self._is_digit(self._peek()):
            self._advance()
        
        # Look for a decimal
        if self._peek() == '.' and self._is_digit(self._peek_next()):
            # Consume the '.'
            self._advance()
            # Keep advancing until we reached the end of the number
            while self._is_digit(self._peek()):
                self._advance()
        
        self._add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))


    '''
    Checks to see if the next character matches expected
    '''
    def _match(self, expected):
        if self._is_at_end():
            return False
        if self.source[self.current] != expected: # if the next character is not expected
            return False

        self.current += 1
        return True
    

    '''
    Checks the next character
    '''
    def _peek(self):
        if self._is_at_end():
            return '\0'
        return self.source[current]
    

    def _peek_next(self):
        if (self.current + 1) >= len(self.source):
            return '\0'
        return self.source[self.current + 1]


    def _is_at_end(self):
        return (current >= len(self.source))
    

    def _is_digit(self, c):
        return c in self.digits


    '''
    Moves forward one character
    '''
    def _advance(self):
        self.current += 1
        return self.source[self.current - 1]
    

    def _add_token(self, token_type):
        self._add_token(token_type, None)
    

    def _add_token(self, token_type, literal):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
    

    def _advance_line(self):
        self.line += 1