import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main


class TestCLI(unittest.TestCase):
    def test_choice_1_displays_student_details(self):
        with patch("builtins.input", side_effect=["Enos Arenga", "1", "6"]):
            output = io.StringIO()
            with redirect_stdout(output):
                main.main()

        rendered = output.getvalue()
        self.assertIn("Welcome, Enos Arenga!", rendered)
        self.assertIn("Name: Enos Arenga", rendered)
        self.assertNotIn("INVALID CHOICE", rendered)

    def test_choice_5_displays_classmates(self):
        with patch("builtins.input", side_effect=["Enos Arenga", "5", "6"]):
            output = io.StringIO()
            with redirect_stdout(output):
                main.main()

        rendered = output.getvalue()
        self.assertIn("Your are The Only one Doing", rendered)
        self.assertNotIn("INVALID CHOICE", rendered)


if __name__ == "__main__":
    unittest.main()
