'''Defines the scope of a MiniJava block of code.'''


class Scope:
    def __init__(self, scope_level=0):
        self.table = dict()
        self.level = scope_level

    '''Insert a new entry on this scope'''
    def insert(self, entry_name, entry_values=None):
        if( entry_name in self.table ):
            self.table[entry_name].update(entry_values)
        else:
            self.table[entry_name] = entry_values
        #print(self.table)

    '''Verify if a given entry exists on this scope.'''
    def is_in(self, entry_name):
        return entry_name in self.table

    '''Return the associated value of some entry name if it exists onthis scope.'''
    def lookup(self, entry_name):
        return self.table[entry_name] if (self.is_in(entry_name)) else None
