from getpass import getpass


class InputUtil(object):
    '''Performs common Input actions.'''

    @staticmethod
    def gather_input(prompt, is_password=False):
        '''Gathers user input.
        
        Arguments:
            prompt {str} -- The prompt to use when gathering user input.
        
        Keyword Arguments:
            is_password {bool} -- If True, a password is being gathered and getpass should be used. (default: {False})
        
        Returns:
            str -- The gathered user input.
        '''

        user_input = None

        # We want to continue attempting to gather info until the user provides some.
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
        '''Gathers a boolean from the user.
        
        Arguments:
            prompt {str} -- The prompt to use when gathering user input.
            true_option {str} -- The user input that represents True.
            false_option {str} -- The user input that represents False.
        
        Returns:
            bool -- The boolean user input.
        '''

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

                    user_input = True

                    break

                if user_input.upper() == false_option.upper():

                    user_input = False

                    break

        return user_input

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
