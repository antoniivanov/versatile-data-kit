# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import pathlib

from vdk.api.plugin.hook_markers import hookimpl
from vdk.internal.builtin_plugins.run.job_context import JobContext

TEMPLATE_NAME = "set-test-property"


class TemplatePlugin:
    def __init__(
        self,
        template_name: str = TEMPLATE_NAME,
        template_path: pathlib.Path = pathlib.Path(__file__).parent.joinpath(
            "template-job"
        ),
    ):
        self.__template_name = template_name
        self.__template_path = template_path

    @hookimpl
    def initialize_job(self, context: JobContext) -> None:
        context.templates.add_template(self.__template_name, self.__template_path)


# def test_extension_with_job_input_execute_template(session_ip):
#     session_ip.get_ipython().push(variables={"VDK_EXTRA_PLUGINS": [TemplatePlugin()]})
#
#     with get_vdk_ipython(session_ip) as ip:
#         ip.get_ipython().run_cell("job_input = VDK.get_initialized_job_input()")
#         plugin_registry = ip.user_global_ns["VDK"].job._job_context.core_context.plugin_registry
#         plugin_registry.load_plugin_with_hooks_impl(TemplatePlugin())
#
#         ip.get_ipython().run_cell("job_input.execute_template('set-test-property', {})")
#
#         assert ip.get_ipython().run_cell("job_input.set_all_properties({'test':'test'})")
#         assert ip.get_ipython().run_cell("job_input.get_property('test')").result == 'test'
#
