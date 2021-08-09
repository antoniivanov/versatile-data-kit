import logging
import socket
import time
import uuid
from datetime import datetime, timedelta
from retrying import retry


from taurus.vdk.heartbeat.config import Config
from taurus.vdk.heartbeat.heartbeat_test import HeartbeatTest
from taurus.vdk.heartbeat.job_controller import JobController
from taurus.vdk.heartbeat.tracing import LogDecorator

log = logging.getLogger(__name__)


class EmptyRunTest(HeartbeatTest):
    """
    Very simple test that does basically nothing.
    It's meant to be used if you need to verify just Control operations and does not
    care for running jobs.
    """

    def __init__(self, config: Config):
        super().__init__(config)

    @LogDecorator(log)
    def setup(self):
        pass

    @LogDecorator(log)
    def clean_up(self):
        pass

    @LogDecorator(log)
    def execute_test(self):
        pass