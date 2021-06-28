# Copyright 2021 dashboard_template Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Example utilities for loading image data (ImageNet & Tiny ImageNet)."""

import os
import glob
import pandas as pd
from typing import Tuple, List


def load_imagenet(
        version: str = 'tiny',
        sample_per_label: str = 20) -> Tuple[List[str], List[str], pd.DataFrame]:
    """Gating function for loading ImageNet image paths and its paths."""

    fpath_rootdirs = './data_dirs.csv'
    root_dirs = {}
    try: 
        with open(fpath_rootdirs, 'r') as f:
            lines = f.readlines()
            for l in lines:
                ver, root_dir = l.rstrip().split(',')
                root_dirs[ver] = root_dir
    except Exception as e:
        raise IOError(f'Error in reading file of paths, {e}')
    if version == 'tiny':
        df, df_label_id_name = load_tiny_imagenet(
            root_dir=root_dirs['tiny'],
            sample_per_label=sample_per_label)
    elif version == 'full':
        df, df_label_id_name = load_full_imagenet(
            root_dir=root_dirs['full'],
            sample_per_label=sample_per_label)
    else:
        raise NotImplementedError(f'ImageNet version {version} is not supported.')
    return df, df_label_id_name


def load_full_imagenet(
        root_dir: str,
        sample_per_label: int = 20,
        labelspace_version: str = 'observed') -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load the full ImageNet1K image paths and labels."""

    fname_labelmap = 'synset_words.txt'
    fpath_labelmap = os.path.join(root_dir, fname_labelmap)
    img_dirs = glob.glob(os.path.join(root_dir, 'ILSVRC', 'Data', 'CLS-LOC', 'train', 'n*'))

    # Load labelmap txt file
    with open(fpath_labelmap, 'r') as f:
        lines = f.readlines()
        label_ids = []
        label_names = []

        for l in lines:
            label_id = l.split(' ')[0]
            label_name = ' '.join(l.rstrip().split(' ')[1:])
            label_ids.append(label_id)
            label_names.append(label_name)

    df_label_id_name = pd.DataFrame.from_dict({
        'label_id': label_ids,
        'label_name': label_names,
    })

    df_belt = []
    for img_dir in img_dirs:
        label_id = img_dir.split('/')[-1]
        img_fpaths = glob.glob(os.path.join(img_dir, '*.JPEG'))[:sample_per_label]
        img_ids = [fpath.split('/')[-1].rstrip('.JPEG') for fpath in img_fpaths]
        label_name = df_label_id_name[df_label_id_name['label_id']==label_id]['label_name'].tolist()[0]
        df_part = pd.DataFrame.from_dict(
            {'img_id': img_ids,
             'img_fpath': img_fpaths,
             'label_id': [label_id] * len(img_fpaths),
             'label_name': [label_name] * len(img_fpaths)})
        df_belt.append(df_part)
    df = pd.concat(df_belt)

    if labelspace_version == 'observed':
        df_label_id_name = df.groupby(
            by=['label_id','label_name'])\
            .size()\
            .reset_index()\
            .rename(columns={0:'count'})[['label_id','label_name']]
    return df, df_label_id_name


def load_tiny_imagenet(
        root_dir: str,
        sample_per_label: int = 20,
        labelspace_version: str = 'observed') -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load the Tiny ImageNet image paths and labels."""

    fname_labelmap = 'words.txt'
    fpath_labelmap = os.path.join(root_dir, fname_labelmap)
    img_dirs = glob.glob(os.path.join(root_dir, 'train', 'n*', 'images'))
    df_label_id_name = pd.read_csv(fpath_labelmap,
                                   delimiter='\t',
                                   header=None,
                                   names=['label_id', 'label_name'])
    df_belt = []
    for img_dir in img_dirs:
        label_id = img_dir.split('/')[-2]
        img_fpaths = glob.glob(os.path.join(img_dir, '*.JPEG'))[:sample_per_label]
        img_ids = [fpath.split('/')[-1].rstrip('.JPEG') for fpath in img_fpaths]
        label_name = df_label_id_name[df_label_id_name['label_id']==label_id]['label_name'].tolist()[0]
        df_part = pd.DataFrame.from_dict(
            {'img_id': img_ids,
             'img_fpath': img_fpaths,
             'label_id': [label_id] * len(img_fpaths),
             'label_name': [label_name] * len(img_fpaths)})
        df_belt.append(df_part)
    df = pd.concat(df_belt)

    if labelspace_version == 'observed':
        df_label_id_name = df.groupby(
            by=['label_id','label_name'])\
            .size()\
            .reset_index()\
            .rename(columns={0:'count'})[['label_id','label_name']]
    return df, df_label_id_name