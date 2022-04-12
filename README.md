# Neptune + Sacred Integration

Neptune is a tool used for experiment tracking, model registry, data versioning, and live model monitoring. This integration lets you use it as a UI (frontend) for the experiments you track in Sacred.

## What will you get with this integration? 

* Log, display, organize, and compare ML experiments in a single place
* Version, store, manage, and query trained models, and model building metadata
* Record and monitor model training, evaluation, or production runs live

## What will be logged to Neptune?

* Hyper-parameters
* Losses & metrics
* Training code(Python scripts or Jupyter notebooks) and git information
* Dataset version
* Model Configuration
* [Other metadata](https://docs.neptune.ai/you-should-know/what-can-you-log-and-display)

![image](https://user-images.githubusercontent.com/97611089/160633857-48aa87ac-fcab-4225-8172-05aba159feaf.png)
*Example custom dashboard in the Neptune UI*


## Resources

* [Documentation](https://docs.neptune.ai/integrations-and-supported-tools/experiment-tracking/sacred)
* [Code example on GitHub](https://github.com/neptune-ai/examples/tree/main/integrations-and-supported-tools/sacred/scripts)
* [Example dashboard in the Neptune app](https://app.neptune.ai/o/common/org/sacred-integration/e/SAC-11/dashboard/Sacred-Dashboard-6741ab33-825c-4b25-8ebb-bb95c11ca3f4)
* [Run example in Google Colab](https://colab.research.google.com/github/neptune-ai/examples/blob/main/integrations-and-supported-tools/sacred/notebooks/Neptune_Sacred.ipynb)

## Example

```python
# On the command line:
pip install neptune-client[sacred] sacred torch torchvision
```
```python
# In Python:
import neptune.new as neptune


# Start a run
run = neptune.init(project = "common/sacred-integration",
                   api_token = "ANONYMOUS")

# Create a sacred experiment
experiment = Experiment("image_classification", interactive=True)

# Add NeptuneObserver and run the experiment
experiment.observers.append(NeptuneObserver(run=neptune_run))
experiment.run()
```

## Support

If you got stuck or simply want to talk to us, here are your options:

* Check our [FAQ page](https://docs.neptune.ai/getting-started/getting-help#frequently-asked-questions)
* You can submit bug reports, feature requests, or contributions directly to the repository.
* Chat! When in the Neptune application click on the blue message icon in the bottom-right corner and send a message. A real person will talk to you ASAP (typically very ASAP),
* You can just shoot us an email at support@neptune.ai
