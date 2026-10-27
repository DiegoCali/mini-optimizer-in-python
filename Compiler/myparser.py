"""
program: statements;

statements: statements statement
            | statement

statement: 'print' logical ';'
         | 'if' '(' logical ')' '{' statements '}'
         | 'if' '(' logical ')' '{' statements '}' 'else' '{' statements '}'
         | 'while' '(' logical ')' '{' statements '}'
         | ID '=' logical ';'

logical: logical '&&' condition
       | logical '||' condition
       | condition

condition: expression '==' expression
         | expression '<' expression
         | expression '>' expression
         | expression '<=' expression
         | expression '>=' expression
         | expression

expression: expression '+' term
          | expression '-' term
          | term
        
term: term '*' factor
    | factor

factor: '(' expression ')'
      | NUMBER
      | ID    
      | 'true'
      | 'false'    
"""
from helper import *
from mylexer import tokens
from ply.yacc import yacc

def _labels(*values):
    labels = []
    for value in values:
        if isinstance(value, list):
            labels.extend(_labels(*value))
        else:
            labels.append(value)
    return labels

def p_program(p):
    'program : statements'    

def p_statements_recursive(p):
    'statements : statements statement'    

def p_statements_single(p):
    'statements : statement'    

def p_statement_print(p):
    'statement : PRINT logical SEMICOLON'
    print(f"print {p[2]['temp']}")

def p_statement_if(p):
    'statement : IF marked_init LPAREN logical marked_if RPAREN LKEY statements RKEY marked_if_end'
    for label in p[4]['false']:
        print(f"{label}:")
    print(f"{p[2]['final']}:")

def p_statement_if_else(p):
    'statement : IF marked_init LPAREN logical marked_if RPAREN LKEY statements RKEY marked_then ELSE marked_else LKEY statements RKEY'
    print(f"{p[2]['final']}:")

def p_statement_while(p):
    'statement : WHILE marked_init LPAREN logical marked_if RPAREN LKEY statements RKEY marked_while_end'
    print(f"goto {p[2]['entry']}")
    for label in p[4]['false']:
        print(f"{label}:")
    print(f"{p[2]['final']}:")

def p_statement_assign(p):
    'statement : ID ASSIGN logical SEMICOLON'
    print(f"{p[1]} = {p[3]['temp']}")

def p_marked_init(p):
    'marked_init : '
    entry = newLabel()
    print(f"{entry}:")
    p[0] = { 'entry': entry, 'final': newLabel() }

def p_marked_if(p):
    'marked_if : '
    for label in p[-1]['true']:
        print(f"{label}:")

def p_marked_if_end(p):
    'marked_if_end : '

def p_marked_then(p):
    'marked_then : '
    print(f"goto {p[-8]['final']}")

def p_marked_while_end(p):
    'marked_while_end : '

def p_marked_else(p):
    'marked_else : '
    for label in p[-8]['false']:
        print(f"{label}:")

def p_logical_and(p):
    'logical : logical marked_true AND condition'    
    p[0] = {
        'true': _labels(p[4]['true']),
        'false': _labels(p[1]['false'], p[4]['false'])
    }

def p_logical_or(p):
    'logical : logical marked_false OR condition'    
    p[0] = {
        'true': _labels(p[1]['true'], p[4]['true']),
        'false': _labels(p[4]['false'])
    }

def p_marked_true(p):
    'marked_true : '
    for label in p[-1]['true']:
        print(f"{label}:")

def p_marked_false(p):
    'marked_false : '
    for label in p[-1]['false']:
        print(f"{label}:")

def p_logical_condition(p):
    'logical : condition'    
    if 'true' in p[1] and 'false' in p[1]:
        p[0] = { 'true': p[1]['true'], 'false': p[1]['false'] }
    else:
        p[0] = { 'temp': p[1]['temp'] }    

def p_condition_eq(p):
    'condition : expression EQ expression'
    trueLabel = newLabel()
    falseLabel = newLabel()
    print(f"if {p[1]['temp']} == {p[3]['temp']} goto {trueLabel}")
    print(f"goto {falseLabel}")        
    p[0] = { 'true': [trueLabel], 'false': [falseLabel] }

def p_condition_lt(p):
    'condition : expression LT expression'
    trueLabel = newLabel()
    falseLabel = newLabel()
    print(f"if {p[1]['temp']} < {p[3]['temp']} goto {trueLabel}")
    print(f"goto {falseLabel}")        
    p[0] = { 'true': [trueLabel], 'false': [falseLabel] }

def p_condition_gt(p):
    'condition : expression GT expression'
    trueLabel = newLabel()
    falseLabel = newLabel()
    print(f"if {p[1]['temp']} > {p[3]['temp']} goto {trueLabel}")
    print(f"goto {falseLabel}")        
    p[0] = { 'true': [trueLabel], 'false': [falseLabel] }

def p_condition_le(p):
    'condition : expression LE expression'
    trueLabel = newLabel()
    falseLabel = newLabel()
    print(f"if {p[1]['temp']} <= {p[3]['temp']} goto {trueLabel}")
    print(f"goto {falseLabel}")        
    p[0] = { 'true': [trueLabel], 'false': [falseLabel] }

def p_condition_ge(p):
    'condition : expression GE expression'
    trueLabel = newLabel()
    falseLabel = newLabel()
    print(f"if {p[1]['temp']} >= {p[3]['temp']} goto {trueLabel}")
    print(f"goto {falseLabel}")        
    p[0] = { 'true': [trueLabel], 'false': [falseLabel] }

def p_condition_expression(p):
    'condition : expression'
    p[0] = { 'temp': p[1]['temp'] }

def p_expression_plus(p):
    'expression : expression PLUS term'
    temp = newTemp()
    print(f"{temp} = {p[1]['temp']} + {p[3]['temp']}")
    p[0] = { 'temp': temp }

def p_expression_minus(p):
    'expression : expression MINUS term'
    temp = newTemp()
    print(f"{temp} = {p[1]['temp']} - {p[3]['temp']}")
    p[0] = { 'temp': temp }

def p_expression_term(p):
    'expression : term'
    p[0] = { 'temp': p[1]['temp'] }

def p_term_times(p):
    'term : term TIMES factor'
    temp = newTemp()
    print(f"{temp} = {p[1]['temp']} * {p[3]['temp']}")
    p[0] = { 'temp': temp }

def p_term_factor(p):
    'term : factor'
    p[0] = { 'temp': p[1]['temp'] }

def p_factor_paren(p):
    'factor : LPAREN expression RPAREN'
    p[0] = { 'temp': p[2]['temp'] }

def p_factor_number(p):
    'factor : NUMBER'
    temp = newTemp()
    print(f"{temp} = {p[1]}")    
    p[0] = { 'temp': temp }

def p_factor_id(p):
    'factor : ID'
    temp = newTemp()
    print(f"{temp} = {p[1]}")    
    p[0] = { 'temp': temp }

def p_factor_true(p):
    'factor : TRUE'
    temp = newTemp()
    print(f"{temp} = 1")    
    p[0] = { 'temp': temp }

def p_factor_false(p):
    'factor : FALSE'
    temp = newTemp()
    print(f"{temp} = 0")    
    p[0] = { 'temp': temp }

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")

parser = yacc()
