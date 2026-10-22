# ZpllMET: Parameterized neural network for rare-signal classification

Analysis code for my CMS search for a new heavy particle (Z′ → chargino pairs → two leptons + missing energy) using the full LHC Run 2 dataset. Result: [arXiv:2603.11035](https://arxiv.org/abs/2603.11035). I presented it at Moriond 2025.

The core problem is a classic imbalanced classification task: find a very rare signal hidden in Standard Model background that is many orders of magnitude larger, without knowing the signal's true mass in advance.

## What's in here

- **Parameterized neural network (PNN).** One TensorFlow/Keras model trained across 34 signal mass hypotheses, with the masses fed in as extra input features. A single network replaces 34 separate classifiers and interpolates between mass points. See `Pnn_v1-all.ipynb` and `Utils/Model.py`.
- **Feature engineering.** 13 kinematic features (lepton momenta, transverse mass, MT2, angular separations, missing energy) ranked by individual ROC AUC.
- **Weighted training and evaluation.** Per-event weights for cross section and simulation corrections; weighted ROC/AUC, train vs. test overfitting checks (`Utils/CommonTrain.py`, `EvaluatePNN-*.ipynb`).
- **Systematic uncertainties.** Model outputs re-evaluated under shifted inputs (e.g. missing-energy scale up/down) to measure how robust the classifier is (`SystematicPlots_*.ipynb`, `Utils/SystHelper.py`).
- **Statistical inference.** Classifier output histograms fed into a binned likelihood fit to set limits over the 2D mass plane (`combine/`, `2Dlimit_*.ipynb`).
- **Reproducible runs.** Config-driven (`config/`), templated batch jobs (`templates/`, `run_selection.sh`) across 3 channels × 4 data-taking periods, and a Dockerfile (`build/`).

## Stack

Python, TensorFlow/Keras, pandas, NumPy, scikit-learn, ROOT, Jupyter on CERN SWAN, Docker.

## Note

The input data are internal to the CMS collaboration and are not included, so the notebooks will not run as-is. The code is shared to show the modeling and analysis approach.
