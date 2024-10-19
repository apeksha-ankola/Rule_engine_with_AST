from flask import Flask, jsonify, render_template, request, redirect, url_for
from ast_builder import create_ast        # Use absolute import
from rule_engine import Node, evaluate_ast
from db.database import save_rule             # Absolute import from db

app = Flask(__name__)

@app.route('/create_rule', methods=['POST'])
def create_rule():
    try:
        data = request.get_json()
        rule_string = data['rule']
        ast = create_ast(rule_string)  # Generate the AST
        save_rule(rule_string, ast)    # Save the rule in the database
        return jsonify({"ast": ast.to_dict()})  # Return the AST
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Return error message as JSON


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

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/result')
def result():
    rule_string = request.args.get('rule_string')
    ast = create_ast(rule_string)
    # Assuming you have a context for evaluation, you can define it here
    context = {}  # Define your evaluation context
    evaluation_result = evaluate_rule(ast, context)
    return render_template('result.html', rule_string=rule_string, result=evaluation_result)

if __name__ == '__main__':
    app.run(debug=True)
