"""
Run this before testing makes it to find bugs.
"""
import os
import shutil

def clean():
    # Define the directories to clean
    directories = ['_AutoCitation/log', '_AutoCitation/__pycache__']
    
    for directory in directories:
        if os.path.exists(directory):
            # Remove all files in the directory
            shutil.rmtree(directory)
            # Recreate the directory
            os.makedirs(directory)
            print(f'Cleaned and recreated: {directory}')
        else:
            print(f'Directory does not exist: {directory}')
if __name__ == "__main__":
    clean()
