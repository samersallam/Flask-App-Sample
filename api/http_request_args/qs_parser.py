from flask import request


class QueryStringParser:
    """ A class to parse the query string arguments and make a report about parsing problems if any  happens """

    def __init__(self, models):
        self.models = models
        self.parsed_args = dict()
        self.passed_args = None
        self.extra_args = None
        self.report = 'Would you please check the query string arguments where: \n'
        self.invalid = False

    def set_invalid(self):
        self.invalid = True

    def parse_args(self):
        """ Parse the query string """

        # Try to parse
        for model in self.models:
            try:
                model_args = model.parse_args()
                self.parsed_args.update(model_args)
            except:
                self.set_invalid()
                break

        self.get_parsing_report()

    def get_parsing_report(self):

        if not self.invalid:
            # Check if there are any extra args
            extra_args = self.get_extra_request_args(self.parsed_args)
            if len(extra_args) == 0:
                return

        self.set_invalid()
        accepted_args = self.get_request_args(QueryStringParser.get_accepted_model_args)
        required_args = self.get_request_args(QueryStringParser.get_required_model_args)
        optional_args = self.get_request_args(QueryStringParser.get_optional_model_args)
        missing_args = self.get_request_args(QueryStringParser.get_missing_model_args,
                                             passed_args=self.get_passed_request_args())

        self.update_parsing_report('accepted', accepted_args)
        self.update_parsing_report('required', required_args)
        self.update_parsing_report('optional', optional_args)
        self.update_parsing_report('missing', missing_args)

    def update_parsing_report(self, name, args):

        args = [arg for arg_set in args for arg in arg_set]
        if len(args):
            self.report += 'The following arguments are {} {} \n'.format(name, args)
        else:
            self.report += 'No arguments are {} \n'.format(name)

    def get_extra_request_args(self, parsed_args):
        if self.extra_args is None:
            passed_args = self.get_passed_request_args()
            self.extra_args = list(set(passed_args) - set(parsed_args))
        return self.extra_args

    def get_passed_request_args(self):
        if self.passed_args is None:
            self.passed_args = request.args.to_dict()
        return self.passed_args

    def get_request_args(self, request_args_func, **func_args):
        for model in self.models:
            func_args['model'] = model
            yield request_args_func(**func_args)

    @staticmethod
    def get_accepted_model_args(model):
        for arg in model.args:
            arg_type = arg.type.__name__
            arg_type = arg_type if arg.action != 'append' else 'list of {}'.format(arg_type)
            yield {arg.name: arg_type}

    @staticmethod
    def get_missing_model_args(model, passed_args):
        for arg in model.args:
            if arg.required and arg.name not in passed_args:
                yield arg.name

    @staticmethod
    def get_required_model_args(model):
        for arg in model.args:
            if arg.required:
                yield arg.name

    @staticmethod
    def get_optional_model_args(model):
        for arg in model.args:
            if not arg.required:
                yield arg.name