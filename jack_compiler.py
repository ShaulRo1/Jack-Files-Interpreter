import os
import sys
from compilation_engine import *

##############################################################################
# FILE : jack_compiler.py                                                    #
# EXERCISE : nand2tetris project10 2016-2017                                 #
# DESCRIPTION : A program that analyzing jack programs, parse them and       #
#               understands their structure. convert them to XML tree        #
#               representation                                               #
##############################################################################


NUMBER_OF_ARGUMENTS = 2


def compile_one_file(file_name):
    """

    :param file_name:
    :return:
    """
    tokenizer = JackTokenizer(file_name)
    output_file_name = file_name[:file_name.find('.')]+".vm"
    output_file = open(output_file_name, 'w')
    compilation_engine = CompilationEngine(file_name, output_file, tokenizer)
    compilation_engine.compile_class()


def main(input_path):
    """ The main function"""
    if os.path.isfile(input_path):  # it is a file- execute once
        compile_one_file(input_path)
    # it is a directory- execute analyze for each '.jack' file in it
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith(".jack"):
                compile_one_file(input_path + os.sep + filename)


if __name__ == '__main__':
    if len(sys.argv) == NUMBER_OF_ARGUMENTS:
        main(sys.argv[1])
    else:
        print("WRONG NUMBER OF ARGUMENTS!\nUSAGE: jack_compiler.py <path>")
