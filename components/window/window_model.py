# ????????

from PySide6.QtCore import Signal, QObject

from common.class_7zip import ModelExtract, ModelBreakFolder, ModelCoverFile, ModelArchive, \
    TYPES_MODEL_EXTRACT, TYPES_MODEL_COVER_FILE, TYPES_MODEL_BREAK_FOLDER, TYPES_POSITION, TYPES_MODEL_ARCHIVE
from common.class_file_info import FileInfoList, FileInfo
from components.window.thread_7zip import ThreadTest, ThreadExtract, TemplateThread


class TemplateModelSignal(QObject):
    """????,????????"""
    StepInfo = Signal(str, name='????')
    SignalCurrentFile = Signal(str, name='????????')
    SignalTaskCount = Signal(int, name='?????????')
    SignalTaskIndex = Signal(int, name='?????????')
    SignalCurrentPw = Signal(str, name='???????')
    SignalPwCount = Signal(int, name='???????')
    SignalPwIndex = Signal(int, name='?????????')
    SignalResult = Signal(FileInfo, name='????????')
    SignalStart = Signal(name='??')
    SignalFinish = Signal(FileInfoList, name='??,????????????')

    def __init__(self):
        super().__init__()

    def _transfer_signal(self, child_thread: TemplateThread):
        """????"""
        child_thread.SignalCurrentFile.connect(self.SignalCurrentFile)
        child_thread.SignalTaskCount.connect(self.SignalTaskCount)
        child_thread.SignalTaskIndex.connect(self.SignalTaskIndex)
        child_thread.SignalCurrentPw.connect(self.SignalCurrentPw)
        child_thread.SignalPwCount.connect(self.SignalPwCount)
        child_thread.SignalPwIndex.connect(self.SignalPwIndex)
        child_thread.SignalResult.connect(self.SignalResult)
        child_thread.SignalStart.connect(self.SignalStart)
        child_thread.SignalFinish.connect(self.SignalFinish)
        child_thread.StepInfo.connect(self.StepInfo)


