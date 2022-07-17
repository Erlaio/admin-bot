import pathlib


class ConfigUtils:
    @staticmethod
    def get_project_root():
        return pathlib.Path(__file__).parent.parent
