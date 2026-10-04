# ?????????
# ???????????,??????????????
import configparser
import os
from typing import Union

from common.class_7zip import ModelArchive, Position, ModelExtract, ModelCoverFile, ModelBreakFolder, \
    TYPES_MODEL_ARCHIVE, TYPES_MODEL_BREAK_FOLDER, TYPES_POSITION, TYPES_MODEL_COVER_FILE, TYPES_MODEL_EXTRACT, \
    TYPES_MODEL_PRE_FILTER, ModelPreFilter

_CONFIG_FILE = 'setting.ini'  # ?????????(???????????)
_SPLIT_WORD = '?'


class SettingModel:
    """?????????"""

    def __init__(self):
        # ??????????
        self._check_config_exists()

        # ??????????
        self.config = configparser.ConfigParser()
        self.config.read(_CONFIG_FILE, encoding='utf-8')

        # ???????
        self._model_archive = _ChildSettingModelArchive(self.config)
        self._model_pre_filter = _ChildSettingModelPreFilter(self.config)
        self._try_unknown_filetype = _ChildSettingTryUnknownFiletype(self.config)
        self._read_password_from_filename = _ChildSettingReadPasswordFromFilename(self.config)
        self._write_filename = _ChildSettingWriteFilename(self.config)
        self._model_extract = _ChildSettingModelExtract(self.config)
        self._delete_file = _ChildSettingDeleteFile(self.config)
        self._recursive_extract = _ChildSettingRecursiveExtract(self.config)
        self._mode_cover_file = _ChildSettingModelCover(self.config)
        self._break_folder = _ChildSettingBreakFolder(self.config)
        self._extract_output_folder = _ChildSettingExtractOutputFolder(self.config)
        self._extract_filter = _ChildSettingExtractFilter(self.config)
        self._7zip_path = _ChildSetting7ZipPath(self.config)
        self._top_window = _ChildSettingTopWindow(self.config)
        self._lock_size = _ChildSettingLockSize(self.config)
        self._webp_to_jpg = _ChildSettingWebpToJpg(self.config)
        self._webp_delete_source = _ChildSettingWebpDeleteSource(self.config)
        self._area_order = _ChildSettingAreaOrder(self.config)

    @staticmethod
    def _check_config_exists():
        """??????????"""
        if not os.path.exists(_CONFIG_FILE):
            with open(_CONFIG_FILE, 'w', encoding='utf-8'):
                pass

    def get_model_archive(self):
        return self._model_archive.read()

    def set_model_archive(self, model: TYPES_MODEL_ARCHIVE):
        self._model_archive.set(model)

    def set_model_archive_extract(self):
        self.set_model_archive(ModelArchive.Extract())

    def set_model_archive_test(self):
        self.set_model_archive(ModelArchive.Test())

    def get_model_pre_filter(self):
        return self._model_pre_filter.read_mode()

    def set_model_pre_filter(self, model: TYPES_MODEL_PRE_FILTER):
        self._model_pre_filter.set_mode(model)

    def set_model_pre_filter_default(self):
        self.set_model_pre_filter(ModelPreFilter.Default())

    def set_model_pre_filter_blacklist(self):
        self.set_model_pre_filter(ModelPreFilter.BlackList())

    def set_model_pre_filter_whitelist(self):
        self.set_model_pre_filter(ModelPreFilter.WhiteList())

    def get_model_pre_filter_blacklist_rule(self):
        return self._model_pre_filter.read_black_list()

    def set_model_pre_filter_blacklist_rule(self, rule: list[str]):
        self._model_pre_filter.set_black_list(rule)

    def get_model_pre_filter_whitelist_rule(self):
        return self._model_pre_filter.read_white_list()

    def set_model_pre_filter_whitelist_rule(self, rule: list[str]):
        self._model_pre_filter.set_white_list(rule)

    def get_try_unknown_filetype_is_enable(self):
        return self._try_unknown_filetype.read()

    def set_try_unknown_filetype_is_enable(self, is_enable: bool):
        self._try_unknown_filetype.set(is_enable)

    def get_read_password_from_filename_is_enable(self):
        return self._read_password_from_filename.read()

    def set_read_password_from_filename_is_enable(self, is_enable: bool):
        self._read_password_from_filename.set(is_enable)

    def get_write_filename_is_enable(self):
        return self._write_filename.read_is_enable()

    def set_write_filename_is_enable(self, is_enable: bool):
        self._write_filename.set_is_enable(is_enable)

    def get_write_filename_left_word(self):
        return self._write_filename.read_left_word()

    def set_write_filename_left_word(self, word: str):
        self._write_filename.set_left_word(word)

    def get_write_filename_right_word(self):
        return self._write_filename.read_right_word()

    def set_write_filename_right_word(self, word: str):
        self._write_filename.set_right_word(word)

    def get_write_filename_position(self):
        return self._write_filename.read_position()

    def get_write_filename_position_str(self):
        return self.get_write_filename_position().text

    def set_write_filename_position(self, position: TYPES_POSITION):
        self._write_filename.set_position(position)

    def get_write_filename_preview(self):
        return self._write_filename.get_preview()

    def get_model_extract(self):
        return self._model_extract.read()

    def set_model_extract(self, model: TYPES_MODEL_EXTRACT):
        self._model_extract.set(model)

    def set_model_extract_smart(self):
        self.set_model_extract(ModelExtract.Smart())

    def set_model_extract_direct(self):
        self.set_model_extract(ModelExtract.Direct())

    def set_model_extract_same_folder(self):
        self.set_model_extract(ModelExtract.SameFolder())

    def get_delete_file_is_enable(self):
        return self._delete_file.read_is_enable()

    def set_delete_file_is_enable(self, is_enable: bool):
        self._delete_file.set_is_enable(is_enable)

    def get_delete_file_mode(self):
        """v2.2.1:??????"""
        return self._delete_file.read_delete_mode()

    def set_delete_file_mode(self, mode: str):
        """v2.2.1:??????"""
        self._delete_file.set_delete_mode(mode)

    def get_delete_file_is_send_to_trash(self):
        """v2.2.1:????????"""
        return self._delete_file.is_send_to_trash()

    def get_recursive_extract_is_enable(self):
        return self._recursive_extract.read()

    def set_recursive_extract_is_enable(self, is_enable: bool):
        self._recursive_extract.set(is_enable)

    def get_model_cover(self):
        return self._mode_cover_file.read()

    def get_model_cover_str(self):
        return self.get_model_cover().text

    def set_model_cover(self, model: TYPES_MODEL_COVER_FILE):
        self._mode_cover_file.set(model)

    def get_break_folder_is_enable(self):
        return self._break_folder.read_is_enable()

    def set_break_folder_is_enable(self, is_enable: bool):
        self._break_folder.set_is_enable(is_enable)

    def get_break_folder_model(self):
        return self._break_folder.read_model()

    def get_break_folder_model_str(self):
        return self.get_break_folder_model().text

    def set_break_folder_model(self, model: TYPES_MODEL_BREAK_FOLDER):
        self._break_folder.set_model(model)

    def get_extract_output_folder_is_enable(self):
        return self._extract_output_folder.read_is_enable()

    def set_extract_output_folder_is_enable(self, is_enable: bool):
        self._extract_output_folder.set_is_enable(is_enable)

    def get_extract_output_folder_path(self):
        return self._extract_output_folder.read_path()

    def set_extract_output_folder_path(self, path: str):
        self._extract_output_folder.set_path(path)

    def get_extract_filter_is_enable(self):
        return self._extract_filter.read_is_enable()

    def set_extract_filter_is_enable(self, is_enable: bool):
        self._extract_filter.set_is_enable(is_enable)

    def get_extract_filter_rules(self):
        return self._extract_filter.read_rules()

    def get_extract_filter_rules_str(self):
        return self._extract_filter.read_rules_str()

    def set_extract_filter_rules(self, rules: str):
        self._extract_filter.set_rules(rules)

    def get_7zip_path(self):
        return self._7zip_path.read()

    def set_7zip_path(self, path: str):
        self._7zip_path.set(path)

    def get_top_window_is_enable(self):
        return self._top_window.read()

    def set_top_window_is_enable(self, is_enable: bool):
        self._top_window.set(is_enable)

    def get_lock_size_is_enable(self):
        return self._lock_size.read_is_enable()

    def set_lock_size_is_enable(self, is_enable: bool):
        self._lock_size.set_is_enable(is_enable)

    def get_lock_size_height(self):
        return self._lock_size.read_height()

    def set_lock_size_height(self, height: int):
        self._lock_size.set_height(height)

    def get_lock_size_width(self):
        return self._lock_size.read_width()

    def set_lock_size_width(self, width: int):
        self._lock_size.set_width(width)

    def get_webp_to_jpg_is_enable(self):
        """v2.2.1:??webp?jpg????"""
        return self._webp_to_jpg.read()

    def set_webp_to_jpg_is_enable(self, is_enable: bool):
        """v2.2.1:??webp?jpg????"""
        self._webp_to_jpg.set(is_enable)

    def get_webp_delete_source_is_enable(self):
        """v2.2.1:??webp??????????"""
        return self._webp_delete_source.read()

    def set_webp_delete_source_is_enable(self, is_enable: bool):
        """v2.2.1:??webp??????????"""
        self._webp_delete_source.set(is_enable)

    def get_area_order(self):
        """v2.2.1:????????"""
        return self._area_order.read()

    def set_area_order(self, order: str):
        """v2.2.1:????????"""
        self._area_order.set(order)


