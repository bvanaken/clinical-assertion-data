# Assertion Detection - Model Inference

Here you find a sample inference pipeline for clinical assertion classification. Based on clinical input text, we use [scispacy](https://allenai.github.io/scispacy/) to detect disease entities and apply our [model](https://huggingface.co/bvanaken/clinical-assertion-negation-bert) to classify their assertion types.

## How to run demo script:
`pip install -r requirements.txt`

`python inference.py`

The sample text can be found (and changed) in [inference.py](https://github.com/bvanaken/clinical-assertion-data/blob/7cebe24ce32bea0cd1f44c73c5ff6de84979a04b/model/inference.py#L94).