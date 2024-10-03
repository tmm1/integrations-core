# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from typing import Any  # noqa: F401
import os
from datadog_checks.base import AgentCheck  # noqa: F401

# from datadog_checks_dev.datadog_checks.dev.tooling.manifest_utils import Agent


# from datadog_checks.base.utils.db import QueryManager
# from requests.exceptions import ConnectionError, HTTPError, InvalidURL, Timeout
# from json import JSONDecodeError

def get_directory_size(path):
    if not os.path.exists(path):
        raise FileNotFoundError("The directory `{directory}` does not exist")
    if os.path.islink(path): # Skip symlinks for now
        return 0
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            try:
                total_size += os.path.getsize(file_path)
            except OSError:
                # Ignore errors like deleted files or permissions issues
                pass
    return total_size



class EnricoExperimentCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'enrico_experiment'

    def __init__(self, name, init_config, instances):
        super(EnricoExperimentCheck, self).__init__(name, init_config, instances)

        # Use self.instance to read the check configuration
        # self.url = self.instance.get("url")

        # If the check is going to perform SQL queries you should define a query manager here.
        # More info at
        # https://datadoghq.dev/integrations-core/base/databases/#datadog_checks.base.utils.db.core.QueryManager
        # sample_query = {
        #     "name": "sample",
        #     "query": "SELECT * FROM sample_table",
        #     "columns": [
        #         {"name": "metric", "type": "gauge"}
        #     ],
        # }
        # self._query_manager = QueryManager(self, self.execute_query, queries=[sample_query])
        # self.check_initializations.append(self._query_manager.compile_queries)

    def check(self, _):
        # type: (Any) -> None
        # The following are useful bits of code to help new users get started.

        # Perform HTTP Requests with our HTTP wrapper.
        # More info at https://datadoghq.dev/integrations-core/base/http/
        # try:
        #     response = self.http.get(self.url)
        #     response.raise_for_status()
        #     response_json = response.json()

        # except Timeout as e:
        #     self.service_check(
        #         "can_connect",
        #         AgentCheck.CRITICAL,
        #         message="Request timeout: {}, {}".format(self.url, e),
        #     )
        #     raise

        # except (HTTPError, InvalidURL, ConnectionError) as e:
        #     self.service_check(
        #         "can_connect",
        #         AgentCheck.CRITICAL,
        #         message="Request failed: {}, {}".format(self.url, e),
        #     )
        #     raise

        # except JSONDecodeError as e:
        #     self.service_check(
        #         "can_connect",
        #         AgentCheck.CRITICAL,
        #         message="JSON Parse failed: {}, {}".format(self.url, e),
        #     )
        #     raise

        # except ValueError as e:
        #     self.service_check(
        #         "can_connect", AgentCheck.CRITICAL, message=str(e)
        #     )
        #     raise

        # This is how you submit metrics
        # There are different types of metrics that you can submit (gauge, event).
        # More info at https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck

        # breakpoint()

        try:
            directory_path = "."
            directory_size = get_directory_size(directory_path)
            self.gauge("enric.directory.size", directory_size)
        except FileNotFoundError:
            self.service_check("can_connect", AgentCheck.CRITICAL)
            self.gauge("enric.directory.size", 0)
            return
        else:
            self.service_check("can_connect", AgentCheck.OK)



        # Perform database queries using the Query Manager
        # self._query_manager.execute()

        # This is how you use the persistent cache. This cache file based and persists across agent restarts.
        # If you need an in-memory cache that is persisted across runs
        # You can define a dictionary in the __init__ method.
        # self.write_persistent_cache("key", "value")
        # value = self.read_persistent_cache("key")

        # If your check ran successfully, you can send the status.
        # More info at
        # https://datadoghq.dev/integrations-core/base/api/#datadog_checks.base.checks.base.AgentCheck.service_check
        # self.service_check("can_connect", AgentCheck.OK)

        # If it didn't then it should send a critical service check
        # self.service_check("can_connect", AgentCheck.CRITICAL)
