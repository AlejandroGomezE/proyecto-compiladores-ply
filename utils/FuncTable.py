class Table:
    # Scope Table
    def __init__(self, parent_ref):
        self.ref = -1
        self.parent_ref = parent_ref
        self.params = []
        self.vars = {}
        self.functions = {}
        self.func_name = None
        self.quad_start = None
        self.return_type = None
        self.return_value = None

    def add_parameter(self, name):
        self.params.append(name)

    def add_variable(self, name, type, addr=-1):
        self.vars[name] = {
            'type': type,
            'addr': addr,
        }

    def __str__(self):
        message = "Scope Ref: %s, Parent Ref: %s, Function Name: %s, Return Type: %s, Params: %s \nfuncs:\n" % (
            self.ref, self.parent_ref, self.func_name, self.return_type, self.params)

        for func in self.functions:
            message += "\t%s\n" % func

        message += "vars:\n"

        for var in self.vars:
            message += "\t%s: %s\n" % (var, self.vars[var])

        return message + '\n'


class FuncTable():
    # Functions Table
    def __init__(self):
        # When the table is created, global scope is defined with parent scope ref -1
        self.counter = 0
        global_scope = Table(-1)
        self.dict = {}
        self.add_scope(global_scope)

    def add_scope(self, scope):
        # Assign current scope counter number to scope as scope ref, assign scope content to that ref, and increment counter
        scope.ref = self.counter
        self.dict[scope.ref] = scope
        self.counter = self.counter + 1

    def __str__(self):
        message = ''
        for table in self.dict.values():
            message += str(table)

        return message
