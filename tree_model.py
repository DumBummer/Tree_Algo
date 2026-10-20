"""Tree construction, safe expression parsing, traversal and evaluation."""
from dataclasses import dataclass
from collections import deque
import ast
import math
import re

@dataclass(eq=False)
class Node:
    value: str
    left: 'Node | None' = None
    right: 'Node | None' = None

OPERATORS = {'+': lambda a,b:a+b, '-':lambda a,b:a-b, '*':lambda a,b:a*b,
             '/':lambda a,b:a/b, '%':lambda a,b:a%b, '^':lambda a,b:a**b}

def number(text):
    try:
        value = float(text)
    except ValueError:
        raise ValueError('Use only numbers, or only alphabetical words.') from None
    if not math.isfinite(value):
        raise ValueError('Numbers must be finite.')
    return value

def build_values(text, kind='Numerical', layout='Binary search tree'):
    tokens = re.split(r'[\s,]+', text.strip())
    if not text.strip():
        raise ValueError('Enter some values first.')
    if len(tokens) > 127:
        raise ValueError('Use at most 127 nodes.')
    if kind == 'Alphabetical':
        if not all(t.isalpha() for t in tokens):
            raise ValueError('Alphabetical mode accepts letters and words only.')
        key = str.casefold
    else:
        for token in tokens: number(token)
        key = number
    nodes = [Node(t) for t in tokens]
    root = nodes[0]
    if layout == 'Level-filled tree':
        for i, node in enumerate(nodes):
            if 2*i+1 < len(nodes): node.left = nodes[2*i+1]
            if 2*i+2 < len(nodes): node.right = nodes[2*i+2]
    else:
        for node in nodes[1:]:
            current = root
            while True:
                side = 'left' if key(node.value) < key(current.value) else 'right'
                if getattr(current, side) is None:
                    setattr(current, side, node)
                    break
                current = getattr(current, side)
    return root

def build_expression(text, notation='Infix'):
    if not text.strip(): raise ValueError('Enter an expression first.')
    if len(text) > 2000: raise ValueError('Expression is too long.')
    if notation == 'Infix':
        try: parsed = ast.parse(text.replace('^', '**'), mode='eval')
        except (SyntaxError, RecursionError): raise ValueError('Invalid infix expression.') from None
        mapping = {ast.Add:'+', ast.Sub:'-', ast.Mult:'*', ast.Div:'/', ast.Mod:'%', ast.Pow:'^'}
        def convert(n):
            if isinstance(n, ast.Constant) and type(n.value) in (int,float):
                number(str(n.value))
                return Node(str(n.value))
            if isinstance(n, ast.BinOp) and type(n.op) in mapping:
                return Node(mapping[type(n.op)], convert(n.left), convert(n.right))
            if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
                return Node('pos' if isinstance(n.op,ast.UAdd) else 'neg', convert(n.operand))
            raise ValueError('Use numbers and + - * / % ^ with parentheses only.')
        try: root = convert(parsed.body)
        except RecursionError: raise ValueError('Expression is too deeply nested.') from None
    else:
        tokens = text.split()
        stack = []
        for token in (reversed(tokens) if notation == 'Prefix' else tokens):
            if token in OPERATORS:
                if len(stack) < 2: raise ValueError('Each operator needs two operands. Separate tokens with spaces.')
                a,b = stack.pop(),stack.pop()
                stack.append(Node(token,a,b) if notation == 'Prefix' else Node(token,b,a))
            else:
                number(token)
                stack.append(Node(token))
        if len(stack) != 1: raise ValueError('Expression has unused operands or missing operators.')
        root = stack[0]
    if len(traversals(root)['Preorder']) > 127: raise ValueError('Use at most 127 nodes.')
    return root

def traversals(root):
    result = {name:[] for name in ('Preorder','Inorder','Postorder','Level order')}
    def walk(n):
        if n is None: return
        result['Preorder'].append(n)
        walk(n.left)
        result['Inorder'].append(n)
        walk(n.right)
        result['Postorder'].append(n)
    walk(root)
    queue = deque([root] if root else [])
    while queue:
        n = queue.popleft()
        result['Level order'].append(n)
        queue.extend(child for child in (n.left,n.right) if child)
    return result

def evaluate(root):
    if root.value in ('neg','pos'):
        return (-1 if root.value == 'neg' else 1)*evaluate(root.left)
    if root.value not in OPERATORS: return number(root.value)
    a,b = evaluate(root.left),evaluate(root.right)
    if root.value == '^' and (abs(b)>1000 or abs(a)>1e100):
        raise ValueError('Exponent is too large.')
    try: result = OPERATORS[root.value](a,b)
    except (ZeroDivisionError, OverflowError, ValueError):
        raise ValueError('Undefined arithmetic: check division, modulo, or exponent.') from None
    if isinstance(result,complex) or not math.isfinite(result): raise ValueError('Result must be a finite real number.')
    return result

def format_number(value): return format(value,'.12g')
