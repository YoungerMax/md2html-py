import argparse

import ntpath
import os

parser = argparse.ArgumentParser()

parser.add_argument("--input", "-i", help="The input (Markdown) file. This is required", required=True,
                    dest="input")
parser.add_argument("--output", "-o", help="The output (HTML) file. Defaults to output.html", dest="output",
                    default="output.html")

args = parser.parse_args()


def fix_separators(string: str):
    return string.replace("/", os.sep)


if os.path.isdir(args.output):
    args.output = fix_separators(os.path.join(args.output, ntpath.basename(os.path.splitext(args.input)[0]) + ".html"))

print("Discovering")

txt = open(args.input, "rt").read()

lines = txt.split("\n")

discoveries = []

section_key = {
    "#": {
        "#": "h1",
        "##": "h2",
        "###": "h3",
        "####": "h4",
        "#####": "h5",
        "######": "h6",
    },
    "`": {
        "`": "code"
    },
    "*": {
        "*": "i",
        "**": "strong"
    },
    "~~": {
        "~~": "strike"
    },
    "-": {
        "-": "li"
    }
}

for line in lines:

    section = "p"
    text = ""

    current_modifier = ""
    modifier = ""

    for char in line:
        for key in section_key.keys():
            if line.startswith(key):
                for m in section_key[key]:
                    if line.startswith(m):
                        modifier = m
                        section = section_key[key][m]

    text = line.replace(modifier, '')

    discoveries.append({"section": section, "text": text})

print("Translating")

translations = []

for discovery in discoveries:
    string = f"<{discovery['section']}>{discovery['text']}</{discovery['section']}>"
    translations.append(string)

final = ""

print("Breaking lines")
for t in translations:
    final += '    ' + t + '\n'

title = discoveries[0]['text']

print("Replacing")
out = f"""
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>{title}</title>
    <link href="style.css" rel="stylesheet" />
  </head>
  <body>
{final}
  </body>
</html>
"""

print("Writing")
open(args.output, "wt").write(out)

print("Done >> Writen to " + args.output)
