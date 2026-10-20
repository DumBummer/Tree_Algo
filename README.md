# Tree Studio

A Python desktop tree graph system with a cream card interface and a dark, glowing node canvas, inspired by the supplied references.

## Run on Windows / VS Code

Install Python 3.10 or newer with Tcl/Tk enabled, then open this folder in VS Code:

```powershell
python main.py
```

No pip packages required. On Debian/Ubuntu, install `python3-tk` if Tkinter is missing.

## Build a tree

- Select Numerical or Alphabetical; enter values separated by spaces or commas.
- Binary search tree inserts in input order; smaller values go left, equal or larger values go right. Alphabetical comparisons ignore case. Duplicates are preserved.
- Level-filled tree places input values across each level from left to right.
- Numerical mode without operators sums every node, including duplicates. Every traversal has the same sum because it visits the same nodes.
- Enable operators to create an expression tree. Infix supports parentheses, unary signs, and `+ - * / % ^`. Exponentiation uses normal precedence and right associativity. Prefix and postfix require space-separated tokens, binary operators, and signed numeric operands (for example `-3`).
- Examples: infix `(8 + 4) * 3`; prefix `* + 8 4 3`; postfix `8 4 + 3 *`. All evaluate to 36.
- Expression value is calculated from the original tree, never by treating each traversal as an infix formula. Inorder traversal displays node labels without grouping parentheses.
- Mixed alphabetical/numeric values are rejected. Maximum 127 nodes; finite real arithmetic only.

## Explore

Four colored rows display preorder, inorder, postorder, and level order. Click a traversal row, use Step, or Play/Pause to highlight its node sequence. Text fields allow copying results and horizontal scrolling with the cursor keys.

The graph frame starts empty. Drag anywhere to pan, use the direction buttons, scroll to zoom around the pointer, or use + / − and Fit. Click a node to inspect its value. Build, Load example, and Clear are interactive.

## Project structure

- `main.py`: GUI, canvas, controls and traversal animation.
- `tree_model.py`: data model, construction, traversal, safe arithmetic parsing and evaluation; no GUI dependencies.
- `test_tree_model.py`: automated algorithm and validation tests.

Run tests with `python -m unittest -v`.
