# ?????????
# ?????,???????
import os
import sys

import lzytools
import lzytools_Qt
from PySide6.QtCore import Signal, QEvent, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog

from components.page_setting.res.icon_base64 import ICON_CHOOSE, ICON_OPEN, ICON_BLACK_LIST, ICON_WHITE_LIST
from components.page_setting.res.ui_page_setting import Ui_Form


class SettingViewer(QWidget):
    """?????????"""
    ChangeArchiveModelTest = Signal(bool, name="???????")
    ChangeArchiveModelExtract = Signal(bool, name="???????")
    ChangePreFilterModeDefault = Signal(bool, name="??????????????")
    ChangePreFilterModeBlackList = Signal(bool, name="???????????????")
    ChangePreFilterModeBlackListRule = Signal(list, name="???????????????")
    ChangePreFilterModeWhiteList = Signal(bool, name="???????????????")
    ChangePreFilterModeWhiteListRule = Signal(list, name="???????????????")
    ChangeTryUnknownFiletype = Signal(bool, name="???????????")
    ChangeReadPasswordFromFilename = Signal(bool, name="???????????")
    ChangeWriteFilename = Signal(bool, name="???????")
    ChangeWriteFilenameLeftPart = Signal(str, name="??????????")
    ChangeWriteFilenameRightPart = Signal(str, name="??????????")
    ChangeWriteFilenamePosition = Signal(str, name="????????")
    ChangeExtractModelSmart = Signal(bool, name="????????")
    ChangeExtractModelDirect = Signal(bool, name="????????")
    ChangeExtractModelSameFolder = Signal(bool, name="??????????")
    ChangeDeleteFile = Signal(bool, name="??????????")
    ChangeDeleteMode = Signal(str, name="??????")
    ChangeRecursiveExtract = Signal(bool, name="??????")
    ChangeWebpToJpg = Signal(bool, name="??webp?jpg")
    ChangeWebpDeleteSource = Signal(bool, name="??webp?????")
    ClickAdjustAreaOrder = Signal(name="????????")
    ChangeCoverModel = Signal(str, name="??????")
    ChangeBreakFolder = Signal(bool, name="???????")
    ChangeBreakFolderModel = Signal(str, name="?????????")
    ChangeExtractOutputFolder = Signal(bool, name="???????????")
    ChangeExtractOutputFolderPath = Signal(str, name="????????")
    ChangeExtractFilter = Signal(bool, name="?????????")
    ChangeExtractFilterRule = Signal(str, name="???????????")
    Change7ZipPath = Signal(str, name="??7zip??")
    ChangeTopWindow = Signal(bool, name="??????")
    ChangeLockSize = Signal(bool, name="????????")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # ???
        self._bind_signal()
        self._set_icon()

        # ?????
        self._timer_black_list_rule = QTimer()
        self._timer_black_list_rule.setInterval(1000)
        self._timer_black_list_rule.setSingleShot(True)
        self._timer_black_list_rule.timeout.connect(self._emit_black_list_rule)

        self._timer_white_list_rule = QTimer()
        self._timer_white_list_rule.setInterval(1000)
        self._timer_white_list_rule.setSingleShot(True)
        self._timer_white_list_rule.timeout.connect(self._emit_white_list_rule)

        # ?ComboBox???????,???????
        self.ui.comboBox_break_folder.installEventFilter(self)
        self.ui.comboBox_pw_position.installEventFilter(self)
        self.ui.comboBox_cover_file.installEventFilter(self)

    def lock(self):
        """???????,????"""
        self._set_enable(False)

    def unlock(self):
        """???????,????"""
        self._set_enable(True)

    def _choose_dirpath(self):
        """?????,????????"""
        dirpath = QFileDialog.getExistingDirectory(self, "????????")
        if dirpath:
            self.ui.lineEdit_extract_output_folder.setText(dirpath)

    def _choose_7zip_path(self):
        """?????,?????7zip??"""
        path, _ = QFileDialog.getOpenFileName(self, "??7Zip??", filter="7z.exe (7z.exe)")
        if path:
            path = os.path.normpath(path)
            if os.path.basename(path) == '7z.exe':
                # ??7zip????????,????????
                # ????
                app_path = sys.argv[0]
                app_parent = os.path.dirname(app_path)
                app_parent = os.path.normpath(app_parent)
                # ????
                if lzytools.file.is_subpath(app_parent, path):
                    relative_path = os.path.relpath(path, app_parent)
                    relative_path_full = os.path.join('.\\', relative_path)
                    print(relative_path_full)
                    self.ui.lineEdit_7zip_path.setText(relative_path_full)
                else:
                    self.ui.lineEdit_7zip_path.setText(path)

    def _open_dirpath(self):
        """?????????"""
        dirpath = self.ui.lineEdit_extract_output_folder.text()
        if dirpath:
            os.startfile(dirpath)

    def _set_icon(self):
        self.ui.toolButton_open_black_list.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_BLACK_LIST))
        self.ui.toolButton_open_white_list.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_WHITE_LIST))
        self.ui.toolButton_choose.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_CHOOSE))
        self.ui.toolButton_open.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_OPEN))
        self.ui.toolButton_choose_7zip_path.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_CHOOSE))

    def _set_enable(self, is_enable: bool):
        self.ui.radioButton_mode1_test.setEnabled(is_enable)
        self.ui.radioButton_mode1_extract.setEnabled(is_enable)
        self.ui.radioButton_pre_filter_mode_default.setEnabled(is_enable)
        self.ui.radioButton_pre_filter_mode_black_list.setEnabled(is_enable)
        self.ui.radioButton_pre_filter_mode_white_list.setEnabled(is_enable)
        self.ui.toolButton_open_black_list.setEnabled(is_enable)
        self.ui.toolButton_open_white_list.setEnabled(is_enable)
        self.ui.checkBox_read_password_from_filename.setEnabled(is_enable)
        self.ui.checkBox_try_unknown_filetype.setEnabled(is_enable)
        self.ui.lineEdit_7zip_path.setEnabled(is_enable)
        self.ui.widget_test.setEnabled(is_enable)
        self.ui.widget_extract.setEnabled(is_enable)

    """??????????"""

    def set_setting_model_extract(self):
        """?????????:????"""
        self.ui.radioButton_mode1_extract.setChecked(True)
        self.ui.radioButton_mode1_test.setChecked(False)
        # ??/????????
        self._show_settings_extract()
        # ????????
        self.ChangeArchiveModelExtract.emit(True)

    def set_setting_model_test(self):
        """?????????:????"""
        self.ui.radioButton_mode1_extract.setChecked(False)
        self.ui.radioButton_mode1_test.setChecked(True)
        # ??/????????
        self._show_settings_test()
        # ????????
        self.ChangeArchiveModelTest.emit(True)

    def set_setting_pre_filter_mode_default(self):
        """?????????:????"""
        self.ui.radioButton_pre_filter_mode_default.setChecked(True)
        self.ui.radioButton_pre_filter_mode_black_list.setChecked(False)
        self.ui.radioButton_pre_filter_mode_white_list.setChecked(False)

    def set_setting_pre_filter_mode_black_list(self):
        """?????????:?????"""
        self.ui.radioButton_pre_filter_mode_black_list.setChecked(True)
        self.ui.radioButton_pre_filter_mode_default.setChecked(False)
        self.ui.radioButton_pre_filter_mode_white_list.setChecked(False)

    def set_setting_pre_filter_mode_black_list_rule(self, rules: list[str]):
        """?????????:???????"""
        self.ui.textEdit_black_list.clear()
        for rule in rules:
            if rule:
                self.ui.textEdit_black_list.append(rule)

    def set_setting_pre_filter_mode_white_list(self):
        """?????????:?????"""
        self.ui.radioButton_pre_filter_mode_white_list.setChecked(True)
        self.ui.radioButton_pre_filter_mode_default.setChecked(False)
        self.ui.radioButton_pre_filter_mode_black_list.setChecked(False)

    def set_setting_pre_filter_mode_white_list_rule(self, rules: list[str]):
        """?????????:???????"""
        self.ui.textEdit_white_list.clear()
        for rule in rules:
            if rule:
                self.ui.textEdit_white_list.append(rule)

    def _show_settings_extract(self):
        """??????????,??????????"""
        self.ui.widget_extract.setVisible(True)
        self.ui.widget_test.setVisible(False)

    def _show_settings_test(self):
        """??????????,??????????"""
        self.ui.widget_extract.setVisible(False)
        self.ui.widget_test.setVisible(True)

    def set_setting_is_try_unknown_filetype(self, is_enable: bool):
        """????
        ???????????????"""
        self.ui.checkBox_try_unknown_filetype.setChecked(is_enable)

    def set_setting_is_read_password_from_filename(self, is_enable: bool):
        """????
        ???????????????"""
        self.ui.checkBox_read_password_from_filename.setChecked(is_enable)

    def set_setting_write_filename(self, is_enable: bool):
        """??????
        ???????????????????"""
        self.ui.checkBox_write_filename.setChecked(is_enable)

    def set_setting_write_filename_left_part(self, text: str):
        """??????
        ??????????????"""
        self.ui.lineEdit_left_word.setText(text)

    def set_setting_write_filename_right_part(self, text: str):
        """??????
        ??????????????"""
        self.ui.lineEdit_right_word.setText(text)

    def set_setting_write_filename_position(self, option: str):
        """??????
        ????????????
        :param option: ???comboBox????"""
        self.ui.comboBox_pw_position.setCurrentText(option)

    def set_setting_write_filename_preview(self, preview: str):
        """??????
        ???????????????"""
        self.ui.label_preview_filename.setText(preview)

    def set_setting_extract_model_smart(self):
        """??????
        ???????????(?????BandiZip)"""
        self.ui.radioButton_mode2_smart_extract.setChecked(True)
        self.ui.radioButton_mode2_direct_extract.setChecked(False)
        self.ui.radioButton_mode2_extract_same_folder.setChecked(False)

    def set_setting_extract_model_direct(self):
        """??????
        ???????????(????????)"""
        self.ui.radioButton_mode2_smart_extract.setChecked(False)
        self.ui.radioButton_mode2_direct_extract.setChecked(True)
        self.ui.radioButton_mode2_extract_same_folder.setChecked(False)

    def set_setting_extract_model_same_folder(self):
        """??????
        ??????????????(?????????????)"""
        self.ui.radioButton_mode2_smart_extract.setChecked(False)
        self.ui.radioButton_mode2_direct_extract.setChecked(False)
        self.ui.radioButton_mode2_extract_same_folder.setChecked(True)

    def set_setting_delete_file(self, is_enable: bool):
        """??????
        ??????????"""
        self.ui.checkBox_delete_origin.setChecked(is_enable)

    def set_setting_delete_mode(self, mode: str):
        """v2.2.1:??????(trash/direct)"""
        if mode == 'direct':
            self.ui.comboBox_delete_mode.setCurrentIndex(1)
        else:
            self.ui.comboBox_delete_mode.setCurrentIndex(0)

    def set_setting_webp_to_jpg(self, is_enable: bool):
        """v2.2.1:??webp?jpg"""
        self.ui.checkBox_webp_to_jpg.setChecked(is_enable)

    def set_setting_webp_delete_source(self, is_enable: bool):
        """v2.2.1:??webp??????????"""
        self.ui.checkBox_webp_delete_source.setChecked(is_enable)

    def set_setting_recursive_extract(self, is_enable: bool):
        """??????
        ?????????????????(??????????????)"""
        self.ui.checkBox_recursive_extract.setChecked(is_enable)

    def set_setting_cover_model(self, option: str):
        """??????
        ??????????
        :param option: ???comboBox????"""
        self.ui.comboBox_cover_file.setCurrentText(option)

    def set_setting_break_folder(self, is_enable: bool):
        """??????
        ??????????????????"""
        self.ui.checkBox_break_folder.setChecked(is_enable)

    def set_setting_break_folder_model(self, option: str):
        """??????
        ??????????
        :param option: ???comboBox????"""
        self.ui.comboBox_break_folder.setCurrentText(option)

    def set_setting_extract_to_folder(self, is_enable: bool):
        """??????
        ???????????"""
        self.ui.checkBox_extract_output_folder.setChecked(is_enable)

    def set_setting_extract_output_folder(self, dirpath: str):
        """??????
        ????????"""
        self.ui.lineEdit_extract_output_folder.setText(dirpath)
        self.ui.lineEdit_extract_output_folder.setToolTip(dirpath)

    def set_setting_filter(self, is_enable: bool):
        """??????
        ???????????"""
        self.ui.checkBox_extract_filter.setChecked(is_enable)

    def set_setting_filter_rule(self, rule: str):
        """??????
        ????????"""
        self.ui.plainTextEdit_extract_filter_rule.setPlainText(rule)

    def set_setting_7zip_path(self, filepath: str):
        """??7zip??"""
        self.ui.lineEdit_7zip_path.setText(filepath)

    def set_top_window(self, is_enable: bool):
        """????????"""
        self.ui.checkBox_top_window.setChecked(is_enable)

    def set_lock_size(self, is_enable: bool):
        """??????????"""
        self.ui.checkBox_lock_size.setChecked(is_enable)

    """??????????"""

    def _bind_signal(self):
        """????"""
        # ??
        self.ui.toolButton_choose.clicked.connect(self._choose_dirpath)
        self.ui.toolButton_choose_7zip_path.clicked.connect(self._choose_7zip_path)
        self.ui.toolButton_open.clicked.connect(self._open_dirpath)
        # ??
        self.ui.radioButton_mode1_extract.clicked.connect(self._change_archive_model)
        self.ui.radioButton_mode1_test.clicked.connect(self._change_archive_model)
        # ???????
        self.ui.radioButton_pre_filter_mode_default.clicked.connect(self._change_pre_filter_model)
        self.ui.radioButton_pre_filter_mode_black_list.clicked.connect(self._change_pre_filter_model)
        self.ui.radioButton_pre_filter_mode_white_list.clicked.connect(self._change_pre_filter_model)
        self.ui.textEdit_black_list.textChanged.connect(self._change_black_list_rule)
        self.ui.textEdit_white_list.textChanged.connect(self._change_white_list_rule)
        self.ui.toolButton_open_black_list.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.toolButton_open_white_list.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_return_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_return_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))

        # ??????
        self.ui.checkBox_try_unknown_filetype.stateChanged.connect(self.ChangeTryUnknownFiletype.emit)
        # ?????????
        self.ui.checkBox_read_password_from_filename.stateChanged.connect(self.ChangeReadPasswordFromFilename.emit)
        # ???????
        self.ui.checkBox_write_filename.stateChanged.connect(self.ChangeWriteFilename.emit)
        self.ui.lineEdit_left_word.textChanged.connect(self.ChangeWriteFilenameLeftPart.emit)
        self.ui.lineEdit_right_word.textChanged.connect(self.ChangeWriteFilenameRightPart.emit)
        self.ui.comboBox_pw_position.currentTextChanged.connect(self.ChangeWriteFilenamePosition.emit)
        # ????
        self.ui.radioButton_mode2_smart_extract.clicked.connect(self._change_extract_model)
        self.ui.radioButton_mode2_direct_extract.clicked.connect(self._change_extract_model)
        self.ui.radioButton_mode2_extract_same_folder.clicked.connect(self._change_extract_model)
        # ?????
        self.ui.checkBox_delete_origin.stateChanged.connect(self.ChangeDeleteFile.emit)
        # v2.2.1:????
        self.ui.comboBox_delete_mode.currentTextChanged.connect(
            lambda: self.ChangeDeleteMode.emit('direct' if self.ui.comboBox_delete_mode.currentIndex() == 1 else 'trash'))
        # v2.2.1:webp?jpg
        self.ui.checkBox_webp_to_jpg.stateChanged.connect(self.ChangeWebpToJpg.emit)
        # v2.2.1:webp?????
        self.ui.checkBox_webp_delete_source.stateChanged.connect(self.ChangeWebpDeleteSource.emit)
        # ????
        self.ui.checkBox_recursive_extract.stateChanged.connect(self.ChangeRecursiveExtract.emit)
        # ????
        self.ui.comboBox_cover_file.currentTextChanged.connect(self.ChangeCoverModel.emit)
        # ?????
        self.ui.checkBox_break_folder.stateChanged.connect(self.ChangeBreakFolder.emit)
        self.ui.comboBox_break_folder.currentTextChanged.connect(
            lambda: self.ChangeBreakFolderModel.emit(self.ui.comboBox_break_folder.currentText()))
        # ???????
        self.ui.checkBox_extract_output_folder.stateChanged.connect(self.ChangeExtractOutputFolder.emit)
        self.ui.lineEdit_extract_output_folder.textChanged.connect(self.ChangeExtractOutputFolderPath.emit)
        # ????
        self.ui.checkBox_extract_filter.stateChanged.connect(self.ChangeExtractFilter.emit)
        self.ui.plainTextEdit_extract_filter_rule.textChanged.connect(
            lambda: self.ChangeExtractFilterRule.emit(self.ui.plainTextEdit_extract_filter_rule.toPlainText()))
        # ???7Zip??
        self.ui.lineEdit_7zip_path.textChanged.connect(self.Change7ZipPath.emit)
        # ????
        self.ui.checkBox_top_window.stateChanged.connect(self.ChangeTopWindow.emit)
        # ??????
        self.ui.checkBox_lock_size.stateChanged.connect(self.ChangeLockSize.emit)
        # v2.2.1:??????
        self.ui.pushButton_adjust_area_order.clicked.connect(self.ClickAdjustAreaOrder.emit)

    def _change_archive_model(self):
        if self.ui.radioButton_mode1_extract.isChecked():
            self.ChangeArchiveModelExtract.emit(True)
            self._show_settings_extract()
        elif self.ui.radioButton_mode1_test.isChecked():
            self.ChangeArchiveModelTest.emit(True)
            self._show_settings_test()

    def _change_pre_filter_model(self):
        if self.ui.radioButton_pre_filter_mode_default.isChecked():
            self.ChangePreFilterModeDefault.emit(True)
        elif self.ui.radioButton_pre_filter_mode_black_list.isChecked():
            self.ChangePreFilterModeBlackList.emit(True)
        elif self.ui.radioButton_pre_filter_mode_white_list.isChecked():
            self.ChangePreFilterModeWhiteList.emit(True)

    def _change_extract_model(self):
        if self.ui.radioButton_mode2_smart_extract.isChecked():
            self.ChangeExtractModelSmart.emit(True)
        elif self.ui.radioButton_mode2_direct_extract.isChecked():
            self.ChangeExtractModelDirect.emit(True)
        elif self.ui.radioButton_mode2_extract_same_folder.isChecked():
            self.ChangeExtractModelSameFolder.emit(True)

    def _change_black_list_rule(self):
        self._timer_black_list_rule.start()

    def _change_white_list_rule(self):
        self._timer_white_list_rule.start()

    def _emit_black_list_rule(self):
        rule = self.ui.textEdit_black_list.toPlainText()
        rules = [i for i in rule.split('\n') if i]
        self.ChangePreFilterModeBlackListRule.emit(rules)

    def _emit_white_list_rule(self):
        rule = self.ui.textEdit_white_list.toPlainText()
        rules = [i for i in rule.split('\n') if i]
        self.ChangePreFilterModeWhiteListRule.emit(rules)

    def eventFilter(self, obj, event):
        # ??ComboBox?????
        if obj == self.ui.comboBox_break_folder and event.type() == QEvent.Wheel:
            return True
        elif obj == self.ui.comboBox_cover_file and event.type() == QEvent.Wheel:
            return True
        elif obj == self.ui.comboBox_pw_position and event.type() == QEvent.Wheel:
            return True
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = SettingViewer()
    program_ui.show()
    app_.exec()
