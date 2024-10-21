from flask import Flask, jsonify, render_template, request
from ast_builder import create_ast, ASTError  # Import custom error class if defined
from rule_engine import Node, evaluate_ast
from db.database import save_rule  # Absolute import from db

app = Flask(__name__)

@app.route('/create_rule', methods=['POST'])
def create_rule():
    data = request.get_json()
    rule_string = data.get('rule')

    # Basic validation for empty input
    if not rule_string:
        return jsonify({"error": "Rule string cannot be empty."}), 400

    try:
        ast = create_ast(rule_string)  # Generate the AST
        save_rule(rule_string, ast)    # Save the rule in the database
        return jsonify({"ast": ast.to_dict()})  # Serialize it to a dictionary
    except ASTError as e:  # Handle specific AST errors
        return jsonify({"error": str(e)}), 400
    except Exception as e:  # Handle any other unexpected errors
        return jsonify({"error": "An error occurred while processing the rule: " + str(e)}), 500

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
    ast_dict = data.get('ast')  # The AST in dictionary form
    context = data.get('context')  # Access the context here

    if not ast_dict or not context:
        return jsonify({"error": "AST and context are required for evaluation."}), 400

    try:
        # Convert dictionary AST to Node objects
        ast = dict_to_node(ast_dict)

        # Evaluate the AST
        result = evaluate_ast(ast, context)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": "An error occurred during evaluation: " + str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    rule_string = request.args.get('rule_string')
    ast = create_ast(rule_string)
    context = {}  # Define your evaluation context
    evaluation_result = evaluate_ast(ast, context)  # Call the correct evaluation function
    return render_template('result.html', rule_string=rule_string, result=evaluation_result)

if __name__ == '__main__':
    app.run(debug=True)
