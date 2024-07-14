import os
import shutil
from fnmatch import fnmatch


class FileAssistant:
    def __init__(self, directory_path: str):
        """
        :param directory_path: Path to the directory to traverse
        """
        self.directory_path = directory_path
        self._matching_files = set()
        self._skip_directories = list()
        self._file_extensions = list()

    def get_count_lines(self, file_extensions: tuple | list | set | frozenset,
                        skip_directories: tuple | list | set | frozenset) -> int:
        """
        Counts the total number of lines in all files with the specified extensions,
        excluding files in the specified directories.

        :param file_extensions: File extensions to search for
        :param skip_directories: Directories to skip

        :return: Total number of lines in all matching files.
        """
        self._skip_directories = skip_directories
        self._file_extensions = file_extensions
        self._matching_files = set()
        [
            self._add_set(root, files) for root, _, files in os.walk(self.directory_path)
            if not self._is_valid_directory(root, self._skip_directories)
        ]
        all_line_count = sum(self._file_count_lines(file_path) for file_path in self._matching_files)
        return all_line_count

    def remove_directories(self, list_dir: tuple | list | set | frozenset) -> int:
        """
        Deletes the specified directories and returns the number of directories removed.

        :param list_dir: Directories to delete

        :return: Number of directories removed
        """
        count_removed_dirs = 0
        for root, directories, _ in os.walk(self.directory_path):
            cnt = [
                shutil.rmtree(os.path.join(root, d)) for d in directories
                if self._is_valid_directory(os.path.join(root, d), list_dir)
            ]
            count_removed_dirs += len(cnt)
        return count_removed_dirs

    def _add_set(self, root: str, files: list):
        """
        Adds files with the specified extensions to the set of matching files.

        :param root: Current directory
        :param files: List of files in the current directory
        """
        self._matching_files |= {
            os.path.join(root, file) for file in files
            if any([file.endswith(endswith) for endswith in self._file_extensions])
        }

    def _is_valid_directory(self, current_path: str, patterns: tuple | list | set | frozenset) -> bool:
        """
        Checks if the current path matches one of the specified directory patterns.

        :param current_path: Current path
        :param patterns: Directory patterns

        :return: True if the path matches one of the patterns, otherwise False
        """
        f = any(fnmatch(current_path, fr'{self.directory_path}*\{pat}*') for pat in patterns)
        return f

    @staticmethod
    def _file_count_lines(file_path: str) -> int:
        """
        Counts the number of lines in a file.

        :param file_path: Path to the file

        :return: Number of lines in the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return sum(1 for _ in file)
        except (IOError, OSError) as e:
            print(f"Error reading file {file_path}: {e}")
            return 0


if __name__ == '__main__':
    dir_path = r'C:\your_directory'

    # File extensions to search for
    endswith_files = ('.py', '.js', '.css', 'html')
    # Directories to skip during traversal
    skip_dir = ('venv', '__pycache__', '.idea')
    # Directories to delete
    remove_dir = ('test', 'trash')

    fa = FileAssistant(dir_path)

    count_lines = fa.get_count_lines(endswith_files, skip_dir)
    print('Number of lines -', count_lines)
    count_remove_dir = fa.remove_directories(remove_dir)
    print('Removed directories -', count_remove_dir)
