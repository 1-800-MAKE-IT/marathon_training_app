import os
import shutil
import streamlit as st

def clear_directory(directory_path):
    try:
        # Check if the directory exists
        if os.path.exists(directory_path):
            # Iterate over all files and directories in the given directory
            for file_name in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file_name)
                # Check if the file is a regular file (not a directory)
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Remove the file
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove the directory and all its contents
            st.success(f"Successfully cleared contents of directory: {directory_path}")
        else:
            st.error(f"Directory not found: {directory_path}")
    except Exception as e:
        st.error(f"Error clearing directory: {str(e)}")
