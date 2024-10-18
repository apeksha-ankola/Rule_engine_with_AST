import pytest
from app.ast_builder import create_ast
from app.rule_engine import evaluate_ast

def test_create_ast():
    rule = "(age > 30 AND department = 'Sales')"
    ast = create_ast(rule)
    assert ast is not None

def test_evaluate_rule():
    rule = "(age > 30 AND department = 'Sales')"
    data = {"age": 35, "department": "Sales", "salary": 60000}
    ast = create_ast(rule)
    result = evaluate_rule(ast, data)
    assert result == True

if __name__ == '__main__':
    pytest.main()
