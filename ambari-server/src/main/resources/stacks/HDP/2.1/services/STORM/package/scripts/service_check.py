#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management import *
from resource_management.libraries.functions import get_unique_id_and_date

class ServiceCheck(Script):
  def service_check(self, env):
    import params
    env.set_params(params)

    unique = get_unique_id_and_date()

    File("/tmp/wordCount.jar",
         content=StaticFile("wordCount.jar")
    )

    cmd = format("env JAVA_HOME={java64_home} storm jar /tmp/wordCount.jar storm.starter.WordCountTopology WordCount{unique} -c nimbus.host={nimbus_host}")

    Execute(cmd,
            logoutput=True,
            path=params.storm_bin_dir,
            user=params.storm_user
    )

    Execute(format("env JAVA_HOME={java64_home} storm kill WordCount{unique}"),
            path=params.storm_bin_dir,
            user=params.storm_user
    )

if __name__ == "__main__":
  ServiceCheck().execute()
