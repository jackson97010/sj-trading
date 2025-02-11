from pathlib import Path

'''
Locating the File in a Known Directory.
'''

# Get the directory of the current script and build the path to Sinopac.pfx
pfx_path = Path(__file__).parent / "Sinopac.pfx"
print("Absolute path:", pfx_path.resolve())


'''
Searching recursively for the Sinopac.pfx file

from pathlib import Path

# Search recursively for Sinopac.pfx starting from the current directory
for file in Path(".").rglob("Sinopac.pfx"):
    print("Found file at:", file.resolve())
'''


