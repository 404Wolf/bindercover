from dataclasses import dataclass
import pylatex as pl
from pylatex.utils import italic, bold


@dataclass(kw_only=True, slots=True)
class BinderCover:
    name: str
    course: str
    semester: str
    year: str
    email: str
    phone: str

    def generate_pdf(self):
        doc = pl.Document(documentclass="article")

        # hide page numbers
        doc.append(pl.Command("pagestyle", "empty"))

        doc.packages.append(pl.Package("geometry", options=("margin=1in",)))
        doc.packages.append(pl.Package("fontspec"))
        doc.append(
            pl.Command(
                "setmainfont",
                arguments=("rockwell.tff",),
                options=(
                    "ItalicFont=rockwell-italic.TFF",
                ),
            )
        )

        doc.append(pl.VerticalSpace("1in"))

        # Add the name of the course and semester
        centered = pl.Center()
        centered.append(pl.Command("fontsize", arguments=("46pt", "46pt")))
        centered.append(pl.Command("selectfont"))
        centered.append(f"{self.course} (S{self.semester})")
        doc.append(centered)

        # Add the name of the person to near the bottom
        centered = pl.Center()
        centered.append(pl.VerticalSpace("6in"))
        centered.append(pl.Command("fontsize", arguments=("24pt", "24pt")))
        centered.append(pl.Command("selectfont"))
        centered.append(f"{self.name}")
        centered.append(italic(f"({self.email}, {self.phone})"))
        doc.append(centered)

        doc.generate_pdf("test", clean_tex=False, compiler="xelatex")


test = BinderCover(
    name="John Smith",
    course="English",
    semester="1",
    email="John@smith.com",
    phone="(929)555-5555",
)
test.generate_pdf()
