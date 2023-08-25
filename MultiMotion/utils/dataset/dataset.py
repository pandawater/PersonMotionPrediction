import torch
import os
from torch.utils.data import Dataset
import numpy as np
from utils import data_utils, vis_2p


class Datasets(Dataset):
    def __init__(self, opt, is_train=True):

        self.path_to_data = "D:\data_csv\\"
        self.is_train = is_train
        if is_train:#train
            self.in_n = opt.input_n
            self.out_n = opt.kernel_size
            self.split = 0
        else: #test
            self.in_n = 50
            self.out_n = opt.output_n
            self.split = 1
        self.skip_rate = 1
        self.p3d = {}
        self.data_idx = []

        if opt.protocol == 'pro3': # unseen action split
            if is_train: #train on acro2
                acts = ['arm wrestle', 'basketball charge', \
                        'hold thighs', 'boxing', 'comfort1', \
                        'comfort2', 'body heart', 'shake hands', \
                        'cpr', 'backslapping to induce vomiting', 'hugging', \
                        'arrest', 'judo hold', 'piggy-back', \
                        'push car', 'security check', 'wrestling', \
                        'sumo', 'whisper', 'sit-ups', \
                        'two person jump', 'assisted stretching', 'clap hands']
            else: #test on acro1
                acts = ['arm wrestle']


                #if opt.test_split is not None: #test per ac

        key = 0
        for action_idx in np.arange(len(acts)):
            action = acts[action_idx]
            directory = '{0}bvh_leader\{1}'.format(self.path_to_data,action)

            for root, dirs, files in os.walk(directory):

                    dir_path = root
                    files_in_dir = [file for file in os.listdir(dir_path) if
                                    os.path.isfile(os.path.join(dir_path, file))]
                    for index, file_name in enumerate(files_in_dir):
                        if index % 4 == 0:
                            filename_leader = os.path.join(dir_path, file_name)
                            filename_follower = filename_leader.replace('bvh_leader', 'bvh_follower')
                            # print("Reading leader action {0}, filename".format(filename_leader))
                            # print("Reading follower action {0}".format(filename_follower))
                            #print(filename_leader)
                            the_sequence_leader = data_utils.readCSVasFloat(filename_leader, with_key=True)
                            the_sequence_follower = data_utils.readCSVasFloat(filename_follower, with_key=True)
                            num_frames1 = the_sequence_leader.shape[0]
                            num_frames2 = the_sequence_follower.shape[0]
                            if num_frames1 != num_frames2:
                                print("wrong_load{0}".format(filename_leader))
                            the_sequence = data_utils.normExPI_2p_by_frame(the_sequence_leader, the_sequence_follower)
                            the_sequence = torch.from_numpy(the_sequence).float().cuda()

                            if self.is_train:  # train
                                seq_len = self.in_n + self.out_n
                                valid_frames = np.arange(0, num_frames1 - seq_len + 1, self.skip_rate)
                            else:  # test
                                seq_len = self.in_n + 30
                                valid_frames = data_utils.find_indices_64(num_frames1, seq_len)
                            p3d = the_sequence
                            self.p3d[key] = p3d.view(num_frames1, -1).cpu().data.numpy()
                            tmp_data_idx_1 = [key] * len(valid_frames)
                            tmp_data_idx_2 = list(valid_frames)
                            self.data_idx.extend(zip(tmp_data_idx_1, tmp_data_idx_2))
                            key += 1






        self.dimension_use = np.arange(37*2*3)
        self.in_features = len(self.dimension_use)

    def __len__(self):
        return np.shape(self.data_idx)[0]

    def __getitem__(self, item):
        key, start_frame = self.data_idx[item]
        fs = np.arange(start_frame, start_frame + self.in_n + self.out_n)
        data = self.p3d[key][fs][:,self.dimension_use]
        return data