class _ModuleChildSetting:
    """???:???"""

    def __init__(self, config: configparser.ConfigParser):
        """:param config: ?????ConfigParser??"""
        self.config = config

    def _read_key(self, section: str, key: str, default_value):
        """?????????,??????????"""
        return self.config.get(section, key, fallback=default_value)

    def _set_value(self, section: str, key: str, value: str):
        """?????"""
        if section not in self.config:
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self.config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))


class _ModuleChildSettingSingleEnable(_ModuleChildSetting):
    """???:???,??????????"""

    def __init__(self, config, section: str, key: str, default_value: bool):
        super().__init__(config)
        self.section = section
        self.key = key
        self._default_value = default_value

    def read(self) -> bool:
        """?????"""
        value = self._read_key(self.section, self.key, self._default_value)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key, '???????')

    def set(self, value: bool):
        """?????"""
        self._set_value(self.section, self.key, str(value))


class _ModuleChildSettingSingleText(_ModuleChildSetting):
    """???:???,?????????"""

    def __init__(self, config, section: str, key: str, default_value: str):
        super().__init__(config)
        self.section = section
        self.key = key
        self._default_value = default_value

    def read(self) -> str:
        """?????"""
        return self._read_key(self.section, self.key, self._default_value)

    def set(self, value: str):
        """?????"""
        self._set_value(self.section, self.key, str(value))


