# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import logging

import structlog

# Configure structlog to work with standard logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Create a structlog-bound logger
logger = structlog.get_logger()

# This will produce structured logs
logger.info("event_log", key1="value1", key2="value2")
