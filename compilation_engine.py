from jack_tokenizer import *
from symbol_table import *
from vm_writer import *
##################################################
# FILE : compilation_engine.py                   #
# WRITERS : Robinov Shaul, shaul_ro, 309673184   #
#           Roi Shaag, roi351, 204056915         #
# EXERCISE : Nand2Tetris ex10 2016-2017          #
# DESCRIPTION : Jack programs compiler           #
##################################################


CLASS_VAR_DEC_OPENER = ["static", "field"]
SUBROUTINE_DEC_OPENER = ["constructor", "function", "method"]
OP_ARR = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
SPECIAL_SYMBOLS = {"<": "&lt;", ">": "&gt;", "&": "&amp;", "\"": "&quot;",
                   "\n": "\\n", "\t": "\\t", "\r": "\\r"}

KINDS_TO_STR = {SymbolKinds.ARG: "argument", SymbolKinds.FIELD: "this",
                SymbolKinds.STATIC: "static", SymbolKinds.VAR: "local"}

STR_TO_KINDS = {"argument": SymbolKinds.ARG, "field": SymbolKinds.FIELD,
                "static": SymbolKinds.STATIC, "local": SymbolKinds.VAR}

BINARY_OP = {"+": "add", "-": "sub", "=": "eq", ">": "gt", "<": "lt",
             "&": "and", "|": "or", "*": "call Math.multiply 2",
             "/": "call Math.divide 2"}

UNARY_OP = {"-": "neg", "~": "not"}


