#
# Copyright (c) 2021, Neptune Labs Sp. z o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import annotations

import json
import os
import warnings

from neptune import Run
from neptune.handler import Handler
from neptune.integrations.utils import expect_not_an_experiment
from neptune.types import File
from neptune.utils import stringify_unsupported
from sacred.dependencies import get_digest
from sacred.observers import RunObserver

from neptune_sacred.impl.utils import custom_flatten_dict
from neptune_sacred.impl.version import __version__

INTEGRATION_VERSION_KEY = "source_code/integrations/neptune-sacred"


class NeptuneObserver(RunObserver):
    """Logs Sacred experiment metadata to Neptune.

    The experiment data can be accessed and shared via the web app or API.

    Args:
        run:
            Pass a Neptune run if you want to continue logging to an existing run.
            Learn more about resuming runs: https://docs.neptune.ai/logging/to_existing_object
            You can also pass a namespace handler instead of a run.
        base_namespace:
            In the Neptune run, the root namespace that will contain all the logged metadata.

    Examples:
        Create sacred experiment:

        >>> from numpy.random import permutation
        >>> from sklearn import svm, datasets
        >>> from sacred import Experiment
        >>> ex = Experiment("iris_rbf_svm")

        Add Neptune observer:

        >>> import neptune
        >>> from neptune_sacred import NeptuneObserver
        >>> run = neptune.init_run()
        >>> ex.observers.append(NeptuneObserver(run=run))

        Run experiment:

        >>> @ex.config
        ... def cfg():
        ...     C = 1.0
        ...     gamma = 0.7

        >>> @ex.automain
        ... def _run(C, gamma, _run):
        ...     iris = datasets.load_iris()
        ...     per = permutation(iris.target.size)
        ...     iris.data = iris.data[per]
        ...     iris.target = iris.target[per]
        ...     clf = svm.SVC(C, "rbf", gamma=gamma)
        ...     clf.fit(iris.data[:90], iris.target[:90])
        ...     return clf.score(iris.data[90:], iris.target[90:])

    You may also want to check the following:

    Sacred integration docs page:
        https://docs.neptune.ai/integrations/sacred
    Example run displayed in Neptune:
        https://app.neptune.ai/o/common/org/sacred-integration/e/SAC-1341/all
    """

    def __init__(
        self,
        run: Run | Handler,
        *,
        base_namespace="experiment",
    ):

        super(NeptuneObserver, self).__init__()
        expect_not_an_experiment(run)

        self._run = run

        if isinstance(self._run, Handler):
            self._root_object = self._run.get_root_object()
        else:
            self._root_object = self._run

        self.base_namespace = base_namespace
        self.resources = {}

        self._root_object[INTEGRATION_VERSION_KEY] = __version__

    def started_event(self, ex_info, command, host_info, start_time, config, meta_info, _id):
        self._root_object["sys/name"] = ex_info["name"]
        self._run[self.base_namespace]["config"] = stringify_unsupported(custom_flatten_dict(config))
        self._run[self.base_namespace]["sacred_config/sacred_id"] = str(_id)
        self._run[self.base_namespace]["sacred_config/host_info"] = stringify_unsupported(host_info)
        self._run[self.base_namespace]["sacred_config/meta_info"] = stringify_unsupported(
            custom_flatten_dict(meta_info)
        )
        self._run[self.base_namespace]["sacred_config/experiment_info"] = stringify_unsupported(
            custom_flatten_dict(ex_info)
        )

    def completed_event(self, stop_time, result: dict):
        if result:
            for i, (k, v) in enumerate(result.items()):
                if isinstance(v, str):
                    self._run[self.base_namespace][f"metrics/results/{k}"] = v
                elif isinstance(v, int) or isinstance(v, float):
                    self._run[self.base_namespace][f"metrics/results/{k}"] = float(v)
                elif isinstance(v, list) or isinstance(v, dict):
                    self._run[self.base_namespace][f"metrics/results/{k}"] = json.dumps(v)
                elif isinstance(v, File):
                    self._run[self.base_namespace][f"metrics/results/{k}"].upload(v)
                else:
                    warnings.warn(f"Logging results does not support type '{type(v)}' results. Ignoring this result")

    def interrupted_event(self, interrupt_time, status):
        pass

    def failed_event(self, fail_time, fail_trace):
        pass

    def artifact_event(self, name, filename, metadata=None, content_type=None):
        filename = os.path.split(filename)[-1]
        self._run[self.base_namespace][f"io_files/artifacts/{name}"].upload(filename)

    def resource_event(self, filename):
        if filename not in self.resources:
            md5 = get_digest(filename)
            self.resources[filename] = md5

        self._run[self.base_namespace]["io_files/resources"] = list(self.resources.items())

    def log_metrics(self, metrics_by_name, info):
        for metric_name, metric_ptr in metrics_by_name.items():
            for step, value, timestamp in zip(metric_ptr["steps"], metric_ptr["values"], metric_ptr["timestamps"]):
                self._run[self.base_namespace][f"metrics/{metric_name}"].append(
                    step=int(step), value=value, timestamp=timestamp.timestamp()
                )
