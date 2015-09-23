class CSP:
    def __init__(self):
        # self.variables is a list of the variables in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        self.queue = []

        #keeps track of how many nodes that have only one value in their domain,
        #when this reaches the amount of nodes, the csp is solved
        self.progress = 0

    def printConstraints(self, variable):
        for i in self.constraints[variable]:
            print(i.expression)


    # func = makefunc(['x', 'y', 'z'], 'x + y < 2*z')
    def makefunc(self, varNames, expression, envir=globals()):
        args = ""
        for n in varNames: args = args + "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")", envir)

    #not general yet, because it only works for constraints involving two variables,
    #need one extra for loop for each additional variable
    def revise(self, variable, constraint):
        modified = False

        variableTexts = []
        variablesInvolved = constraint.variables
        for j in variablesInvolved:
            variableTexts.append(j.text)

        func = self.makefunc(variableTexts, constraint.expression)
        test = []
        if len(variablesInvolved) == 1:
            for j in self.domains[variablesInvolved[0]]:
                if not func(j):
                    test.append(j)
                    if len(self.domains[variable]) == 1:
                        self.progress += 1
                    modified = True
            for j in test:
                self.domains[variable].remove(j)

        elif len(variablesInvolved) == 2:
            for j in self.domains[variablesInvolved[0]]:
                for k in self.domains[variablesInvolved[1]]:
                    if func(j, k):
                        break
                else:
                    test.append(j)
                    if len(self.domains[variable]) == 1:
                        self.progress += 1
                    modified = True
            for j in test:
                self.domains[variable].remove(j)
        return modified

    #initialize the queue containing variables and constraint pairs to filter variable domains
    def initializeQueue(self):
        for i in self.variables:
            for j in self.constraints[i]:
                self.queue.append((i, j))

    #filter the variable domains until no more deductions can be made
    def domainFilter(self):
        while self.queue:
            varConsTuple = self.queue.pop(0)
            currentVariable = varConsTuple[0]
            currentConstraint = varConsTuple[1]

            if self.revise(currentVariable, currentConstraint):
                for i in self.constraints[currentVariable]:
                    if i != currentConstraint:
                        self.queue.append((currentVariable, i))

    def rerun(self, variable):
        for i in self.constraints[variable]:
            for j in range(len(i.variables)):
                if i.variables[j] != variable:
                    for k in self.constraints[i.variables[j]]:
                        if k.contains(variable):
                            self.queue.append((i.variables[j], k))

    def isSolved(self):
        if self.progress >= len(self.variables):
            return True
        return False