'''
Software ExPI
Copyright Inria
Year 2021
Contact : wen.guo@inria.fr
GPL license.
'''
#vis_2p.py
# visualize input + pred/gt + error bar for a couple of actors

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FFMpegFileWriter, FFMpegWriter
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm

class ExPI3D(object):
    def __init__(self):
        #ExPI
        self.I   = np.array([0,0,0, 1,2,3,4,5, 7,8,9,10,11, 13,14,15,16,16,16,17,18,19,20,21,22,23,25,26,27,28,29,30,31,33,34,35])
        self.J   = np.array([1,7,13,2,3,4,5,6, 8,9,10,11,12,14,15,16,17,25,33,18,19,20,21,22,23,24,26,27,28,29,30,31,32,34,35,36])
        self.LR  = np.array([1,0,0, 1,1,1, 0,0,0, 0,0,0,0,  1,1,1,1], dtype=bool)
        self.ax = plt.figure().add_subplot(projection='3d')

        self.ax.cla()
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        self.ax.set_xlim3d([-50,50])#self.x)
        self.ax.set_zlim3d([-60,65])#self.y)
        self.ax.set_ylim3d([-50,50])#self.z)
        self.ax.axis('off')

    def update(self, f, channels, channels2=None):
        assert channels.size == 222, "channels should have 222 for 2p, it has %d instead" % channels.size

        # channels: 2p for gt
        vals_ = np.reshape( channels, (74, 3) )
        vals_l = vals_[:37,:]
        vals_f = vals_[37:,:]
        for j in range(2):
            vals = [vals_l,vals_f][j]
            for i in np.arange( len(self.I) ):
                x = np.array( [vals[self.I[i], 0], vals[self.J[i], 0]] )
                y = np.array( [vals[self.I[i], 1], vals[self.J[i], 1]] )
                z = np.array( [vals[self.I[i], 2], vals[self.J[i], 2]] )
                self.ax.plot(x, y, z, lw=2, c="lightcoral" if j ==0 else "cornflowerblue")

        # channels2: 2p for pred
        if channels2 is not None:
            vals2_ = np.reshape( channels2, (74, -1) )
            vals2_l = vals2_[:37,:]
            vals2_f = vals2_[37:,:]
            for j in range(2): # pred
                vals2 = [vals2_l, vals2_f][j]
                for i in np.arange( len(self.I) ):
                    x = np.array( [vals2[self.I[i], 0], vals2[self.J[i], 0]] )
                    y = np.array( [vals2[self.I[i], 1], vals2[self.J[i], 1]] )
                    z = np.array( [vals2[self.I[i], 2], vals2[self.J[i], 2]] )
                    self.ax.plot(x, y, z, lw=2, c="darkred" if j == 0 else "darkblue")

        # time string
        if f>=50:
            time_string = "Pred/GT: "+str((f-49))+'frame'
        else: # input
            time_string = "Input: "+str((f-49)*1000/25.0)+'ms'
        self.ax.text2D(-0.04,-0.1, time_string, fontsize=15)


def vis_pi_compare(p3d_gt, p3d_pred, save_path, err_list=None):
    # p3d_gt: numpy array with len (50+output_n,222)
    # p3d_pred: numpy array with len (output_n,222)
    # save_path: path and name for saving the mp4 video, eg: ./outputs/test.mp4
    # err_list: numpy array with len output_n

    num_frames_gt = len(p3d_gt) #75
    num_frames_pred = len(p3d_pred) #25
    p3d_gt = p3d_gt.reshape((num_frames_gt,-1))
    p3d_pred = p3d_pred.reshape((num_frames_pred,-1))

    metadata = dict(title='01', artist='Matplotlib',comment='motion')
    writer = FFMpegFileWriter(fps=10, metadata=metadata)
    fig = plt.figure()
    ob = ExPI3D()

    import os

    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"目录 '{save_path}' 创建成功")

    with writer.saving(fig, save_path+'example.mp4', 120):
        f = 0
        for i in tqdm(range(num_frames_gt - num_frames_pred)): # vis input
            ## uncomment to vis input as well
            ob.update(f, p3d_gt[i])
            writer.grab_frame()
            plt.pause(0.01)
            plt.clf()
            f += 1
        for i in tqdm(range(num_frames_gt - num_frames_pred,num_frames_gt)): # vis pred vs gt
            ob.__init__()
            ob.update(f, p3d_gt[i], p3d_pred[i-num_frames_gt+num_frames_pred])

            ## draw an error bar for err_list
            if err_list is not None: #draw an error bar for err_list
                err = err_list[i-num_frames_gt+num_frames_pred]
                ob.ax.text2D(-0.04,-0.085, 'JME:'+str(round(err,1))+'mm', fontsize=15)
                fig.add_artist(patches.Rectangle((0.35, 0.11), 0.35, 0.025, ec = 'black', fc='white', fill=False, lw=0.5))
                max_err=500
                err_len = err/max_err * 0.35
                fig.add_artist(patches.Rectangle((0.35, 0.11), err_len, 0.025, fill=True,lw=0.5))
            ## uncomment to save imgs for each frame
            plt.savefig(save_path+'_'+str(i)+'.jpg')

            writer.grab_frame()
            plt.pause(0.01)
            f += 1
    plt.close()