class WindowModel(QObject):
    """????????"""
    StepInfo = Signal(str, name='????')
    SignalCurrentFile = Signal(str, name='????????')
    SignalTaskCount = Signal(int, name='?????????')
    SignalTaskIndex = Signal(int, name='?????????')
    SignalCurrentPw = Signal(str, name='???????')
    SignalPwCount = Signal(int, name='???????')
    SignalPwIndex = Signal(int, name='?????????')
    SignalResult = Signal(FileInfo, name='????????')
    SignalStart = Signal(name='??')
    SignalFinish = Signal(FileInfoList, name='??,????????????')

    def __init__(self):
        super().__init__()
        self.model_test_file = ModelTestFile()
        self.model_extract_file = ModelExtractFile()
        self.archive_model = None  # ????????

        # ????
        self._transfer_signal(self.model_test_file)
        self._transfer_signal(self.model_extract_file)

    def accept_files(self, file_info: FileInfoList):
        """???????,????/????"""
        print('??????????')
        if isinstance(self.archive_model, ModelArchive.Test):
            print('??????')
            self.model_test_file.process_file(file_info)
        elif isinstance(self.archive_model, ModelArchive.Extract):
            print('??????')
            self.model_extract_file.process_file(file_info)

    def stop_task(self):
        """????"""
        self.model_test_file.stop_task()
        self.model_extract_file.stop_task()

    def set_passwords(self, passwords: list):
        self.model_extract_file.set_passwords(passwords)
        self.model_test_file.set_passwords(passwords)

    def set_archive_model(self, archive_model: TYPES_MODEL_ARCHIVE):
        self.archive_model = archive_model

    def set_is_read_password_from_filename(self, value: bool):
        self.model_test_file.set_is_read_password_from_filename(value)
        self.model_extract_file.set_is_read_password_from_filename(value)

    def set_extract_model(self, extract_model: TYPES_MODEL_EXTRACT):
        self.model_extract_file.set_extract_model(extract_model)

    def set_is_delete_file(self, value: bool):
        self.model_extract_file.set_is_delete_file(value)

    def set_delete_mode(self, value: str):
        """v2.2.1:??????"""
        self.model_extract_file.set_delete_mode(value)

    def set_is_webp_to_jpg(self, value: bool):
        """v2.2.1:??webp?jpg"""
        self.model_extract_file.set_is_webp_to_jpg(value)

    def set_webp_delete_source(self, value: bool):
        """v2.2.1:??webp??????????"""
        self.model_extract_file.set_webp_delete_source(value)

    def set_is_recursive_extract(self, value: bool):
        self.model_extract_file.set_is_recursive_extract(value)

    def set_cover_model(self, cover_model: TYPES_MODEL_COVER_FILE):
        self.model_extract_file.set_cover_model(cover_model)

    def set_is_break_folder(self, value: bool):
        self.model_extract_file.set_is_break_folder(value)

    def set_break_folder_model(self, break_folder_model: TYPES_MODEL_BREAK_FOLDER):
        self.model_extract_file.set_break_folder_model(break_folder_model)

    def set_is_extract_to_folder(self, value: bool):
        self.model_extract_file.set_is_extract_to_folder(value)

    def set_extract_output_folder(self, value: str):
        self.model_extract_file.set_extract_output_folder(value)

    def set_is_filter(self, value: bool):
        self.model_extract_file.set_is_filter(value)

    def set_filter_rules(self, value: list):
        self.model_extract_file.set_filter_rules(value)

    def set_is_write_filename(self, value: bool):
        self.model_test_file.set_is_write_filename(value)

    def set_write_filename_left_word(self, value: str):
        self.model_test_file.set_write_filename_left_word(value)

    def set_write_filename_right_word(self, value: str):
        self.model_test_file.set_write_filename_right_word(value)

    def set_write_filename_position(self, value: TYPES_POSITION):
        self.model_test_file.set_write_filename_position(value)

    def _transfer_signal(self, child_thread: TemplateModelSignal):
        """????"""
        child_thread.SignalCurrentFile.connect(self.SignalCurrentFile)
        child_thread.SignalTaskCount.connect(self.SignalTaskCount)
        child_thread.SignalTaskIndex.connect(self.SignalTaskIndex)
        child_thread.SignalCurrentPw.connect(self.SignalCurrentPw)
        child_thread.SignalPwCount.connect(self.SignalPwCount)
        child_thread.SignalPwIndex.connect(self.SignalPwIndex)
        child_thread.SignalResult.connect(self.SignalResult)
        child_thread.SignalStart.connect(self.SignalStart)
        child_thread.SignalFinish.connect(self.SignalFinish)
        child_thread.StepInfo.connect(self.StepInfo)


class ModelTestFile(TemplateModelSignal):
    """???????"""

    def __init__(self):
        super().__init__()
        self.thread_test = ThreadTest()
        self.passwords = list()
        self.is_read_password_from_filename = False  # ???????????

        # ???????
        self._transfer_signal(self.thread_test)

    def set_passwords(self, passwords: list):
        """????"""
        self.passwords = passwords

    def set_is_read_password_from_filename(self, value: bool):
        """?????????????"""
        self.is_read_password_from_filename = value

    def stop_task(self):
        """????"""
        self.thread_test.stop_task()

    def process_file(self, file_info: FileInfoList):
        """????"""
        print('??????????,???')
        self.thread_test.set_task(file_info)
        self.thread_test.set_passwords(self.passwords)
        self.thread_test.set_is_read_pw_from_filename(self.is_read_password_from_filename)
        self.thread_test.start()

    def set_is_write_filename(self, value: bool):
        self.thread_test.is_write_filename = value

    def set_write_filename_left_word(self, value: str):
        self.thread_test.write_left_part = value

    def set_write_filename_right_word(self, value: str):
        self.thread_test.write_right_part = value

    def set_write_filename_position(self, value: TYPES_POSITION):
        self.thread_test.write_position = value


