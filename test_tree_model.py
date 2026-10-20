import unittest
from tree_model import *

class TreeTests(unittest.TestCase):
    def test_traversals(self):
        orders=traversals(build_values('8 4 12 2 6 10 14'))
        expected={'Preorder':'8 4 2 6 12 10 14','Inorder':'2 4 6 8 10 12 14','Postorder':'2 6 4 10 14 12 8','Level order':'8 4 12 2 6 10 14'}
        for name,values in expected.items():self.assertEqual([n.value for n in orders[name]],values.split())
    def test_alpha(self):
        self.assertEqual([n.value for n in traversals(build_values('M f T B','Alphabetical'))['Inorder']],['B','f','M','T'])
    def test_level_filled(self):
        root=build_values('9 1 8 2',layout='Level-filled tree')
        self.assertEqual(root.left.left.value,'2')
    def test_sum_duplicates_negatives(self):
        nodes=traversals(build_values('-2 3.5 3.5'))
        for order in nodes.values():self.assertEqual(sum(number(n.value) for n in order),5)
    def test_notations(self):
        for text,notation in [('(8+4)*(10-7)','Infix'),('* + 8 4 - 10 7','Prefix'),('8 4 + 10 7 - *','Postfix')]:
            self.assertEqual(evaluate(build_expression(text,notation)),36)
    def test_precedence(self):
        for text,expected in [('2^3^2',512),('-2^2',-4),('2^-2',.25),('10%3',1),('-(2+3)',-5)]:
            self.assertEqual(evaluate(build_expression(text)),expected)
    def test_invalid(self):
        for text in ['', '2 a', 'NaN', 'inf']:
            with self.assertRaises(ValueError):build_values(text)
        for text in ['__import__("os")','x+2','True','[1]', '1//2','2 +']:
            with self.assertRaises(ValueError):build_expression(text)
        for text in ['1/0','1%0','(-1)^0.5','2^1001']:
            with self.assertRaises(ValueError):evaluate(build_expression(text))
        for text in ['2 +','2 3','+ 2']:
            with self.assertRaises(ValueError):build_expression(text,'Postfix')
    def test_limits(self):
        with self.assertRaises(ValueError):build_values(' '.join(['1']*128))
        self.assertEqual(len(traversals(build_values(' '.join(map(str,range(127)))))['Preorder']),127)

if __name__=='__main__':unittest.main()
