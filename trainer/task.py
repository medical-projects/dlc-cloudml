import tensorflow as tf
import argparse
import os
import sys

from trainer import train

FLAGS = None


def main(_):
    train.train(FLAGS)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_dir',
        help='Directory to find training data',
        default='C:/Users/shires/DeepLabCutData/cell_01_video'
    )
    parser.add_argument(
        '--task',
        help='Task name',
        default='pole-whisking'
    )
    parser.add_argument(
        '--date',
        help='Data date',
        default='Sep6'
    )
    parser.add_argument(
        '--train_fraction',
        help='Train fraction',
        default=0.95
    )
    parser.add_argument(
        '--shuffle',
        help='Shuffle',
        default=1
    )
    parser.add_argument(
        '--weights_dir',
        help='Directory to find inital weights',
        default='../models/'
    )
    parser.add_argument(
        '--log_dir',
        help='Directory to save logs',
        default='./log'
    )

    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
