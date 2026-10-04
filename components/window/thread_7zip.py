import os
import time

import lzytools
import lzytools_archive
from PySide6.QtCore import QThread, Signal

from common import function_move, function_file, function_filename, function_7zip
from common.class_7zip import Result7zip, ModelCoverFile, ModelExtract, ModelBreakFolder, Position, \
    TYPES_MODEL_EXTRACT, TYPES_MODEL_BREAK_FOLDER
from common.class_file_info import FileInfo, FileInfoList


def _convert_webp_to_jpg_in_folder(folder_path: str, delete_source: bool = True):
    """v2.2.1:????????webp?????jpg??
    :param folder_path: ?????????
    :param delete_source: ????????webp??"""
    try:
        from PIL import Image
    except ImportError:
        print('Pillow???,??webp?jpg')
        return

    converted_count = 0
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith('.webp'):
                webp_path = os.path.join(root, filename)
                jpg_path = os.path.splitext(webp_path)[0] + '.jpg'
                try:
                    img = Image.open(webp_path)
                    # ??RGBA??(webp???????)
                    if img.mode in ('RGBA', 'P'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    else:
                        img = img.convert('RGB')
                    img.save(jpg_path, 'JPEG', quality=95)
                    img.close()
                    # v2.2.1:???????????webp??
                    if delete_source:
                        lzytools.file.delete(webp_path, send_to_trash=False)
                    converted_count += 1
                except Exception as e:
                    print(f'webp?jpg??: {webp_path}, ??: {e}')
    if converted_count > 0:
        print(f'webp?jpg??,??? {converted_count} ???')


class TemplateThread(QThread):
    """?????"""
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
        self.fileinfo_task: FileInfoList = None  # ???????????
        self.passwords = list()  # ????
        self.is_read_pw_from_filename = False  # ???????????
        self.is_stop_task = False  # ??????

    def set_task(self, task: FileInfoList):
        """??????"""
        print('??????')
        self.fileinfo_task = task

    def set_passwords(self, passwords: list):
        """??????"""
        print('??????')
        self.passwords = passwords.copy()

        if function_7zip.FAKE_PASSWORD not in self.passwords:
            self.passwords.insert(0, function_7zip.FAKE_PASSWORD)

    def set_is_read_pw_from_filename(self, is_enable: bool):
        """?????????????"""
        self.is_read_pw_from_filename = is_enable

    def stop_task(self):
        """????"""
        self.is_stop_task = True

    def _run_command_l_with_fake_password(self, file: str):
        """????????l????,???????????????
        :return:True,????l??????
               False,????l??????
               Result7zip?,????,??????"""
        self.StepInfo.emit('?????????...')
        print('??????')
        _7ZIP_PATH = function_7zip.get_7zip_path()
        test_result = function_7zip.process_7zip_l(_7ZIP_PATH, file, function_7zip.FAKE_PASSWORD)
        # ???Success,????????,??????l????
        if isinstance(test_result, Result7zip.Success):
            return False
        # ???Result7zip.WrongPassword,?????l??????
        elif isinstance(test_result, Result7zip.WrongPassword):
            return True
        # ???Result7zip.WrongFiletype,?????(??,???????????7zip????????????,?????????)
        # elif isinstance(test_result, Result7zip.WrongFiletype):
        #     return True
        # ?????????,???????,???????
        elif isinstance(test_result, (Result7zip.WrongFiletype, Result7zip.Skip, Result7zip.Warning, Result7zip.MissingVolume,
                             Result7zip.UnknownError, Result7zip.ErrorCommand, Result7zip.NotEnoughMemory,
                             Result7zip.UserStopped)):
            return test_result
        else:
            return False


class ThreadTest(TemplateThread):
    """?????"""

    def __init__(self):
        super().__init__()
        self.is_write_filename = False
        self.write_left_part = ''
        self.write_right_part = ''
        self.write_position = Position.Left()

    def run(self):
        print('???????')
        self.is_stop_task = False
        self.SignalStart.emit()
        self.SignalPwCount.emit(len(self.passwords))
        self.SignalTaskCount.emit(self.fileinfo_task.count())

        for index, file_info in enumerate(self.fileinfo_task.get_file_infos(), start=1):
            if self.is_stop_task:
                break
            else:
                pass

            self.SignalTaskIndex.emit(index)
            file_info: FileInfo
            file_first = file_info.filepath
            self.SignalCurrentFile.emit(file_first)
            print('???????:', file_first)
            test_result = self.test_file(file_first, self.passwords)

            # ???????,????????
            if isinstance(test_result, Result7zip.Success):
                # ??????????
                if self.is_write_filename:
                    right_password = test_result.password
                    self._write_to_filename(file_info, right_password)

            # ??????????,?????
            file_info.set_7zip_result(test_result)
            if isinstance(test_result, Result7zip.Success):
                file_info.set_password(test_result.password)
            self.SignalResult.emit(file_info)

        # ?????????
        self.SignalFinish.emit(self.fileinfo_task)

    def test_file(self, filepath: str, passwords: list):
        """??????"""
        # ????????
        if not os.path.exists(filepath):
            return Result7zip.Skip()

        # ???????????????????
        if self.is_read_pw_from_filename:
            _filetitle = lzytools_archive.get_filetitle(os.path.basename(filepath))
            pws_filename = function_filename.read_password_from_filename(_filetitle)
            for _pw in pws_filename:
                if _pw and _pw not in passwords:
                    passwords.append(_pw)

        # ?????????,??????????l?t??(l???t????,????l??)
        print('???? ??????????')
        fake_result = self._run_command_l_with_fake_password(filepath)
        # ???????????,l?t???????????,?????
        smallest_file_path_inside = function_7zip.get_smallest_file_in_archive(filepath)
        print(f"???? {smallest_file_path_inside}")
        if fake_result is True:  # ????l????????
            print('??l????????')
            for index_pw, pw in enumerate(passwords, start=1):
                if self.is_stop_task:
                    break
                else:
                    pass
                self.SignalPwIndex.emit(index_pw)
                self.SignalCurrentPw.emit(pw)
                _7ZIP_PATH = function_7zip.get_7zip_path()
                final_result = function_7zip.process_7zip_l(_7ZIP_PATH, filepath, pw,
                                                            smallest_file_path_inside)
                # ???????????,???????,??????
                if isinstance(final_result, Result7zip.WrongPassword):
                    continue
                else:
                    break
        elif fake_result is False:  # ?????l??,????t??
            print('??t????????')
            for index_pw, pw in enumerate(passwords, start=1):
                if self.is_stop_task:
                    break
                else:
                    pass
                self.SignalPwIndex.emit(index_pw)
                self.SignalCurrentPw.emit(pw)
                _7ZIP_PATH = function_7zip.get_7zip_path()
                final_result = function_7zip.process_7zip_t(_7ZIP_PATH, filepath, pw,
                                                            smallest_file_path_inside)
                # ???????????,???????,??????
                if isinstance(final_result, Result7zip.WrongPassword):
                    continue
                else:
                    break
        else:  # ????????,???????,???????
            print('???????????????,???????')
            final_result = fake_result

        # ??????
        try:
            return final_result
        except:
            return fake_result

    def _write_to_filename(self, file_info: FileInfo, password: str):
        """????????"""
        # ?????????,??????
        if password == function_7zip.FAKE_PASSWORD:
            return
        # ??????
        position = self.write_position
        left_part = self.write_left_part
        right_part = self.write_right_part
        if isinstance(position, Position.Left) and not right_part:  # ????????????????
            right_part = ' '
        elif isinstance(position, Position.Right) and not left_part:
            left_part = ' '
        pw_part = f'{left_part}{password}{right_part}'

        # ??????????(??????,??????????,??????????)
        if file_info.related_files:
            files_need_to_change = list(file_info.related_files)
        else:
            files_need_to_change = [file_info.filepath]

        # ?????
        for file in files_need_to_change:
            filename = os.path.basename(file)
            filetitle = lzytools_archive.get_filetitle(filename)
            extension = filename.replace(filetitle, '', 1)
            # ???????
            if isinstance(position, Position.Left):
                new_filename = f'{pw_part}{filetitle}{extension}'
            elif isinstance(position, Position.Right):
                new_filename = f'{filetitle}{pw_part}{extension}'
            else:
                raise Exception('??????')
            # ???
            new_filepath = os.path.join(os.path.dirname(file), new_filename)
            os.rename(file, new_filepath)


class ThreadExtract(TemplateThread):
    """?????"""

    def __init__(self):
        super().__init__()
        # ?????
        self.cover_model: str = ''
        self.is_extract_to_folder: bool = False
        self.extract_output_path: str = ''
        self.is_filter: bool = False
        self.filter_rules: list = []
        self.is_delete_file: bool = True
        self.delete_mode: str = 'trash'  # v2.2.1:????(trash/direct)
        self.is_webp_to_jpg: bool = True  # v2.2.1:???webp?jpg
        self.webp_delete_source: bool = True  # v2.2.1:webp????????
        self.last_temp_folder = ''  # ???????????,?????????????

        # ?????
        self.extract_model: TYPES_MODEL_EXTRACT = None  # ????
        self.is_break_folder: bool = False  # ???????
        self.break_folder_model: TYPES_MODEL_BREAK_FOLDER = None

    def run(self):
        print('???????')
        self.is_stop_task = False
        self.SignalStart.emit()
        self.SignalPwCount.emit(len(self.passwords))
        self.SignalTaskCount.emit(self.fileinfo_task.count())

        for index, file_info in enumerate(self.fileinfo_task.get_file_infos(), start=1):
            if self.is_stop_task:
                break
            else:
                pass

            self.SignalTaskIndex.emit(index)
            file_info: FileInfo
            file_first = file_info.filepath
            self.SignalCurrentFile.emit(file_first)
            print('???????:', file_first)

            # ????????/???????
            if self.is_extract_to_folder and self.extract_output_path:
                part_extract_to = self.extract_output_path
            else:
                part_extract_to = os.path.dirname(file_first)
            guess_temp_folder = function_7zip.get_temp_dirpath(part_extract_to, file_first)
            if self.last_temp_folder:
                if self.last_temp_folder.lower() == guess_temp_folder.lower():
                    pass
                else:
                    if os.path.exists(self.last_temp_folder) and not lzytools.file.get_size(self.last_temp_folder):
                        lzytools.file.delete(self.last_temp_folder)
            else:
                pass
            self.last_temp_folder = guess_temp_folder

            extract_result, extract_path = self.extract_file(file_first, self.passwords)

            # ??????????,?????
            file_info.set_7zip_result(extract_result)
            if isinstance(extract_result, Result7zip.Success):
                file_info.set_password(extract_result.password)
                file_info.set_extract_path(extract_path)
            self.SignalResult.emit(file_info)

        # ??????????????
        if os.path.exists(self.last_temp_folder) and not lzytools.file.get_size(self.last_temp_folder):
            lzytools.file.delete(self.last_temp_folder)
        self.last_temp_folder = ''

        # ?????????
        self.SignalFinish.emit(self.fileinfo_task)

    def extract_file(self, filepath: str, passwords: list):
        # ????????
        if not os.path.exists(filepath):
            return Result7zip.Skip(), None

        # ???????????????????
        if self.is_read_pw_from_filename:
            _filetitle = lzytools_archive.get_filetitle(os.path.basename(filepath))
            pws_filename = function_filename.read_password_from_filename(_filetitle)
            for _pw in pws_filename:
                if _pw not in passwords:
                    passwords.append(_pw)

        # ?????????,?????????????
        print('???? ??????????')
        fake_result = self._run_command_l_with_fake_password(filepath)
        if fake_result is True:  # ????l????????
            print('??l????????,???????????')
            final_result, extract_path = self.extract_after_test_l(filepath, passwords)
        elif fake_result is False:  # ???lt??,????x??????
            print('????x??????')
            final_result, extract_path = self.extract_with_test_x(filepath, passwords)
        else:  # ??????????,???????
            final_result = fake_result
            extract_path = None

        return final_result, extract_path

    def extract_after_test_l(self, filepath: str, passwords: list):
        """??l??????,????????????????,???????"""
        # ???????????,l?t???????????,?????
        self.StepInfo.emit('?????????...')
        smallest_file_path_inside = function_7zip.get_smallest_file_in_archive(filepath)
        # ???,????????
        final_result = None  # ????
        extract_path = None  # ??????,??????????
        for index_pw, pw in enumerate(passwords, start=1):
            if self.is_stop_task:
                break
            else:
                pass

            self.SignalPwIndex.emit(index_pw)
            self.SignalCurrentPw.emit(pw)
            _7ZIP_PATH = function_7zip.get_7zip_path()
            final_result = function_7zip.process_7zip_l(_7ZIP_PATH, filepath, pw,
                                                        smallest_file_path_inside)
            # ??????????,???????
            if isinstance(final_result, Result7zip.Success):
                true_password = pw
                final_result, extract_path = self.extract(filepath, true_password)
                break
            # ????????????,?????
            elif isinstance(final_result, Result7zip.WrongPassword):
                pass
            # ???????????,?????
            else:
                break

        return final_result, extract_path

    def extract_with_test_x(self, filepath: str, passwords: list):
        """??x????????,????????"""
        # ????????,???????????????,???x????????????,??????????????,????????t???????
        # ?????????t??????,?????,?????x???????,??t?????????t????????
        start_time = time.time()
        self.StepInfo.emit('?????????...')
        _7ZIP_PATH = function_7zip.get_7zip_path()
        final_result = function_7zip.process_7zip_t(_7ZIP_PATH, filepath, function_7zip.FAKE_PASSWORD)
        runtime_t = time.time() - start_time  # t?????

        is_continue_with_t = False  # ??t?????????t????????
        extract_path = None  # ??????,??????????
        # ??x????
        for index_pw, pw in enumerate(passwords, start=1):
            if self.is_stop_task:
                break
            else:
                pass

            if is_continue_with_t:
                break

            self.SignalPwIndex.emit(index_pw)
            self.SignalCurrentPw.emit(pw)
            start_time = time.time()
            final_result, extract_path = self.extract(filepath, pw)
            runtime_x = time.time() - start_time  # x?????
            # ???????????,?????
            if isinstance(final_result, Result7zip.Success):
                break
            # ??????????????,?????
            elif isinstance(final_result, Result7zip.WrongPassword):
                pass
            # ???????,???????
            else:
                break

            # ????,?????????
            if runtime_t < runtime_x:
                is_continue_with_t = True

        # ???t??
        if is_continue_with_t:
            for index_pw, pw in enumerate(passwords, start=1):
                if self.is_stop_task:
                    break
                else:
                    pass

                self.SignalPwIndex.emit(index_pw)
                self.SignalCurrentPw.emit(pw)
                _7ZIP_PATH = function_7zip.get_7zip_path()
                final_result = function_7zip.process_7zip_t(_7ZIP_PATH, filepath, pw)
                # ??????????,???????
                if isinstance(final_result, Result7zip.Success):
                    final_result, extract_path = self.extract(filepath, pw)
                    break
                # ????????????,?????
                elif isinstance(final_result, Result7zip.WrongPassword):
                    pass
                # ???????????,?????
                else:
                    break

        return final_result, extract_path

    def extract(self, file, password):
        """????"""
        # ???????
        # ????
        if isinstance(self.cover_model, str):
            part_cover = self.cover_model
        elif isinstance(self.cover_model, (ModelCoverFile.RenameOld,
                                           ModelCoverFile.RenameNew,
                                           ModelCoverFile.Skip,
                                           ModelCoverFile.Overwrite)):
            part_cover = self.cover_model.switch
        else:
            raise Exception('????????')

        # ????
        if self.is_extract_to_folder and self.extract_output_path:
            part_extract_to = self.extract_output_path
        else:
            part_extract_to = os.path.dirname(file)
        print('part_extract_to', self.is_extract_to_folder, self.extract_output_path)

        # ?????
        if self.is_filter and self.filter_rules:
            filter_rule = self.filter_rules
        else:
            filter_rule = []

        _7ZIP_PATH = function_7zip.get_7zip_path()
        result_7zip = function_7zip.progress_7zip_x_with_temp_folder(_7ZIP_PATH, file, password,
                                                                     cover_model=part_cover,
                                                                     output_folder=part_extract_to,
                                                                     filter_rule=filter_rule)

        # ?????????(??????????)
        filename_origin = lzytools_archive.get_filetitle(os.path.basename(file))

        # ??????,????????
        if isinstance(result_7zip, Result7zip.Success):
            # ?????????????????/???
            self.StepInfo.emit('????,????????...')
            temp_folder = function_7zip.get_temp_dirpath(part_extract_to, file)  # ???????
            parent_folder = os.path.dirname(temp_folder)  # ????????
            if isinstance(self.extract_model, ModelExtract.Smart):
                extract_path = function_move.move_to_smart(temp_folder, parent_folder, dirname_=filename_origin)
            elif isinstance(self.extract_model, ModelExtract.SameFolder):
                extract_path = function_move.move_to_same_dirname(temp_folder, parent_folder, dirname_=filename_origin)
            elif isinstance(self.extract_model, ModelExtract.Direct):
                extract_path = function_move.move_to_no_deal(temp_folder, parent_folder)
            else:
                extract_path = None
            # ???????(??????????????)
            if self.is_break_folder:
                self.StepInfo.emit('????,??????...')
                if os.path.isdir(extract_path):
                    if isinstance(self.break_folder_model, ModelBreakFolder.MoveToTop):
                        extract_path = function_file.break_folder_top(extract_path)
                    elif isinstance(self.break_folder_model, ModelBreakFolder.MoveBottom):
                        extract_path = function_file.break_folder_bottom(extract_path)
                    elif isinstance(self.break_folder_model, ModelBreakFolder.MoveFiles):
                        extract_path = function_file.break_folder_files(extract_path)
                    else:
                        pass
            # v2.1.32:webp?????jpg
            if self.is_webp_to_jpg and extract_path and os.path.exists(extract_path):
                self.StepInfo.emit('????,webp????jpg?...')
                _convert_webp_to_jpg_in_folder(extract_path, delete_source=self.webp_delete_source)
            # ???????(??????????,v2.2.1:???????????/????)
            file_info = self.fileinfo_task.get_file_info(file)
            related_files = file_info.related_files
            if self.is_delete_file:
                send_to_trash = (self.delete_mode == 'trash')
                for i in related_files:
                    lzytools.file.delete(i, send_to_trash=send_to_trash)

            print("????:", file, "????", result_7zip, "????", extract_path)
            return result_7zip, extract_path
        else:
            # ???????????????????,??????????(???????????)
            if self.is_stop_task:
                guess_temp_folder = function_7zip.get_temp_dirpath(part_extract_to, file)
                if os.path.exists(guess_temp_folder):
                    lzytools.file.delete(guess_temp_folder)

            return result_7zip, None
