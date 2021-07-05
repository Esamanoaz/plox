from tokentype import TokenType
from token import Token
import lox

class Scanner:
    def __init__(self, source, interpreter):
        self.source = source
        self.interpreter = interpreter
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        self.alpha = [ # lowercase, uppercase, and underscore
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
            'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
            'Y', 'Z',
            '_'
        ]
        self.digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # .isdigit() could work but it checks more than we want or need
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
            '=': lambda c: TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL,
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
        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE,
        }

    '''
    Scans the source and returns a token list -> self.tokens
    '''
    def scan_tokens(self):
        while not self._is_at_end():
            # We are at the beggining of the next lexeme
            self.start = self.current
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
            c = self.token_strings[c](c) # get key c and return value c (which is a lambda returning the correct token)
            if c is not None:
                self._add_token(c)
        elif self._is_digit(c): 
            self._number_logic()
        elif self._is_alpha(c):
            self._identifier_logic()
        else:
            self.interpreter.error(line=self.line, message='Unexpected character.')
    

    def _identifier_logic(self):
        while self._is_alpha_numeric(self._peek()):
            self._advance()

        # if the lexeme is not a keyword, the lexeme is an identifier. Otherwise, return the keyword token type
        text = self.source[self.start:self.current]
        t_type = self.keywords.get(text) # t_type means token type
        if t_type is None:
           t_type = TokenType.IDENTIFIER
        
        self._add_token(t_type)
    

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
            self.interpreter.error(line=self.line, message='Unterminated string.')
            return None # return so that we skip the below code and an index error is not thrown
        
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
        return self.source[self.current]
    

    def _peek_next(self):
        if (self.current + 1) >= len(self.source):
            return '\0'
        return self.source[self.current + 1]


    def _is_alpha(self, c):
        return c in self.alpha # this includes '_'
    

    def _is_alpha_numeric(self, c):
        return self._is_alpha(c) or self._is_digit(c)


    def _is_at_end(self):
        return (self.current >= len(self.source))
    

    def _is_digit(self, c):
        return c in self.digits


    '''
    Moves forward one character
    '''
    def _advance(self):
        self.current += 1
        return self.source[self.current - 1]


    def _add_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))


    def _advance_line(self):
        self.line += 1