from jinja2 import Environment, FileSystemLoader


class LatexTemplate:
    def __init__(self, filepath, template):
        """
        A class for rendering LaTeX templates using Jinja2.

        This class can be reused to render different sets of data with the same
        template.

        Args:
            filepath: The path to the directory containing the template.
            template: The name of the template file.
        """

        self.env = Environment(
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
            loader=FileSystemLoader(filepath),
        )
        self.template = self.env.get_template(template)

    def render(self, **kwargs) -> str:
        """
        Renders the template with the given keyword arguments.

        Args:
            **kwargs: The keyword arguments to be passed to the template.

        Returns:
            str: The rendered template.
        """
        for key, value in tuple(kwargs.items()):
            value = value.replace("|", "\\|")
            kwargs[key] = f"\\lstinline|{value}|"
        return self.template.render(**kwargs)
