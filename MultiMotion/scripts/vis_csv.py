import csv
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

nb_kpts = 37
p1_order0 = [0,0,0, 1,2,3,4,5, 7,8,9,10,11, 13,14,15,16,16,16,17,18,19,20,21,22,23,25,26,27,28,29,30,31,33,34,35]
p1_order1 = [1,7,13,2,3,4,5,6, 8,9,10,11,12,14,15,16,17,25,33,18,19,20,21,22,23,24,26,27,28,29,30,31,32,34,35,36]
#p1_order0 = [1,1,1,    2, 3, 4, 28, 29, 30, 31, 32, 22,23,24,25,26, 16,17,18,19,20, 10,11,12,13,14,6,7,8]
#p1_order1 = [28,22,2,  3, 4, 5, 29, 30, 31, 32, 33, 23,24,25,26,27, 17,18,19,20,21, 11,12,13,14,15,7,8,9]
order_orig = ['Solving', 'Hips',\
              #0,1
              'LeftUpLeg', 'LeftLeg',  'LeftFoot',  'LeftForeFoot',  'LeftToeBase', 'LeftToeBaseEnd', \
              #2,7
              'RightUpLeg', 'RightLeg', 'RightFoot', 'RightForeFoot',  'RightToeBase',  'RightToeBaseEnd',\
              #8,13
              'Spine', 'Spine', 'Spine2',  'Spine3', \
              #14,17
              'LeftShoulder',  'LeftArm',  'LeftForeArm',  'LeftHand',  'LeftHandMiddle1', 'LeftHandMiddle1End',  'LeftHandThumb1', 'LeftHandThumb1End',\
              #18,25
              'RightShoulder',  'RightArm',  'RightForeArm',  'RightHand', 'RightHandMiddle1', 'RightHandMiddle1End', 'RightHandThumb1',  'RightHandThumb1End', \
              #26,33
              'Neck',  'Neck1',  'Head',  'HeadEnd']
              #34,37

motion = ['arm wrestle', 'basketball charge', \
          'hold thighs', 'boxing', 'comfort', 'comfort2', \
          'body heart', 'shake hands', 'cpr', \
          'backslapping to induce vomiting', 'hugging', 'arrest', \
          'judo hold', 'piggy-back', 'push car',\
          'security check', 'wrestling', 'sumo', \
          'whisper', 'sit-ups', 'two person jump', 'assisted stretching'\
          'clap hands']

def main():
    root_path1 = "D:/data_csv/bvh_follower/hold thighs/0006_worldpos.csv"
    root_path2 = "D:/data_csv/bvh_leader/hold thighs/0006_worldpos.csv"

    gt1 = load_csv(root_path1)
    gt2 = load_csv(root_path2)
    vis_3d(gt1,gt2)
    #print(gt)

def load_csv(root_path):
    ## read gt
    tsv_file = open(root_path)
    read_tsv = csv.reader(tsv_file, delimiter=",")
    #gt = {}
    t = 1
    for row in read_tsv:
        if t == 1:
            order = [str(o) for o in row][1:]

            print(order)
        if t == 400:
            #img_id = t - 2 + offset
            #img_name = 'img-' + str(img_id).zfill(6) + '.jpg'
            gt = np.array([float(g) for g in row][1:])#.reshape((nb_kpts, 3))
            print(len(gt))
        t += 1
    #print(t)
    tsv_file.close()
    return gt

def vis_3d(pose_list1,pose_list2):
    p1 = np.array(pose_list1, dtype=np.float32).reshape((nb_kpts, 3))
    p2 = np.array(pose_list2, dtype=np.float32).reshape((nb_kpts, 3))
    p1_y, p1_x, p1_z = p1[:, 1], p1[:, 0], p1[:, 2]
    p2_y, p2_x, p2_z = p2[:, 1], p2[:, 0], p2[:, 2]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(nb_kpts):
            ax.scatter(p1_x[i], p1_y[i], p1_z[i], c='black')

    for i in range(len(p1_order0)):
        ax.plot([p1_x[p1_order0[i]], p1_x[p1_order1[i]]], \
                [p1_y[p1_order0[i]], p1_y[p1_order1[i]]], \
                [p1_z[p1_order0[i]], p1_z[p1_order1[i]]], \
                c='r')

    for i in range(nb_kpts):
            ax.scatter(p2_x[i], p2_y[i], p2_z[i], c='black')
    for i in range(len(p1_order0)):
        ax.plot([p2_x[p1_order0[i]], p2_x[p1_order1[i]]], \
                [p2_y[p1_order0[i]], p2_y[p1_order1[i]]], \
                [p2_z[p1_order0[i]], p2_z[p1_order1[i]]], \
                c='r')
    ax.set_xlabel('x')
    ax.set_ylabel('depth')
    ax.set_zlabel('y')
    ax.set_zlim(-40, 120)  # (0,1800)
    plt.xlim(-40, 80)
    plt.ylim(-40, 80)
    ax.view_init(30, -120)

    plt.show()

if __name__ == '__main__':
        main()