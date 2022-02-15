# Python program to get parent
# directory


import os

# get current directory
path = os.getcwd()
print("Current Directory", path)

# parent directory
parent = os.path.dirname(path)
print("Parent directory", parent)
