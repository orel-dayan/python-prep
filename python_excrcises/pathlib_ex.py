from concurrent.futures import process
from pathlib import Path
import tempfile
import os

# example of using pathlib to create a temporary directory and write a file in it
p = Path("test.txt")
p.write_text("Hello, World!")
print(p.read_text())
print(p.exists())
print(p.is_file())
print(p.is_dir())
print(p.stat()) # returns a os.stat_result object with information about the file, such as size, permissions, and timestamps
print(p.parent) # returns the parent directory of the file
print(p.name) # returns the name of the file
print(p.suffix) # returns the file extension
# Path("test.txt").rename("test2.txt") # rename the file test.txt to test2.txt
Path("dir").mkdir(parents=True, exist_ok=True) # create a directory called dir, if it doesn't exist, and create any parent directories as needed
# remove directory dir
Path("dir").rmdir() # remove the directory dir, only if it is empty

# example of using pathlib to create a temporary directory and write a file in it
config = Path.home() / ".config" / "myapp" / "settings.json"
print(config)
# Linux:   /home/orel/.config/myapp/settings.json
# Windows: C:\Users\orel\.config\myapp\settings.json


# Cross-platform anchors -- these work everywhere
home = Path.home()          # C:\Users\orel  or  /home/orel
cwd = Path.cwd()
script_dir = Path(__file__).resolve().parent

# Temp directory

tmp = Path(tempfile.gettempdir())

# Windows-specific folders via environment variables

appdata = Path(os.environ["APPDATA"])        # C:\Users\orel\AppData\Roaming
localapp = Path(os.environ["LOCALAPPDATA"])  # C:\Users\orel\AppData\Local


with tempfile.TemporaryDirectory() as td:
    work = Path(td)
    (work / "data.txt").write_text("hello", encoding="utf-8")

    print((work / "data.txt").exists())   # True



# # One-liners for small files
# text = Path("config.json").read_text(encoding="utf-8")
# data = Path("image.png").read_bytes()

# Path("out.txt").write_text("hello\n", encoding="utf-8")
# Path("out.bin").write_bytes(b"\x00\x01")

# # For large files or line-by-line, open() still works
# with Path("big.log").open(encoding="utf-8") as f:
#     for line in f:
#         process(line)
        
        
# Create directory tree; no error if it already exists
Path("output/logs").mkdir(parents=True, exist_ok=True)


old = Path("old.txt")
if old.exists():
    old.rename("new.txt")
else:
    print("old.txt does not exist, skipping rename")
Path("temp.txt").unlink(missing_ok=True)  # delete file, 3.8+
# Path("empty_dir").rmdir()                 # only if empty

# Non-empty directory still needs shutil
# import shutil
# shutil.rmtree(Path("build"))

p = Path("../data/./file.txt")

p.resolve()        # absolute, symlinks resolved, .. collapsed
p.absolute()       # absolute but does NOT normalize -- rarely what you want
p.is_absolute()    # True/False

Path("/a/b/c.txt").relative_to("/a")  # Path('b/c.txt')

from pathlib import Path

base = Path("src")

base.glob("*.py")          # .py files, this level only
base.glob("*")             # everything, this level only
base.glob("**/*.py")       # .py recursively -- same as rglob("*.py")
base.glob("test_*.py")     # prefix match
base.glob("*.[ch]")        # .c or .h
base.glob("data?.csv")     # data1.csv, dataX.csv - single char
base.glob("**/")           # directories only, recursively


# Templete 
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOG_DIR = PROJECT_ROOT / "logs"

for d in (DATA_DIR, RAW_DIR, OUTPUT_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)
    
    
from pathlib import Path

p = Path("data.txt")

try:
    content = p.read_text(encoding="utf-8")
except FileNotFoundError:
    content = ""
except PermissionError:
    print(f"No access to {p}")
    raise
except IsADirectoryError:
    print(f"{p} is a directory, not a file")
except UnicodeDecodeError:
    content = p.read_text(encoding="latin-1")   # fallback for legacy files


# import csv
# from pathlib import Path

# p = Path("data.csv")

# # csv needs a file object, not a string - newline="" is required
# with p.open(newline="", encoding="utf-8") as f:
#     for row in csv.DictReader(f):
#         print(row)

# with p.open("w", newline="", encoding="utf-8") as f:
#     writer = csv.DictWriter(f, fieldnames=["name", "score"])
#     writer.writeheader()
#     writer.writerow({"name": "test", "score": 95})

# import os
# os.environ.get("API_KEY", "default_value") # get the value of the environment variable API_KEY, if it doesn't exist, return default_value
# os.path.join("dir", "file.txt") # join the directory dir and the file file.txt into a single path



# template = Path("template.txt").read_text() # read the content of the file template.txt and store it in the variable template
# print(template.format(name="Alice", count=5)) # use the format method to replace the
# # option 1
# template ="Hello {name} how are you? you have seen {count} times"
# print(template.format(name="Alice", count=5))
# # option 2
# # template with index, the number in {} is the index of the argument in format()
# template ="Hello {0} how are you? you have seen {1} times"
# print(template.format("Alice", 5))
# # the index can be repeated, so you can use the same argument multiple times
# template  ="Hello {0} how are you? you have seen {1} times, {0} is your name"
# print(template.format("Alice", 5))
# # option 3 - {} is empty placeholder, it will be filled in order
# template ="Hello {} how are you? you have seen {} times"
# print(template.format("Alice", 5))

# # some rules: .2f means 2 decimal places, .2s means 2 characters,
# template = "The value of pi is approximately {0:.2f}"
# print(template.format(3.14159))

# #  .2e means scientific notation with 2 decimal places
# template = "The value of pi is approximately {0:.2e}"
# print(template.format(3.14159))

# #$ means to format as currency
# template = "The price is ${0:,.2f}"
# print(template.format(1234567.89))

# # > means to align to the right, < means to align to the left, ^ means to align to the center
# template = "The value is {0:>10}"
# print(template.format(42))
# template = "The value is {0:<10}"
# print(template.format(42))
# template = "The value is {0:^10}"
# print(template.format(42))

