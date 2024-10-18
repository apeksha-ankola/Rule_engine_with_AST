class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        result = {"type": self.type}
        if self.value:
            result["value"] = self.value
        if self.left:
            result["left"] = self.left.to_dict()
        if self.right:
            result["right"] = self.right.to_dict()
        return result

def create_ast(rule_string):
    tokens = rule_string.replace("(", " ( ").replace(")", " ) ").split()
    stack = []
    current = None

    for token in tokens:
        if token == '(':
            stack.append(current)
            current = None
        elif token == ')':
            if len(stack) > 0:
                current = stack.pop()
        elif token in ["AND", "OR"]:
            node = Node("operator", token)
            node.left = current
            current = node
        elif token in [">", "<", "=", "!="]:
            operator_node = Node("operator", token)
            operator_node.left = current
            current = operator_node
        else:
            operand_node = Node("operand", token)
            if current is None:
                current = operand_node
            else:
                current.right = operand_node

    if current is None:
        print("Error: No valid AST could be created from the rule string.")
    return current

def evaluate_ast(node, context):
    if node is None:
        return None  # Handle the case where node is None

    # Check the type of node
    if node.type == "operand":
        if node.value.isnumeric():
            return int(node.value)
        elif node.value.startswith("'") and node.value.endswith("'"):
            return node.value.strip("'")
        else:
            return context.get(node.value, None)

    elif node.type == "operator":
        left_value = evaluate_ast(node.left, context)
        right_value = evaluate_ast(node.right, context)

        if node.value == ">":
            return left_value > right_value
        elif node.value == "<":
            return left_value < right_value
        elif node.value == "=":
            return left_value == right_value
        elif node.value == "!=":
            return left_value != right_value
        elif node.value == "AND":
            return left_value and right_value
        elif node.value == "OR":
            return left_value or right_value

    return None

# Main Code Execution
if __name__ == "__main__":
    rule_string = "(age > 30 AND department = 'Sales')"
    ast = create_ast(rule_string)  # Create AST from rule string

    # Define the context for evaluation
    context = {
        "age": 35,
        "department": "Sales"
    }

    # Evaluate the AST
    result = evaluate_ast(ast, context)
    print("Result of AST evaluation:", result)
