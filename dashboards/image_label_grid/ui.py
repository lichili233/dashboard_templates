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
"""Main UI program."""

import streamlit as st
import numpy as np
import pandas as pd
from utils_data import load_imagenet


def paginator_by_label(title: str,
                       df_items_labels: pd.DataFrame,
                       df_labels: pd.DataFrame,
                       on_sidebar: bool = True,
                       item_col: str = 'img_fpath',
                       label_id_col: str = 'label_id',
                       label_name_col: str = 'label_name'):
    """Paginates a set of images by their labels.

    Derived from: 
    'paginator' function by Adrien Treuille (https://gist.github.com/treuille)
    https://gist.github.com/treuille/2ce0acb6697f205e44e3e0f576e810b7
    """

    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    n_pages = df_labels.shape[0]
    page_format_func = lambda i: df_labels.iloc[i,:][label_name_col]
    page_number = location.selectbox(label=title,
                                     options=range(n_pages),
                                     format_func=page_format_func)
    
    # Iterate over the items in the page to let the user display them.
    label_id = df_labels.iloc[page_number,:][label_id_col]
    items_page = df_items_labels[df_items_labels[label_id_col]==label_id]
    item_paths = items_page[item_col].tolist()
    item_labels = items_page[label_name_col].tolist()

    # Preview data as interactive dataframe
    st.markdown("## data preview:")
    st.dataframe(data=items_page, width=None, height=None)

    return item_paths, item_labels


def main():
    """Main application function."""
    st.markdown(
        body="<h1 style='text-align: center; color: red;'>Computer Vision Image-Label Data Previewer</h1>", 
        unsafe_allow_html=True)
    sample_per_label = st.slider(
        label='Sample size per label',
        min_value=10,
        max_value=200,
        step=10,
        help='Fixes the amount of sample showing for each ImageNet label.')
    width_per_image = st.slider(
        label='Width per image',
        min_value=64,
        max_value=512,
        step=16,
        help='Resizes the images to this width for display.')
    version_choice = st.radio(
        label='Select a dataset',
        options=['full','tiny'],
        help='The version of ImageNet to be chosen for display.')
    shuffle_choice = st.radio(
        label='Shuffle images per label',
        options=['True','False'],
        help='Randomly shuffle the images per label for display.')
    df, df_label_id_name = load_imagenet(
        version=version_choice, 
        sample_per_label=sample_per_label,
        shuffle=eval(shuffle_choice))
    images_on_page, labels_on_page = paginator_by_label(
        title='Select a label',
        df_items_labels=df,
        df_labels=df_label_id_name,
        on_sidebar=True,
        item_col='img_fpath',
        label_id_col='label_id',
        label_name_col='label_name')
    st.image(
        image=images_on_page,
        width=width_per_image,
        caption=labels_on_page)


if __name__ == '__main__':
    main()