##############################################################################
# FILE : vm_writer.py                                                        #
# WRITER : Roi_Shaag , roi351 , 20405691                                     #
#          Robinov Shaul, shaul_ro, 309673184                                #
# EXERCISE : nand2tetris project10 2016-2017                                 #
# DESCRIPTION : A program that contains a class definition of VmWriter,      #
#               that represents a module that encapsulates the VM command    #
#               syntax                                                       #
##############################################################################


class VmWriter:
    """
    Emits VM commands into a file, encapsulating the VM command syntax.
    """
    def __init__(self, output_file):
        """
        Creates a new file and prepares it for writing
        """
        self.__out = output_file

    def write_arithmetic(self, command):
        """
        Writes a VM arithmetic command
        :param command:
        """
        self.__out.write(command + "\n")

    def write_push(self, segment, index):
        """
        Writes a VM pop command.
        :param segment: the name of the memory segment
        :param index:
        """
        self.__out.write("push " + segment + " " + str(index) + "\n")

    def write_pop(self, segment, index):
        """
        Writes a VM push command.
        :param segment: the name of the memory segment
        :param index:
        """
        self.__out.write("pop " + segment + " " + str(index) + "\n")

    def write_label(self, label):
        """
        Writes a VM label command.
        :param label:
        """
        self.__out.write("label " + label + "\n")

    def write_goto(self, label):
        """
        Writes a VM goto command.
        :param label:
        """
        self.__out.write("goto " + label + "\n")

    def write_if(self, label):
        """
        Writes a VM if-goto command.
        :param label:
        """
        self.__out.write("if-goto " + label + "\n")

    def write_call(self, name, n_args):
        """
        Writes a VM call command.
        :param name:
        :param n_args:
        """
        self.__out.write("call " + name + " " + str(n_args) + "\n")

    def write_function(self, name, n_locals):
        """
        Writes a VM function command.
        :param name:
        :param n_locals:
        """
        self.__out.write("function " + name + " " + str(n_locals) + "\n")

    def write_return(self):
        """
        Writes a VM return command.
        """
        self.__out.write("return\n")

    def close_output_file(self):
        """
        Closes the output file
        """
        self.__out.close()






