from flask import Flask, request, jsonify
from ast_builder import create_ast
from rule_engine import evaluate_ast, Node

app = Flask(__name__)


@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json['rule']
    ast = create_ast(rule_string)  # Generate the AST
    return jsonify({"ast": ast.to_dict()})  # Serialize it to a dictionary


def dict_to_node(ast_dict):
    """Convert dictionary representation of AST to Node objects."""
    if ast_dict['type'] == 'operand':
        return Node(node_type='operand', value=ast_dict['value'])
    elif ast_dict['type'] == 'operator':
        left_node = dict_to_node(ast_dict['left'])
        right_node = dict_to_node(ast_dict['right'])
        return Node(node_type='operator', value=ast_dict['value'], left=left_node, right=right_node)
    return None


@app.route('/evaluate_rule', methods=['POST'])
def evaluate():
    data = request.json
    ast_dict = data['ast']  # The AST in dictionary form
    context = data['context']  # Access the context here

    # Convert dictionary AST to Node objects
    ast = dict_to_node(ast_dict)

    # Evaluate the AST
    result = evaluate_ast(ast, context)
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)
