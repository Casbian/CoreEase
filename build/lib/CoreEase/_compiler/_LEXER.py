#=========================================================================
class LexicalError(Exception):
    pass
class Lexer:
    def __init__(self,filename):
        import re
        print(f"[LEXER] Initializing lexer with file:{filename}")
        with open(filename,'r',encoding='utf-8') as file:
            self.source_code=file.read()
        self.tokens=[]
        self.token_spec=[
            ('FSTRING',r'(f"([^"\\]*(?:\\.[^"\\]*)*)"|f\'([^\'\\]*(?:\\.[^\'\\]*)*)\')'),
            ('RAWSTRING',r'(r"([^"\\]*(?:\\.[^"\\]*)*)"|r\'([^\'\\]*(?:\\.[^\'\\]*)*)\')'),
            ('STRING',r'("([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\')'),
            ('NUMBER',r'\b\d+(\.\d+)?([eE][-+]?\d+)?\b'),
            ('KEYWORD',r'\b(if|else|elif|while|for|def|return|import|from|as|class|try|except|finally|break|continue|pass|lambda|yield|with|not|or|and|is|in|global|nonlocal|del|assert|raise|async|await|match|case)\b'),
            ('BOOLEAN',r'\b(True|False|None)\b'),
            ('AUG_ASSIGN',r'(\+=|-=|\*=|/=|%=|\*\*=|//=|&=|\|=|\^=|>>=|<<=)'),
            ('EQ',r'=='),
            ('NEQ',r'!='),
            ('LTE',r'<='),
            ('GTE',r'>='),
            ('SHIFT_LEFT',r'<<'),
            ('SHIFT_RIGHT',r'>>'),
            ('FLOORDIV',r'//'),
            ('POW',r'\*\*'),
            ('ASSIGN',r'='),
            ('PLUS',r'\+'),
            ('MINUS',r'-'),
            ('MULT',r'\*'),
            ('DIV',r'/'),
            ('MOD',r'%'),
            ('LT',r'<'),
            ('GT',r'>'),
            ('BIT_OR',r'\|'),
            ('BIT_AND',r'&'),
            ('BIT_XOR',r'\^'),
            ('BIT_NOT',r'~'),
            ('LPAREN',r'\('),
            ('RPAREN',r'\)'),
            ('LBRACE',r'\{'),
            ('RBRACE',r'\}'),
            ('LBRACKET',r'\['),
            ('RBRACKET',r'\]'),
            ('COMMA',r','),
            ('COLON',r':'),
            ('DOT',r'\.'),
            ('SEMICOLON',r';'),
            ('DECORATOR',r'@[a-zA-Z_][a-zA-Z_0-9]*'),
            ('ID',r'[a-zA-Z_][a-zA-Z_0-9]*'),
            ('COMMENT',r'#.*'),
            ('NEWLINE',r'\n'),
            ('SKIP',r'[ \t]+'),
            ('UNKNOWN',r'.')
        ]
        self.token_regex='|'.join(f'(?P<{name}>{pattern})'for name,pattern in self.token_spec)
        self.token_pattern=re.compile(self.token_regex,re.DOTALL)
        self.indent_stack=[0]
    def tokenize(self):
        import re
        print("[LEXER] Starting tokenization")
        lines=self.source_code.splitlines()
        i=0
        previous_indent=0
        while i < len(lines):
            line=lines[i]
            line_number=i+1
            print(f"[LEXER] Processing line {line_number}:{line}")
            if not line.strip():
                #print(f"[LEXER DEBUG] Empty or whitespace-only line at {line_number}. Adding NEWLINE token.")
                self.tokens.append(('NEWLINE','\n'))
                i+=1
                continue
            indent_match=re.match(r'^[ \t]*',line)
            indent_size=len(indent_match.group(0)) if indent_match else 0
            #print(f"[LEXER DEBUG] Detected indent size:{indent_size} at line {line_number}")
            if indent_size > previous_indent:
                self.tokens.append(('INDENT',indent_size))
                self.indent_stack.append(indent_size)
                #print(f"[LEXER DEBUG] INDENT token added. New indent level:{indent_size}")
            while indent_size < previous_indent:
                popped=self.indent_stack.pop()
                self.tokens.append(('DEDENT',popped))
                #print(f"[LEXER DEBUG] DEDENT token added. Popped indent:{popped}")
                previous_indent=self.indent_stack[-1] if self.indent_stack else 0
            previous_indent=indent_size
            pos=0
            line_length=len(line)
            while pos < line_length:
                if line[pos:pos+3] in ('"""',"'''"):
                    quote=line[pos:pos+3]
                    #print(f"[LEXER DEBUG] Detected start of multi-line string with delimiter {quote} at line {line_number} pos {pos}")
                    pos+=3
                    token_value=""
                    end_index=line.find(quote,pos)
                    if end_index!=-1:
                        token_value=line[pos:end_index]
                        pos=end_index+3
                        #print(f"[LEXER DEBUG] Multi-line string closed on same line {line_number} at pos {end_index}")
                    else:
                        token_value=line[pos:]+"\n"
                        i+=1
                        found=False
                        while i < len(lines):
                            next_line=lines[i]
                            end_index=next_line.find(quote)
                            if end_index!=-1:
                                token_value+=next_line[:end_index]
                                #print(f"[LEXER DEBUG] Multi-line string closed on line {i+1} at pos {end_index}")
                                line=next_line
                                line_length=len(line)
                                pos=end_index+3
                                found=True
                                break
                            else:
                                token_value+=next_line+"\n"
                            i+=1
                        if not found:
                            #print(f"[LEXER DEBUG] Warning:Unterminated multi-line string starting at line {line_number}")
                            pos=line_length
                    self.tokens.append(('MULTILINE_STRING',token_value))
                    #print(f"[LEXER DEBUG] MULTILINE_STRING token added with value:{repr(token_value)}")
                    continue
                m=self.token_pattern.match(line,pos)
                if not m:
                    print(f"[LEXER DEBUG] No regex match at line {line_number} pos {pos}. Breaking out of loop.")
                    break
                kind=m.lastgroup
                value=m.group()
                #print(f"[LEXER DEBUG] Matched {kind} token:{repr(value)} at line {line_number} pos {pos}")
                pos=m.end()
                if kind in ('SKIP','COMMENT'):
                    #print(f"[LEXER DEBUG] Skipping token {kind} with value {repr(value)}")
                    continue
                if kind=='UNKNOWN':
                    raise LexicalError(f"✘  Lexical Error:Unrecognized token'{value}'at line {line_number}")
                if kind=='NUMBER':
                    value=float(value) if ('.'in value or'e'in value.lower()) else int(value)
                    #print(f"[LEXER DEBUG] NUMBER token converted to {value}")
                elif kind in ('STRING','FSTRING','RAWSTRING'):
                    orig_value=value
                    value=value.lstrip('fFrR').strip('\'"')
                    #print(f"[LEXER DEBUG] Processed {kind} token. Original:{repr(orig_value)},Processed:{repr(value)}")
                self.tokens.append((kind,value))
                #print(f"[LEXER DEBUG] Token appended:({kind},{repr(value)})")
            #print(f"[LEXER DEBUG] End of line {line_number} reached. Adding NEWLINE token.")
            self.tokens.append(('NEWLINE','\n'))
            i+=1
        while len(self.indent_stack) > 1:
            popped=self.indent_stack.pop()
            self.tokens.append(('DEDENT',popped))
            print(f"[LEXER] Final DEDENT token added. Popped indent:{popped}")
        print(f"[LEXER] Finished tokenization. Total tokens:{len(self.tokens)}")
        from collections import Counter
        token_counts=Counter(token[0] for token in self.tokens)
        print("[LEXER] Token summary:")
        for token_type,count in token_counts.items():
            print(f" {token_type}:{count}")
        return self.tokens
#=========================================================================