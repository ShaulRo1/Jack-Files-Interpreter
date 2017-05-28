#################################################
# FILE : jack_tokenizer.py                       #
# WRITERS : Robinov Shaul, shaul_ro, 309673184   #
#           Roi Shaag, roi351, 204056915         #
# EXERCISE : Nand2Tetris ex10 2016-2017          #
# DESCRIPTION : Jack programs Tokenizer          #
##################################################

import re
import os
import sys
from enum import Enum


NUMBER_REGEX = "^\d+$"
STRING_REGEX = "^\".*\"$"  # The string regex accepts empty string
IDENTIFIER_REGEX = "^[_A-Za-z][_a-zA-Z0-9]*$"
COMMENT_REGEX = "//.*"

EMPTY_STRING = ""
KEYWORDS_ARR = ["class", "constructor", "function", "method", "field",
                "static", "var", "int", "char", "boolean", "void", "true",
                "false", "null", "this", "let", "do", "if", "else", "while",
                "return"]

SYMBOLS_ARR = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*",
               "/", "&", "|", "<", ">", "=", "~"]

SKIP_SPACES = ["\n", "\r", "\t"]


class TokenType(Enum):
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5


class JackTokenizer:
    def __init__(self, file_name):
        self.__file = open(file_name)
        self.__cur_char = ""
        self.__next_char = self.__file.read(1)
        self.__get_next_char()
        self.__cur_token_type = ""
        self.__cur_token = ""

    def has_more_tokens(self):
        """
        :return: true iff the file has more tokens
        """
        if self.__cur_char != "":
            return True
        return False

    def __get_next_char(self):
        """
        This method gets the next char from the file, skipping \n \r and \t,
        and updates the cur_char and next_char accordingly.
        """
        self.__cur_char = self.__next_char
        if self.__next_char == "":
            return
        self.__next_char = self.__file.read(1)


    def __skip_comments(self):
        """
        This method advances the cur_char to the end of a comment.
        """
        if self.__cur_char == "/" and self.__next_char == "/":
            self.__skip_one_line_comment()
            if self.__cur_char == "\n":
                self.__get_next_char()
        elif self.__cur_char == "/" and self.__next_char == "*":
            self.__skip_multi_line_comment()
            self.__get_next_char()
            return
        else:
            return
        if self.__cur_char == "/":
            self.__skip_comments()

    def __skip_one_line_comment(self):
        """
        This method advances the cur_char to the end of a singe line comment.
        i.e a comment of the type '//'
        """
        while self.__cur_char != "\n" and self.__cur_char != "":
            self.__get_next_char()
        self.__get_next_char()

    def __skip_multi_line_comment(self):
        """
        This method advances the cur_char to the end of a multi line comment.
        i.e a comment of the type '/*' or '/**'
        """
        self.__get_next_char()
        self.__get_next_char()
        while not (self.__cur_char == "*" and self.__next_char == "/")\
                and self.__cur_char != "":
            self.__get_next_char()
        self.__get_next_char()

    def get_curr_token(self):
        """
        :return: the last token read from the file
        """
        return self.__cur_token

    def token_type(self):
        """
        :return: the type of the current token.
        """
        return self.__cur_token_type

    def keyword(self):
        """
        :return: the keyword which is the current token.
        """
        # Should be called only when tokenType() is KEYWORD.
        if self.__cur_token_type == TokenType.KEYWORD:
            return self.__cur_token
        return "Error, current token is not of KEYWORD type."

    def symbol(self):
        """
        :return: the character which is the current token.
        """
        # Should be called only when tokenType() is SYMBOL.
        if self.__cur_token_type == TokenType.SYMBOL:
            return self.__cur_token
        return "Error, current token is not of SYMBOL type."

    def identifier(self):
        """
        :return: the identifier which is the current token.
        """
        # Should be called only when tokenType() is IDENTIFIER
        if self.__cur_token_type == TokenType.IDENTIFIER:
            return self.__cur_token
        return "Error, current token is not of IDENTIFIER type."

    def int_val(self):
        """
        :return: the integer value of the current token.
        """
        # Should be called only when tokenType() is INT_CONST
        if self.__cur_token_type == TokenType.INT_CONST:
            return self.__cur_token
        return "Error, current token is not of INT_CONST type."

    def string_val(self):
        """
        :return: the string value of the current token, without the double
                 quotes.
        """
        # Should be called only when tokenType() is STRING_CONST.
        if self.__cur_token_type == TokenType.STRING_CONST:
            return self.__cur_token
        return "Error, current token is not of STRING_CONST type."

    def __handle_string_token(self):
        """
        This method updates the current token to be the string in the
        parenthesis.
        """
        self.__cur_token = ""
        self.__get_next_char()
        while self.__cur_char != "\"":
            self.__cur_token += self.__cur_char
            self.__get_next_char()
        self.__cur_token_type = TokenType.STRING_CONST
        self.__get_next_char()

    def __update_cur_token(self, token_type):
        """
        :param cur_token:
        :param token_type:
        :return:
        """
        self.__cur_token_type = token_type
        self.__get_next_char()

    def advance(self):
        self.__cur_token = ""
        while self.__cur_char != "":
            self.__skip_comments()
            if self.__cur_char == "\"":
                self.__handle_string_token()
                return
            elif self.__cur_token in KEYWORDS_ARR and \
                    (self.__cur_char in SKIP_SPACES or
                     self.__cur_char == " "):
                self.__update_cur_token(TokenType.KEYWORD)
                return
            elif self.__cur_token in KEYWORDS_ARR and self.__cur_char in \
                    SYMBOLS_ARR:
                self.__cur_token_type = TokenType.KEYWORD
                return
            elif self.__cur_token in SYMBOLS_ARR:
                self.__update_cur_token(TokenType.SYMBOL)
                return
            elif (self.__cur_char in SYMBOLS_ARR or
                          self.__cur_char == " ") and self.__cur_token != "":
                self.__handle_int_or_identifier_token()
                return
            elif self.__cur_char in SYMBOLS_ARR:
                self.__cur_token = self.__cur_char
                self.__update_cur_token(TokenType.SYMBOL)
                return
            else:
                self.__cur_token += self.__cur_char.strip()
                self.__get_next_char()

    def __handle_int_or_identifier_token(self):
        """
        :param new_token:
        :return:
        """
        if re.match(IDENTIFIER_REGEX, self.__cur_token):
            self.__cur_token_type = TokenType.IDENTIFIER
            return
        elif re.match(NUMBER_REGEX, self.__cur_token):
            self.__cur_token_type = TokenType.INT_CONST
            return
        else:
            print("Error handling token, called int or identifier"
                  "but its neither")

    def peek(self):
        return self.__cur_char