# ?????????
# ????Viewer???,?????????Model????????,???Viewer??
from PySide6.QtCore import QObject, Signal

from common.class_7zip import ModelArchive, ModelExtract, TYPES_MODEL_ARCHIVE, ModelPreFilter
from components.page_setting.setting_model import SettingModel
from components.page_setting.setting_viewer import SettingViewer


class SettingPresenter(QObject):
    """?????????"""
    SignalTopWindow = Signal(bool, name='??????')
    SignalLockSize = Signal(bool, name='????????')
    SignalChangeArchiveModel = Signal(object, name='??????????')

    def __init__(self, viewer: SettingViewer, model: SettingModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        # ???
        self._load_setting()  # ?? ????????????????UI,????????????
        self._bind_signal()

    def get_archive_model(self):
        """????????????? ??/??"""
        return self.model.get_model_archive()

    def get_extract_output_folder(self):
        """????????,????????"""
        is_enable = self.model.get_extract_output_folder_is_enable()
        path = self.model.get_extract_output_folder_path()
        if is_enable and path:
            return path
        else:
            return None

    def get_is_try_unknown_filetype(self):
        """???????????????"""
        return self.model.get_try_unknown_filetype_is_enable()

    def update_filename_with_pw_preview(self):
        """????????????"""
        self.viewer.set_setting_write_filename_preview(self.model.get_write_filename_preview())

    def lock_setting(self):
        """?????,?????"""
        self.viewer.lock()

    def unlock_setting(self):
        """?????,?????"""
        self.viewer.unlock()

    def change_archive_model(self, archive_model: TYPES_MODEL_ARCHIVE):
        """????????????"""
        if isinstance(archive_model, ModelArchive.Test):
            self.viewer.set_setting_model_test()
        elif isinstance(archive_model, ModelArchive.Extract):
            self.viewer.set_setting_model_extract()
        else:
            raise Exception(archive_model, "??????")

    def change_unknown_filetype(self, is_enable: bool):
        """?????????????????"""
        self.viewer.set_setting_is_try_unknown_filetype(is_enable)

    def change_recursive_extract(self, is_enable: bool):
        """??????????"""
        self.viewer.set_setting_recursive_extract(is_enable)

    def change_delete_file(self, is_enable: bool):
        """??????????"""
        self.viewer.set_setting_delete_file(is_enable)

    def change_top_window(self, is_enable: bool):
        """??????????"""
        self.viewer.set_top_window(is_enable)

    def _bind_signal(self):
        """??Viewer??"""
        self.viewer.ChangeArchiveModelTest.connect(self.model.set_model_archive_test)
        self.viewer.ChangeArchiveModelTest.connect(self.SignalChangeArchiveModel.emit)
        self.viewer.ChangeArchiveModelExtract.connect(self.model.set_model_archive_extract)
        self.viewer.ChangeArchiveModelExtract.connect(self.SignalChangeArchiveModel.emit)
        self.viewer.ChangePreFilterModeDefault.connect(self.model.set_model_pre_filter_default)
        self.viewer.ChangePreFilterModeBlackList.connect(self.model.set_model_pre_filter_blacklist)
        self.viewer.ChangePreFilterModeBlackListRule.connect(self.model.set_model_pre_filter_blacklist_rule)
        self.viewer.ChangePreFilterModeWhiteList.connect(self.model.set_model_pre_filter_whitelist)
        self.viewer.ChangePreFilterModeWhiteListRule.connect(self.model.set_model_pre_filter_whitelist_rule)
        self.viewer.ChangeTryUnknownFiletype.connect(self.model.set_try_unknown_filetype_is_enable)
        self.viewer.ChangeReadPasswordFromFilename.connect(self.model.set_read_password_from_filename_is_enable)
        self.viewer.ChangeWriteFilename.connect(self.model.set_write_filename_is_enable)
        self.viewer.ChangeWriteFilenameLeftPart.connect(self.model.set_write_filename_left_word)
        self.viewer.ChangeWriteFilenameLeftPart.connect(self.update_filename_with_pw_preview)
        self.viewer.ChangeWriteFilenameRightPart.connect(self.model.set_write_filename_right_word)
        self.viewer.ChangeWriteFilenameRightPart.connect(self.update_filename_with_pw_preview)
        self.viewer.ChangeWriteFilenamePosition.connect(self.model.set_write_filename_position)
        self.viewer.ChangeWriteFilenamePosition.connect(self.update_filename_with_pw_preview)
        self.viewer.ChangeExtractModelSmart.connect(self.model.set_model_extract_smart)
        self.viewer.ChangeExtractModelDirect.connect(self.model.set_model_extract_direct)
        self.viewer.ChangeExtractModelSameFolder.connect(self.model.set_model_extract_same_folder)
        self.viewer.ChangeDeleteFile.connect(self.model.set_delete_file_is_enable)
        self.viewer.ChangeDeleteMode.connect(self.model.set_delete_file_mode)
        self.viewer.ChangeWebpToJpg.connect(self.model.set_webp_to_jpg_is_enable)
        self.viewer.ChangeWebpDeleteSource.connect(self.model.set_webp_delete_source_is_enable)
        self.viewer.ClickAdjustAreaOrder.connect(self._adjust_area_order)
        self.viewer.ChangeRecursiveExtract.connect(self.model.set_recursive_extract_is_enable)
        self.viewer.ChangeCoverModel.connect(self.model.set_model_cover)
        self.viewer.ChangeBreakFolder.connect(self.model.set_break_folder_is_enable)
        self.viewer.ChangeBreakFolderModel.connect(self.model.set_break_folder_model)
        self.viewer.ChangeExtractOutputFolder.connect(self.model.set_extract_output_folder_is_enable)
        self.viewer.ChangeExtractOutputFolderPath.connect(self.model.set_extract_output_folder_path)
        self.viewer.ChangeExtractFilter.connect(self.model.set_extract_filter_is_enable)
        self.viewer.ChangeExtractFilterRule.connect(self.model.set_extract_filter_rules)
        self.viewer.Change7ZipPath.connect(self.model.set_7zip_path)
        self.viewer.ChangeTopWindow.connect(self.model.set_top_window_is_enable)
        self.viewer.ChangeTopWindow.connect(self.SignalTopWindow.emit)
        self.viewer.ChangeLockSize.connect(self.model.set_lock_size_is_enable)
        self.viewer.ChangeLockSize.connect(self.SignalLockSize.emit)

    def _load_setting(self):
        """??????,??Viewer"""
        archive_model = self.model.get_model_archive()
        if isinstance(archive_model, ModelArchive.Test):
            self.viewer.set_setting_model_test()
        elif isinstance(archive_model, ModelArchive.Extract):
            self.viewer.set_setting_model_extract()
        else:
            raise Exception(archive_model, "??????")

        pre_filter_model = self.model.get_model_pre_filter()
        if isinstance(pre_filter_model, ModelPreFilter.Default):
            self.viewer.set_setting_pre_filter_mode_default()
        elif isinstance(pre_filter_model, ModelPreFilter.BlackList):
            self.viewer.set_setting_pre_filter_mode_black_list()
        elif isinstance(pre_filter_model, ModelPreFilter.WhiteList):
            self.viewer.set_setting_pre_filter_mode_white_list()
        else:
            raise Exception(pre_filter_model, "??????")

        self.viewer.set_setting_pre_filter_mode_black_list_rule(
            self.model.get_model_pre_filter_blacklist_rule())
        self.viewer.set_setting_pre_filter_mode_white_list_rule(
            self.model.get_model_pre_filter_whitelist_rule())

        self.viewer.set_setting_is_try_unknown_filetype(self.model.get_try_unknown_filetype_is_enable())
        self.viewer.set_setting_is_read_password_from_filename(self.model.get_read_password_from_filename_is_enable())

        self.viewer.set_setting_write_filename(self.model.get_write_filename_is_enable())
        self.viewer.set_setting_write_filename_left_part(self.model.get_write_filename_left_word())
        self.viewer.set_setting_write_filename_right_part(self.model.get_write_filename_right_word())
        self.viewer.set_setting_write_filename_position(self.model.get_write_filename_position_str())
        self.viewer.set_setting_write_filename_preview(self.model.get_write_filename_preview())

        extract_model = self.model.get_model_extract()
        if isinstance(extract_model, ModelExtract.Smart):
            self.viewer.set_setting_extract_model_smart()
        elif isinstance(extract_model, ModelExtract.Direct):
            self.viewer.set_setting_extract_model_direct()
        elif isinstance(extract_model, ModelExtract.SameFolder):
            self.viewer.set_setting_extract_model_same_folder()
        else:
            raise Exception(extract_model, "??????")

        self.viewer.set_setting_delete_file(self.model.get_delete_file_is_enable())
        self.viewer.set_setting_delete_mode(self.model.get_delete_file_mode())
        self.viewer.set_setting_webp_to_jpg(self.model.get_webp_to_jpg_is_enable())
        self.viewer.set_setting_webp_delete_source(self.model.get_webp_delete_source_is_enable())

        self.viewer.set_setting_recursive_extract(self.model.get_recursive_extract_is_enable())

        self.viewer.set_setting_cover_model(self.model.get_model_cover_str())

        self.viewer.set_setting_break_folder(self.model.get_break_folder_is_enable())
        self.viewer.set_setting_break_folder_model(self.model.get_break_folder_model_str())

        self.viewer.set_setting_extract_to_folder(self.model.get_extract_output_folder_is_enable())
        self.viewer.set_setting_extract_output_folder(self.model.get_extract_output_folder_path())

        self.viewer.set_setting_filter(self.model.get_extract_filter_is_enable())

        self.viewer.set_setting_filter_rule(self.model.get_extract_filter_rules_str())

        self.viewer.set_setting_7zip_path(self.model.get_7zip_path())

        self.viewer.set_top_window(self.model.get_top_window_is_enable())

        self.viewer.set_lock_size(self.model.get_lock_size_is_enable())

    def _adjust_area_order(self):
        """v2.2.1:????????"""
        from PySide6.QtWidgets import QInputDialog, QMessageBox
        areas = ['?????', '???', '????', '????', '????']
        current_order = self.model.get_area_order()
        if current_order:
            current_list = current_order.split(',')
        else:
            current_list = areas
        text, ok = QInputDialog.getText(
            None, '??????',
            '??????(????):\n' + '\n'.join([f'{i+1}. {a}' for i, a in enumerate(current_list)]),
            text=','.join(current_list))
        if ok and text:
            self.model.set_area_order(text.strip())
            QMessageBox.information(None, '??', '???????,???????')
