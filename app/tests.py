import pytest
from app.ast_builder import combine_rules, create_ast
from app.rule_engine import evaluate_ast
from app.db.database import save_rule, session, Rule


def test_create_ast():
    rule = "(age > 30 AND department = 'Sales')"
    ast = create_ast(rule)
    assert ast is not None

def test_evaluate_rule():
    rule = "(age > 30 AND department = 'Sales')"
    data = {"age": 35, "department": "Sales", "salary": 60000}
    ast = create_ast(rule)
    result = evaluate_ast(ast, data)
    assert result == True

def test_save_rule():
    rule = "(age > 30 AND department = 'Sales')"
    ast = create_ast(rule)
    save_rule(rule, ast)  # Save the rule
    # Retrieve the last rule to verify
    last_rule = session.query(Rule).order_by(Rule.id.desc()).first()
    assert last_rule is not None
    assert last_rule.rule_string == rule

def test_combine_rules():
    """
    Test combining multiple rules into a single AST.
    """
    rules = ["age > 30", "salary < 50000"]
    combined_ast = combine_rules(rules, "AND")
    assert combined_ast.value == "AND"
    assert combined_ast.left.value == ">"
    assert combined_ast.right.value == "<"

def test_invalid_token():
    """
    Test that an invalid token raises a ValueError.
    """
    with pytest.raises(ValueError):
        create_ast("age > 30 AND salary << 50000")  # Invalid token "<<"

def test_invalid_attribute():
    """
    Test that using an invalid attribute raises a ValueError.
    """
    rule = create_ast("invalid_attr > 30")
    with pytest.raises(ValueError):
        evaluate_ast(rule, context={"age": 40, "salary": 45000})

if __name__ == '__main__':
    pytest.main()
