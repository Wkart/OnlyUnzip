# ????????
import os
import sys

import lzytools
from lzytools_Qt import ObjectEmittingStream

from common import function_7zip, function_subprocess
from common.class_7zip import ModelArchive
from common.class_file_info import FileInfoList
from common.class_result_collector import ResultCollector
from components import page_home, page_password, page_setting, page_history, page_about, page_password_manager, \
    dialog_temp_password, page_error_info
from components.window.thread_queue_receiver import ThreadQueueReceiver
from components.window.window_model import WindowModel
from components.window.window_viewer import WindowViewer


class WindowPresenter:
    """????????"""

    def __init__(self, viewer: WindowViewer, model: WindowModel):
        self.viewer = viewer
        self.model = model

        # ????
        self.app_title_default = 'OnlyUnzip'  # ??????

        # ?????
        self.result_collector = ResultCollector()

        # ??????????(????)
        self.is_user_stop = False

        # ????
        if getattr(sys, 'frozen', False) or getattr(sys, '_nuitka',
                                                    False) or '__compiled__' in globals():  # frozen??PyInstaller??,_nuitka??Nuitka??
            # ????????
            # ????????
            self.stderr_stream = ObjectEmittingStream()
            # ?????????????
            self.stderr_stream.TextWritten.connect(self.show_stderr_info)
            # ??????
            sys.stderr = self.stderr_stream
        else:
            # ????????
            pass

        # ???????????
        self.page_home = page_home.get_presenter()
        self.viewer.add_page_home(self.page_home.viewer)
        self.page_password = page_password.get_presenter()
        self.viewer.add_page_password(self.page_password.viewer)
        self.page_setting = page_setting.get_presenter()
        self.viewer.add_page_setting(self.page_setting.viewer)
        self.page_history = page_history.get_presenter()
        self.viewer.add_page_history(self.page_history.viewer)
        self.page_error_info = page_error_info.get_presenter()
        self.viewer.add_page_error_info(self.page_error_info.viewer)
        self.page_about = page_about.get_viewer()
        self.viewer.add_page_about(self.page_about)
        self.page_password_manager = page_password_manager.get_presenter()
        self.viewer.add_page_password_manager(self.page_password_manager.viewer)
        self.dialog_temp_password = dialog_temp_password.get_presenter()

        # ??????
        self.queue_receiver = ThreadQueueReceiver()
        self.queue_receiver.Data.connect(self.update_extract_progress)
        self.queue_receiver.start()

        # ??
        self.set_model_setting()

        # ??????
        self._get_window_setting()

        # ????
        self.page_setting.SignalTopWindow.connect(self.top_window)
        self.page_setting.SignalLockSize.connect(self.lock_size)
        self.page_setting.SignalChangeArchiveModel.connect(self.set_app_title_suffix)
        self.page_home.FileInfo.connect(self.accept_file_info_list)  # ???????
        self.page_home.SignalNoFiles.connect(self.finished_by_no_files)
        self.page_home.SignalExistsTempFolder.connect(self.finished_by_temp_folder)
        self.page_home.SignalError7ZipPath.connect(self.finished_by_error_7zip_path)
        self.page_home.UserStop.connect(self.finished_by_user_stop)
        self.page_home.UserStopAfter.connect(self.finished_by_user_stop_after_current)
        self.page_home.OpenAbout.connect(self.open_about)
        self.page_home.OpenTempPassword.connect(self.open_temp_password)
        self.page_home.AskUpdateSetting.connect(self.set_home_setting)
        self.page_home.ChangeSettingArchiveModel.connect(self.page_setting.change_archive_model)
        self.page_home.ChangeSettingTryUnknownFiletype.connect(self.page_setting.change_unknown_filetype)
        self.page_home.ChangeSettingRecursiveExtract.connect(self.page_setting.change_recursive_extract)
        self.page_home.ChangeSettingDeleteOrigin.connect(self.page_setting.change_delete_file)
        self.page_home.ChangeSettingTopWindow.connect(self.page_setting.change_top_window)
        self.page_password.OpenPasswordManager.connect(self.open_password_manager)
        self.page_password_manager.SignalDeleted.connect(self.deleted_passwords)
        self.dialog_temp_password.WriteTODB.connect(self.write_temp_pws_to_db)
        self._bind_model_signal()
        self.viewer.PageChanged.connect(self._page_changed)

    def accept_paths_from_cmd(self, paths: list):
        """???????"""
        self.is_user_stop = False
        self.page_home.drop_paths(paths)

    def accept_file_info_list(self, file_info: FileInfoList):
        """???????,???????"""
        self.is_user_stop = False
        # ?????,?????
        self.page_setting.lock_setting()
        # ?????????
        self.page_home.banned_drop()
        # ??????????????
        self.set_model_passwords()
        self.set_model_setting()
        # ???????
        self.show_page_test_or_extract()
        self.model.accept_files(file_info)

    def set_model_passwords(self):
        """????????????????"""
        passwords = self.page_password.get_passwords()
        temp_passwords = self.dialog_temp_password.get_passwords()
        joined = temp_passwords + passwords
        joined = lzytools.common.dedup_list(joined)
        self.model.set_passwords(joined)

    def set_model_setting(self):
        """???????????????"""
        archive_model = self.page_setting.model.get_model_archive()
        self.model.set_archive_model(archive_model)

        read_pw_from_filename = self.page_setting.model.get_read_password_from_filename_is_enable()
        self.model.set_is_read_password_from_filename(read_pw_from_filename)

        is_write_filename = self.page_setting.model.get_write_filename_is_enable()
        write_filename_left_part = self.page_setting.model.get_write_filename_left_word()
        write_filename_right_part = self.page_setting.model.get_write_filename_right_word()
        write_filename_position = self.page_setting.model.get_write_filename_position()
        self.model.set_is_write_filename(is_write_filename)
        self.model.set_write_filename_left_word(write_filename_left_part)
        self.model.set_write_filename_right_word(write_filename_right_part)
        self.model.set_write_filename_position(write_filename_position)

        extract_model = self.page_setting.model.get_model_extract()
        self.model.set_extract_model(extract_model)

        delete_file = self.page_setting.model.get_delete_file_is_enable()
        self.model.set_is_delete_file(delete_file)

        delete_mode = self.page_setting.model.get_delete_file_mode()
        self.model.set_delete_mode(delete_mode)

        webp_to_jpg = self.page_setting.model.get_webp_to_jpg_is_enable()
        self.model.set_is_webp_to_jpg(webp_to_jpg)

        webp_delete_source = self.page_setting.model.get_webp_delete_source_is_enable()
        self.model.set_webp_delete_source(webp_delete_source)

        recursive_extract = self.page_setting.model.get_recursive_extract_is_enable()
        self.model.set_is_recursive_extract(recursive_extract)

        cover_model = self.page_setting.model.get_model_cover()
        self.model.set_cover_model(cover_model)

        is_break_folder = self.page_setting.model.get_break_folder_is_enable()
        break_folder_model = self.page_setting.model.get_break_folder_model()
        self.model.set_is_break_folder(is_break_folder)
        self.model.set_break_folder_model(break_folder_model)

        is_extract_to_folder = self.page_setting.model.get_extract_output_folder_is_enable()
        extract_output_folder = self.page_setting.model.get_extract_output_folder_path()
        self.model.set_is_extract_to_folder(is_extract_to_folder)
        self.model.set_extract_output_folder(extract_output_folder)

        is_filter = self.page_setting.model.get_extract_filter_is_enable()
        filter_rule = self.page_setting.model.get_extract_filter_rules()
        self.model.set_is_filter(is_filter)
        self.model.set_filter_rules(filter_rule)

    def show_page_test_or_extract(self):
        """????????????"""
        archive_model = self.page_setting.model.get_model_archive()
        if isinstance(archive_model, ModelArchive.Test):
            self.page_home.set_info_testing()
        elif isinstance(archive_model, ModelArchive.Extract):
            self.page_home.set_info_extracting()

        self.viewer.hide_button_error_info()

    def show_stderr_info(self, info: str):
        """??????"""
        # ??????
        self.page_home.set_info_error()
        # ????????????
        self.page_error_info.append_info(info)
        # ????????
        self.viewer.open_page_error_info()
        # ?????????
        self.viewer.show_button_error_info()

    def open_about(self):
        self.viewer.open_page_about()

    def open_temp_password(self):
        self.dialog_temp_password.exec()

    def set_home_setting(self):
        """???????????????"""
        archive_model = self.page_setting.model.get_model_archive()
        try_unknown_filetype = self.page_setting.model.get_try_unknown_filetype_is_enable()
        delete_file = self.page_setting.model.get_delete_file_is_enable()
        recursive_extract = self.page_setting.model.get_recursive_extract_is_enable()
        top_window = self.page_setting.model.get_top_window_is_enable()

        self.page_home.update_setting(archive_model=archive_model,
                                      try_unknown_filetype=try_unknown_filetype,
                                      recursive_extract=recursive_extract,
                                      delete_origin=delete_file,
                                      top_window=top_window)

    def write_temp_pws_to_db(self):
        """??????????"""
        temp_pws = self.dialog_temp_password.get_passwords()
        self.page_password.update_password(temp_pws)

    def finished(self, results: FileInfoList):
        """??????"""
        # ?????
        self.page_setting.unlock_setting()

        # ?????????
        self.page_home.allowed_drop()

        # ????????,???????,??????
        self.collect_result(results)

        # ??????????,????????????
        passwords_success = results.get_success_passwords()
        print('???????', passwords_success)

        # ???????????(??????????,?????????????)
        db_passwords = self.page_password.get_passwords()
        temp_passwords = self.dialog_temp_password.get_passwords()
        filter_passwords = passwords_success
        for pw in passwords_success:
            if pw in temp_passwords and pw not in db_passwords:
                filter_passwords.remove(pw)

        # ??????
        if filter_passwords:
            self.page_password.update_use_count(filter_passwords)
            self.page_password.show_pw_count_info()

        # ??????????,???????????
        print('????????', results)
        if not self.is_user_stop and not results.is_user_stop() and results.count_success():
            is_recursive_extract = self.page_setting.model.get_recursive_extract_is_enable()
            # ??????,???????
            if is_recursive_extract:
                success_filepaths = results.get_success_files()
                self.page_home.drop_paths(success_filepaths, is_recursive=True)
            # ???????????,????????,??????
            else:
                result_info_simple, file_info_detail = self.result_collector.get_result_info()
                self.page_home.set_info_finished(result_info_simple, result_info_tip=file_info_detail)
        else:
            result_info_simple, file_info_detail = self.result_collector.get_result_info()
            self.page_home.set_info_finished(result_info_simple, result_info_tip=file_info_detail)

    def finished_by_no_files(self):
        """????:????????-?????????"""
        # ?????
        self.page_setting.unlock_setting()
        # ?????????
        self.page_home.allowed_drop()
        # ?????????????,?????Skip??,??????????(??????????????)
        if not self.result_collector.get_count_all_result():
            self.page_home.set_info_skip()
        else:
            finish_info_simple, file_info_detail = self.result_collector.get_result_info()
            self.page_home.set_info_finished(finish_info_simple, result_info_tip=file_info_detail)

    def finished_by_temp_folder(self, path: str = ''):
        """????:????????-???????"""
        # ?????
        self.page_setting.unlock_setting()

        # ?????????
        self.page_home.allowed_drop()

        self.page_home.set_info_exists_temp_folder(path)

    def finished_by_error_7zip_path(self, path: str = ''):
        """????:????????-7zip????"""
        # ?????
        self.page_setting.unlock_setting()

        # ?????????
        self.page_home.allowed_drop()

        self.page_home.set_info_error_7zip_path()

    def finished_by_user_stop(self):
        """????:??????"""
        # ?????
        self.page_setting.unlock_setting()
        # ?????????
        self.page_home.allowed_drop()
        # ??????
        finish_info_simple, file_info_detail = self.result_collector.get_result_info()
        self.page_home.set_info_finished(finish_info_simple, result_info_tip=file_info_detail)
        # ??????
        self.is_user_stop = True
        self.model.stop_task()
        process = function_7zip.get_running_process()
        function_subprocess.stop_process(process)

    def finished_by_user_stop_after_current(self):
        """????:??????(????,??????????)"""
        self.is_user_stop = True
        self.model.stop_task()

    def update_extract_progress(self, progress: int):
        """??????"""
        self.page_home.set_progress_extract(progress)

    def collect_result(self, results: FileInfoList):
        """????,???????????????"""
        for file_info in results.get_file_infos():
            result = file_info.get_7zip_result()
            self.result_collector.add_result(result)

    @staticmethod
    def delete_temp_folder_if_exists(results: FileInfoList):
        """????????????"""
        for file_info in results.get_file_infos():
            extract_path = file_info.extract_path
            # ??????????????????????
            if extract_path:
                parent_folder = os.path.dirname(extract_path)
                temp_folder = function_7zip.get_temp_dirpath(parent_folder)
                if os.path.exists(temp_folder):
                    lzytools.file.delete_empty_folder(temp_folder, send_to_trash=False)

    def top_window(self, is_enable: bool):
        """??????"""
        if is_enable:
            self.viewer.top_window()
        else:
            self.viewer.disable_top_window()

    def lock_size(self, is_enable: bool):
        """??????"""
        if is_enable:
            self.viewer.lock_size()
            self.page_setting.model.set_lock_size_width(self.viewer.width())
            self.page_setting.model.set_lock_size_height(self.viewer.height())
        else:
            self.viewer.disable_lock_size()

    def set_default_app_title(self, title: str):
        """????????"""
        self.app_title_default = title
        self.viewer.setWindowTitle(title)
        self.set_app_title_suffix()

    def set_app_title_suffix(self):
        """??????????:[??]/[??]"""
        archive_model = self.page_setting.get_archive_model()
        suffix = ''
        if isinstance(archive_model, ModelArchive.Test):
            suffix = '[??]'
        elif isinstance(archive_model, ModelArchive.Extract):
            suffix = '[??]'

        new_title = f'{self.app_title_default} {suffix}'
        self.viewer.setWindowTitle(new_title)

    def _get_window_setting(self):
        """??window????"""
        is_top_window = self.page_setting.model.get_top_window_is_enable()
        self.top_window(is_top_window)

        is_lock_size = self.page_setting.model.get_lock_size_is_enable()
        if is_lock_size:
            width = self.page_setting.model.get_lock_size_width()
            height = self.page_setting.model.get_lock_size_height()
            self.viewer.resize(width, height)
        self.lock_size(is_lock_size)

    def open_password_manager(self):
        """???????"""
        self.viewer.open_page_password_manager()
        self.page_password_manager.update_count()
        self.page_password_manager.hidden_preview()

    def deleted_passwords(self):
        """???????????"""
        self.page_password.reload()
        self.page_password.show_pw_count_info()
        self.open_password_manager()

    def _page_changed(self):
        """????????"""
        self.page_home.hide_float_button()

    def _bind_model_signal(self):
        """??????,???????"""
        self.model.SignalCurrentFile.connect(self.page_home.set_current_file)
        self.model.SignalTaskCount.connect(self.page_home.set_task_count)
        self.model.SignalTaskIndex.connect(self.page_home.set_task_index)
        self.model.SignalCurrentPw.connect(self.page_home.set_current_password)
        self.model.SignalPwCount.connect(self.page_home.set_password_count)
        self.model.SignalPwIndex.connect(self.page_home.set_password_index)
        self.model.SignalResult.connect(self.page_history.collection_history)
        # self.model.SignalStart.connect(None)
        self.model.SignalFinish.connect(self.finished)
        self.model.StepInfo.connect(self.page_home.set_current_file_step_tip)
