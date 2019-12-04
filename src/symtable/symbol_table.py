'''The symbol table of the semantic analysis is defined here.'''


class SymbolTable:
    def __init__(self):
        self.scopes = []
        self.current_scope_level = 0

    '''Insert a new scope on this symbol table'''
    def insert(self, scope):
        self.current_scope_level = self.current_scope_level + 1
        scope.level = self.current_scope_level
        self.scopes.append(scope)

    '''Removes the current scope from the table'''
    def remove(self):
        self.current_scope_level = self.current_scope_level - 1
        self.scopes.pop()

    '''Verify if a given entry exists on this table.'''
    def is_in(self, entry_name):
        if len(self.scopes) > 0:
            return self.scopes[0].is_in(entry_name) or self.__is_below_the_top(entry_name, len(self.scopes) - 2)
        return False

    def __is_below_the_top(self, entry_name, position):
        if position < 0:
            return False
        return self.scopes[position].is_in(entry_name) or self.__is_below_the_top(entry_name, position - 1)

    '''Return the associated value of some entry name if it exists on this table.'''
    def lookup(self, entry_name):
        for scope in reversed(self.scopes):
            if scope.is_in(entry_name):
                return scope.lookup(entry_name)
