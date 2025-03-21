# Chine CoREF - model  

This repository records the training process of a fine-tuned RoBERTa model to identify protests on Chinese Weibo posts.

Our work is largely inspired by Jennifer Pan's paper [CASM: A Deep-Learning Approach for Identifying Collective Action Events with Text and Image Data from Social Media](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/SS4LNN). We can see this project as a modernised reproduction of this paper with SOTA LLMs.

---

## Code Organization
1. ```data/```: training data
2. ```src/```: models
3. ```scripts/```:
   - ```generate_positive.ipynb```: a data-vizualization script for Jennifer Pan's original dataset to generate positive set for training
   - ```create_training_set.py```: generate negative set for training
   - ```test_training_server.ipynb```: test the training process on 10% for our dataset
   - ```traing_server.ipynb```: training on the whole dataset
   - ```use_model.ipynb``` (for future development): some qualitative test for our fine-tuned model

## Getting Started

To get started, create a virtual environment containing the required dependencies

```bash
python -m venv ./coref_env
pip install -r ./requirements.txt
```

## Reproducing Experiments
Below, we describe the steps required for reproducing our training process

### Download datasets
For positive set, download Jennifer Pan's dataset from [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/SS4LNN) and put `protest_posts.csv` at `./data/raw/`

For negative set, download [senti-weibo](https://drive.google.com/file/d/1yMCP44ICH1Gl29x920QyT9LQCnVg_2S6/view) from [this github repo](https://github.com/wansho/senti-weibo?tab=readme-ov-file)

### Prepare datasets
Run ```generate_positive.ipynb``` to generate positive set

Run ```python create_training_set.py -h``` for help to generate training dataset

### Prepare model and training
Run ```training_server.ipynb``` to download and train the model