class _ChildSettingModelArchive(_ModuleChildSetting):
    """??? ???????"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ModelArchive'
        self.key = 'model'
        self._default_value = ModelArchive.Test()

    def read(self) -> TYPES_MODEL_ARCHIVE:
        """?????"""
        value = self._read_key(self.section, self.key, self._default_value)
        # ?????????????????
        if isinstance(value, (ModelArchive.Test, ModelArchive.Extract)):
            return value
        elif value == ModelArchive.Test.value:
            return ModelArchive.Test()
        elif value == ModelArchive.Extract.value:
            return ModelArchive.Extract()
        else:
            raise ValueError(self.section, self.key, '???????')

    def set(self, value: TYPES_MODEL_ARCHIVE):
        """?????"""
        value_str = value.value
        self._set_value(self.section, self.key, value_str)


class _ChildSettingModelPreFilter(_ModuleChildSetting):
    """??? ???????"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ModelPreFilter'
        # ??
        self.key_mode = 'model'
        self._default_value_mode = ModelPreFilter.Default()
        # ?????(???????)
        self.key_black_list = 'black_list'
        self._default_value_black_list = r'\.xls$||\.xlsx$||\.xlsm$||\.doc$||\.docx$||\.docm$||\.ppt$||\.pptx$||\.pptm$||\.csv$||\.odt$||\.ods$||\.odp$||\.epub$||\.kmz$||\.cbz$||\.ipa$||\.jar$||\.war$||\.ear$||\.aar$||\.xpi$||\.crx$||\.vsix$||\.nupkg$||\.whl$||\.apk$||\.exe$||\.appx$||\.msix$||\.aab$||\.xapk$||\.vpk$||\.pck$||\.ba2$||\.love$||\.mcpack$||\.mcworld$||\.bsa$||\.mpq$||\.sav$||\.dat$||\.pak$||\.quicksave$||\.autosave$'
        # ??????(???????)
        self.key_white_list = 'white_list'
        self._default_value_white_list = r'\.zip$||\.xz$||\.7z$||\.rar$||\.tar$||\.iso$||\.gz$||\.arj$||\.cramfs$||\.bzip2$||\.cab$||\.dmg$||\.wim$||\.gzip$||\.chm$||\.ext$||\.ar$||\.cpio$||\.\d+$||\.part\d+$||\.z\d+$'

    def read_mode(self) -> TYPES_MODEL_PRE_FILTER:
        """?????"""
        value = self._read_key(self.section, self.key_mode, self._default_value_mode)
        # ?????????????????
        if isinstance(value, (ModelPreFilter.Default, ModelPreFilter.BlackList, ModelPreFilter.WhiteList)):
            return value
        elif value == ModelPreFilter.Default.value:
            return ModelPreFilter.Default()
        elif value == ModelPreFilter.BlackList.value:
            return ModelPreFilter.BlackList()
        elif value == ModelPreFilter.WhiteList.value:
            return ModelPreFilter.WhiteList()
        else:
            raise ValueError(self.section, self.key_mode, '???????')

    def set_mode(self, value: TYPES_MODEL_PRE_FILTER):
        """?????"""
        value_str = value.value
        self._set_value(self.section, self.key_mode, value_str)

    def read_black_list(self) -> list[str]:
        """?????"""
        value = self._read_key(self.section, self.key_black_list, self._default_value_black_list)
        value = value.split('||')
        if value:
            return value
        else:
            return []

    def set_black_list(self, value: list[str]):
        """?????"""
        value_str = '||'.join(value)
        self._set_value(self.section, self.key_black_list, value_str)

    def read_white_list(self) -> list[str]:
        """?????"""
        value = self._read_key(self.section, self.key_white_list, self._default_value_white_list)
        value = value.split('||')
        if value:
            return value
        else:
            return []

    def set_white_list(self, value: list[str]):
        """?????"""
        value_str = '||'.join(value)
        self._set_value(self.section, self.key_white_list, value_str)


