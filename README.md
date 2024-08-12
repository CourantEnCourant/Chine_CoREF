# Chine CoREF - model  

This repository stores a fine-tuned RoBERTa model to classify Chinese Weibo posts as ***protests*** or ***non-protests*** posts. It is thus a binary classification for strings.  

This documentation shows how to reproduce our results.  

---

 ## **Table of Contents**

- [Chine CoREF - model](#chine-coref---model)
  - [**Table of Contents**](#table-of-contents)
  - [Before you start](#before-you-start)
    - [Python packages requirements](#python-packages-requirements)
    - [How to use our scripts](#how-to-use-our-scripts)
    - [How did we create our datasets?](#how-did-we-create-our-datasets)

## Before you start

### Python packages requirements
- After creating a virtual env, use `pip install -r requirements.txt` to install required packages.  

NB: we highly recommand installing these packages manually, as those in our `requirements.txt` are configurated to adapt to our the server we used. We also chose to use `virtualenv` because `conda` did not work well on our server. Feel free to use your prefered method.  

### How to use our scripts
- For any .py scripts, use `python script.py -h` to see documentation.  
- For any .ipynb scripts, please refer to commentaries over each cell.  

### How did we create our datasets?


