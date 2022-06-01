# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :   test.py
@Time    :   2022/05/20 18:42:09
@Author  :   Li Ruikun
@Version :   1.0
@Contact :   1842604700@qq.com
@License :   (C)Copyright 2022 Li Ruikun, All rights reserved.
@Desc    :   Predict the test dataset
"""

import os
import cv2
import torch
import argparse
from tqdm import tqdm
from torchvision import transforms

from TrainPipeline.dataset import TEST_Dataset
from utils.exception_handler import exception_handler
from models.dcgan import Generator as dc_generator
from models.backbone import FeatureExtractor
from utils.log import denormalize


parser = argparse.ArgumentParser()
parser.add_argument('--cuda', type=int, default=0, help='xxx')
parser.add_argument('--use_gpu', type=bool, default=True, help='xxx')
parser.add_argument('--type', type=str, default='Radar', help='Image type to predict')
parser.add_argument('--img_size', type=int, default=256, help='Image size')
parser.add_argument('--latent_dim', type=int, default=100, help='xxx')
parser.add_argument('--channels', type=int, default=1, help='xxx')

# config
opt = parser.parse_args()
torch.cuda.set_device(opt.cuda)


@exception_handler
def Predict(opt):
    """Predict the Test Dataset
            
    Parameters:
    ------- 
    opt:
        the config of the model
    g_path:
        the path of the generator
    fe_path:
        the path of the feature extractor
    lstm_path:
        the path of the LSTM
    """

    print('🎉 开始预测!')

    # mkdir
    os.makedirs('submit/', exist_ok=True)
    result_dir = 'submit/'+opt.type.upper()+'/'
    os.makedirs(result_dir, exist_ok=True)


    # Initialize feature_extractor, generator, predictor ,optimizer and loss_fn
    feature_extractor = FeatureExtractor(opt.img_size, opt.latent_dim)
    generator = dc_generator(opt)
    predictor = torch.nn.LSTM(input_size=100, hidden_size=100, batch_first=True, num_layers=5)

    # Device
    if opt.use_gpu:
        predictor.to('cuda')
        feature_extractor.to('cuda')
        generator.to('cuda')

    # Load model
    fe_path = f'best/{opt.type.lower()}_fe.pth'
    g_path = f'best/{opt.type.lower()}_generator.pth'
    lstm_path = f'best/{opt.type.lower()}_predictor.pth'
    feature_extractor.load_state_dict(torch.load(fe_path))
    generator.load_state_dict(torch.load(g_path))
    predictor.load_state_dict(torch.load(lstm_path))
    print(f'🌈 {opt.type.lower()} 模型加载成功！')

    # Configure data loader
    datasets = TEST_Dataset(img_dir='data/TestB1/' + f'{opt.type.capitalize()}', img_size=opt.img_size)
    dataloader = range(104)

    print(f'🔋 {opt.type.capitalize()} 数据加载成功！')

    # ----------
    #  Predicting
    # ----------

    bar_format = '{desc}{n_fmt:>3s}/{total_fmt:<5s} |{bar}|{postfix}'
    print('🚀 开始测试！')

    with tqdm(total=len(dataloader), bar_format=bar_format) as bar:
        for folder_id in dataloader:
            
            # make sub dir
            sub_result_dir = result_dir + '{:03d}/'.format(folder_id+1)
            os.makedirs(sub_result_dir, exist_ok=True)
            
            # display the first part of progress bar
            bar.set_description(f"\33[36m🌌 ")
            
            # Get the data
            imgs = datasets[folder_id].to('cuda')

            # Predict a batch of images
            history_features = feature_extractor(imgs).unsqueeze(0)
            pred_features, _ = predictor(history_features)
            pred_features = pred_features.squeeze(dim=0)
            
            # Generate the predict images
            pred_imgs = generator(pred_features)         
            pred_imgs = denormalize(pred_imgs.data)
            for j in range(20):
                result = cv2.resize(torch.permute(pred_imgs[j], (1,2,0)).cpu().numpy(), (560, 480))
                cv2.imwrite(sub_result_dir + f"{opt.type.lower()}_{(j+1):03d}.png", result)

            # display the last part of progress bar
            bar.set_postfix_str('\33[0m')
            bar.update()

if __name__ == '__main__':
    Predict(opt)