class _ChildSettingTryUnknownFiletype(_ModuleChildSettingSingleEnable):
    """??? ????????"""

    def __init__(self, config):
        super().__init__(config, section='TryUnknownFiletype', key='is_enable', default_value=False)


class _ChildSettingReadPasswordFromFilename(_ModuleChildSettingSingleEnable):
    """??? ???????????"""

    def __init__(self, config):
        super().__init__(config, section='ReadPasswordFromFilename', key='is_enable', default_value=False)


class _ChildSettingWriteFilename(_ModuleChildSetting):
    """??? ????????"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'WriteFilename'
        # ????
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # ?????? ????
        self.key_left_word = 'left_word'
        self._default_value_left_word = ''
        # ?????? ????
        self.key_right_word = 'right_word'
        self._default_value_right_word = ''
        # ?????? ??
        self.key_position = 'position'
        self._default_value_position = Position.Left()

    def get_preview(self) -> str:
        """????????????"""
        left_part = self.read_left_word()
        right_part = self.read_right_word()
        position = self.read_position()
        if isinstance(position, Position.Left) and not right_part:  # ????????????????
            right_part = ' '
        elif isinstance(position, Position.Right) and not left_part:
            left_part = ' '
        pw_part = f'{left_part}??{right_part}'
        filename_part = '????'
        if isinstance(position, Position.Left):
            preview = f'{pw_part}{filename_part}'
        elif isinstance(position, Position.Right):
            preview = f'{filename_part}{pw_part}'
        else:
            preview = '???????'

        return preview

    def read_is_enable(self) -> bool:
        """????? ????"""
        value = self._read_key(self.section, self.key_is_enable, self._default_value_is_enable)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key_is_enable, '???????')

    def set_is_enable(self, value: bool):
        """????? ????"""
        self._set_value(self.section, self.key_is_enable, str(value))

    def read_left_word(self) -> str:
        """????? ??????"""
        return self._read_key(self.section, self.key_left_word, self._default_value_left_word)

    def set_left_word(self, value: str):
        """????? ??????"""
        self._set_value(self.section, self.key_left_word, str(value))

    def read_right_word(self) -> str:
        """????? ??????"""
        return self._read_key(self.section, self.key_right_word, self._default_value_right_word)

    def set_right_word(self, value: str):
        """????? ??????"""
        self._set_value(self.section, self.key_right_word, str(value))

    def read_position(self) -> TYPES_POSITION:
        """????? ????"""
        value = self._read_key(self.section, self.key_position, self._default_value_position)
        if isinstance(value, (Position.Left, Position.Right)):
            return value
        elif value == Position.Left.text:
            return Position.Left()
        elif value == Position.Right.text:
            return Position.Right()
        else:
            raise ValueError(self.section, self.key_position, '???????')

    def set_position(self, value: TYPES_POSITION):
        """????? ????"""
        if isinstance(value, (Position.Left, Position.Right)):
            value_str = value.text
        else:
            value_str = value
        self._set_value(self.section, self.key_position, value_str)


class _ChildSettingModelExtract(_ModuleChildSetting):
    """??? ????"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ModelExtract'
        self.key = 'model'
        self._default_value = ModelExtract.Smart()

    def read(self) -> TYPES_MODEL_EXTRACT:
        """?????"""
        value = self._read_key(self.section, self.key, self._default_value)
        # ?????????????????
        if isinstance(value, (ModelExtract.Smart, ModelExtract.Direct, ModelExtract.SameFolder)):
            return value
        elif value == ModelExtract.Smart.value:
            return ModelExtract.Smart()
        elif value == ModelExtract.Direct.value:
            return ModelExtract.Direct()
        elif value == ModelExtract.SameFolder.value:
            return ModelExtract.SameFolder()
        else:
            raise ValueError(self.section, self.key, '???????')

    def set(self, value: TYPES_MODEL_EXTRACT):
        """?????"""
        value_str = value.value
        self._set_value(self.section, self.key, value_str)


