INPUT_ERROR_MESSAGE = 'Invalid input arguments, expected'
OUTPUT_ERROR_MESSAGE = 'Invalid output value, expected'


def validate(error_message, values_to_check, valid_types):
    if not all(isinstance(value, valid_types) for value in values_to_check):
        expected_types = ', '.join(str(current_type) for current_type in valid_types)
        print(f'{error_message} {expected_types}!')


def type_check(criteria):
    def type_check_by_criteria(*outer_args, **outer_kwargs):
        valid_types = tuple(outer_args) + tuple(outer_kwargs.values())

        def decorator(func):
            def decorated(*args, **kwargs):
                if criteria == 'in':
                    validate(INPUT_ERROR_MESSAGE, tuple(args) + tuple(kwargs.values()), valid_types)

                result = func(*args, **kwargs)

                if criteria == 'out' and not isinstance(result, valid_types):
                    expected_types = ', '.join(str(current_type) for current_type in valid_types)
                    print(f'{OUTPUT_ERROR_MESSAGE} {expected_types}!')

                return result

            return decorated

        return decorator

    return type_check_by_criteria