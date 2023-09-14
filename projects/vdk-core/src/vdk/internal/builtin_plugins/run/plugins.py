# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import importlib
import pathlib
from typing import List
from typing import Optional

import pluggy
from vdk.api.plugin.hook_markers import hookimpl
from vdk.api.plugin.plugin_registry import HookCallResult
from vdk.internal.builtin_plugins.config import vdk_config
from vdk.internal.builtin_plugins.run.execution_results import ExecutionResult
from vdk.internal.builtin_plugins.run.execution_results import StepResult
from vdk.internal.builtin_plugins.run.execution_state import ExecutionStateStoreKeys
from vdk.internal.builtin_plugins.run.job_context import JobContext
from vdk.internal.builtin_plugins.run.run_status import ExecutionStatus
from vdk.internal.builtin_plugins.run.step import Step
from vdk.internal.plugin.plugin import PluginRegistry


class JobSpecificHooksLoaderPlugin:
    """
    We are loading hooks that are specifically used only during a run of a data job.
    """

    @hookimpl
    def vdk_start(
        self, plugin_registry: PluginRegistry, command_line_args: List
    ) -> None:
        job_path = self._get_job_path(command_line_args)
        if job_path:
            self._load_plugins(plugin_registry, job_path)

    def _load_plugins(
        self, plugin_registry: PluginRegistry, job_path: pathlib.Path
    ) -> None:
        plugins_dir = job_path / "plugins"
        for item in plugins_dir.iterdir():
            if item.suffix == ".py":
                spec = importlib.util.spec_from_file_location(item.stem, item)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                plugin_registry.load_plugin_with_hooks_impl(module, name=item.stem)

    def _get_job_path(self, command_line_args: List) -> Optional[pathlib.Path]:
        # TODO: improve hooks/plugin framework to enable per sub-command configuration in a less hacky way.
        if command_line_args and "run" in command_line_args:
            index = command_line_args.index("run")
            if len(command_line_args) > index + 1:
                return pathlib.Path(command_line_args[index + 1])
        return None
