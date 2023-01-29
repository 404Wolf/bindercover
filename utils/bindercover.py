import os
import subprocess
from dataclasses import dataclass
from typing import ClassVar

from jinja2 import Environment, FileSystemLoader

latex_jinja_env = Environment(
    block_start_string="\BLOCK{",
    block_end_string="}",
    variable_start_string="\VAR{",
    variable_end_string="}",
    comment_start_string="\#{",
    comment_end_string="}",
    line_statement_prefix="%%",
    line_comment_prefix="%#",
    trim_blocks=True,
    autoescape=False,
    loader=FileSystemLoader("./templates"),
)


@dataclass(kw_only=True, slots=True)
class BinderCover:
    name: str
    course: str
    semester: str
    year: str
    email: str
    phone: str

    template: ClassVar = latex_jinja_env.get_template("bindercover.tex")

    def generate_pdf(self, filename: str):
        """
        Generates a PDF file from the bindercover template and return the filename.

        Args:
            filename (str): The filename of the generated PDF file.
                Omit the file extension; it will be set to .pdf automatically.

        Returns:
            str: The filename of the generated PDF file.
        """
        # Set the semester/year string depending on the user input
        if self.semester == "":
            semesterYear = self.year
        elif self.year == "":
            semesterYear = f"S{self.semester}"
        else:
            semesterYear = f"S{self.semester}, {self.year}"

        # Depending on the length of the course name, adjust the
        generated = self.template.render(
            name=self.name,
            course=self.course,
            semesterYear=semesterYear,
            email=self.email,
            phone=self.phone
        )

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
