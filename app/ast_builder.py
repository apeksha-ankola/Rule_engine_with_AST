class ASTError(Exception):
    """Custom exception for AST errors."""
    pass


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
    Raises an ASTError for invalid tokens or syntactic errors.
    """
    rule_string = rule_string.strip()  # Remove leading/trailing spaces
    tokens = rule_string.replace("(", " ( ").replace(")", " ) ").split()  # Handle parentheses
    stack = []
    current = None
    valid_operators = ["AND", "OR", ">", "<", "=", "!="]

    # Track the last processed token
    last_token = None

    for token in tokens:
        # Validate each token
        if token not in valid_operators and not token.replace("'", "").isalnum() and token not in ["(", ")"]:
            raise ASTError(f"Invalid token in rule: {token}")

        if token == '(':
            stack.append(current)
            current = None
            last_token = token
        elif token == ')':
            if stack:
                if current:
                    last_operator = stack.pop()
                    if last_operator:
                        last_operator.right = current
                        current = last_operator
                else:
                    raise ASTError("Unexpected closing parenthesis: opening without a corresponding closing.")
            else:
                raise ASTError("Unexpected closing parenthesis: no matching opening parenthesis.")
            last_token = token
        elif token in ["AND", "OR"]:
            if last_token in valid_operators + ["(", None]:
                raise ASTError(f"Unexpected operator: {token} following {last_token}.")
            node = Node("operator", token)
            if current:  # If there's already a current node, set it as the left child
                node.left = current
            current = node  # Update current to the new operator node
            last_token = token
        elif token in [">", "<", "=", "!="]:
            if last_token in valid_operators + ["(", None]:
                raise ASTError(f"Unexpected comparison operator: {token} following {last_token}.")
            operator_node = Node("operator", token)
            if current:  # If there's already a current operand, set it as the left child
                operator_node.left = current
            current = operator_node  # Update current to the new operator node
            last_token = token
        else:
            # This is an operand
            if last_token in valid_operators + ["(", None]:
                operand_node = Node("operand", token)
                if current is None:  # If current is None, this is the first operand
                    current = operand_node
                else:
                    # If current is an operator, set the operand as the right child
                    if current.type == "operator":
                        current.right = operand_node
                    else:
                        raise ASTError(f"Unexpected operand: {token} following {last_token}.")
            else:
                raise ASTError(f"Unexpected operand: {token} following {last_token}.")
            last_token = token

    # If we reach here, we need to check for completeness of the current tree
    if current is None:
        raise ASTError("Empty rule: no valid AST generated.")

    # Ensure no unmatched opening parentheses
    if stack:
        raise ASTError("Unmatched opening parentheses in rule.")

    # Check if the last token processed is an operator or an opening parenthesis
    if last_token in ["AND", "OR", ">", "<", "=", "!="]:
        raise ASTError(f"Unexpected end of rule: incomplete expression ends with operator '{last_token}'.")

    return current


if __name__ == "__main__":
    # Test valid rule
    rule_string = "(age > 30 AND department = 'Sales')"
    try:
        ast = create_ast(rule_string)
        print("AST for single rule:")
        print(ast.to_dict())
    except ASTError as e:
        print(f"Error: {str(e)}")

    # Test invalid rules
    invalid_rules = [
        "(age > 30 AND department = 'Sales'",  # Missing closing parenthesis
        "age > 30 AND = 'Sales'",  # Invalid operator
        "(age > 30 AND)",  # Incomplete expression
        "(age ( 30 AND department = 'Sales')"  # Invalid token
    ]

    for rule in invalid_rules:
        try:
            print(f"Testing invalid rule: {rule}")
            create_ast(rule)  # This should raise an error
        except ASTError as e:
            print(f"Error for rule '{rule}': {str(e)}")
