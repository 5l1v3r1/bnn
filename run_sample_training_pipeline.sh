#!/usr/bin/env bash
set -x

rm -rf sample_data/labels/ ckpts/r12 tb/r12 sample_predictions.db

set -e

# run labelling UI
./label_ui.py \
    --image-dir sample_data/training/ \
    --label-db sample_data/labels.db \
    --width 768 --height 1024

# materialise label database into bitmaps
./materialise_label_db.py \
    --label-db sample_data/labels.db \
    --directory sample_data/labels/ \
    --width 768 --height 1024

# generate some samples of the data
./data.py \
    --image-dir sample_data/training/ \
    --label-dir sample_data/labels/ \
    --width 768 --height 1024

# train for a bit...
# note: this is nowhere near enough to get a good result; just
#       included for end to end testing
./train.py \
    --run r12 \
    --steps 100 \
    --train-steps 10 \
    --train-image-dir sample_data/training/ \
    --test-image-dir sample_data/test/ \
    --label-dir sample_data/labels/ \
    --width 768 --height 1024

# run inference against unlabelled data
./predict.py \
    --run r12 \
    --image-dir sample_data/unlabelled \
    --output-label-db sample_predictions.db \
    --export-pngs predictions
