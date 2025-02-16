#=========================================================================
class ParserError(Exception):
    pass
class ASTNode:
    def __init__(self,type,value=None,left=None,right=None,children=None,body=None,params=None,condition=None,handler=None,decorators=None):
        self.type=type
        self.value=value
        self.left=left
        self.right=right
        self.children=children or []
        self.body=body or []
        self.params=params or []
        self.condition=condition
        self.handler=handler
        self.decorators=decorators or []
    def __repr__(self):
        return (
            f"ASTNode(type={self.type},value={self.value},left={self.left},"
            f"right={self.right},children={self.children},body={self.body},"
            f"params={self.params},condition={self.condition},handler={self.handler},"
            f"decorators={self.decorators})"
        )
class Parser:
    def __init__(self,tokens):
        print("[PARSER] Initializing parser")
        print("[PARSER DEBUG] Tokens received:",tokens)
        self.tokens=tokens
        self.pos=0
    def parse(self):
        print("[PARSER DEBUG] Entering parse() method.")
        print("[PARSER] Starting parsing")
        statements=[]
        while self.pos<len(self.tokens):
            print(f"[PARSER DEBUG] parse() loop-current pos: {self.pos},current token: {self.tokens[self.pos] if self.pos<len(self.tokens) else None}")
            stmt=self.statement()
            if stmt is not None:
                print(f"[PARSER] Parsed statement: {stmt}")
                statements.append(stmt)
        print(f"[PARSER] Finished parsing. Total statements: {len(statements)}")
        print("\n[AST ASCII Tree]")
        self.print_ast_tree(statements)
        return statements
    def statement(self):
        print("[PARSER DEBUG] Entering statement() method.")
        while self.peek() in ('NEWLINE','DEDENT','SKIP'):
            self.advance()
        decorators=[]
        while self.peek()=='DECORATOR':
            dec_token=self.advance()
            decorators.append(dec_token[1])
            if self.peek()=='NEWLINE':
                self.advance()
        if self.peek()=='ID':
            temp_pos=self.pos
            self.advance()
            while self.peek()=='DOT':
                self.advance()
                if self.peek()=='ID':
                    self.advance()
                else:
                    break
            if self.peek() in ('COMMA','ASSIGN'):
                self.pos=temp_pos
                return self.assignment()
            else:
                self.pos=temp_pos
        if self.match('KEYWORD'):
            keyword=self.previous()[1]
            print(f"[PARSER] Detected keyword: {keyword}")
            match keyword:
                case'def':
                    node=self.function_definition()
                    node.decorators=decorators
                    return node
                case'if':
                    return self.if_statement()
                case'while':
                    return self.while_loop()
                case'for':
                    return self.for_loop()
                case'return':
                    return self.return_statement()
                case'class':
                    node=self.class_definition()
                    node.decorators=decorators
                    return node
                case'try':
                    return self.try_except_block()
                case'lambda':
                    return self.lambda_expression()
                case'match':
                    return self.match_statement()
                case'import':
                    return self.import_statement()
                case'raise':
                    return self.raise_statement()
                case _:
                    self.pos-=1
        expr=self.expression()
        return expr
    def raise_statement(self):
        print("[PARSER DEBUG] Entering raise_statement() method.")
        print("[PARSER] Parsing raise statement")
        expr=None
        if self.peek() not in ('NEWLINE','DEDENT'):
            expr=self.expression()
        node=ASTNode('RAISE',right=expr)
        print("[PARSER] Finished raise statement")
        return node
    def assignment(self):
        print("[PARSER DEBUG] Entering assignment() method.")
        target=self.assignment_target()
        if self.peek()=='COMMA':
            if target.type!='VAR':
                raise ParserError("Multi-assignment is only allowed for variable identifiers.")
            targets=[target.value]
            while self.match('COMMA'):
                targets.append(self.expect('ID')[1])
            self.expect('ASSIGN')
            expr=self.expression()
            if len(targets)==1:
                print(f"[PARSER] Finished assignment: {targets[0]}={expr}")
                return ASTNode('ASSIGN',targets[0],right=expr)
            else:
                print(f"[PARSER] Finished multi-assignment: {targets}={expr}")
                return ASTNode('MULTI_ASSIGN',value=targets,right=expr)
        else:
            self.expect('ASSIGN')
            expr=self.expression()
            if target.type=='VAR':
                print(f"[PARSER] Finished assignment: {target.value}={expr}")
                return ASTNode('ASSIGN',target.value,right=expr)
            elif target.type=='ATTR_ACCESS':
                print(f"[PARSER] Finished attribute assignment: {target.left.value}.{target.value}={expr}")
                return ASTNode('ATTR_ASSIGN',left=target.left,value=target.value,right=expr)
            else:
                raise ParserError(f"Invalid assignment target: {target}")
    def assignment_target(self):
        print("[PARSER DEBUG] Entering assignment_target() method.")
        token=self.expect('ID')
        node=ASTNode('VAR',token[1])
        while self.match('DOT'):
            attr_name=self.expect('ID')[1]
            node=ASTNode('ATTR_ACCESS',left=node,value=attr_name)
        return node
    def expression(self):
        print("[PARSER DEBUG] Entering expression() method.")
        expr=self.logical_or()
        if self.match('COMMA'):
            expressions=[expr]
            expressions.append(self.logical_or())
            while self.match('COMMA'):
                expressions.append(self.logical_or())
            print(f"[PARSER] Parsed tuple expression: {expressions}")
            return ASTNode('TUPLE',children=expressions)
        print(f"[PARSER] Parsed expression: {expr}")
        return expr
    def logical_or(self):
        print("[PARSER DEBUG] Entering logical_or() method.")
        expr=self.logical_and()
        while self.peek()=='KEYWORD'and self.tokens[self.pos][1]=='or':
            op=self.advance()[1]
            print(f"[PARSER] Parsing logical OR with operator: {op}")
            right=self.logical_and()
            expr=ASTNode('BIN_OP',op,left=expr,right=right)
        return expr
    def logical_and(self):
        print("[PARSER DEBUG] Entering logical_and() method.")
        expr=self.equality()
        while self.peek()=='KEYWORD'and self.tokens[self.pos][1]=='and':
            op=self.advance()[1]
            print(f"[PARSER] Parsing logical AND with operator: {op}")
            right=self.equality()
            expr=ASTNode('BIN_OP',op,left=expr,right=right)
        return expr
    def equality(self):
        print("[PARSER DEBUG] Entering equality() method.")
        expr=self.relational()
        while self.peek() in ('EQ','NEQ'):
            op=self.advance()[0]
            print(f"[PARSER] Parsing equality operator: {op}")
            right=self.relational()
            expr=ASTNode('BIN_OP',op,left=expr,right=right)
        return expr
    def relational(self):
        print("[PARSER DEBUG] Entering relational() method.")
        expr=self.additive()
        while self.peek() in ('GT','LT','GTE','LTE'):
            op=self.advance()[0]
            print(f"[PARSER] Parsing relational operator: {op}")
            right=self.additive()
            expr=ASTNode('BIN_OP',op,left=expr,right=right)
        return expr
    def additive(self):
        print("[PARSER DEBUG] Entering additive() method.")
        expr=self.multiplicative()
        while self.peek() in ('PLUS','MINUS'):
            op=self.advance()[0]
            print(f"[PARSER] Parsing additive operator: {op}")
            right=self.multiplicative()
            expr=ASTNode('BIN_OP',op,left=expr,right=right)
        return expr
    def multiplicative(self):
        print("[PARSER DEBUG] Entering multiplicative() method.")
        expr=self.power()
        while self.peek() in ('MULT','DIV','MOD','FLOORDIV'):
            if self.peek()=='MULT'and self.pos+1<len(self.tokens) and self.tokens[self.pos+1][0]=='MULT':
                break
            op=self.advance()[0]
            print(f"[PARSER] Parsing multiplicative operator: {op}")
            right=self.power()
            expr=ASTNode('BIN_OP',op,left=expr,right=right)
        return expr
    def power(self):
        print("[PARSER DEBUG] Entering power() method.")
        expr=self.unary()
        while self.match('POW'):
            print("[PARSER] Parsing exponentiation operator'**'")
            right=self.unary()
            expr=ASTNode('BIN_OP','POW',left=expr,right=right)
        return expr
    def unary(self):
        print("[PARSER DEBUG] Entering unary() method.")
        if self.match('MINUS'):
            print("[PARSER] Detected unary minus")
            right=self.unary()
            return ASTNode('UNARY_OP','-',right=right)
        elif self.match('PLUS'):
            print("[PARSER] Detected unary plus")
            right=self.unary()
            return ASTNode('UNARY_OP','+',right=right)
        elif self.match('BIT_NOT'):
            print("[PARSER] Detected unary bitwise-not'~'")
            right=self.unary()
            return ASTNode('UNARY_OP','~',right=right)
        else:
            return self.call(self.primary())
    def call(self,expr):
        print("[PARSER DEBUG] Entering call() method.")
        while True:
            if self.match('LPAREN'):
                print("[PARSER] Parsing function call")
                expr=self.finish_call(expr)
            elif self.match('DOT'):
                print("[PARSER] Parsing attribute access")
                attr_name=self.expect('ID')[1]
                expr=ASTNode('ATTR_ACCESS',left=expr,value=attr_name)
            else:
                break
        return expr
    def finish_call(self,callee):
        print("[PARSER DEBUG] Entering finish_call() method.")
        args=[]
        if self.peek()!='RPAREN':
            args.append(self.expression())
            while self.match('COMMA'):
                args.append(self.expression())
        self.expect('RPAREN')
        print(f"[PARSER] Finished function call: {callee} with args: {args}")
        return ASTNode('FUNC_CALL',callee,children=args)
    def primary(self):
        print("[PARSER DEBUG] Entering primary() method.")
        if self.match('NUMBER'):
            node=ASTNode('NUMBER',self.previous()[1])
            print(f"[PARSER] Parsed number: {node.value}")
            return node
        elif self.match('STRING','MULTILINE_STRING','FSTRING','RAWSTRING'):
            node=ASTNode('STRING',self.previous()[1])
            print(f"[PARSER] Parsed string: {node.value}")
            return node
        elif self.match('ID'):
            node=ASTNode('VAR',self.previous()[1])
            print(f"[PARSER] Parsed variable: {node.value}")
            return node
        elif self.match('LPAREN'):
            print("[PARSER] Parsing parenthesized expression")
            first_expr=self.expression()
            if self.peek()=='KEYWORD'and self.tokens[self.pos][1]=='for':
                return self.generator_expression(first_expr)
            else:
                self.expect('RPAREN')
                return first_expr
        elif self.match('LBRACKET'):
            return self.list_literal()
        elif self.match('LBRACE'):
            return self.dict_literal()
        elif self.peek()=='KEYWORD'and self.tokens[self.pos][1]=='lambda':
            print("[PARSER] Detected lambda expression in primary()")
            self.advance()
            return self.lambda_expression()
        else:
            raise ParserError(f"Unexpected token {self.tokens[self.pos]} at position {self.pos}")
    def list_literal(self):
        print("[PARSER DEBUG] Entering list_literal() method.")
        print("[PARSER] Parsing list literal")
        elements=[]
        if self.peek()=='RBRACKET':
            self.expect('RBRACKET')
            node=ASTNode('LIST',children=elements)
            print(f"[PARSER] Finished list literal: {node}")
            return node
        first_expr=self.expression()
        if self.peek()=='KEYWORD'and self.tokens[self.pos][1]=='for':
            return self.list_comprehension(first_expr)
        elements.append(first_expr)
        while self.match('COMMA'):
            if self.peek()=='RBRACKET':
                break
            elements.append(self.expression())
        self.expect('RBRACKET')
        node=ASTNode('LIST',children=elements)
        print(f"[PARSER] Finished list literal: {node}")
        return node
    def list_comprehension(self,target_expr):
        print("[PARSER DEBUG] Entering list_comprehension() method.")
        print("[PARSER] Parsing list comprehension")
        self.expect('KEYWORD')
        var_name=self.expect('ID')[1]
        if not (self.match('KEYWORD') and self.previous()[1]=='in'):
            raise ParserError("Expected'in'in list comprehension after'for'")
        source_expr=self.expression()
        condition_expr=None
        if self.peek()=='KEYWORD'and self.tokens[self.pos][1]=='if':
            self.advance()
            condition_expr=self.expression()
        self.expect('RBRACKET')
        comp_node=ASTNode(
           'LIST_COMP',
            children=[target_expr,ASTNode('VAR',var_name),source_expr],
            condition=condition_expr
        )
        print(f"[PARSER] Finished list comprehension: {comp_node}")
        return comp_node
    def generator_expression(self,target_expr):
        print("[PARSER DEBUG] Entering generator_expression() method.")
        print("[PARSER] Parsing generator expression")
        self.expect('KEYWORD')
        var_name=self.expect('ID')[1]
        if not (self.match('KEYWORD') and self.previous()[1]=='in'):
            raise ParserError("Expected'in'in generator expression after'for'")
        source_expr=self.expression()
        condition_expr=None
        if self.peek()=='KEYWORD'and self.tokens[self.pos][1]=='if':
            self.advance()
            condition_expr=self.expression()
        self.expect('RPAREN')
        gen_node=ASTNode(
           'GEN_EXPR',
            children=[target_expr,ASTNode('VAR',var_name),source_expr],
            condition=condition_expr
        )
        print(f"[PARSER] Finished generator expression: {gen_node}")
        return gen_node
    def dict_literal(self):
        print("[PARSER DEBUG] Entering dict_literal() method.")
        print("[PARSER] Parsing dictionary literal")
        pairs=[]
        if self.peek()!='RBRACE':
            key=self.expression()
            self.expect('COLON')
            value=self.expression()
            pairs.append((key,value))
            while self.match('COMMA'):
                if self.peek()=='RBRACE':
                    break
                key=self.expression()
                self.expect('COLON')
                value=self.expression()
                pairs.append((key,value))
        self.expect('RBRACE')
        node=ASTNode(
           'DICT',
            children=[ASTNode('PAIR',children=[k,v]) for k,v in pairs]
        )
        print(f"[PARSER] Finished dictionary literal: {node}")
        return node
    def function_definition(self):
        print("[PARSER DEBUG] Entering function_definition() method.")
        func_name=self.expect('ID')[1]
        print(f"[PARSER] Parsing function definition for: {func_name}")
        self.expect('LPAREN')
        params=[]
        if self.peek()!='RPAREN':
            params.append(self.expect('ID')[1])
            while self.match('COMMA'):
                params.append(self.expect('ID')[1])
        self.expect('RPAREN')
        self.expect('COLON')
        while self.peek()=='NEWLINE':
            self.advance()
        if self.peek()!='INDENT':
            raise ParserError(f"Expected INDENT after function definition,got {self.tokens[self.pos]} at position {self.pos}")
        body=self.block()
        node=ASTNode('FUNC_DEF',value=func_name,params=params,body=body)
        print(f"[PARSER] Finished function definition for: {func_name}")
        return node
    def if_statement(self):
        print("[PARSER DEBUG] Entering if_statement() method.")
        print("[PARSER] Parsing if statement")
        condition=self.expression()
        self.expect('COLON')
        while self.peek()=='NEWLINE':
            self.advance()
        body=self.block()
        else_body=None
        if self.match('KEYWORD') and self.previous()[1]=='else':
            self.expect('COLON')
            while self.peek()=='NEWLINE':
                self.advance()
            else_body=self.block()
        node=ASTNode('IF',condition=condition,body=body,children=else_body)
        print("[PARSER] Finished if statement")
        return node
    def while_loop(self):
        print("[PARSER DEBUG] Entering while_loop() method.")
        print("[PARSER] Parsing while loop")
        condition=self.expression()
        self.expect('COLON')
        while self.peek()=='NEWLINE':
            self.advance()
        body=self.block()
        node=ASTNode('WHILE',condition=condition,body=body)
        print("[PARSER] Finished while loop")
        return node
    def for_loop(self):
        print("[PARSER DEBUG] Entering for_loop() method.")
        print("[PARSER] Parsing for loop")
        var_name=self.expect('ID')[1]
        if not (self.match('KEYWORD') and self.previous()[1]=='in'):
            raise ParserError(f"Expected'in'in for loop,got {self.tokens[self.pos]} at position {self.pos}")
        iterable=self.expression()
        self.expect('COLON')
        while self.peek()=='NEWLINE':
            self.advance()
        body=self.block()
        node=ASTNode('FOR',value=var_name,left=iterable,body=body)
        print(f"[PARSER] Finished for loop for variable: {var_name}")
        return node
    def return_statement(self):
        print("[PARSER DEBUG] Entering return_statement() method.")
        print("[PARSER] Parsing return statement")
        expr=None
        if self.peek() not in ('NEWLINE','DEDENT'):
            expr=self.expression()
        node=ASTNode('RETURN',right=expr)
        print("[PARSER] Finished return statement")
        return node
    def class_definition(self):
        print("[PARSER DEBUG] Entering class_definition() method.")
        print("[PARSER] Parsing class definition")
        class_name=self.expect('ID')[1]
        self.expect('COLON')
        while self.peek()=='NEWLINE':
            self.advance()
        body=self.block()
        node=ASTNode('CLASS',value=class_name,body=body)
        print(f"[PARSER] Finished class definition for: {class_name}")
        return node
    def try_except_block(self):
        print("[PARSER DEBUG] Entering try_except_block() method.")
        print("[PARSER] Parsing try/except block")
        self.expect('COLON')
        while self.peek()=='NEWLINE':
            self.advance()
        try_body=self.block()
        while self.peek()=='NEWLINE':
            self.advance()
        except_blocks=[]
        final_body=None
        while self.match('KEYWORD') and self.previous()[1]=='except':
            except_type=None
            except_name=None
            if self.peek() not in ('COLON','NEWLINE','INDENT'):
                except_type=self.advance()
                if self.peek()=='KEYWORD'and self.tokens[self.pos][1]=='as':
                    self.advance()
                    except_name=self.expect('ID')[1]
            self.expect('COLON')
            while self.peek()=='NEWLINE':
                self.advance()
            except_body=self.block()
            except_blocks.append((except_type,except_name,except_body))
            while self.peek()=='NEWLINE':
                self.advance()
        if self.match('KEYWORD') and self.previous()[1]=='finally':
            self.expect('COLON')
            while self.peek()=='NEWLINE':
                self.advance()
            final_body=self.block()
        node=ASTNode('TRY',body=try_body,children=except_blocks,right=final_body)
        print("[PARSER] Finished try/except block")
        return node
    def lambda_expression(self):
        print("[PARSER DEBUG] Entering lambda_expression() method.")
        print("[PARSER] Parsing lambda expression")
        params=[]
        if self.peek()!='COLON':
            params.append(self.expect('ID')[1])
            while self.match('COMMA'):
                params.append(self.expect('ID')[1])
        self.expect('COLON')
        expr=self.expression()
        node=ASTNode('LAMBDA',params=params,body=[expr])
        print("[PARSER] Finished lambda expression")
        return node
    def match_statement(self):
        print("[PARSER DEBUG] Entering match_statement() method.")
        print("[PARSER] Parsing match statement")
        value=self.expression()
        self.expect('COLON')
        while self.peek()=='NEWLINE':
            self.advance()
        body=self.block()
        node=ASTNode('MATCH',value=value,body=body)
        print("[PARSER] Finished match statement")
        return node
    def import_statement(self):
        print("[PARSER DEBUG] Entering import_statement() method.")
        print("[PARSER] Parsing import statement")
        module=self.imported_name()
        if self.match('LPAREN'):
            args=[]
            if self.peek()!='RPAREN':
                args.append(self.expression())
                while self.match('COMMA'):
                    args.append(self.expression())
            self.expect('RPAREN')
            node=ASTNode('IMPORT_CALL',module,children=args)
        else:
            node=ASTNode('IMPORT',module)
        print(f"[PARSER] Finished import statement for module: {module}")
        return node
    def imported_name(self):
        print("[PARSER DEBUG] Entering imported_name() method.")
        parts=[]
        if self.match('ID'):
            parts.append(self.previous()[1])
        else:
            raise ParserError(f"Expected module name after import,got {self.tokens[self.pos]} at position {self.pos}")
        while self.peek() in ('DOT','ID'):
            if self.peek()=='DOT':
                self.advance()
                if self.match('ID'):
                    parts.append(self.previous()[1])
                else:
                    raise ParserError(f"Expected identifier after DOT in import,got {self.tokens[self.pos]} at position {self.pos}")
            elif self.peek()=='ID':
                parts.append(self.advance()[1])
        return".".join(parts)
    def block(self):
        print("[PARSER DEBUG] Entering block() method.")
        print("[PARSER] Parsing block")
        while self.peek()=='NEWLINE':
            self.advance()
        self.expect('INDENT')
        statements=[]
        while self.pos<len(self.tokens) and self.peek()!='DEDENT':
            stmt=self.statement()
            if stmt is not None:
                statements.append(stmt)
        self.expect('DEDENT')
        print(f"[PARSER] Finished block with {len(statements)} statement(s)")
        return statements
    def match(self,*types):
        print(f"[PARSER DEBUG] match() called with types={types},current pos={self.pos},current token={(self.tokens[self.pos] if self.pos<len(self.tokens) else None)}")
        if self.pos<len(self.tokens) and self.tokens[self.pos][0] in types:
            self.pos+=1
            return True
        return False
    def expect(self,type):
        print(f"[PARSER DEBUG] expect() called with type={type},current pos={self.pos},current token={(self.tokens[self.pos] if self.pos<len(self.tokens) else None)}")
        if self.pos>=len(self.tokens):
            raise ParserError(f"Expected {type},but reached end of input.")
        if self.tokens[self.pos][0]==type:
            self.pos+=1
            return self.tokens[self.pos-1]
        else:
            raise ParserError(f"Expected {type},but got {self.tokens[self.pos]} at position {self.pos}")
    def peek(self):
        if self.pos<len(self.tokens):
            return self.tokens[self.pos][0]
        return None
    def advance(self):
        print(f"[PARSER DEBUG] advance() called. current pos={self.pos},token={self.tokens[self.pos] if self.pos<len(self.tokens) else None}")
        token=self.tokens[self.pos]
        self.pos+=1
        return token
    def previous(self):
        return self.tokens[self.pos-1]
    def print_ast_tree(self,nodes):
        for i,node in enumerate(nodes):
            is_last=(i==len(nodes)-1)
            self.print_ascii_tree(node,"",is_last)
    def print_ascii_tree(self,node,prefix,is_last):
        if not isinstance(node,ASTNode):
            branch="└──"if is_last else"├──"
            print(prefix+branch+str(node))
            return
        branch="└──"if is_last else"├──"
        print(prefix+branch+f"{node.type}:{node.value}")
        children=[]
        if node.left:
            children.append(("Left",node.left))
        if node.right:
            children.append(("Right",node.right))
        if node.children:
            children.append(("Children",node.children))
        if node.body:
            children.append(("Body",node.body))
        if node.params:
            children.append(("Params",node.params))
        if node.condition:
            children.append(("Condition",node.condition))
        if node.handler:
            children.append(("Handler",node.handler))
        if node.decorators:
            children.append(("Decorators",node.decorators))
        for j,(label,child) in enumerate(children):
            last_child=(j==len(children)-1)
            new_prefix=prefix+("  "if is_last else"│  ")
            if isinstance(child,list):
                print(new_prefix+("└──"if last_child else"├──")+label+":")
                for k,subchild in enumerate(child):
                    self.print_ascii_tree(subchild,new_prefix+("  "if last_child else"│  "),k==len(child)-1)
            else:
                print(new_prefix+("└──"if last_child else"├──")+label+":")
                self.print_ascii_tree(child,new_prefix+("  "if last_child else"│  "),True)
#=========================================================================