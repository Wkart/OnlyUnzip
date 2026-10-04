# ?????????????????
import os

import lzytools_archive
from PySide6.QtCore import QThread, Signal


class ThreadFiletypeArchive(QThread):
    """?????????????????"""
    Archives = Signal(list, name='??????')

    def __init__(self, ):
        super().__init__()
        self.files = []  # ?????????

    def set_files(self, files: list):
        self.files = files

    def run(self):
        archive_files = []
        for file in self.files:
            if not is_exclude_file_extension(file):
                if lzytools_archive.is_archive_by_filename(os.path.basename(file)):
                    archive_files.append(file)
                elif os.path.exists(file) and lzytools_archive.is_archive(file):
                    archive_files.append(file)

        self.files.clear()

        self.Archives.emit(archive_files)


def is_exclude_file_extension(filename: str):
    """????????,?????????"""
    _exclude_file_extension = ['exe', 'apk', 'csv', 'xls', 'xlsx', 'doc', 'docx', 'ppt']

    file_extension = os.path.splitext(filename)[1].strip().strip('.').strip()
    if file_extension.lower() in _exclude_file_extension:
        return True

    return False
