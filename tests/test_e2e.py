import neptune.new as neptune
import torch
from neptune.new.integrations.sacred import NeptuneObserver


def test_e2e(experiment, model):
    if torch.device("cuda:0"):
        torch.cuda.empty_cache()

    # Step 1: Initialize Neptune and create new Neptune Run
    neptune_run = neptune.init_run()

    # Step 2: Add NeptuneObserver() to your sacred experiment's observers
    experiment.observers.append(NeptuneObserver(run=neptune_run))

    # Step 3: Run you experiment and explore metadata in Neptune UI
    experiment.run()

    # More Options
    # Step 4: Log Artifacts (Model architecture and weights)

    # Save model architecture
    model_fname = "model"
    with open(f"{model_fname}_arch.txt", "w") as f:
        f.write(str(model))

    # Save model weights
    torch.save(model.state_dict(), f"./{model_fname}.pth")

    # Log model architecture and weights
    experiment.add_artifact(name=model_fname + "_arch", filename=f"./{model_fname}_arch.txt")
    experiment.add_artifact(name=model_fname, filename=f"./{model_fname}.pth")

    neptune_run.sync()

    assert neptune_run["experiment/config/data_dir"].fetch() == "data/CIFAR10"

    assert neptune_run.exists("experiment/io_files/artifacts/model")
    assert neptune_run.exists("experiment/io_files/artifacts/model_arch")

    assert 0 < neptune_run["experiment/metrics/results/final_acc"].fetch() < 1

    assert neptune_run.exists("experiment/sacred_config/experiment_info")
    assert neptune_run.exists("experiment/sacred_config/meta_info")

    # Stop run
    neptune_run.stop()
