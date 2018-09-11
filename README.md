# Masters Dissertation

## Abstract
Identification of small cars in satellite imagery has a wide variety of applications. However, it is unclear what role resolution plays in small object detection accuracy, measured as average precision (AP). This study investigates the impact of spatial and object resolution (pixels per car) on car detection accuracy in satellite imagery using convolutional neural networks (CNNs). Two trials were conducted using the publicly available xView database. In the first trial, Inception-Single Shot Multibox Detector (I-SSD) CNN models were trained on images that had been downsampled, simulating low resolution images. In the second, I-SSD models were trained on images that had been upsampled (simulating low resolution images that had been enlarged). Subsequently, AP was modelled as a linear function of object size and downsample factor. Experimental results suggest that object resolution is a greater determinant of model accuracy than spatial resolution. Additionally, model accuracy may be increased by increasing overall image size.

### Note
This repository contains work done in completion of the requirements for the University College London MSc in Geographic Information Science 2018.  Results are considered preliminary and are not for dissemination or publication.  This repository is an educational resource only.

