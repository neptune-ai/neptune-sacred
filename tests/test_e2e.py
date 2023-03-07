import neptune
import torch

from neptune_sacred import NeptuneObserver


def test_e2e(experiment, model):

    # Step 1: Initialize Neptune and create new Neptune Handler
    neptune_handler = neptune.init_run()["sacred"]

    # Step 2: Add NeptuneObserver() to your sacred experiment's observers
    experiment.observers.append(NeptuneObserver(run=neptune_handler))

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

    run = neptune_handler.get_root_object()
    run.sync()

    assert run["sacred/experiment/config/data_dir"].fetch() == "data/CIFAR10"

    assert run.exists("sacred/experiment/io_files/artifacts/model")
    assert run.exists("sacred/experiment/io_files/artifacts/model_arch")

    assert 0 < run["sacred/experiment/metrics/results/final_acc"].fetch() < 1

    assert run.exists("sacred/experiment/sacred_config/experiment_info")
    assert run.exists("sacred/experiment/sacred_config/meta_info")

    # Stop run
    run.stop()
