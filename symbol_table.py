##############################################################################
# FILE : symbol_table.py                                                     #
# EXERCISE : nand2tetris project11 2016-2017                                 #
# DESCRIPTION : A program that contains a class definition of SymbolTable    #
#               that associates the identifier names found in the program    #
#               with identifier properties: type, kind, and running index.   #
##############################################################################
from enum import Enum


class SymbolKinds(Enum):
    STATIC = 1
    FIELD = 2
    ARG = 3
    VAR = 4

TYPE = 0
KIND = 1
INDEX = 2


class SymbolTable:
    """
    A symbol table that associates the identifier names found in the program
    with identifier properties needed for compilation: type, kind, and
    running index.
    The symbol table for Jack programs has two nested scopes (class/
    subroutine)
    """
    def __init__(self):
        """
        Creates a new empty symbol table
        """
        self.__class_table = {}
        self.__subroutine_table = {}
        self.__field_counter = 0
        self.__static_counter = 0
        self.__arg_counter = 0
        self.__local_counter = 0

    def start_subroutine(self):
        """
        Starts a new subroutine scope (i.e. resets the subroutine's symbol
        table)
        """
        self.__subroutine_table = {}
        self.__arg_counter = 0
        self.__local_counter = 0

    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type, and kind,
        and assigns it a running index. STATIC and FIELD identifiers have a
        class scope, while ARG and VAR identifiers have a subroutine scope.
        :param name:
        :param type:
        :param kind:
        """
        if kind == SymbolKinds.STATIC:
            self.__class_table[name] = [type, kind, self.__static_counter]
            self.__static_counter += 1
        elif kind == SymbolKinds.FIELD:
            self.__class_table[name] = [type, kind, self.__field_counter]
            self.__field_counter += 1
        elif kind == SymbolKinds.ARG:
            self.__subroutine_table[name] = [type, kind, self.__arg_counter]
            self.__arg_counter += 1
        elif kind == SymbolKinds.VAR:
            self.__subroutine_table[name] = [type, kind, self.__local_counter]
            self.__local_counter += 1
        else:
            print("ERROR: no such symbol kind")

    def var_count(self, kind):
        """
        :param kind:
        :return: The number of variables of the given kind already defined
        in the current scope
        """
        if kind == SymbolKinds.STATIC:
            return self.__static_counter
        elif kind == SymbolKinds.FIELD:
            return self.__field_counter
        elif kind == SymbolKinds.ARG:
            return self.__arg_counter
        elif kind == SymbolKinds.VAR:
            return self.__local_counter
        else:
            print("ERROR: no such symbol kind")

    def kind_of(self, name):
        """
        :param name:
        :return: The kind of the named identifier in the current scope. If
        the identifier is unknown in the current scope, returns None.
        """
        if name in self.__subroutine_table:
            return self.__subroutine_table[name][KIND]
        elif name in self.__class_table:
            return self.__class_table[name][KIND]
        else:
            return None

    def type_of(self, name):
        """
        :param name:
        :return: The type of the named identifier in the current scope.
        """
        if name in self.__subroutine_table:
            return self.__subroutine_table[name][TYPE]
        elif name in self.__class_table:
            return self.__class_table[name][TYPE]
        else:
            return None

    def index_of(self, name):
        """
        :param name:
        :return: The index assigned to the named identifier.
        """
        if name in self.__subroutine_table:
            return self.__subroutine_table[name][INDEX]
        elif name in self.__class_table:
            return self.__class_table[name][INDEX]
        else:
            return None

