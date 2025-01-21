from torchvision.transforms import Compose, Resize, Normalize, ToTensor
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import numpy as np
import torch
import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.metrics import auc
from ranx import Run, fuse
import faiss