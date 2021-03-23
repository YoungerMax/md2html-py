import argparse
import os

from md2html import runner, util


# Fix the passed arguments for use inside the app
def fix_args(args):
    # Get the absolute paths for the input and output
    args.input = os.path.abspath(args.input)
    args.output = os.path.abspath(args.output)

    # If a directory is passed,
    # then get the name of the input file and set the output
    # file to the name of the file with the .html extension
    # inside that directory
    if os.path.isdir(args.output):
        args.output = util.fix_separators(
            os.path.join(
                args.output, os.path.basename(os.path.splitext(args.input)[0]) + ".html"
            )
        )

    # Return the fixed arguments
    return args


# This is what will be called on when the app starts
def main():
    # Initialize an argument parser
    parser = argparse.ArgumentParser()

    # Input file (.md) argument
    parser.add_argument(
        "--input",
        "-i",
        help="The input file path (Markdown)",
        required=True,
        dest="input"
    )

    # Output file (.html) argument
    parser.add_argument(
        "--output",
        "-o",
        help="The output file path (HTML)",
        dest="output",
        default="output.html"
    )

    # Parse arguments
    args = parser.parse_args()

    # Fix arguments for use and run through the
    # stages
    runner.run(fix_args(args))


# Entry point
if __name__ == '__main__':
    main()