class _ChildSettingDeleteFile(_ModuleChildSetting):
    """??? ????????????(v2.2.1:????????/????)"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'DeleteFile'
        # ????
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # ????:trash(??????)/ direct(????)
        self.key_delete_mode = 'delete_mode'
        self._default_value_delete_mode = 'trash'

    def read_is_enable(self) -> bool:
        """????? ????"""
        value = self._read_key(self.section, self.key_is_enable, self._default_value_is_enable)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key_is_enable, '???????')

    def set_is_enable(self, value: bool):
        """????? ????"""
        self._set_value(self.section, self.key_is_enable, str(value))

    def read_delete_mode(self) -> str:
        """????? ????"""
        return self._read_key(self.section, self.key_delete_mode, self._default_value_delete_mode)

    def set_delete_mode(self, value: str):
        """????? ????"""
        self._set_value(self.section, self.key_delete_mode, value)

    def is_send_to_trash(self) -> bool:
        """????????"""
        return self.read_delete_mode() == 'trash'


class _ChildSettingRecursiveExtract(_ModuleChildSettingSingleEnable):
    """??? ??????"""

    def __init__(self, config):
        super().__init__(config, section='RecursiveExtract', key='is_enable', default_value=False)

    def set(self, value: bool):
        """?????"""
        self._set_value(self.section, self.key, str(value))


class _ChildSettingModelCover(_ModuleChildSetting):
    """??? ????"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ModelCover'
        self.key = 'model'
        self._default_value = ModelCoverFile.Overwrite()

    def read(self) -> TYPES_MODEL_COVER_FILE:
        """?????"""
        value = self._read_key(self.section, self.key, self._default_value)
        # ?????????????????
        if isinstance(value, (ModelCoverFile.Overwrite, ModelCoverFile.Skip, ModelCoverFile.RenameNew,
                              ModelCoverFile.RenameOld)):
            return value
        elif value == ModelCoverFile.Overwrite.text:
            return ModelCoverFile.Overwrite()
        elif value == ModelCoverFile.Skip.text:
            return ModelCoverFile.Skip()
        elif value == ModelCoverFile.RenameNew.text:
            return ModelCoverFile.RenameNew()
        elif value == ModelCoverFile.RenameOld.text:
            return ModelCoverFile.RenameOld()
        else:
            raise ValueError(self.section, self.key, '???????')

    def set(self, value: TYPES_MODEL_COVER_FILE):
        """?????"""
        if not isinstance(value, str):
            value = value.value
        self._set_value(self.section, self.key, value)


