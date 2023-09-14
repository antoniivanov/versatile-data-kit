# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import logging
import time

from tqdm import tqdm


class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


logging.basicConfig(level=logging.INFO, handlers=[TqdmLoggingHandler()])


logs = logging.getLogger("hi")

logs.info("Standard info")


# Initialize the parent progress bar

parent_progress = tqdm(
    total=11, desc="Job", position=0, leave=True, dynamic_ncols=False
)

for i in range(5):
    time.sleep(0.2)
    parent_progress.update(1)

    # Initialize the child progress bar
    child_progress = tqdm(
        total=0, desc=f"Step {i+1}", position=1, leave=False, dynamic_ncols=False
    )
    child_progress2 = tqdm(
        total=0,
        desc=f"Step Parallel {i+1}",
        position=2,
        leave=False,
        dynamic_ncols=False,
    )

    logs.info("Start progressing on each of the steps")
    for j in range(9):
        time.sleep(1.5)
        logs.info(" progressing on each of the steps")
        if j % 2 == 0 and j < 5:
            child_progress.update(1)
            if j == 4:
                child_progress.close()
        else:
            child_progress2.update(1)

    # Close and clear the child progress bar
    child_progress2.close()
    # print("\033[K", end='\r', flush=True)

# Close the parent progress bar
parent_progress.close()
