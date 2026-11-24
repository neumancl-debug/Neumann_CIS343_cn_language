import token

from error_handling import RuntimeError

# Environment class for managing variable scopes and values.
class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    # Defines a new variable in the current environment with the given name and value. 
    def define(self, name, value):
        self.values[name] = value

    # Retrieves the value of a variable by its token. If the variable is not found in the current environment
        name = token.lexeme

        if name in self.values:
           return self.values[name]
        
        if self.enclosing is not None:
            return self.enclosing.get(token)
        # If the variable is not found in any enclosing environment, raise a runtime error indicating that the variable is undefined.
        raise RuntimeError(token, f"Undefined variable '{name}'.")

    # Assigns a new value to an existing variable by its token. If the variable is not found in the current environment,
    def assign(self, token, value):
        name = token.lexeme

        if name in self.values:
            self.values[name] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(token, value)
            return
        # If the variable is not found in any enclosing environment, raise a runtime error indicating that the variable is undefined.
        raise RuntimeError(token, f"Undefined variable '{name}'.")
    