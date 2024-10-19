class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # "operator" or "operand"
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
    """
    Converts a rule string into an Abstract Syntax Tree (AST).
    Raises a ValueError for invalid tokens.
    """
    # Clean up and tokenize the rule string
    rule_string = rule_string.strip()  # Remove leading/trailing spaces
    tokens = rule_string.replace("(", " ( ").replace(")", " ) ").split()  # Handle parentheses
    stack = []
    current = None
    valid_operators = ["AND", "OR", ">", "<", "=", "!="]

    for token in tokens:
        # Validate each token
        if token not in valid_operators and not token.replace("'", "").isalnum() and token not in ["(", ")"]:
            raise ValueError(f"Invalid token in rule: {token}")

        if token == '(':
            stack.append(current)
            current = None
        elif token == ')':
            if stack:
                if current:
                    last_operator = stack.pop()
                    if last_operator:
                        last_operator.right = current
                        current = last_operator
        elif token in ["AND", "OR"]:
            node = Node("operator", token)
            if current:  # If there's already a current node, set it as the left child
                node.left = current
            current = node  # Update current to the new operator node
        elif token in [">", "<", "=", "!="]:
            operator_node = Node("operator", token)
            if current:  # If there's already a current operand, set it as the left child
                operator_node.left = current
            current = operator_node  # Update current to the new operator node
        else:
            operand_node = Node("operand", token)
            if current is None:  # If current is None, this is the first operand
                current = operand_node
            else:
                # If current is an operator, set the operand as the right child
                if current.type == "operator" and current.right is None:
                    current.right = operand_node
                else:
                    # If current is an operand, create a new operator node
                    new_operator = Node("operator", current.value)
                    new_operator.left = current
                    new_operator.right = operand_node
                    current = new_operator

    # Check if there is any unresolved operator in the stack
    while stack:
        last_operator = stack.pop()
        if last_operator:
            last_operator.right = current
            current = last_operator

    # Return the final AST
    return current


# Function to combine multiple rules into one AST
def combine_rules(rules, operator="AND"):
    """
    Combines multiple rules into a single AST using the provided operator (AND/OR).
    """
    combined_ast = None
    for rule in rules:
        ast = create_ast(rule)  # Create AST for each rule
        if combined_ast is None:
            combined_ast = ast  # Initialize AST with the first rule
        else:
            # Combine ASTs using the provided operator
            combined_ast = Node(node_type="operator", value=operator, left=combined_ast, right=ast)
    return combined_ast


# Example Usage
rule_string = "(age > 30 AND department = 'Sales')"
ast = create_ast(rule_string)
if ast:
    print(ast.to_dict())
else:
    print("AST is None.")
