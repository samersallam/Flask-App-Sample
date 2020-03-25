import re
from copy import deepcopy
from abc import  ABCMeta, abstractmethod
from .utilities import FunctionArgsAssertion


class ArgumentTypeValidator:
    """ To check the argument type """

    @staticmethod
    def has_type(arg_val, req_type):
        FunctionArgsAssertion.assert_type(req_type)
        return True if type(arg_val) is req_type else False


class IterableArgumentValidator:
    """ This class has some useful function for Iterable arguments """

    @staticmethod
    def in_collection(arg_val, req_collection):
        """ Check if an element is inside a collection """
        FunctionArgsAssertion.assert_iterable(req_collection)
        return True if arg_val in req_collection else False

    @staticmethod
    def has_length(arg_val, req_length_range):
        """ Make sure the collection length is within the selected range """
        FunctionArgsAssertion.assert_iterable(arg_val)
        FunctionArgsAssertion.assert_range(req_length_range)

        if req_length_range[0] < 0 or req_length_range[1] < 0:
            raise Exception('Both numbers in the req_range should be positive')

        col_len = len(arg_val)
        return True if col_len >= req_length_range[0] and col_len <= req_length_range[1] else False


class Argument(metaclass=ABCMeta):
    """ An abstract class to represent the argument """

    def __init__(self, name, required, arg_type):
        self.name = name
        self.required = required
        self.arg_type = arg_type
        self.functions_list = None
        self.invalid = False
        self.missing = False
        self.report = ''

    def update_name(self, name):
        self.name = name

    def set_invalid_arg(self):
        self.invalid = True

    def set_missing_arg(self):
        self.missing = True

    def update_report(self, new_info):
        self.set_invalid_arg()
        self.report += new_info + '\n'

    @abstractmethod
    def assert_arg(self, args_dict):
        """ Compulsory check of existence and the data type """
        self.reset_arg()
        if not self.assert_existence(args_dict):
            return

        arg_val = args_dict[self.name]

        if not self.assert_type(arg_val):
            return

        return args_dict[self.name]  # The argument value

    def reset_arg(self):
        self.invalid = False
        self.missing = False
        self.report = ''

    def assert_existence(self, args_dict):
        """ Check if the argument is available or not """
        arg_available = IterableArgumentValidator.in_collection(self.name, args_dict)

        if not arg_available and self.required:
            self.set_missing_arg()
            self.update_report('{} is missing'.format(self.name))

        return arg_available

    def assert_type(self, arg_val):
        """ Check the argument type """
        type_status = ArgumentTypeValidator.has_type(arg_val, self.arg_type)

        if not type_status:
            current_type = type(arg_val)
            self.update_report('{} data type is {} but it should be {}'.format(
                self.name, current_type.__name__, self.arg_type.__name__))

        return type_status

    def assert_req_options(self, arg_val):
        """ Check if the argument value belongs to the required options """
        if type(self) not in [NumberArgument, StringArgument]:
            raise Exception('Valid only for NumberArgument and StringArgument types')

        if self.req_options and not IterableArgumentValidator.in_collection(arg_val, self.req_options):
            self.update_report('{} should be one of the following options {} but the passed value is {}'.format(
                self.name, self.req_options, arg_val))
            return False
        return True

    def assert_length(self, arg_val):
        """ Check if the argument length is within the allowed range """
        if type(self) not in [ListArgument, StringArgument]:
            raise Exception('Valid only for ListArgument and StringArgument types')

        if self.length_range and not NumberArgument.in_range(len(arg_val), self.length_range):
            self.update_report('{} length should be in the range {} but the current length is {}'.format(
                self.name, self.length_range, len(arg_val)))
            return False
        return True

    def assert_functions_list(self, arg_val):
        """ Useful to check other functions that are not implemented in this class """
        if not self.functions_list:
            return

        for func in self.functions_list:
            if not func(arg_val):
                self.update_report('{} should satisfy {} but the passed value is {}'.format(
                    self.name, func.__name__, arg_val))

    def __repr__(self):
        if self.invalid:
            return f'The argument is invalid\nReport:\n{self.report}'
        else:
            return 'The argument is valid'


class NumberArgument(Argument):
    """ A class to represent the number argument which could be int or float """

    def __init__(self, name, required, arg_type, req_range=None, req_options=None,
                 comparison_operator=None, functions_list=None):
        FunctionArgsAssertion.assert_number_type(arg_type)
        super().__init__(name, required, arg_type)
        self.req_range = req_range
        self.req_options = req_options
        self.comparison_operator = comparison_operator
        self.functions_list = functions_list

    def assert_arg(self, args_dict):
        arg_val = super().assert_arg(args_dict)

        if arg_val is None:
            return

        self.assert_req_range(arg_val)
        self.assert_req_options(arg_val)
        self.assert_comparison(arg_val)
        self.assert_functions_list(arg_val)

    def assert_req_range(self, arg_val):
        """ To check if the argument value in the required range """
        if self.req_range and not NumberArgument.in_range(arg_val, self.req_range):
            self.update_report('{} should be in the range {} but the passed value is : {}'.format(
                self.name, self.req_range, arg_val))
            return False
        return True

    def assert_comparison(self, arg_val):
        """ To check if the argument value satisfies the comparison operator """
        if self.comparison_operator and not self.comparison_operator.compare(arg_val):
            self.update_report('{} should be {} {} but the passed value is : {}'.format(
                self.name, self.comparison_operator.operator_name.replace('_', ' '),
                self.comparison_operator.operand, arg_val))
            return False
        return True

    @staticmethod
    def in_range(arg_val, req_range):
        FunctionArgsAssertion.assert_range(req_range)
        return True if arg_val >= req_range[0] and arg_val <= req_range[-1] else False


