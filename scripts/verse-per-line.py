import sys
import re
import os

# Define the path to the folder containing the files
folder_path = "../"

# Create a subfolder named "verse-per-line" if it doesn't already exist
if not os.path.exists(os.path.join(folder_path, "verse-per-line")):
    os.makedirs(os.path.join(folder_path, "verse-per-line"))

# List of file names
file_list = [
    "TNT.txt",
    "TNT2.txt",
]

# Loop through the file names
for file in file_list:
    # Get the full file path by joining the folder path and file name
    file_path = os.path.join(folder_path, file)

    # Get the filename from the path
    filename = os.path.basename(file_path)
    
    # Read the file
    with open(file_path, "r") as inputfile:
        clean = inputfile.read()
        
        # Remove page numbers
        clean = re.sub('<Page = \d+>', '', clean)
        # Scrub newlines
        clean = re.sub('\n', '', clean)
        # Clean/standardize references
        clean = re.sub('\$\$\$(.*?)(\.\d+)\.(\d+)', '\n\\1\\2:\\3 ', clean)
        # Clean book Titles
        clean = re.sub('<Title = (.*?)>', '\n\n# \\1 #', clean)
        # Create section breaks
        clean = re.sub('(?m)^([1-3A-Za-z]+\.\d+:\d+ )<SB>', '\n\\1', clean)
        # Note: we have to look for 'PΒ' as well (that 2nd Β is Greek capital beta) because of a typo at Mat.26.55. See README for more details
        clean = re.sub('<(PB|PΒ)>', '', clean)
        # Remove a solitary <SB> (at the end of 1Ti.6.21)
        clean = re.sub('<SB>', '', clean)
        # Clean the "subscript"
        clean = re.sub('<Subsc = (.*?)>', '\n## \\1 ##', clean)
        # Remove extra newlines at beginning of the file
        clean = re.sub('(?m)^\n\n', '', clean)
        clean = re.sub('(?m)^(# .*?)\n', '\\1', clean)
        
    # Save the files in the "verse-per-line" subfolder
    with open(os.path.join(folder_path, "verse-per-line", file), "w", encoding="utf-8") as outputfile:
        outputfile.write(clean)
