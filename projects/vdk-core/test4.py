# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import threading


class NotThreadSafeExample:
    def __init__(self):
        self._progress = 0

    def update_progress(self, iterations):
        temp = self._progress  # Step 1
        temp += iterations  # Step 2
        self._progress = temp  # Step 3


# Create an instance of the not-thread-safe class
example = NotThreadSafeExample()

# Create two threads that will both update progress
thread1 = threading.Thread(target=example.update_progress, args=(5,))
thread2 = threading.Thread(target=example.update_progress, args=(3,))

# Start both threads almost simultaneously
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()

# Show the final result
print("Final progress:", example._progress)
