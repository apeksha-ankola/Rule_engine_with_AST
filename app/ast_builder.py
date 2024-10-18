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
    tokens = rule_string.replace("(", " ( ").replace(")", " ) ").split()
    stack = []
    current = None

    for token in tokens:
        if token == '(':
            stack.append(current)
            current = None
        elif token == ')':
            if stack:
                if current:
                    # If there's a current node, pop the last operator
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
                    # If current is an operand, we can create a new operator node
                    # to maintain the tree structure
                    new_operator = Node("operator", current.value)
                    new_operator.left = current
                    new_operator.right = operand_node
                    current = new_operator

    # Check if current is None before returning
    if current is None:
        print("Error: No valid AST could be created from the rule string.")
    return current

# Example Usage
rule_string = "(age > 30 AND department = 'Sales')"
ast = create_ast(rule_string)
if ast:
    print(ast.to_dict())
else:
    print("AST is None.")
