from job_finder.util.input_util import InputUtil
import unittest


class TestInputUtil(unittest.TestCase):

    def test_gather_input(self):

        user_input = InputUtil.gather_input('Please provide input.')

        self.assertIsNotNone(user_input)

        self.assertIsNot(user_input, '')

        user_pass = InputUtil.gather_input('Please provide a password.', is_password=True)

        self.assertIsNotNone(user_pass)

        self.assertIsNot(user_pass, '')

    def test_gather_boolean_input(self):

        user_input = InputUtil.gather_boolean_input('Please answer yes or no.')

        self.assertIsNotNone(user_input)

        self.assertIn(user_input, [True, False])

    def test_gather_selection_input(self):

        selections = {
            'First': 'First_val',
            'Second': 'Second_val'
        }

        user_input = InputUtil.gather_selection_input(selections)

        self.assertIsNotNone(user_input)

        self.assertIn(user_input,selections.values())


if __name__ == "__main__":
 
    unittest.main()
