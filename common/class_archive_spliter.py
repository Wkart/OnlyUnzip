# ???????
import os
from typing import Tuple, Dict

import lzytools_archive

from common.class_7zip import ArchiveRole, TYPES_ARCHIVE_ROLE


class ArchiveSpliter:
    """??????? ??????/??????"""

    def __init__(self):
        self.archives = []  # ??????(?????????,?????????)
        self._archive_members: Dict[str, list] = dict()  # ????????,???{????:[???????], ...}
        self._archive_roles: Dict[str, TYPES_ARCHIVE_ROLE] = dict()  # ????????,???{????:???????, ...}

    def analyse_files(self, files: list):
        """??????
        :param files: ?????????"""
        # ??
        self.archives = []
        self._archive_members = dict()
        # ?????????????????
        normal_archives, volume_archives = self._split(files)
        print('?????????????', normal_archives, volume_archives)
        # ??????????
        for archive in normal_archives:
            self.archives.append(archive)
            self._archive_members[archive] = [archive]
            self._archive_roles[archive] = ArchiveRole.Normal()
        # ???????????
        first_volume_archives, volume_members = self._analyse_volume_archive(volume_archives)
        # ??????????
        for i in first_volume_archives:
            if i not in self.archives:
                self.archives.append(i)
                self._archive_members[i] = volume_members[i]
            else:
                self._archive_members[i].extend(volume_members[i])
            self._archive_roles[i] = ArchiveRole.VolumeFirst()
        for i in volume_members:
            if i not in self._archive_roles:
                self._archive_roles[i] = ArchiveRole.VolumeMember()

    def is_has_archives(self) -> bool:
        """??????????"""
        return len(self.archives) > 0

    def get_role(self, filepath: str):
        """???????????????"""
        return self._archive_roles[filepath]

    def get_files(self):
        """??????(???????)"""
        return self.archives.copy()

    def get_members(self, filepath: str):
        """?????????????????"""
        return self._archive_members[filepath].copy()

    @staticmethod
    def _split(files) -> Tuple[list, list]:
        """"?????????
        :return: ????????,????????"""
        volume_archives = []
        normal_archives = []
        for file in files:
            if lzytools_archive.is_volume_archive_by_filename(os.path.basename(file)):
                volume_archives.append(file)
            else:
                normal_archives.append(file)
        return normal_archives, volume_archives

    @staticmethod
    def _analyse_volume_archive(volume_archives: list) -> Tuple[list, dict]:
        """"???????????
        :return: ???????,???????(???{????:[???????], ...})"""
        parent_dirpaths = set()  # ?????,????????????
        first_volumes = []  # ?????????????
        members = {}  # ??????,???{????:[???????], ...}
        # ???????
        for file in volume_archives:
            # ???????????????,??????key
            virtual_first_volume_filename = lzytools_archive.guess_first_volume_archive_filename(file)
            virtual_first_volume_path = os.path.normpath(
                os.path.join(os.path.dirname(file), virtual_first_volume_filename))
            if virtual_first_volume_path not in first_volumes:
                first_volumes.append(virtual_first_volume_path)
                members[virtual_first_volume_path] = []
            members[virtual_first_volume_path].append(file)
            parent_dirpaths.add(os.path.dirname(file))

        # ????????
        for dirpath in parent_dirpaths:
            listdir = [os.path.normpath(os.path.join(dirpath, i)) for i in os.listdir(dirpath)]
            for path in listdir:
                virtual_first_volume_filename = lzytools_archive.guess_first_volume_archive_filename(path)
                if virtual_first_volume_filename:
                    virtual_first_volume_path = os.path.normpath(os.path.join(dirpath, virtual_first_volume_filename))
                    if virtual_first_volume_path in first_volumes and path not in members[virtual_first_volume_path]:
                        members[virtual_first_volume_path].append(path)

        return first_volumes, members
