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
    def gather_boolean_input(prompt):
        '''Gathers yes/no input from the user.
        
        Arguments:
            prompt {str} -- The prompt to provide the user.
        
        Returns:
            bool -- True if the user answers Yes.
        '''

        user_input = None

        # We want to continue until we have some valid input.
        while True:

            # We want to show them their options, and normalize their input.

            user_input = input(f'{user_input} [Y/N]').strip().upper()[0]

            if (
                user_input and
                user_input in ['Y','N']
            ):

                user_input = (
                    True
                    if user_input == 'Y'
                    else False
                )

                break

        return user_input

    @staticmethod
    def gather_selection_input(selection_dict):
        '''Gathers a user's input from a selection of options, returning the associated object in the provided dict.
        
        Arguments:
            selection_dict {dict} -- The dictionary of selections, key is the option to show the user and the value is the object to return if it's selected. 
        
        Returns:
            object -- The object in the selection_dict associated with the option the user selected.
        '''

        user_selection = None

        '''
        We want to normalize the options so we can
        make accurate comparisons with the user input.
        '''
        normalized_selections = dict(
            (
                selection.upper(),
                result
            )
            for selection, result
            in selection_dict.items()
        )

        # We want to continue until we have some valid input.
        while True:

            print('Please make a selection from the following:')

            for key_index, key in enumerate(selection_dict.keys()):

                print(f'{key_index + 1}) {key}')

            user_input = input('?').strip().upper()

            if user_input:

                '''
                We want to give the user the option to
                provide either the index of the selection
                or the selection itself.
                '''
                try:
                    
                    # We want to check if the user provided an index value.
                    user_input = int(user_input)

                    # We want to make sure the user_input matches the 0-based index of the keys list.
                    user_input -= 1

                    # We want to make sure the user input is in the appropriate range.
                    if (
                        user_input >= 0 and
                        user_input < len(selection_dict)
                    ):

                        user_selection = list(selection_dict.values())[user_input]

                        break

                # Caught if the user input isn't an index value.
                except Exception as e:

                    # We want to make sure the user input is one of the available selections.
                    if user_input in normalized_selections.keys():

                        user_selection = normalized_selections[user_input]

                        break
            
            '''
            If the process hasn't broken out at this point,
            it's due to invalid input from the user.
            We want to let them know.
            '''
            print('Please provide an appropriate selection.')

        return user_selection


