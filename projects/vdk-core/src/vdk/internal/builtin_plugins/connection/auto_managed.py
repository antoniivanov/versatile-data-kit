# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import functools
import importlib
import inspect
import sys


def is_pep249_compatible(connector):
    required_methods = {
        "connect",
        "cursor",
        "commit",
        "rollback",
        "close",
    }

    cursor_methods = {
        "execute",
        "fetchone",
        "fetchmany",
        "fetchall",
        "close",
    }

    if not all(hasattr(connector, method) for method in required_methods):
        return False

    cursor_instance = connector.cursor()
    if not all(hasattr(cursor_instance, method) for method in cursor_methods):
        return False

    return True


def wrap_connect(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("PEP 249 compatible connection is being opened...")
        connection = func(*args, **kwargs)
        return connection

    return wrapper


class Pep249ImportHook:
    def __init__(self, module_names):
        self.module_names = module_names

    def find_spec(self, fullname, path, target=None):
        if fullname in self.module_names:
            return importlib.util.spec_from_loader(fullname, loader=self)
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        connector = importlib.import_module(module.__name__)
        if is_pep249_compatible(connector):
            connector.connect = wrap_connect(connector.connect)
        sys.modules[module.__name__] = connector
        return connector


def auto_manage():
    known_connector_libraries = ["sqlite3", "psycopg2", "MySQLdb", "pyodbc", "pymysql"]

    """
    When we import a module in Python, the interpreter goes through the sys.meta_path list in order,
    looking for a finder object that knows how to handle the requested module.
    The sys.meta_path list contains finder objects that are responsible for
    locating and loading modules from various sources like built-in modules,
    frozen modules, and modules from the file system.
    By inserting the custom import hook at the beginning of the list (index 0),
    we ensure that the hook is executed before the other finders,
    allowing us to intercept and modify the imported modules as needed.
    """
    import_hook = Pep249ImportHook(known_connector_libraries)
    sys.meta_path.insert(0, import_hook)

    # Wrap the connect method for already imported modules
    for module_name, module in sys.modules.items():
        if module_name in known_connector_libraries and module is not None:
            if is_pep249_compatible(module):
                print(
                    "PEP 249 compatible connection is found in imported module: "
                    + module_name
                )
                module.connect = wrap_connect(module.connect)