class CompilationEngine:
    """
    Effects the actual compilation output. Gets its input from a
    JackTokenizer and emits its parsed structure into an output file/stream.
    This module emits a structured printout of the code, wrapped in XML tags.
    """
    def __init__(self, input_file, output_file, tokenizer):
        """
        Creates a new compilation engine with the given input and output
        """
        self.__label_counter = 0
        self.__input_file = input_file
        self.__vm_writer = VmWriter(output_file)
        self.__out = output_file
        self.__tokenizer = tokenizer
        self.__symbol_table = SymbolTable()
        self.__tokenizer.advance()
        self.__num_of_spaces = 0
        self.__class_name = ""

    def __eat_and_compile(self, expected_token):
        """
        :return:
        """
        # print(self.__tokenizer.get_curr_token())
        if self.__tokenizer.get_curr_token() != expected_token:
            print("actual: "+self.__tokenizer.get_curr_token()+"\nexpected: "
                  + expected_token)
            print("Compilation Error!")
        else:
            self.__tokenizer.advance()


    def __compile_name(self, id_kind="", is_defined=False, id_type=""):
        """

        """
        if self.__tokenizer.get_curr_token() in KEYWORDS_ARR:
            self.__tokenizer.advance()
        else:
            self.__compile_identifier(self.__tokenizer.get_curr_token(),
                                      is_defined, id_kind, id_type)

    def __compile_identifier(self, name, is_defined=False, id_kind="",
                             id_type=""):
        """

        :param is_defined:
        :param id_type:
        :param id_kind:
        :return:
        """
        if id_type and is_defined:
            self.__symbol_table.define(name, id_type, STR_TO_KINDS[id_kind])
        self.__tokenizer.advance()


    def compile_class(self):
        """
        Compiles a complete class
        """
        self.__eat_and_compile("class")
        self.__class_name = self.__tokenizer.get_curr_token()
        self.__compile_identifier(name=self.__tokenizer.get_curr_token(),
                                  is_defined=True, id_kind="class")
        self.__eat_and_compile("{")
        while self.__tokenizer.get_curr_token() in CLASS_VAR_DEC_OPENER:
            self.compile_class_var_dec()
        while self.__tokenizer.get_curr_token() in SUBROUTINE_DEC_OPENER:
            self.compile_subroutine_dec()
        self.__eat_and_compile("}")

    def compile_class_var_dec(self):
        """
        Compiles a static variable declaration, or a field declaration.
        """
        identifier_kind = None
        for opener in CLASS_VAR_DEC_OPENER:
            if self.__tokenizer.get_curr_token() == opener:
                identifier_kind = opener
                self.__eat_and_compile(opener)
                break
        identifier_type = self.__tokenizer.get_curr_token()
        self.__compile_name(id_kind="class")
        self.__compile_identifier(self.__tokenizer.get_curr_token(), True,
                                  identifier_kind, identifier_type)
        while self.__tokenizer.get_curr_token() == ",":
            self.__eat_and_compile(",")
            self.__compile_identifier(self.__tokenizer.get_curr_token(), True,
                                      identifier_kind, identifier_type)
        self.__eat_and_compile(";")

    def compile_subroutine_dec(self):
        """
        Compiles a complete method' function' or constructor.
        """
        self.__symbol_table.start_subroutine()
        is_void = False
        if self.__tokenizer.get_curr_token() == "constructor":
                self.__eat_and_compile("constructor")
                self.__compile_name(id_kind="class")
                constructor_name = self.__compile_subroutine_dec_line()
                self.__compile_constructor_body(constructor_name)
        elif self.__tokenizer.get_curr_token() == "function":
                self.__eat_and_compile("function")
                if self.__tokenizer.get_curr_token() == "void":
                    is_void = True
                self.__compile_name(id_kind="class")
                function_name = self.__compile_subroutine_dec_line()
                self.__compile_function_body(function_name, is_void)
        elif self.__tokenizer.get_curr_token() == "method":
                self.__eat_and_compile("method")
                if self.__tokenizer.get_curr_token() == "void":
                    is_void = True
                self.__compile_name(id_kind="class")
                self.__symbol_table.define("this", self.__class_name,
                                           SymbolKinds.ARG)
                method_name = self.__compile_subroutine_dec_line()
                self.__compile_method_body(method_name, is_void)

    def __compile_subroutine_dec_line(self):

        subroutine_name = self.__tokenizer.get_curr_token()
        self.__compile_name(id_kind="subroutine", is_defined=True)

        self.__eat_and_compile("(")
        self.compile_parameter_list()
        self.__eat_and_compile(")")
        return subroutine_name

    def compile_parameter_list(self):
        """
        Compiles a (possibly empty) parameter list. Does not handle the
        enclosing "()"
        """
        if self.__tokenizer.get_curr_token() != ")":
            id_type = self.__tokenizer.get_curr_token()
            self.__compile_name(id_kind="class")
            self.__compile_name(id_kind="argument", is_defined=True,
                                id_type=id_type)

            while self.__tokenizer.get_curr_token() == ",":
                self.__eat_and_compile(",")
                id_type = self.__tokenizer.get_curr_token()
                self.__compile_name(id_kind="class")
                self.__compile_name(id_kind="argument", is_defined=True,
                                    id_type=id_type)

    def __compile_function_body(self, function_name, is_void):
        full_name = self.__class_name + "." + function_name

        self.__eat_and_compile("{")
        while self.__tokenizer.get_curr_token() == "var":
            self.compile_var_dec()
        self.__vm_writer.write_function(full_name,
                                        self.__symbol_table.var_count(
                                            SymbolKinds.VAR))
        self.compile_statements(is_void)
        self.__eat_and_compile("}")

    def __compile_method_body(self, method_name, is_void):
        full_name = self.__class_name + "." + method_name
        self.__eat_and_compile("{")
        while self.__tokenizer.get_curr_token() == "var":
            self.compile_var_dec()
        self.__vm_writer.write_function(full_name,
                                        self.__symbol_table.var_count(
                                            SymbolKinds.VAR))
        self.__vm_writer.write_push("argument", 0)
        self.__vm_writer.write_pop("pointer", 0)
        self.compile_statements(is_void)
        self.__eat_and_compile("}")

    def __compile_constructor_body(self, constructor_name):
        """
        Compiles a subroutine's body.
        """
        full_name = self.__class_name + "." + constructor_name
        self.__eat_and_compile("{")
        while self.__tokenizer.get_curr_token() == "var":
            self.compile_var_dec()
        self.__vm_writer.write_function(full_name,
                                        self.__symbol_table.var_count(
                                            SymbolKinds.VAR))
        self.__vm_writer.write_push("constant",
                                    self.__symbol_table.var_count(
                                        SymbolKinds.FIELD))
        self.__vm_writer.write_call("Memory.alloc", 1)
        self.__vm_writer.write_pop("pointer", 0)
        self.compile_statements(False)
        self.__eat_and_compile("}")

    def compile_var_dec(self):
        """
        Compiles a var declaration.
        """
        self.__eat_and_compile("var")
        id_type = self.__tokenizer.get_curr_token()
        self.__compile_name(id_kind="class")
        self.__compile_name(id_kind="local", is_defined=True, id_type=id_type)
        while self.__tokenizer.get_curr_token() == ",":
            self.__eat_and_compile(",")
            self.__compile_name(id_kind="local", is_defined=True,
                                id_type=id_type)
        self.__eat_and_compile(";")

    def compile_statements(self, is_void):
        """
        Compiles a sequence of statements. Does not handle the
        enclosing "{}"
        """
        while self.__tokenizer.get_curr_token() != "}":
            if self.__tokenizer.get_curr_token() == "let":
                self.compile_let()
            elif self.__tokenizer.get_curr_token() == "if":
                self.compile_if(is_void)
            elif self.__tokenizer.get_curr_token() == "while":
                self.compile_while(is_void)
            elif self.__tokenizer.get_curr_token() == "do":
                self.compile_do()
            elif self.__tokenizer.get_curr_token() == "return":
                self.compile_return(is_void)
            else:
                print("Compilation Error!")

    def compile_let(self):
        """
        Compiles a let statement
        """
        self.__eat_and_compile("let")
        var_name = self.__tokenizer.get_curr_token()
        if self.__tokenizer.peek() == "[":
            self.__compile_array_assignment()
        else:
            self.__compile_name(id_kind=KINDS_TO_STR[
                                self.__symbol_table.kind_of(var_name)],
                                id_type=self.__symbol_table.type_of(var_name))
            self.__eat_and_compile("=")
            self.compile_expression()
            segment = KINDS_TO_STR[self.__symbol_table.kind_of(var_name)]
            index = self.__symbol_table.index_of(var_name)
            self.__vm_writer.write_pop(segment, index)
        self.__eat_and_compile(";")

    def compile_if(self, is_void):
        """
        Compiles an if statement, possibly with a trailing else statement.
        """
        self.__label_counter += 1
        self.__eat_and_compile("if")
        self.__eat_and_compile("(")
        self.compile_expression()
        self.__vm_writer.write_arithmetic("not")
        self.__eat_and_compile(")")
        self.__eat_and_compile("{")
        elseLabel = "ELSE_" + str(self.__label_counter)
        endLabel = "END_IF_" + str(self.__label_counter)
        self.__vm_writer.write_if(elseLabel)
        self.compile_statements(is_void)
        self.__vm_writer.write_goto(endLabel)
        self.__eat_and_compile("}")
        if self.__tokenizer.get_curr_token() == "else":
            self.__eat_and_compile("else")
            self.__eat_and_compile("{")
            self.__vm_writer.write_label(elseLabel)
            self.compile_statements(is_void)
            self.__eat_and_compile("}")
        else:
            self.__vm_writer.write_label(elseLabel)
        self.__vm_writer.write_label(endLabel)

    def compile_while(self, is_void):
        """
        Compiles a while statement
        """
        self.__label_counter += 1
        while_exp = "WHILE_EXPRESSION_" + str(self.__label_counter)
        end_while_loop = "END_WHILE_LOOP_" + str(self.__label_counter)
        self.__vm_writer.write_label(while_exp)
        self.__eat_and_compile("while")
        self.__eat_and_compile("(")
        self.compile_expression()
        self.__vm_writer.write_arithmetic("not")
        self.__eat_and_compile(")")
        self.__eat_and_compile("{")
        self.__vm_writer.write_if(end_while_loop)
        self.compile_statements(is_void)
        self.__vm_writer.write_goto(while_exp)
        self.__eat_and_compile("}")
        self.__vm_writer.write_label(end_while_loop)

    def compile_do(self):
        """
        Compiles a do statement.
        """
        self.__eat_and_compile("do")
        self.__compile_subroutine_call()
        self.__vm_writer.write_pop("temp", 0)
        self.__eat_and_compile(";")

    def compile_return(self, is_void):
        """
        Compiles a return statement.
        """
        self.__eat_and_compile("return")
        if self.__tokenizer.get_curr_token() != ";":
            self.compile_expression()
        self.__eat_and_compile(";")
        if is_void:
            self.__vm_writer.write_push("constant", 0)
        self.__vm_writer.write_return()

    def compile_expression(self):
        """
        Compiles an expression.
        """
        self.compile_term()
        while self.__tokenizer.get_curr_token() in BINARY_OP:
            binary_op = BINARY_OP[self.__tokenizer.get_curr_token()]
            self.__compile_name()
            self.compile_term()
            self.__vm_writer.write_arithmetic(binary_op)

    def compile_term(self):
        """
        Compiles a term. If the current token is an IDENTIFIER, the routine
        must distinguish between a variable an array entry or a subroutine
        call.
        A single look-ahead token, which may be one of "[", "(", or ".",
        suffices to distinguish between the possibilities. Any other token
        is not part of this term, and should not be advanced over.
        """
        token = self.__tokenizer.get_curr_token()
        if self.__tokenizer.token_type() == TokenType.STRING_CONST:
            self.__vm_writer.write_push("constant", len(token))
            self.__vm_writer.write_call("String.new", 1)
            for char in token:
                self.__vm_writer.write_push("constant", ord(char))
                self.__vm_writer.write_call("String.appendChar", 2)
            self.__compile_name()
        elif self.__tokenizer.token_type() == TokenType.KEYWORD:
            if token == "true":
                self.__vm_writer.write_push("constant", 1)
                self.__vm_writer.write_arithmetic("neg")
            elif token == "false" or token == "null":
                self.__vm_writer.write_push("constant", 0)
            elif token == "this":
                self.__vm_writer.write_push("pointer", 0)
            self.__compile_name()
        elif self.__tokenizer.token_type() == TokenType.INT_CONST:
            self.__vm_writer.write_push("constant", token)
            self.__compile_name()
        elif self.__tokenizer.token_type() == TokenType.SYMBOL:
            if self.__tokenizer.get_curr_token() == "(":
                self.__eat_and_compile("(")
                self.compile_expression()
                self.__eat_and_compile(")")
            else:  # term == unaryOp term
                unary_op = UNARY_OP[token]
                self.__compile_name()
                self.compile_term()
                self.__vm_writer.write_arithmetic(unary_op)
        elif self.__tokenizer.token_type() == TokenType.IDENTIFIER:
            if self.__tokenizer.peek() in [".", "("]:
                self.__compile_subroutine_call()
            elif self.__tokenizer.peek() == "[":
                self.__compile_array_expression()
            else:
                self.__eat_and_compile(self.__tokenizer.get_curr_token())
                segment = KINDS_TO_STR[self.__symbol_table.kind_of(token)]
                index = self.__symbol_table.index_of(token)
                self.__vm_writer.write_push(segment, index)

    def compile_expression_list(self):

        """
        Compiles a (possibly empty) comma-separated list of expressions.
        """
        num_of_expressions = 0
        if self.__tokenizer.get_curr_token() != ")" or (
                self.__tokenizer.get_curr_token() == ")" and
                    self.__tokenizer.token_type() == TokenType.STRING_CONST):
            self.compile_expression()
            num_of_expressions += 1
            while self.__tokenizer.get_curr_token() == ",":
                self.__eat_and_compile(",")
                self.compile_expression()
                num_of_expressions += 1
        return num_of_expressions

    def __compile_subroutine_call(self):
        token = self.__tokenizer.get_curr_token()
        if self.__symbol_table.kind_of(token):
            segment = KINDS_TO_STR[self.__symbol_table.kind_of(token)]
            index = self.__symbol_table.index_of(token)
            self.__vm_writer.write_push(segment, index)
            self.__compile_name(KINDS_TO_STR[self.__symbol_table.kind_of(
                token)], False, self.__symbol_table.type_of(token))
            self.__eat_and_compile(".")
            type = self.__symbol_table.type_of(token)
            subroutine_name = type + "." + self.__tokenizer.get_curr_token()
            self.__compile_name(id_kind="subroutine")
            self.__eat_and_compile("(")
            num_of_arguments = self.compile_expression_list() + 1
            self.__eat_and_compile(")")
        else:
            subroutine_name = token
            self.__compile_name(id_kind="classOrSubroutine")
            num_of_arguments = 0
            if self.__tokenizer.get_curr_token() == ".":
                self.__eat_and_compile(".")
                subroutine_name += "." + self.__tokenizer.get_curr_token()
                self.__compile_name(id_kind="subroutine")
            else:
                subroutine_name = self.__class_name + "." + subroutine_name
                self.__vm_writer.write_push("pointer", 0)
                num_of_arguments = 1
            self.__eat_and_compile("(")
            num_of_arguments += self.compile_expression_list()
            self.__eat_and_compile(")")
        self.__vm_writer.write_call(subroutine_name, num_of_arguments)

    def __compile_array_assignment(self):
        array_name = self.__tokenizer.get_curr_token()
        segment = KINDS_TO_STR[self.__symbol_table.kind_of(array_name)]
        index = self.__symbol_table.index_of(array_name)
        self.__compile_name()
        self.__eat_and_compile("[")
        self.compile_expression()
        self.__eat_and_compile("]")
        self.__vm_writer.write_push(segment, index)
        self.__vm_writer.write_arithmetic("add")
        self.__eat_and_compile("=")
        self.compile_expression()
        self.__vm_writer.write_pop("temp", 0)
        self.__vm_writer.write_pop("pointer", 1)
        self.__vm_writer.write_push("temp", 0)
        self.__vm_writer.write_pop("that", 0)

    def __compile_array_expression(self):
        array_name = self.__tokenizer.get_curr_token()
        segment = KINDS_TO_STR[self.__symbol_table.kind_of(array_name)]
        index = self.__symbol_table.index_of(array_name)
        self.__compile_name()
        self.__eat_and_compile("[")
        self.compile_expression()
        self.__eat_and_compile("]")
        self.__vm_writer.write_push(segment, index)
        self.__vm_writer.write_arithmetic("add")
        self.__vm_writer.write_pop("pointer", 1)
        self.__vm_writer.write_push("that", 0)



