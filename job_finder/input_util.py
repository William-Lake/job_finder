from getpass import getpass


class InputUtil(object):

    @staticmethod
    def gather_input(prompt, is_password=False):

        user_input = None

        while True:

            if is_password:

                user_input = getpass(prompt=prompt).strip()

            else:

                user_input = input(prompt).strip()

            if user_input:

                break

        return user_input
    
    @staticmethod
    def gather_boolean_input(prompt, true_option, false_option):

        user_input = None

        while True:

            user_input = input(
                f'''
                {prompt}

                Options: {true_option} / {false_option}
                '''
            ).strip()

            if user_input:

                if user_input.upper() == true_option.upper():

                    return True

                if user_input.upper() == false_option.upper():

                    return False

    @staticmethod
    def gather_selection_input(selection_dict):

        user_selection = None

        while True:

            print('Please make a selection from the following:')

            for key_index, key in enumerate(selection_dict.keys()):

                print(f'{key_index + 1}) {key}')

            user_input = input('?').strip()

            if user_input:

                try:

                    user_input = int(user_input)

                    if (
                        user_input > 0 and
                            user_input <= len(selection_dict)
                    ):

                        user_selection = list(selection_dict.values())[user_input - 1]

                        break

                except Exception as e:

                    if user_input.upper() in selection_dict.keys():

                        user_selection = selection_dict[user_input]

                        break

        return user_selection
        