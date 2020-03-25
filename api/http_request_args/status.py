from .argument import  IterableArgumentValidator


class ArgumentsStatus:
    def __init__(self, args_dict_name, args_def, args_vals):
        if not IterableArgumentValidator.in_collection(args_dict_name, ['Body', 'Query String']):
            raise Exception('args_dict_name should be Body or Query String')

        self.args_dict_name = args_dict_name
        self.args_def = args_def
        self.args_names = [arg.name for arg in self.args_def]
        self.args_vals = args_vals if args_vals else dict()
        self.invalid_args = False
        self.missing_args = list()
        self.extra_args = list()
        self.report = f'In the {self.args_dict_name}\n'

    def create_final_report(self):
        if self.invalid_args:

            if len(self.missing_args):
                missing_args_msg = f'The following arguments are missing in the {self.args_dict_name}: {self.missing_args}'
            else:
                missing_args_msg = f'No missing arguments in the {self.args_dict_name}'
            self.update_report(missing_args_msg)

            if len(self.extra_args):
                extra_args_msg = f'The following arguments are extra in the {self.args_dict_name}: {self.extra_args}'
            else:
                extra_args_msg = f'No extra arguments in the {self.args_dict_name}'
            self.update_report(extra_args_msg)

    def assert_args(self):
        self.check_extra_args()

        for arg in self.args_def:
            arg.assert_arg(self.args_vals)
            if arg.missing:
                self.update_missing_args(arg.name)

            elif arg.invalid:
                self.update_report(arg.report)

        self.create_final_report()

    def check_extra_args(self):
        self.extra_args = set(self.args_vals) - set(self.args_names)
        if len(self.extra_args):
            self.set_invalid_args()

    def update_missing_args(self, missing_arg):
        self.set_invalid_args()
        self.missing_args.append(missing_arg)

    def update_report(self, report_update):
        self.set_invalid_args()
        self.report += report_update + '\n'

    def set_invalid_args(self):
        self.invalid_args = True

    def __repr__(self):
        if self.invalid_args:
            return f'The arguments are invalid\nReport:\n{self.report}'
        else:
            return 'The arguments are valid'