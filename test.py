#!/usr/bin/env python
from __future__ import print_function

# given a directory of images output a list of image -> predictions

from PIL import Image, ImageDraw
import argparse
import data
import itertools
from label_db import LabelDB
import model
import numpy as np
import os
import tensorflow as tf
import util as u

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--image-dir', type=str, required=True)
parser.add_argument('--run', type=str, required=True, help='model')
parser.add_argument('--batch-size', type=int, default=16)
parser.add_argument('--no-use-skip-connections', action='store_true')
parser.add_argument('--base-filter-size', type=int, default=16)
opts = parser.parse_args()
print(opts)

# test data reader
test_imgs, test_xys_bitmaps = data.img_xys_iterator(base_dir=opts.image_dir,
                                                    batch_size=opts.batch_size,
                                                    patch_fraction=1,
                                                    distort_rgb=False,
                                                    flip_left_right=False,
                                                    repeat=False)

with tf.variable_scope("train_test_model") as scope:  # clumsy :/
  model = model.Model(test_imgs,
                      is_training=False,
                      use_skip_connections=not opts.no_use_skip_connections,
                      base_filter_size=opts.base_filter_size)
  model.calculate_losses_wrt(labels=test_xys_bitmaps,
                             batch_size=opts.batch_size)
  
sess = tf.Session()
model.restore(sess, "ckpts/%s" % opts.run)
    
for idx in itertools.count():
  try:
    dice_l, xent_l = sess.run([model.dice_loss, model.xent_loss])
    print("idx", idx, "dice_loss", dice_l, "xent_loss", xent_l)
  except tf.errors.OutOfRangeError:
    # end of iterator
    break


