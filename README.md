<p align="center">
  <a href="https://www.uit.edu.vn/"><img src="https://www.uit.edu.vn/sites/vi/files/banner.png"></a>
<h1 align="center"><b>CS336.P11.KHTN - MULTIMEDIA INFORMATION RETRIEVAL</b></h1>

## Introduction
* Subject name: MULTIMEDIA INFORMATION RETRIEVAL
* Class code: CS336.P11.KHTN
* Semester: 5 (2024-2025)

### Lecturer
* PhD. Ngo Duc Thanh - thanhnd@gm.uit.edu.vn

### Team members

| No | Name | MSSV | Email | Github |
| :---: | --- | --- | --- | --- |
| 1 | Nguyen Duy Thang | 22521333 | 22521333@gm.uit.edu.vn | [github](https://github.com/DyThen-Kumo) |

### Overview
Image retrieval is an important area of computer vision that focuses on finding relevant images from a database based on a query. This query can be an image, text, or other information. The goal of the problem is to find the images in the database that are most similar or relevant to the input information need according to some predefined criteria.
Input:
- Query: An image or a text that represents information need.
- Database: A collection of images.
Output: A set of images that is relevant to information need.

## Data
* The dataset used is the [Paris Buildings Dataset](https://www.robots.ox.ac.uk/~vgg/data/parisbuildings/). This dataset consists of 6412 images collected from Flickr by searching for specific landmarks of Paris. However, the data is currently not available at the original link, so it will be searched from [another source](https://www.kaggle.com/datasets/skylord/oxbuildings) and use the ground-truth file at the original link.
* The dataset have "Note, 20 of the supplied images are corrupted but are still included for backwards compatibility ". So, we have 6392 available images. 
* There are 50 queries in total stored in _query.txt files including file name and bounding box to represent the area to query.
* The relevant files corresponding to each query are saved in the form _ok.txt and _good.txt

## Solution and Experiment
* Detail in the [report](Report.pdf).
* You should add data to "/static/data" and run app.py to deploy the project.

## Demo
* You can see demo at [Youtube](https://www.youtube.com/watch?v=W8_yNJzeGYQ)

## Reference
[1] Javed A. Aslam and Mark H. Montague. Models for metasearch. In W. Bruce Croft, David J. Harper, Donald H.
Kraft, and Justin Zobel, editors, SIGIR 2001: Proceedings of the 24th Annual International ACM SIGIR
Conference on Research and Development in Information Retrieval, September 9-13, 2001, New Orleans,
Louisiana, USA, pages 275–284. ACM, 2001. doi: 10.1145/383952.384007. URL https://doi.org/10.
1145/383952.384007.

[2] Elias Bassani and Luca Romelli. ranx.fuse: A python library for metasearch. In CIKM, pages 4808–4812. ACM,
2022. doi: 10.1145/3511808.3557207.

[3] Gordon V. Cormack, Charles L. A. Clarke, and Stefan Büttcher. Reciprocal rank fusion outperforms condorcet
and individual rank learning methods. In SIGIR, pages 758–759. ACM, 2009.

[4] Matthijs Douze, Alexandr Guzhva, Chengqi Deng, Jeff Johnson, Gergely Szilvasy, Pierre-Emmanuel Mazaré,
Maria Lomeli, Lucas Hosseini, and Hervé Jégou. The faiss library. 2024.

[5] Edward A. Fox and Joseph A. Shaw. Combination of multiple searches. In TREC, volume 500-215 of NIST
Special Publication, pages 243–252. National Institute of Standards and Technology (NIST), 1993.

[6] Herve Jégou, Matthijs Douze, and Cordelia Schmid. Product quantization for nearest neighbor search. IEEE
Transactions on Pattern Analysis and Machine Intelligence, 33(1):117–128, 2011. doi: 10.1109/TPAMI.2010.
57.

[7] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry,
Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable
visual models from natural language supervision. In Marina Meila and Tong Zhang, editors, Proceedings of the
38th International Conference on Machine Learning, ICML 2021, 18-24 July 2021, Virtual Event, volume 139
of Proceedings of Machine Learning Research, pages 8748–8763. PMLR, 2021. URL http://proceedings.
mlr.press/v139/radford21a.html.