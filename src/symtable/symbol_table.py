'''The symbol table of the semantic analysis is defined here.'''
from .scope import Scope

class SymbolTable:
    def __init__(self):
        self.scopes = []
        self.current_scope_level = 0
        #Creating global scope
        self.scopes.append(Scope(self.current_scope_level)) 

    '''Insert a new scope on this symbol table'''

    def insert_scope(self, scope):
        self.current_scope_level = self.current_scope_level + 1
        scope.level = self.current_scope_level
        self.scopes.append(scope)

    '''Insert a new entry on the top scope'''

    def insert_entry(self, entry_name, entry_values=None):
        self.scopes[self.current_scope_level].insert(entry_name, entry_values)

    '''Removes the current scope from the table'''

    def remove(self):
        if(len(self.scopes) > 0):
            self.current_scope_level = self.current_scope_level - 1
            self.scopes.pop()

    '''Verify if a given entry exists on global scope (0).'''
    def is_in_global(self, entry_name):
        return self.scopes[0].is_in(entry_name)

    """ def __is_below_the_top(self, entry_name, position):
        if position < 0:
            return False
        return self.scopes[position].is_in(entry_name) or self.__is_below_the_top(entry_name, position - 1) """

    '''Return the associated value of some entry name if it exists on this table.'''

    def lookup(self, entry_name):
        for scope in reversed(self.scopes):
            if scope.is_in(entry_name):
                return scope.lookup(entry_name)
