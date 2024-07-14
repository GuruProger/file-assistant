# FileAssistant

FileAssistant is a Python utility class designed to traverse directories, count lines in files with specific extensions, and remove specified directories. This tool is particularly useful for developers who need to manage and analyze large codebases.

___
## Features

- **Count Lines in Files:** 
  - Traverse a given directory and count the total number of lines in files that match specified extensions.
  - Skip specified directories during traversal to focus on relevant files.
  - The row count is fast enough
    ```python
    # Let's measure the time it takes to count all files in numpy1
    np_path = r'.\venv\Lib\site-packages\numpy'
    fa = FileAssistant(np_path)
    
    s = time.time()
    count_lines_python_stubs = fa.get_count_lines(['.py'], [])
    e = time.time()
    print(f"The counted number of lines is {count_lines_python_stubs}, it took {e - s} seconds")
    # Output: The counted number of lines is 230186, it took 0.08706998825073242 seconds
    ```
- **Remove Directories:**
  - Delete specified directories within a given directory path.
  - Return the number of directories removed for tracking purposes.
  - Deletion is fast, as is row counting
___
The program crawls **all** subfolders inside the specified directory, with the exception of skip_directories