class _ChildSettingBreakFolder(_ModuleChildSetting):
    """??? ?????"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'BreakFolder'
        # ????
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # ????
        self.key_model = 'model'
        self._default_value_model = ModelBreakFolder.MoveToTop()

    def read_is_enable(self) -> bool:
        """????? ????"""
        value = self._read_key(self.section, self.key_is_enable, self._default_value_is_enable)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key_is_enable, '???????')

    def set_is_enable(self, value: bool):
        """????? ????"""
        self._set_value(self.section, self.key_is_enable, str(value))

    def read_model(self) -> TYPES_MODEL_BREAK_FOLDER:
        """????? ????"""
        value = self._read_key(self.section, self.key_model, self._default_value_model)
        # ?????????????????
        if isinstance(value, (ModelBreakFolder.MoveBottom, ModelBreakFolder.MoveToTop, ModelBreakFolder.MoveFiles)):
            return value
        elif value == ModelBreakFolder.MoveBottom.text:
            return ModelBreakFolder.MoveBottom()
        elif value == ModelBreakFolder.MoveToTop.text:
            return ModelBreakFolder.MoveToTop()
        elif value == ModelBreakFolder.MoveFiles.text:
            return ModelBreakFolder.MoveFiles()
        else:
            raise ValueError(self.section, self.key_model, '???????')

    def set_model(self,
                  value: TYPES_MODEL_BREAK_FOLDER):
        """????? ????"""
        if not isinstance(value, str):
            value = value.value
        self._set_value(self.section, self.key_model, value)


class _ChildSettingExtractOutputFolder(_ModuleChildSetting):
    """??? ??????"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ExtractOutputFolder'
        # ????
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # ????
        self.key_path = 'path'
        self._default_value_path = ''

    def read_is_enable(self) -> bool:
        """????? ????"""
        value = self._read_key(self.section, self.key_is_enable, self._default_value_is_enable)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key_is_enable, '???????')

    def set_is_enable(self, value: bool):
        """????? ????"""
        self._set_value(self.section, self.key_is_enable, str(value))

    def read_path(self) -> str:
        """????? ??????"""
        return self._read_key(self.section, self.key_path, self._default_value_path)

    def set_path(self, value: str):
        """????? ??????"""
        self._set_value(self.section, self.key_path, value)


