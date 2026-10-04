# ?????????
import os
import re
from typing import Union

from PySide6.QtCore import Signal, QObject

from common import function_setting, function_extract, function_7zip
from common.class_7zip import ModelArchive, TYPES_MODEL_ARCHIVE, ModelPreFilter
from common.class_file_info import FileInfoList
from common.thread_filetype_archive import ThreadFiletypeArchive
from components.page_home.home_model import HomeModel
from components.page_home.home_viewer import HomeViewer
from components.page_home.res.icon_base64 import *


class HomePresenter(QObject):
    """?????????"""
    UserStop = Signal(name="??????(????")
    UserStopAfter = Signal(name="??????(???????????)")
    FileInfo = Signal(FileInfoList, name='????????')
    SignalNoFiles = Signal(name='?????????')
    SignalExistsTempFolder = Signal(str, name='???????,???????????')
    SignalError7ZipPath = Signal(name='7zip????')
    OpenAbout = Signal(name="?????")
    OpenTempPassword = Signal(name="???????")
    AskUpdateSetting = Signal(name="????????")
    ChangeSettingArchiveModel = Signal(object, name="??????")
    ChangeSettingTryUnknownFiletype = Signal(bool, name="????????????")
    ChangeSettingRecursiveExtract = Signal(bool, name="????????")
    ChangeSettingDeleteOrigin = Signal(bool, name="?????????")
    ChangeSettingTopWindow = Signal(bool, name="??????")

    def __init__(self, viewer: HomeViewer, model: HomeModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        # ????
        self._task_count: int = 0
        self._task_index: int = 0
        self._password_count: int = 0
        self._password_index: int = 0

        # ???
        self.set_icon_home()

        # ??????????(????ui??)
        self.thread_check_filetype = ThreadFiletypeArchive()
        self.thread_check_filetype.Archives.connect(self.deal_archive_files)

        # ????
        self.viewer.UserStop.connect(self.UserStop.emit)
        self.viewer.UserStopAfter.connect(self.UserStopAfter.emit)
        self.viewer.DropFiles.connect(self.drop_paths)
        self.viewer.OpenAbout.connect(self.OpenAbout.emit)
        self.viewer.OpenTempPassword.connect(self.OpenTempPassword.emit)
        self.viewer.AskUpdateSetting.connect(self.AskUpdateSetting.emit)
        self.viewer.ChangeSettingArchiveModel.connect(self.ChangeSettingArchiveModel.emit)
        self.viewer.ChangeSettingTryUnknownFiletype.connect(self.ChangeSettingTryUnknownFiletype.emit)
        self.viewer.ChangeSettingRecursiveExtract.connect(self.ChangeSettingRecursiveExtract.emit)
        self.viewer.ChangeSettingDeleteOrigin.connect(self.ChangeSettingDeleteOrigin.emit)
        self.viewer.ChangeSettingTopWindow.connect(self.ChangeSettingTopWindow.emit)
        self.model.RuntimeTotal.connect(self.set_runtime_total)
        self.model.RuntimeCurrent.connect(self.set_runtime_current)

    def drop_paths(self, paths: list, is_recursive: bool = False):
        """????
        :param paths: ????
        :param is_recursive: ????????????????"""
        print('??????,??????')
        # ??7zip??
        _7zip_path = function_7zip.get_7zip_path()
        if not _7zip_path or not os.path.exists(_7zip_path):
            self.SignalError7ZipPath.emit()
            return

        # ??????????
        if not is_recursive:
            self.model.start_timing()
        # ????????????
        self.set_step_notice("""?????...""")
        files = self.model.get_files(paths)
        # ?????????,??????????,????
        if not files:
            self.SignalNoFiles.emit()
            return

        # ???????,???????????????????????,???????????,?????
        archive_model = function_setting.get_archive_model()
        if isinstance(archive_model, ModelArchive.Extract):
            self.set_step_notice("""????????...""")
            # ???????????,?????????
            target_path = function_setting.get_extract_output_folder()
            if target_path:
                is_temp_exists, temp_path = function_extract.is_exists_temp_folder(target_path)
            else:  # ????????????
                is_temp_exists, temp_path = function_extract.is_exists_temp_folder(files)
            if is_temp_exists:
                self.SignalExistsTempFolder.emit(temp_path)
                return

        self.set_step_notice("""???????...""")
        # ?????,????????????????????
        filter_mode = function_setting.get_pre_filter_model()
        files_pre_filter = self.pre_filter_files(files, filter_mode)

        # ????????????,???????,???????
        is_try_unknown_filetype = function_setting.get_is_try_unknown_filetype()
        # filetype?????????????????,??????????????????????,????????????????
        if not is_try_unknown_filetype:
            self.thread_check_filetype.set_files(files_pre_filter)
            self.thread_check_filetype.start()
        else:
            self.deal_archive_files(files_pre_filter)

    def deal_archive_files(self, archives: list):
        """??????"""
        # ???????????????,??????
        archive_spliter = self.model.split_volume_archive(archives)

        # ???????????,?????
        if not archive_spliter.is_has_archives():
            self.SignalNoFiles.emit()
            return

        # ?????????????
        file_info_list = FileInfoList()
        for file in archive_spliter.get_files():
            role = archive_spliter.get_role(file)
            group_files = archive_spliter.get_members(file)
            file_info_list.add_file(file, role, group_files)

        # ????,???????
        self.FileInfo.emit(file_info_list)

    def pre_filter_files(self, files: list, filter_mode: ModelPreFilter):
        """?????"""
        if isinstance(filter_mode, ModelPreFilter.Default):
            return files
        elif isinstance(filter_mode, ModelPreFilter.BlackList):
            return function_setting.filter_by_black_list(files)
        elif isinstance(filter_mode, ModelPreFilter.WhiteList):
            return function_setting.filter_by_white_list(files)
        else:
            raise Exception('????????')

    def banned_drop(self):
        """??????"""
        self.viewer.banned_drop()
        self.set_float_button_enable(False)  # ?????????????????

    def allowed_drop(self):
        """??????"""
        self.viewer.allowed_drop()
        self.set_float_button_enable(True)  # ?????????????????

    def update_setting(self, archive_model: TYPES_MODEL_ARCHIVE,
                       try_unknown_filetype: bool,
                       recursive_extract: bool,
                       delete_origin: bool,
                       top_window: bool):
        """??????"""
        self.viewer.update_setting(archive_model=archive_model,
                                   try_unknown_filetype=try_unknown_filetype,
                                   recursive_extract=recursive_extract,
                                   delete_origin=delete_origin,
                                   top_window=top_window)

    def hide_float_button(self):
        """????????????"""
        self.viewer.hide_float_button()

    def set_float_button_enable(self, is_enable: bool):
        """??????????"""
        self.viewer.set_float_button_enable(is_enable)

    """??"""

    def turn_page_welcome(self):
        """??????"""
        self.viewer.turn_page_welcome()

    """?????"""

    def set_step_notice(self, notice: str):
        """??????"""
        self.viewer.set_step_notice(notice)

    """??????"""

    def set_task_count(self, count: int):
        """?????:????"""
        self._task_count = count

    def set_task_index(self, index: int):
        """?????:??????"""
        self._task_index = index
        self.viewer.set_progress_total(f'{self._task_index}/{self._task_count}')
        # ?????????
        self.model.reset_current_time()

    def set_current_file(self, filepath: str):
        """??????????"""
        filename = os.path.basename(filepath)
        self.viewer.set_current_file(filename, tooltip=filepath)

    def set_runtime_total(self, runtime: str):
        """??????? 0:00:00
        :param runtime: "0:00:00"??????"""
        self.viewer.set_runtime_total(runtime)

    def set_runtime_current(self, runtime: str):
        """??????????? 0:00:00
        :param runtime: "0:00:00"??????"""
        self.viewer.set_runtime_current(runtime)

    def set_password_count(self, count: int):
        """??????:??"""
        self._password_count = count

    def set_password_index(self, index: int):
        """??????:????"""
        self._password_index = index
        self.viewer.set_progress_test(f'{self._password_index}/{self._password_count}')

    def set_current_password(self, password: str):
        """?????????"""
        self.viewer.set_current_password(password)

    def set_progress_extract(self, progress: int):
        """??????? 1%
        :param progress: 0~100???"""
        self.viewer.set_progress_extract(progress)

    def set_current_file_step_tip(self, tip: str):
        """??????????????"""
        self.viewer.set_current_file_step_tip(tip)

    """???"""

    def show_time_final(self):
        """?????????????"""
        self.viewer.show_time_final()

    def show_process_count(self, count: Union[int, str]):
        """?????????"""
        self.viewer.show_process_count(count)

    def show_result_count(self, result_info: str, result_info_tip: str = ''):
        """?????????"""
        self.viewer.show_result_count(result_info, result_info_tip)

    """??????"""

    def set_info_testing(self):
        """?????? ???"""
        # ????
        self.set_icon_testing()
        # ??????
        self.viewer.turn_page_test_and_extract()
        self.viewer.set_child_page_test()

    def set_info_extracting(self):
        """?????? ???"""
        # ????
        self.set_icon_extracting()
        # ??????
        self.viewer.turn_page_test_and_extract()
        self.viewer.set_child_page_test()  # ???????,?????????????

    def set_info_skip(self):
        """?????? ??(??????????)"""
        # ????
        self.set_icon_skip()
        # ?????
        self.model.stop_timing()
        # ??????
        self.set_step_notice("??????????")

    def set_info_exists_temp_folder(self, path: str = ''):
        """?????? ??(????????????)"""
        # ????
        self.set_icon_warning()
        # ?????
        self.model.stop_timing()
        # ??????
        info = "?????????,???????"
        if path:
            link_text = f'<a href="file:///{path}">???????????</a>'
            info = info + '<br>' + link_text
        self.set_step_notice(info)

    def set_info_error_7zip_path(self):
        """?????? ??(7zip????)"""
        # ????
        self.set_icon_warning()
        # ?????
        self.model.stop_timing()
        # ??????
        info = "7Zip????,????????"
        self.set_step_notice(info)

    def set_info_finished(self, result_info: str, result_info_tip: str = ''):
        """?????? ??????,??"""
        # ????
        self.set_icon_complete()
        # ?????
        self.model.stop_timing()
        # ??????
        self.show_time_final()
        self.show_result_count(result_info, result_info_tip)
        # ??????????
        numbers = re.findall(r'\d+', result_info_tip)
        total_sum = sum(int(num) for num in numbers)
        self.show_process_count(total_sum)

    def show_info_stop(self, result_info: str, result_info_tip: str = ''):
        """?????? ????"""
        # ????
        self.set_icon_stop()
        # ?????
        self.model.stop_timing()
        # ??????
        self.show_time_final()
        self.show_result_count(result_info, result_info_tip)
        # ??????????
        numbers = re.findall(r'\d+', result_info_tip)
        total_sum = sum(int(num) for num in numbers)
        self.show_process_count(total_sum)

    def set_info_error(self):
        """?????? ??"""
        # ????
        self.set_icon_error()
        # ?????
        self.model.stop_timing()
        # ??????
        info = "???????,?????????\n??????????"
        self.set_step_notice(info)

    def set_icon_home(self):
        """??????"""
        self.viewer.set_icon(ICON_LOGO_PIXEL)

    def set_icon_complete(self):
        """??????"""
        self.viewer.set_icon(ICON_COMPLETE)

    def set_icon_skip(self):
        """??????"""
        self.viewer.set_icon(ICON_SKIP)

    def set_icon_stop(self):
        """??????"""
        self.viewer.set_icon(ICON_STOPPED)

    def set_icon_warning(self):
        """??????"""
        self.viewer.set_icon(ICON_WARNING)

    def set_icon_extract(self):
        """????????"""
        self.viewer.set_gif_icon(ICON_EXTRACT)

    def set_icon_test(self):
        """????????"""
        self.viewer.set_gif_icon(ICON_TEST)

    def set_icon_extracting(self):
        """???????"""
        self.viewer.set_gif_icon(ICON_EXTRACTING)

    def set_icon_testing(self):
        """???????"""
        self.viewer.set_gif_icon(ICON_TESTING)

    def set_icon_error(self):
        """??????"""
        self.viewer.set_icon(ICON_WARNING_YELLOW)
