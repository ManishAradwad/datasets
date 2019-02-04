from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import functools
import numpy as np
import tensorflow as tf
import tensorflow_datasets.public_api as tfds
from tensorflow_datasets.video.moving_sequence import images_as_moving_sequence    # pylint: disable=unused-import

_OUT_RESOLUTION = (64, 64)
_SEQUENCE_LENGTH = 20
_citation = """
@article{DBLP:journals/corr/SrivastavaMS15,
  author    = {Nitish Srivastava and
               Elman Mansimov and
               Ruslan Salakhutdinov},
  title     = {Unsupervised Learning of Video Representations using LSTMs},
  journal   = {CoRR},
  volume    = {abs/1502.04681},
  year      = {2015},
  url       = {http://arxiv.org/abs/1502.04681},
  archivePrefix = {arXiv},
  eprint    = {1502.04681},
  timestamp = {Mon, 13 Aug 2018 16:47:05 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/SrivastavaMS15},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""


class MovingMnist(tfds.core.GeneratorBasedBuilder):

  VERSION = tfds.core.Version("0.1.0")

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=(
          "Moving variant of MNIST database of handwritten digits. This is the "
          "data used by the authors for reporting model performance. See "
          "`tensorflow_datasets.video.moving_mnist.images_as_moving_sequence` "
          "for generating training/validation data from the MNIST dataset."),
        features=tfds.features.FeaturesDict(
          dict(image_sequence=tfds.features.Video(
              shape=(_SEQUENCE_LENGTH,) + _OUT_RESOLUTION + (1,)))),
        urls=["http://www.cs.toronto.edu/~nitish/unsupervised_video/"],
        citation=_citation
    )

  def _split_generators(self, dl_manager):
    data_path = dl_manager.download(
        "http://www.cs.toronto.edu/~nitish/unsupervised_video/"
        "mnist_test_seq.npy")

    # authors only provide test data.
    # See `tfds.video.moving_mnist.moving_sequence` for mapping function to
    # create training/validation dataset from MNIST.
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            num_shards=5,
            gen_kwargs=dict(data_path=data_path)),
    ]

  def _generate_examples(self, data_path):
    """Generate MOVING_MNIST sequences.

    Args:
      data_path (str): Path to the data file

    Yields:
      20 x 64 x 64 x 1 uint8 numpy arrays
    """
    with tf.io.gfile.GFile(data_path, "rb") as fp:
      images = np.load(fp)
    images = np.transpose(images, (1, 0, 2, 3))
    images = np.expand_dims(images, axis=-1)
    for sequence in images:
      yield dict(image_sequence=sequence)
