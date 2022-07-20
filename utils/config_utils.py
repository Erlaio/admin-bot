import pathlib


class ConfigUtils:
    @staticmethod
    def get_project_root():
        return pathlib.Path(__file__).parent.parent

    @staticmethod
    def get_temp_path():
        return str(pathlib.PurePath(ConfigUtils.get_project_root(), 'temp'))
