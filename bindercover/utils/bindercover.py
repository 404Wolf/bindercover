from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class BinderCover:
    name: str
    course: str
    semester: str
    email: str
    phone: str
