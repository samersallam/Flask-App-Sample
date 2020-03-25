from flask_restplus import reqparse
from .status import ArgumentsStatus
from .qs_parser import QueryStringParser
from .argument import ListArgument


class RequestArgsValidator:
    """ A class responsible for query string and body arguments validation """
    def __init__(self, qs_args_def=list(), body_args_def=list(), body_args=dict()):
        self.qs_args_def = qs_args_def
        self.body_args_def = body_args_def
        self.qs_args = None
        self.body_args = body_args
        self.report = ''
        self.invalid = False

    def update_report(self, msg_ifo):
        self.set_invalid_validation()
        self.report += '{} \n'.format(msg_ifo)

    def set_invalid_validation(self):
        self.invalid = True

    @staticmethod
    def args_def_to_parser(args_def):
        """ Convert list of arguments to Flask request parser """
        args_parser = reqparse.RequestParser()
        for arg in args_def:
            arg_attr = {
                'required': arg.required,
            }

            if isinstance(arg, ListArgument):
                arg_attr['type'] = arg.arg_obj.arg_type
                arg_attr['action'] = 'append'
            else:
                arg_attr['type'] = arg.arg_type
            args_parser.add_argument(arg.name, **arg_attr)

        return args_parser

    def validate(self):
        # 1- Check the query string
        if len(self.qs_args_def):
            # Check if parsing is possible
            qs_args_model = self.args_def_to_parser(self.qs_args_def)
            qs_parser = QueryStringParser([qs_args_model])
            qs_parser.parse_args()

            if qs_parser.invalid:
                self.update_report(qs_parser.report)
            else:
                # Check that all args satisfy the conditions
                self.qs_args = qs_parser.parsed_args
                qs_status = ArgumentsStatus('Query String', self.qs_args_def, self.qs_args)
                qs_status.assert_args()
                if qs_status.invalid_args:
                    self.update_report(qs_status.report)

        # 2- Check the body args
        if len(self.body_args_def):
            body_status = ArgumentsStatus('Body', self.body_args_def, self.body_args)
            body_status.assert_args()

            if body_status.invalid_args:
                self.update_report(body_status.report)