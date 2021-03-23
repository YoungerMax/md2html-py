import os
import sys

# Replace the separators to the system preferred
# separator
def fix_separators(string: str):
    return string.replace("/", os.sep)


# Get assets folder
def get_assets_folder() -> str:
    # Get the python script location from the first
    # argument
    python_script_location = sys.argv[0]

    # Join the assets directory with the script location
    # and get the absolute path
    directory = os.path.abspath(os.path.join(os.path.dirname(python_script_location), 'assets'))

    return directory
