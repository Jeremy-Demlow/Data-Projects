from unittest import TestCase
import os

from easymigration.snowflake.utils import SnowflakeTool


class TestSnowflake(TestCase):
    sf_keys = [k for k in os.environ.keys() if k.startswith('sf')]
    kwargs = {k: os.environ[k] for k in sf_keys}
    print(f"snowflake credentials: {kwargs}")
    obj = SnowflakeTool(**kwargs)
    obj.test_connection()