class StringArgument(Argument):
    """ A class to represent the string argument type """
    email_regex_pattern = '(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[' \
                          '\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[' \
                          'a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][' \
                          '0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[' \
                          'a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[' \
                          '\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'

    password_regex_pattern = '^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})'

    date_regex_pattern = '^\d{1,2}\/\d{1,2}\/\d{4}$'

    def __init__(self, name, required, is_email=False, is_date=False, is_password=False,
                 req_options=None, length_range=None, regex_pattern=None, functions_list=None):

        if (is_email + is_date + is_password) > 1:
            raise Exception('Only one of is_email, is_date, is_password could be True at a time')

        super().__init__(name, required, str)

        self.req_options = req_options
        self.length_range = length_range
        self.is_email = is_email
        self.is_date = is_date
        self.is_password = is_password
        self.regex_pattern = regex_pattern
        self.functions_list = functions_list

    def assert_arg(self, args_dict):
        arg_val = super().assert_arg(args_dict)

        if arg_val is None:
            return

        self.assert_req_options(arg_val)
        self.assert_length(arg_val)
        self.assert_email(arg_val)
        self.assert_password(arg_val)
        self.assert_date(arg_val)
        self.assert_regex_pattern(arg_val)
        self.assert_white_spaces(arg_val)
        self.assert_functions_list(arg_val)

    def assert_email(self, arg_val):
        """ To check if argument match the email pattern """
        if self.is_email and not StringArgument.is_email_func(arg_val):
            self.update_report('{} is not a valid email address'.format(self.name))
            return False
        return True

    @classmethod
    def is_email_func(cls, arg_val):
        """ To check if argument match the email pattern """
        return cls.match_pattern(arg_val, cls.email_regex_pattern)

    @classmethod
    def update_email_regex_pattern(cls, new_pattern):
        cls.email_regex_pattern = new_pattern

    def assert_password(self, arg_val):
        """ To check if argument match the password pattern """
        if self.is_password and not StringArgument.is_password_func(arg_val):
            self.update_report('{} is not a valid password'.format(self.name))
            return False
        return True

    @classmethod
    def is_password_func(cls, arg_val):
        """
        To check if argument match the password pattern
        The default pattern:
        ^	The password string will start this way
        (?=.*[a-z])	The string must contain at least 1 lowercase alphabetical character
        (?=.*[A-Z])	The string must contain at least 1 uppercase alphabetical character
        (?=.*[0-9])	The string must contain at least 1 numeric character
        (?=.*[!@#$%^&*])	The string must contain at least one special character, but we are escaping reserved RegEx characters to avoid conflict
        (?=.{8,})	The string must be eight characters or longer
        """
        return cls.match_pattern(arg_val, cls.password_regex_pattern)

    @classmethod
    def update_password_regex_pattern(cls, new_pattern):
        cls.password_regex_pattern = new_pattern

    def assert_date(self, arg_val):
        """ To check if argument match the date pattern """
        if self.is_date and not StringArgument.is_date_func(arg_val):
            self.update_report('{} is not a valid date'.format(self.name))
            return False
        return True

    @classmethod
    def is_date_func(cls, arg_val):
        """
        To check if argument match the date pattern
        The default pattern matches 4/1/2001 | 12/12/2001 | 55/5/3434
        """
        return cls.match_pattern(arg_val, cls.date_regex_pattern)

    @classmethod
    def update_date_regex_pattern(cls, new_pattern):
        cls.date_regex_pattern = new_pattern

    def assert_regex_pattern(self, arg_val):
        """ To check if argument match the passed regex pattern """
        if self.regex_pattern and not StringArgument.match_pattern(arg_val, self.regex_pattern):
            self.update_report('{} should match the pattern {}'.format(self.name, self.regex_pattern))
            return False
        return True

    @staticmethod
    def match_pattern(arg_val, pattern):
        """ To check if argument match the passed regex pattern """
        status = re.match(pattern, arg_val)
        if status:
            return True
        return False

    def assert_white_spaces(self, arg_val):
        """ To check that not all characters in the argument are white spaces """
        if arg_val.isspace():
            self.update_report('{} should not have only white spaces'.format(self.name))
            return False
        return True


class ListArgument(Argument):
    def __init__(self, name, required, arg_obj, length_range=None):
        super().__init__(name, required, list)
        self.length_range = length_range
        self.arg_obj = arg_obj

    def assert_arg(self, args_dict):
        arg_val = super().assert_arg(args_dict)

        if self.invalid:
            return

        if not self.assert_length(arg_val):
            return

            # Convert list into dict to fit assert_arg function
        items_dict = {'{}[{}]'.format(self.name, ind): item for ind, item in enumerate(arg_val)}

        for ind in items_dict:
            arg_obj = deepcopy(self.arg_obj)
            arg_obj.update_name(ind)
            arg_obj.assert_arg(items_dict)

            if arg_obj.invalid:
                self.update_report(arg_obj.report)
