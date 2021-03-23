import os

from md2html import statics, util


# Base stage class
class Stage:
    # Get the name of the stage
    def get_name(self) -> str:
        pass

    # Run the stage
    #
    # args         The fixed arguments from __init__.py
    #
    # last_output  The return value of the last run stage.
    #              This is None is there was no stage previously.
    def run(self, args, last_output):
        pass


class DiscoveryLineBeginningsStage(Stage):
    # Markdown line class
    class Line:
        # Constructor
        def __init__(self, markdown: str, html: str, line: str):
            # Initial Markdown line prefix
            self.markdown = markdown

            # HTML tag that corresponds to the Markdown prefix
            self.html = html

            # The entire line
            self.line = line

        # Translate to HTML
        def to_html(self) -> str:
            return f"<{self.html}>{self.get_line_without_special_chars()}</{self.html}>"

        # Get the line without the Markdown prefix
        def get_line_without_special_chars(self):
            # TODO: Remove spaces before content in output HTML

            # Check if the HTML tag's length is one
            # Set the length accordingly
            if len(self.html) == 1:
                length = 0
            else:
                length = len(self.markdown)

            # Return everything after the Markdown prefix
            return self.line[length:]

    def get_name(self) -> str:
        return "Discovering line beginnings"

    def run(self, args, last_output):
        # The input Markdown contents
        markdown_file_contents = open(args.input, 'rt').read()

        # Lines of those contents
        file_lines = markdown_file_contents.split('\n')

        # List of the lines but it's the line class
        lines = []

        # Loop each line in the lines of the file
        for line in file_lines:
            # Markdown prefix
            current_markdown = ""

            # The HTML tag prefix right now translated from current_markdown
            current_html_tag = statics.md_default_tag

            # Loop through the Markdown to HTML key
            for markdown, html in statics.md_html:
                # If the line starts with the Markdown prefix
                if line.startswith(markdown):
                    # Set these things
                    current_html_tag = html
                    current_markdown = markdown

            # Append a new Line object to the list
            lines.append(DiscoveryLineBeginningsStage.Line(current_markdown, current_html_tag, line))

        # Return the lines
        return lines

# TODO: Discover inline elements such
# class DiscoveryInlineStage(Stage):
#     def get_name(self) -> str:
#         return "Discovering inline characters"
#
#     def run(self, args, last_output):


# Write the HTML file to disk
class WritingFileStage(Stage):
    def get_name(self) -> str:
        return "Writing file"

    def run(self, args, last_output):
        # Template HTML file path
        html_path = os.path.join(util.get_assets_folder(), util.fix_separators('src/template.html'))

        # CSS styles file path
        style_path = os.path.join(util.get_assets_folder(), util.fix_separators('src/style.css'))

        # Get the contents of the template HTML file
        template_file_html = open(html_path, "rt").read()

        # Get the contents of the template CSS file
        template_file_css = open(style_path, "rt").read()

        # Initialize a body variable
        body = ""

        # Append the HTML version of each line object to
        # the body variable
        for line in last_output:
            body += line.to_html()

        # Replace the variables within the template HTML
        # file
        to_write = template_file_html.format(
            title=last_output[0].get_line_without_special_chars(),
            style=template_file_css,
            body=body
        )

        # Write file
        open(args.output, 'wt').write(to_write)


# Registered stages
stages = [DiscoveryLineBeginningsStage, WritingFileStage]
