from azure.storage.blob import BlobServiceClient
from ruamel.yaml import YAML
from pandas.api.types import is_numeric_dtype
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from snowflake import connector
from snowflake.connector.pandas_tools import write_pandas
from snowflake.connector.pandas_tools import pd_writer

import pandas as pd
import numpy as np
import os, uuid, re, logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("azure.core").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("snowflake.connector").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)