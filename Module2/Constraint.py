class Constraint:


    #create constraint on the following form:

    #varList contains all nodes that are involved in the constraint

    #expression describes how the constraint is structured, for instance (n1 != n2) or (n1 < n2 + n3)
    def __init__(self, varList, expression):
        self.variables = varList
        self.expression = expression

    def contains(self, variable):
        if variable in self.variables:
            return True
        return False








