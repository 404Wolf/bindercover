import os
import subprocess
from dataclasses import dataclass
from typing import ClassVar

from utils.latexJinja import LatexTemplate


def merge_strings(*args):
    """
    Converts any number of strings into a single string, omitting empty strings.
    """
    return " ".join([arg for arg in args if arg != ""])


def format_phone_number(phone_number):
    """
    Formats a phone number into the format (xxx) xxx-xxxx.

    If the phone number is already in the correct format, it is returned as is.

    Args:
        phone_number: The phone number to format.

    Returns:
        str: The formatted phone number.
    """
    if (
        len(phone_number) == 14
        and phone_number[0] == "("
        and phone_number[4] == ")"
        and phone_number[8] == "-"
    ):
        return phone_number
    return f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:10]}"


@dataclass()
class BinderCover:
    name: str = ""
    course1: str = ""
    course2: str = ""
    course3: str = ""
    semester: str = ""
    year: str = ""
    email: str = ""
    phone: str = ""

    renderer: ClassVar = LatexTemplate("./templates", "bindercover.tex")

    def generate_pdf(self, filename: str):
        """
        Generates a PDF file from the bindercover template and return the filename.

        Args:
            filename (str): The filename of the generated PDF file.
                Omit the file extension; it will be set to .pdf automatically.

        Returns:
            str: The filename of the generated PDF file.
        """
        # Depending on the length of the course name, adjust the
        generated = self.renderer.render(
            name=self.name,
            course1=self.course1,
            course2=self.course2,
            course3=self.course3,
            course2ExistsAnd=r"\linebreak\&\linebreak" if self.course2 != "" else "",
            course3ExistsAnd=r"\linebreak\&\linebreak" if self.course3 != "" else "",
            semesterYear=merge_strings(f"S{self.semester}", self.year),
            email=self.email,
            phone=format_phone_number(self.phone).replace("-", "===?"),
        )
        generated = generated.replace("===?", "\\verb|-|")

        # Write the generated template to a file
        with open(f"generated/{filename}.tex", "w") as f:
            f.write(generated)

        # Compile the generated LaTeX template to a PDF file
        subprocess.run(
            [
                "xelatex",
                "-output-directory",
                "generated",
                f"generated/{filename}.tex",
            ]
        )

        # Remove the .tex .log and .aux files
        os.remove(f"generated/{filename}.tex")
        os.remove(f"generated/{filename}.log")
        os.remove(f"generated/{filename}.aux")
