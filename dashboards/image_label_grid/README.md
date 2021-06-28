# Image-label grid viewer

This template aims to help viewing the images per label in a labeled image dataset (demonsrated here using ImageNet1K and Tiny ImageNet as examples).

# Instructions

## Install requirements

```bash
pip install -r requirements.txt
```
## Download ImageNet1K and Tiny ImageNet

### ImageNet1K

1. Download ImageNet1K from 
[ImageNet official site](https://www.image-net.org/challenges/LSVRC/2012/2012-downloads.php#images) and unpack locally.
2. Download ID to text label mapping from [Caffe repository](https://github.com/HoldenCaulfieldRye/caffe/blob/master/data/ilsvrc12/synset_words.txt) and place it locally as `.../ILSVRC2017_CLS-LOC/synset_words.txt`

### Tiny ImageNet

1. Download Tiny ImageNet from [ImageNet official site](https://www.image-net.org/download-images.php)

## Run

```bash
streamlit run ui.py
```