class ModelExtractFile(TemplateModelSignal):
    """???????"""

    def __init__(self):
        super().__init__()
        self.thread_extract = ThreadExtract()
        self.passwords = list()
        # ??????
        self.is_read_password_from_filename = False  # ???????????
        self.extract_model = ModelExtract.Smart()  # ????
        self.is_delete_file = False  # ??????????
        self.delete_mode = 'trash'  # v2.2.1:????(trash/direct)
        self.is_webp_to_jpg = True  # v2.2.1:webp?jpg
        self.webp_delete_source = True  # v2.2.1:webp????????
        self.is_recursive_extract = False  # ??????
        self.cover_model = ModelCoverFile.Overwrite()  # ????????
        self.is_break_folder = False  # ???????
        self.break_folder_model = ModelBreakFolder.MoveToTop()  # ????????
        self.is_extract_to_folder = False  # ??????????
        self.extract_output_folder = ''  # ???????
        self.is_filter = False  # ??????
        self.filter_rules = []  # ????

        # ???????
        self._transfer_signal(self.thread_extract)

    def set_passwords(self, passwords: list):
        self.passwords = passwords

    def set_is_read_password_from_filename(self, value: bool):
        """?????????????"""
        self.is_read_password_from_filename = value

    def stop_task(self):
        """????"""
        self.thread_extract.stop_task()

    def process_file(self, file_info: FileInfoList):
        """????"""
        print('??????????,???')
        self.thread_extract.set_task(file_info)
        self.thread_extract.set_passwords(self.passwords)
        self.thread_extract.set_is_read_pw_from_filename(self.is_read_password_from_filename)
        self.thread_extract.start()

    def set_extract_model(self, extract_model: TYPES_MODEL_EXTRACT):
        self.extract_model = extract_model

    def set_is_delete_file(self, value: bool):
        self.is_delete_file = value

    def set_delete_mode(self, value: str):
        """v2.2.1:??????"""
        self.delete_mode = value

    def set_is_webp_to_jpg(self, value: bool):
        """v2.2.1:??webp?jpg"""
        self.is_webp_to_jpg = value

    def set_webp_delete_source(self, value: bool):
        """v2.2.1:??webp??????????"""
        self.webp_delete_source = value

    def set_is_recursive_extract(self, value: bool):
        self.is_recursive_extract = value

    def set_cover_model(self, cover_model: TYPES_MODEL_COVER_FILE):
        self.cover_model = cover_model
        self._set_thread_args()

    def set_is_break_folder(self, value: bool):
        self.is_break_folder = value

    def set_break_folder_model(self, break_folder_model: TYPES_MODEL_BREAK_FOLDER):
        self.break_folder_model = break_folder_model

    def set_is_extract_to_folder(self, value: bool):
        self.is_extract_to_folder = value
        self._set_thread_args()

    def set_extract_output_folder(self, value: str):
        self.extract_output_folder = value
        self._set_thread_args()

    def set_is_filter(self, value: bool):
        self.is_filter = value
        self._set_thread_args()

    def set_filter_rules(self, value: list):
        self.filter_rules = value
        self._set_thread_args()

    def _set_thread_args(self):
        """????????"""
        # ?????
        self.thread_extract.cover_model = self.cover_model.switch
        self.thread_extract.is_extract_to_folder = self.is_extract_to_folder
        self.thread_extract.extract_output_path = self.extract_output_folder
        self.thread_extract.is_filter = self.is_filter
        self.thread_extract.filter_rules = self.filter_rules
        self.thread_extract.extract_model = self.extract_model
        self.thread_extract.is_break_folder = self.is_break_folder
        self.thread_extract.break_folder_model = self.break_folder_model
        self.thread_extract.is_delete_file = self.is_delete_file
        self.thread_extract.delete_mode = self.delete_mode
        self.thread_extract.is_webp_to_jpg = self.is_webp_to_jpg
        self.thread_extract.webp_delete_source = self.webp_delete_source
