from ruamel.yaml import YAML
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def yml_reader(yml_filepath: str, logger: logging = None):
    """
    Reading the yaml file.

    param: ymal_filepath: path to the yamlfile

    Return: Dictionary of yaml file contents
    """
    logger = logger if logger is not None else logging.getLogger(__name__)
    if os.path.exists(yml_filepath):
        with open(yml_filepath) as stream:
            yml = YAML(typ="safe")
            yml_dict = yml.load(stream)
        return yml_dict
    else:
        logger.info(f"yml_filepath ({yml_filepath}) doesn't exisit")


class ParseYaml:
    """
    Simple Parser from project yamls
    """

    def __init__(self, path: str, f_logger=logging.getLogger(__name__)):
        self._logger = f_logger
        if os.path.exists(path):
            self.yaml_file = yml_reader(path, self._logger)
        else:
            self._logger.info(f'yaml file {path} does not exisit')

    def get_yaml(self, data_list: list = None):
        """
        Return Yaml Query Info

        Args:
            data_list (list, optional): [if None returns full yaml
            allows user to index into yaml file as far as they
            want and index allows.]. Defaults to None.

        Returns:
            [type]: [description]
        """
        if not data_list:
            return self.yaml_file
        yaml_key = self.yaml_file.get(f'{data_list[0]}')
        if len(data_list) > 1:
            for level in data_list[1:]:
                yaml_key = yaml_key.get(f'{level}')
        return yaml_key
