import CoreEase
import os
lexer = CoreEase._compiler._LEXER.Lexer("test.py")        # Initialize Lexer Instance  for Python
tokens = lexer.tokenize()                           # Use Lexer Instance to get ur Tokens (@methods and triple " missing need to fix soon™)
#parser = CoreEase._compiler._PARSER.Parser(tokens)     # Initialize Parser Instance with ur Tokens
#try:
    #ast = parser.parse() 	                        # Create AST Tree for further Use in Emitter or Instacer // or IR for VM 
#except Exception as e:
    #print(e)
    #os.system("pause")
exit("done")