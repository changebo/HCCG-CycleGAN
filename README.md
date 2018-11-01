# HCCG-CycleGAN

[Generating Handwritten Chinese Characters using CycleGAN](https://arxiv.org/abs/1801.08624)  
[Bo Chang*](https://www.stat.ubc.ca/~bchang/), [Qiong Zhang*](https://www.stat.ubc.ca/~qiong.zhang/), [Shenyi Pan](https://www.linkedin.com/in/roypan), [Lili Meng](https://lilimeng1103.wixsite.com/research-site)  
WACV 2018.

## Abstract
Handwriting of Chinese has long been an important skill in East Asia. However, automatic generation of handwritten Chinese characters poses a great challenge due to the large number of characters. Various machine learning techniques have been used to recognize Chinese characters, but few works have studied the handwritten Chinese character generation problem, especially with unpaired training data. In this work, we formulate the Chinese handwritten character generation as a problem that learns a mapping from an existing printed font to a personalized handwritten style. We further propose DenseNet CycleGAN to generate Chinese handwritten characters. Our method is applied not only to commonly used Chinese characters but also to calligraphy work with aesthetic values. Furthermore, we propose content accuracy and style discrepancy as the evaluation metrics to assess the quality of the handwritten characters generated. We then use our proposed metrics to evaluate the generated characters from CASIA dataset as well as our newly introduced Lanting calligraphy dataset.

## Requirement
Python 2.7



## Preprocess handwritting database
The gnt files in CASIA HWDB1.1 database can be downloaded [here](http://www.nlpr.ia.ac.cn/databases/handwriting/Download.html).
```python 
python preprocess/preprocess_hw.py fonts/1252-c.gnt fonts/simhei.ttf 0.1 0.1 
``` 
Both the gnt file for the handwritten data and the ttf/otf file for the source font need to be under the fonts folder. The last two number represents for the split ratio of the training and test data.

## DenseCycleGAN 

### Usage
- Training
```python
cd DenseCycleGAN
DATA_ROOT=./datasets/1252-c-0.1-0.1 name=1252-c-dense5 which_model_netG=densenet_5blocks th train.lua
```

- Testing
```python
DATA_ROOT=./datasets/1252-c-0.1-0.1 name=1252-c-dense5 phase=test th test.lua
```


### Supported `which_model_netG` in training
- `resnet_6blocks`
- `resnet_9blocks`
- `densenet_5blocks`
- `densenet_6blocks`
- `densenet_7blocks`
- `densenet_8blocks`

## BibTeX
```
@inproceedings{chang2018generating, 
  title={Generating Handwritten Chinese Characters Using CycleGAN}, 
  author={Chang, Bo and Zhang, Qiong and Pan, Shenyi and Meng, Lili}, 
  booktitle={IEEE Winter Conference on Applications of Computer Vision}, 
  year={2018} 
}
```
