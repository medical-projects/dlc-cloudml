import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import cv2

import local_processing.analysis_util.analysis_util as au
from skimage.draw import circle, line, bezier_curve
import skvideo
skvideo.setFFmpegPath('C:/Program Files/ffmpeg/bin/')
from local_processing.video_maker.video_processor import VideoProcessorSK as vp
import matplotlib.pyplot as plt

base_folder = 'Z:/Data/BarthAirPuff/'
task = 'air-puff'
date = 'Dec7'
shuffle = 1
train_fraction = 0.95
snapshot_index = 0
video_name = '9 psi.MOV'
pcutoff = 0.3
dotsize = 4
resnet = 50
snapshot = 600000

# for ts plotting
pick_bodypart = 'tip11'
def_color = [255, 0, 0]


def create_video(clip, data_frame):
    scorer = np.unique(data_frame.columns.get_level_values(0))[0]
    body_parts_to_plot = list(np.unique(data_frame.columns.get_level_values(1)))
    color_class = plt.cm.ScalarMappable(cmap='hsv')
    C = color_class.to_rgba(np.linspace(0, 1, len(body_parts_to_plot)))
    colors = (C[:, :3] * 255).astype(np.uint8)

    ny, nx, fps = clip.height(), clip.width(), clip.fps()
    n_frames = len(data_frame.index)

    video = cv2.VideoWriter(os.path.join(base_folder, video_name.split('.')[0] + '-labeled.avi'),
                            cv2.VideoWriter_fourcc(*"XVID"), fps, (nx, ny))

    p_ind = []
    x_p = []
    for index in tqdm(range(n_frames)):
        image = clip.load_frame()
        xs = []
        ys = []
        for bp_index, bp in enumerate(body_parts_to_plot):
            if data_frame[scorer][bp]['likelihood'].values[index] > pcutoff:
                xc = int(data_frame[scorer][bp]['x'].values[index])
                xs.append(xc)
                yc = int(data_frame[scorer][bp]['y'].values[index])
                ys.append(yc)

                rr, cc = circle(yc, xc, dotsize, shape=(ny, nx))
                image[rr, cc, :] = colors[bp_index]

        p_ind.append(int((index / n_frames) * nx))
        x_p.append(ny - data_frame[scorer][pick_bodypart]['y'].values[index])
        for x, xp in enumerate(x_p):
            rr, cc = circle(int(xp) + 100, p_ind[x], 2, shape=(ny, nx))
            image[rr, cc, :] = def_color

        frame = image
        video.write(frame)
        # clip.save_frame(frame)

    cv2.destroyAllWindows()
    video.release()
    clip.close()


def make_labeled_video():
    scorer = 'deep-cut-resnet_' + str(resnet) + '-' + str(int(train_fraction * 100)) + 'shuffle' + \
             str(int(shuffle)) + '-' + str(int(snapshot)) + '-for-task-' + task
    clip = vp(os.path.join(base_folder, video_name),
              os.path.join(base_folder, video_name.split('.')[0] + '-labeled.mp4'))
    data_file = scorer + video_name.split('.')[0] + '.h5'
    data_frame = pd.read_hdf(os.path.join(base_folder, data_file))
    create_video(clip, data_frame)


if __name__ == '__main__':
    make_labeled_video()
