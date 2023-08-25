import torch
import os
from torch.utils.data import Dataset
import numpy as np


acts = ['arm wrestle', 'basketball charge', \
                        'hold thighs', 'boxing', 'comfort1', \
                        'comfort2', 'body heart', 'shake hands',\
                        'cpr', 'backslapping to induce vomiting', 'hugging', \
                        'arrest', 'judo hold', 'piggy-back',\
                        'push car', 'security check', 'wrestling',\
                        'sumo', 'whisper', 'sit-ups',\
                        'two person jump', 'assisted stretching', 'clap hands']
path_to_data = "D:\data_csv\\"
for action_idx in np.arange(len(acts)):
    action = acts[action_idx]
    directory = '{0}bvh_leader\{1}'.format(path_to_data ,action)

    for root, dirs, files in os.walk(directory):

        dir_path = root

        files_in_dir = [file for file in os.listdir(dir_path) if
                        os.path.isfile(os.path.join(dir_path, file))]
        for index, file_name in enumerate(files_in_dir):
            if index%4 !=0:
                filename_leader = os.path.join(dir_path, file_name)
                filename_follower = filename_leader.replace('bvh_leader', 'bvh_follower')
                print("Reading leader action {0}, filename".format(filename_leader))
                # print("Reading follower action {0}".format(filename_follower))