class _ChildSettingExtractFilter(_ModuleChildSetting):
    """??? ?????"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ExtractFilter'
        # ????
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # ????
        self.key_rules = 'rules'
        self._default_value_rules = ''  # ????switch(???-xr!?)

    def read_is_enable(self) -> bool:
        """????? ????"""
        value = self._read_key(self.section, self.key_is_enable, self._default_value_is_enable)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key_is_enable, '???????')

    def set_is_enable(self, value: bool):
        """????? ????"""
        self._set_value(self.section, self.key_is_enable, str(value))

    def read_rules(self) -> list:
        """????? ????"""
        # ??????,??list
        setting = self._read_key(self.section, self.key_rules, self._default_value_rules)
        split = setting.split(_SPLIT_WORD)
        split = ['-xr!' + i for i in split if i]
        return split

    def read_rules_str(self) -> str:
        """????? ????"""
        setting = self._read_key(self.section, self.key_rules, self._default_value_rules)
        split = setting.split(_SPLIT_WORD)
        split = [i for i in split if i]
        text = '\n'.join(split)
        return text

    def set_rules(self, value: Union[str, list]):
        """????? ????(v2.2.1:??????,??html????*.html)"""
        # ??????7zip switch??
        if isinstance(value, str):
            value = value.split('\n')
        value = [i for i in value if i]
        # v2.2.1:??????,?????????(?html),????*.html
        processed = []
        for rule in value:
            rule = rule.strip()
            if rule and not rule.startswith('-xr!') and not rule.startswith('*') and '.' not in rule and not rule.startswith('\\'):
                # ???,????*.??
                processed.append(f'*.{rule}')
            else:
                processed.append(rule)
        value_join = _SPLIT_WORD.join(processed)
        self._set_value(self.section, self.key_rules, value_join)


class _ChildSetting7ZipPath(_ModuleChildSettingSingleText):
    """??? 7zip??"""

    def __init__(self, config):
        super().__init__(config, section='7ZipPath', key='filepath', default_value='')


class _ChildSettingTopWindow(_ModuleChildSettingSingleEnable):
    """??? ????"""

    def __init__(self, config):
        super().__init__(config, section='TopWindow', key='is_enable', default_value=False)


class _ChildSettingLockSize(_ModuleChildSetting):
    """??? ??????"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'LockSize'
        # ????
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = True
        # ????
        self.key_height = 'height'
        self._default_value_height = 300
        # ????
        self.key_width = 'width'
        self._default_value_width = 300

    def read_is_enable(self) -> bool:
        """????? ????"""
        value = self._read_key(self.section, self.key_is_enable, self._default_value_is_enable)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key_is_enable, '???????')

    def set_is_enable(self, value: bool):
        """????? ????"""
        self._set_value(self.section, self.key_is_enable, str(value))

    def read_height(self) -> int:
        """????? ????"""
        value = self._read_key(self.section, self.key_height, self._default_value_height)
        return int(value)

    def set_height(self, value: int):
        """?????????"""
        self._set_value(self.section, self.key_height, str(value))

    def read_width(self) -> int:
        """????? ????"""
        value = self._read_key(self.section, self.key_width, self._default_value_width)
        return int(value)

    def set_width(self, value: int):
        """????? ????"""
        self._set_value(self.section, self.key_width, str(value))


class _ChildSettingWebpToJpg(_ModuleChildSettingSingleEnable):
    """??? v2.2.1:webp?????????jpg??"""

    def __init__(self, config):
        super().__init__(config, section='WebpToJpg', key='is_enable', default_value=True)


class _ChildSettingWebpDeleteSource(_ModuleChildSettingSingleEnable):
    """??? v2.2.1:webp??????????"""

    def __init__(self, config):
        super().__init__(config, section='WebpToJpg', key='delete_source', default_value=True)


class _ChildSettingAreaOrder(_ModuleChildSetting):
    """??? v2.2.1:????????"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'AreaOrder'
        self.key = 'order'
        self._default_value = ''

    def read(self) -> str:
        """????? ????"""
        return self._read_key(self.section, self.key, self._default_value)

    def set(self, value: str):
        """????? ????"""
        self._set_value(self.section, self.key, value)
