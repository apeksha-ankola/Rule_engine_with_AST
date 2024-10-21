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
        print("Token:", token)  # Debug: print each token
        if token == '(':
            stack.append(current)
            current = None
        elif token == ')':
            if len(stack) > 0:
                previous = stack.pop()
                if previous is not None:
                    previous.right = current
                    current = previous
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
                # Attach the operand node correctly
                if current.right is None:
                    current.right = operand_node
                else:
                    print(f"Warning: {current.value} already has a right child. Attaching to the next available node.")  # Debug attachment
                    while current.right is not None:
                        if len(stack) == 0:
                            break
                        current = stack.pop()
                    current.right = operand_node

    if current is None:
        print("Error: No valid AST could be created from the rule string.")
    return current


valid_attributes = {"age", "department", "salary"}


def evaluate_ast(node, context):
    if node is None:
        return None  # Handle the case where node is None

    # Check the type of node
    if node.type == "operand":
        # Handle numeric and string operands
        if node.value.isnumeric():
            return int(node.value)
        elif node.value.startswith("'") and node.value.endswith("'"):
            return node.value.strip("'")
        else:
            return context.get(node.value, None)

    # Handle operator nodes (e.g., AND, OR, >, <)
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


def combine_rules(rules):
    combined_ast = None
    for rule in rules:
        ast = create_ast(rule)  # Create AST from rule string
        if ast is None:
            print(f"Skipping invalid rule: {rule}")
            continue  # Skip invalid rules
        if combined_ast is None:
            combined_ast = ast
        else:
            # Combine the existing AST with the new one
            combined_node = Node("operator", "AND")  # You can change this to OR if needed
            combined_node.left = combined_ast
            combined_node.right = ast
            combined_ast = combined_node
    return combined_ast


# Main Code Execution
if __name__ == "__main__":
    rules = [
        "(age > 30 AND department = 'Sales')",
        "(salary < 50000 OR age < 25)"
    ]

    combined_ast = combine_rules(rules)  # Combine ASTs from multiple rules

    # Define the context for evaluation
    context = {
        "age": 35,
        "department": "Sales",
        "salary": 40000
    }

    # Evaluate the combined AST
    result = evaluate_ast(combined_ast, context)
    print("Result of combined AST evaluation:", result)
