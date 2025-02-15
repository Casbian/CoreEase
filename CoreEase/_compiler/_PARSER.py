#=========================================================================
class ParserError(Exception):
    pass
class ASTNode:
    def __init__(self, type, value=None, left=None, right=None, children=None, body=None, params=None, condition=None, handler=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right
        self.children = children or []
        self.body = body or []
        self.params = params or []
        self.condition = condition
        self.handler = handler
    def __repr__(self):
        return (
            f"ASTNode(type={self.type}, value={self.value}, left={self.left}, "
            f"right={self.right}, children={self.children}, body={self.body}, "
            f"params={self.params}, condition={self.condition}, handler={self.handler})"
        )
class Parser:
    def __init__(self, tokens):
        print("[PARSER] Initializing parser")
        self.tokens = tokens
        self.pos = 0
    def parse(self):
        print("[PARSER] Starting parsing")
        statements = []
        while self.pos < len(self.tokens):
            stmt = self.statement()
            if stmt is not None:
                print(f"[PARSER] Parsed statement: {stmt}")
                statements.append(stmt)
        print(f"[PARSER] Finished parsing. Total statements: {len(statements)}")
        print("\n[AST ASCII Tree]")
        self.print_ast_tree(statements)
        return statements
    def statement(self):
        if self.peek() in ('DEDENT', 'NEWLINE'):
            self.advance()
            return None
        if self.match('KEYWORD'):
            keyword = self.previous()[1]
            print(f"[PARSER] Detected keyword: {keyword}")
            match keyword:
                case 'def': return self.function_definition()
                case 'if': return self.if_statement()
                case 'while': return self.while_loop()
                case 'for': return self.for_loop()
                case 'return': return self.return_statement()
                case 'class': return self.class_definition()
                case 'try': return self.try_except_block()
                case 'lambda': return self.lambda_expression()
                case 'match': return self.match_statement()
                case 'import': return self.import_statement()
                case _:
                    self.pos -= 1
        if self.match('ID') and self.peek() == 'ASSIGN':
            return self.assignment()
        return self.expression()
    def assignment(self):
        var_name = self.previous()[1]
        print(f"[PARSER] Parsing assignment to variable: {var_name}")
        self.expect('ASSIGN')
        expr = self.expression()
        print(f"[PARSER] Finished assignment: {var_name} = {expr}")
        return ASTNode('ASSIGN', var_name, right=expr)
    def expression(self):
        expr = self.logical_or()
        print(f"[PARSER] Parsed expression: {expr}")
        return expr
    def logical_or(self):
        expr = self.logical_and()
        while self.peek() == 'OR':
            op = self.advance()[0]
            print(f"[PARSER] Parsing logical OR with operator: {op}")
            right = self.logical_and()
            expr = ASTNode('BIN_OP', op, left=expr, right=right)
        return expr
    def logical_and(self):
        expr = self.equality()
        while self.peek() == 'AND':
            op = self.advance()[0]
            print(f"[PARSER] Parsing logical AND with operator: {op}")
            right = self.equality()
            expr = ASTNode('BIN_OP', op, left=expr, right=right)
        return expr
    def equality(self):
        expr = self.relational()
        while self.peek() in ('EQ', 'NEQ'):
            op = self.advance()[0]
            print(f"[PARSER] Parsing equality operator: {op}")
            right = self.relational()
            expr = ASTNode('BIN_OP', op, left=expr, right=right)
        return expr
    def relational(self):
        expr = self.additive()
        while self.peek() in ('GT', 'LT', 'GTE', 'LTE'):
            op = self.advance()[0]
            print(f"[PARSER] Parsing relational operator: {op}")
            right = self.additive()
            expr = ASTNode('BIN_OP', op, left=expr, right=right)
        return expr
    def additive(self):
        expr = self.multiplicative()
        while self.peek() in ('PLUS', 'MINUS'):
            op = self.advance()[0]
            print(f"[PARSER] Parsing additive operator: {op}")
            right = self.multiplicative()
            expr = ASTNode('BIN_OP', op, left=expr, right=right)
        return expr
    def multiplicative(self):
        expr = self.power()
        while self.peek() in ('MULT', 'DIV', 'MOD'):
            # If a '**' sequence starts here, handle it in power()
            if self.peek() == 'MULT' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'MULT':
                break
            op = self.advance()[0]
            print(f"[PARSER] Parsing multiplicative operator: {op}")
            right = self.power()
            expr = ASTNode('BIN_OP', op, left=expr, right=right)
        return expr
    def power(self):
        expr = self.call(self.primary())
        if self.peek() == 'MULT' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'MULT':
            print("[PARSER] Parsing exponentiation operator '**'")
            self.advance()  # consume first '*'
            self.advance()  # consume second '*'
            right = self.power()  # right-associative
            expr = ASTNode('BIN_OP', 'POW', left=expr, right=right)
        return expr
    def call(self, expr):
        while True:
            if self.match('LPAREN'):
                print("[PARSER] Parsing function call")
                expr = self.finish_call(expr)
            elif self.match('DOT'):
                print("[PARSER] Parsing attribute access")
                attr_name = self.expect('ID')[1]
                expr = ASTNode('ATTR_ACCESS', left=expr, value=attr_name)
            else:
                break
        return expr
    def finish_call(self, callee):
        args = []
        if self.peek() != 'RPAREN':
            args.append(self.expression())
            while self.match('COMMA'):
                args.append(self.expression())
        self.expect('RPAREN')
        print(f"[PARSER] Finished function call: {callee} with args: {args}")
        return ASTNode('FUNC_CALL', callee, children=args)
    def primary(self):
        if self.match('NUMBER'):
            node = ASTNode('NUMBER', self.previous()[1])
            print(f"[PARSER] Parsed number: {node.value}")
            return node
        elif self.match('STRING'):
            node = ASTNode('STRING', self.previous()[1])
            print(f"[PARSER] Parsed string: {node.value}")
            return node
        elif self.match('ID'):
            node = ASTNode('VAR', self.previous()[1])
            print(f"[PARSER] Parsed variable: {node.value}")
            return node
        elif self.match('LPAREN'):
            print("[PARSER] Parsing parenthesized expression")
            expr = self.expression()
            self.expect('RPAREN')
            return expr
        else:
            raise ParserError(f"Unexpected token {self.tokens[self.pos]} at position {self.pos}")
    def function_definition(self):
        func_name = self.expect('ID')[1]
        print(f"[PARSER] Parsing function definition for: {func_name}")
        self.expect('LPAREN')
        params = []
        if self.peek() != 'RPAREN':
            params.append(self.expect('ID')[1])
            while self.match('COMMA'):
                params.append(self.expect('ID')[1])
        self.expect('RPAREN')
        self.expect('COLON')
        if self.peek() != 'INDENT':
            raise ParserError(f"Expected INDENT after function definition, got {self.tokens[self.pos]} at position {self.pos}")
        body = self.block()
        node = ASTNode('FUNC_DEF', value=func_name, params=params, body=body)
        print(f"[PARSER] Finished function definition for: {func_name}")
        return node
    def if_statement(self):
        print("[PARSER] Parsing if statement")
        condition = self.expression()
        self.expect('COLON')
        body = self.block()
        else_body = None
        if self.match('KEYWORD') and self.previous()[1] == 'else':
            self.expect('COLON')
            else_body = self.block()
        node = ASTNode('IF', condition=condition, body=body, children=else_body)
        print("[PARSER] Finished if statement")
        return node
    def while_loop(self):
        print("[PARSER] Parsing while loop")
        condition = self.expression()
        self.expect('COLON')
        body = self.block()
        node = ASTNode('WHILE', condition=condition, body=body)
        print("[PARSER] Finished while loop")
        return node
    def for_loop(self):
        print("[PARSER] Parsing for loop")
        var_name = self.expect('ID')[1]
        if not (self.match('KEYWORD') and self.previous()[1] == 'in'):
            raise ParserError(f"Expected 'in' in for loop, got {self.tokens[self.pos]} at position {self.pos}")
        iterable = self.expression()
        self.expect('COLON')
        body = self.block()
        node = ASTNode('FOR', value=var_name, left=iterable, body=body)
        print(f"[PARSER] Finished for loop for variable: {var_name}")
        return node
    def return_statement(self):
        print("[PARSER] Parsing return statement")
        expr = None
        if self.peek() not in ('NEWLINE', 'DEDENT'):
            expr = self.expression()
        node = ASTNode('RETURN', right=expr)
        print("[PARSER] Finished return statement")
        return node
    def class_definition(self):
        print("[PARSER] Parsing class definition")
        class_name = self.expect('ID')[1]
        self.expect('COLON')
        body = self.block()
        node = ASTNode('CLASS', value=class_name, body=body)
        print(f"[PARSER] Finished class definition for: {class_name}")
        return node
    def try_except_block(self):
        print("[PARSER] Parsing try/except block")
        try_body = self.block()
        handler = None
        if self.match('KEYWORD') and self.previous()[1] == 'except':
            handler = self.block()
        node = ASTNode('TRY', body=try_body, handler=handler)
        print("[PARSER] Finished try/except block")
        return node
    def lambda_expression(self):
        print("[PARSER] Parsing lambda expression")
        params = []
        if self.peek() != 'COLON':
            params.append(self.expect('ID')[1])
            while self.match('COMMA'):
                params.append(self.expect('ID')[1])
        self.expect('COLON')
        expr = self.expression()
        node = ASTNode('LAMBDA', params=params, body=[expr])
        print("[PARSER] Finished lambda expression")
        return node
    def match_statement(self):
        print("[PARSER] Parsing match statement")
        value = self.expression()
        self.expect('COLON')
        body = self.block()
        node = ASTNode('MATCH', value=value, body=body)
        print("[PARSER] Finished match statement")
        return node
    def import_statement(self):
        print("[PARSER] Parsing import statement")
        module = self.imported_name()
        if self.match('LPAREN'):
            args = []
            if self.peek() != 'RPAREN':
                args.append(self.expression())
                while self.match('COMMA'):
                    args.append(self.expression())
            self.expect('RPAREN')
            node = ASTNode('IMPORT_CALL', module, children=args)
        else:
            node = ASTNode('IMPORT', module)
        print(f"[PARSER] Finished import statement for module: {module}")
        return node
    def imported_name(self):
        parts = []
        if self.match('ID'):
            parts.append(self.previous()[1])
        else:
            raise ParserError(f"Expected module name after import, got {self.tokens[self.pos]} at position {self.pos}")
        while self.peek() in ('DOT', 'ID'):
            if self.peek() == 'DOT':
                self.advance()
                if self.match('ID'):
                    parts.append(self.previous()[1])
                else:
                    raise ParserError(f"Expected identifier after DOT in import, got {self.tokens[self.pos]} at position {self.pos}")
            elif self.peek() == 'ID':
                parts.append(self.advance()[1])
        return ".".join(parts)
    def block(self):
        print("[PARSER] Parsing block")
        statements = []
        self.expect('INDENT')
        while self.pos < len(self.tokens) and self.peek() != 'DEDENT':
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
        self.expect('DEDENT')
        print(f"[PARSER] Finished block with {len(statements)} statement(s)")
        return statements
    def match(self, *types):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] in types:
            self.pos += 1
            return True
        return False
    def expect(self, type):
        if self.pos >= len(self.tokens):
            raise ParserError(f"Expected {type}, but reached end of input.")
        if self.tokens[self.pos][0] == type:
            self.pos += 1
            return self.tokens[self.pos - 1]
        else:
            raise ParserError(f"Expected {type}, but got {self.tokens[self.pos]} at position {self.pos}")
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][0]
        return None
    def advance(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token
    def previous(self):
        return self.tokens[self.pos - 1]
    def print_ast_tree(self, nodes):
        for i, node in enumerate(nodes):
            is_last = (i == len(nodes) - 1)
            self.print_ascii_tree(node, "", is_last)
    def print_ascii_tree(self, node, prefix, is_last):
        if not isinstance(node, ASTNode):
            branch = "└── " if is_last else "├── "
            print(prefix + branch + str(node))
            return
        branch = "└── " if is_last else "├── "
        print(prefix + branch + f"{node.type}: {node.value}")
        children = []
        if node.left:
            children.append(("Left", node.left))
        if node.right:
            children.append(("Right", node.right))
        if node.children:
            children.append(("Children", node.children))
        if node.body:
            children.append(("Body", node.body))
        if node.params:
            children.append(("Params", [str(p) for p in node.params]))
        if node.condition:
            children.append(("Condition", node.condition))
        if node.handler:
            children.append(("Handler", node.handler))
        for j, (label, child) in enumerate(children):
            last_child = (j == len(children) - 1)
            new_prefix = prefix + ("    " if is_last else "│   ")
            if isinstance(child, list):
                print(new_prefix + ("└── " if last_child else "├── ") + label + ":")
                for k, subchild in enumerate(child):
                    self.print_ascii_tree(subchild, new_prefix + ("    " if last_child else "│   "), k == len(child) - 1)
            else:
                print(new_prefix + ("└── " if last_child else "├── ") + label + ":")
                self.print_ascii_tree(child, new_prefix + ("    " if last_child else "│   "), True)
#=========================================================================
