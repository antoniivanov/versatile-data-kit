# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import dataclasses
from copy import deepcopy
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List

import requests


class Session:
    def __init__(self):
        pass

    def __enter__(self):
        # You can perform some setup tasks if needed
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup tasks can be performed here
        pass


class Record:
    def __init__(self, data, metadata=None):
        self.data = data
        self.metadata = metadata

    def get_data(self):
        return self.data

    def get_metadata(self):
        return self.metadata


class DataSourceConnector:
    def connect(self, **session_params) -> Session:
        pass

    def disconnect(self, session: Session):
        pass


class DataSourceExtractor:
    def extract(self, session: Session, **filter_params) -> Iterator[Record]:
        pass

    def get_partitions(self, session: Session, **params) -> List[Dict]:
        """
        If the source can be read in parallel returns a list of partitions
        :param params:
        :return:
        """


# @dataclasses.dataclass
# @config("http")
# class HttpDataSourceConfig:
#
#     @config(description="")
#     base_url: str
#     endpoint: str
#
# vdk_config.register(HttpDataSourceSession)
#
# vdkconfig.get("http")


class HttpDataSourceSession(Session):
    base_url: str
    endpoint: str


class HTTPDataSourceConnector:
    def connect(self, base_url: str) -> Session:
        return HttpDataSourceSession(base_url=base_url)

    def disconnect(self, session: Session):
        # HTTP doesn't require an explicit disconnect usually
        pass


class DataSourceSchema:
    def __init__(self, fields: Dict[str, str]):
        # Example: fields = {'column_name': 'data_type', ...}
        self.fields = fields


class HTTPDataSourceExtractor:
    def __int__(self, session: HttpDataSourceSession, partition_params: Dict = None):
        self._session = session
        self._partition_params = partition_params or {}

    def extract(self, params: Dict = None) -> Iterator[Record]:
        url = f"{self._session.base_url}/{self._session.endpoint}"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            for item in response.json():  # Assuming the response is a JSON array
                yield Record(data=item)
        else:
            # Handle errors
            print(f"Error: {response.status_code}, {response.text}")

    def get_partitions(self, params: List[Any]) -> List[Dict]:
        partitioned_plugins = []
        for partition_params in params:
            new_plugin = deepcopy(self)
            new_plugin.partition_params.update(partition_params)
            partitioned_plugins.append(new_plugin)
        return partitioned_plugins

    def get_schema(self) -> DataSourceSchema:
        pass


# Usage
if __name__ == "__main__":
    http_data_source = HTTPDataSourceExtractor()

    with http_data_source.connect(base_url="http://api.example.com") as session:
        for partition in http_data_source.get_partitions():
            for record in http_data_source.extract(
                session, endpoint="data", params=partition
            ):
                print(record.get_data())  # Process the record
