import os

import cv2 as cv
import numpy as np
import torch
from torchvision import transforms
from tqdm import tqdm

from config import device
from data_gen import data_transforms
from utils import ensure_folder

# IMG_FOLDER = '../data/frame/2020-04-27/shu/5-3'
# TRIMAP_FOLDER = '../data/trimap/2020-04-27/shu/5-3'
# OUTPUT_FOLDER = '../data/detatilmask/2020-04-27/shu/5-3'


def detail_trimap(img_folder, trimap_folder, output_folder):
    checkpoint = 'preModel/BEST_checkpoint.tar'
    checkpoint = torch.load(checkpoint)
    model = checkpoint['model'].module
    model = model.to(device)
    model.eval()

    transformer = data_transforms['valid']

    ensure_folder(output_folder)

    files = [f for f in os.listdir(img_folder) if f.endswith('.png') or f.endswith('.jpg')]

    for file in tqdm(files):
        filename = os.path.join(img_folder, file)
        img = cv.imread(filename)
        print(img.shape)
        h, w = img.shape[:2]

        x = torch.zeros((1, 4, h, w), dtype=torch.float)
        image = img[..., ::-1]  # RGB
        image = transforms.ToPILImage()(image)
        image = transformer(image)
        x[0:, 0:3, :, :] = image

        file = os.path.splitext(file)[0] + ".png"
        filename = os.path.join(trimap_folder, file)
        print('reading {}...'.format(filename))
        trimap = cv.imread(filename, 0)
        x[0:, 3, :, :] = torch.from_numpy(trimap.copy() / 255.)
        # print(torch.max(x[0:, 3, :, :]))
        # print(torch.min(x[0:, 3, :, :]))
        # print(torch.median(x[0:, 3, :, :]))

        # Move to GPU, if available
        x = x.type(torch.FloatTensor).to(device)

        with torch.no_grad():
            pred = model(x)

        pred = pred.cpu().numpy()
        pred = pred.reshape((h, w))

        pred[trimap == 0] = 0.0
        pred[trimap == 255] = 1.0

        out = (pred.copy() * 255).astype(np.uint8)

        filename = os.path.join(output_folder, file)
        cv.imwrite(filename, out)
        print('wrote {}.'.format(filename))
