#=========================================================================
class LexicalError(Exception):
    pass
class Lexer:
    def __init__(self, filename):
        print(f"[LEXER] Initializing lexer with file: {filename}")
        with open(filename, 'r', encoding='utf-8') as file:
            self.source_code = file.read()
        self.tokens = []
        self.token_spec = [
            ('FSTRING', r'f"([^"\\]*(?:\\.[^"\\]*)*)"|f\'([^\']*(?:\\.[^\']*)*)\''), 
            ('STRING', r'"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\']*(?:\\.[^\']*)*)\''), 
            ('MULTILINE_STRING', r'"""(.*?)"""|\'\'\'(.*?)\'\'\''), 
            ('RAWSTRING', r'r"([^"]*)"|r\'([^\']*)\''), 
            ('NUMBER', r'\b\d+(\.\d+)?([eE][-+]?\d+)?\b'),  
            ('KEYWORD', r'\b(if|else|elif|while|for|def|return|import|from|as|class|try|except|finally|break|continue|pass|lambda|yield|with|not|or|and|is|in|global|nonlocal|del|assert|raise|async|await|match|case)\b'),
            ('BOOLEAN', r'\b(True|False|None)\b'),  
            ('ASSIGN', r'='), 
            ('PLUS', r'\+'), 
            ('MINUS', r'-'), 
            ('MULT', r'\*'), 
            ('DIV', r'/'),
            ('MOD', r'%'), 
            ('POW', r'\*\*'), 
            ('FLOORDIV', r'//'),  
            ('EQ', r'=='), 
            ('NEQ', r'!='), 
            ('LTE', r'<='), 
            ('GTE', r'>='), 
            ('LT', r'<'), 
            ('GT', r'>'),
            ('BIT_OR', r'\|'), 
            ('BIT_AND', r'&'), 
            ('BIT_XOR', r'\^'), 
            ('BIT_NOT', r'~'),
            ('SHIFT_LEFT', r'<<'), 
            ('SHIFT_RIGHT', r'>>'),
            ('AUG_ASSIGN', r'(\+=|-=|\*=|/=|%=|\*\*=|//=|&=|\|=|\^=|>>=|<<=)'),
            ('LPAREN', r'\('), 
            ('RPAREN', r'\)'), 
            ('LBRACE', r'\{'), 
            ('RBRACE', r'\}'),
            ('LBRACKET', r'\['), 
            ('RBRACKET', r'\]'), 
            ('COMMA', r','), 
            ('COLON', r':'),
            ('DOT', r'\.'), 
            ('SEMICOLON', r';'),
            ('ID', r'[a-zA-Z_][a-zA-Z_0-9]*'),  
            ('COMMENT', r'#.*'),
            ('MULTILINE_COMMENT', r'"""(.*?)"""|\'\'\'(.*?)\'\'\''),  
            ('NEWLINE', r'\n'),  
            ('SKIP', r'[ \t]+'),  
            ('UNKNOWN', r'.')
        ]
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_spec)
        self.indent_stack = [0]
    def tokenize(self):
        import re
        print("[LEXER] Starting tokenization")
        previous_indent = 0
        for line_number, line in enumerate(self.source_code.splitlines(), start=1):
            print(f"[LEXER] Processing line {line_number}: {line}")
            match = re.match(r'^[ \t]*', line)
            indent_size = len(match.group(0)) if match else 0
            if indent_size > previous_indent:
                self.tokens.append(('INDENT', indent_size))
                self.indent_stack.append(indent_size)
                print(f"[LEXER] Increased indent to {indent_size}")
            while indent_size < previous_indent and self.indent_stack:
                dedent_val = self.indent_stack.pop()
                self.tokens.append(('DEDENT', dedent_val))
                print(f"[LEXER] Dedented to {dedent_val}")
            previous_indent = indent_size
            for match in re.finditer(self.token_regex, line):
                kind = match.lastgroup
                value = match.group()
                if kind == 'UNKNOWN':
                    raise LexicalError(f"✘  Lexical Error: Unrecognized token '{value}' at line {line_number}")
                if kind == 'NUMBER':
                    value = float(value) if '.' in value or 'e' in value.lower() else int(value)
                elif kind in ('STRING', 'FSTRING', 'MULTILINE_STRING', 'RAWSTRING'):
                    value = value[1:-1]
                elif kind in ('COMMENT', 'MULTILINE_COMMENT', 'SKIP'):
                    continue
                self.tokens.append((kind, value))
        while self.indent_stack:
            ded = self.indent_stack.pop()
            self.tokens.append(('DEDENT', ded))
            print(f"[LEXER] Final dedent: {ded}")
        print(f"[LEXER] Finished tokenization. Total tokens: {len(self.tokens)}")
        from collections import Counter
        token_counts = Counter(token[0] for token in self.tokens)
        print("[LEXER] Token summary:")
        for token_type, count in token_counts.items():
            print(f"  {token_type}: {count}")
        return self.tokens
#=========================================================================
