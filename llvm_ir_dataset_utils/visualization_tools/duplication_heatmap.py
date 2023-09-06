"""A script for generating a heatmap showing duplication of bitcode
between languages."""

import logging
import os
import csv
import sys

import plotly.express
import plotly.io

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_multi_string(
    'hash_file', None,
    'A CSV file containing a header and a list of function hashes.')
flags.DEFINE_string('output_file', None, 'The path to the output image.')
flags.DEFINE_enum('hash_key', 'function_hashes',
                  ['function_hashes', 'module_hashes'],
                  'The column name in the CSV containing the hashes.')

flags.mark_flag_as_required('hash_file')
flags.mark_flag_as_required('output_file')


def load_haash_histogram_from_file(file_path):
  hash_histogram = {}
  with open(file_path) as hash_file:
    reader = csv.DictReader(hash_file)
    for row in reader:
      hash_value = row[FLAGS.hash_key]
      if hash_value in hash_histogram:
        hash_histogram[hash_value] += 1
      else:
        hash_histogram[hash_value] = 1
  return hash_histogram


def calculate_overlap(hash_histogram1, hash_histogram2):
  unique_functions = 0
  duplicate_functions = 0
  for function_hash in list(
      set(list(hash_histogram1.keys()) + list(hash_histogram2.keys()))):
    if function_hash in hash_histogram1 and function_hash in hash_histogram2:
      duplicate_functions += hash_histogram1[function_hash] + hash_histogram2[
          function_hash]
    else:
      unique_functions += 1
  return duplicate_functions / (unique_functions + duplicate_functions)


def calculate_duplication(hash_histogram):
  unique_functions = 0
  duplicate_functions = 0
  for function_hash in hash_histogram:
    if hash_histogram[function_hash] > 1:
      duplicate_functions += hash_histogram[function_hash]
    else:
      unique_functions += 1
  return duplicate_functions / (unique_functions + duplicate_functions)


def main(_):
  histograms = {}
  for hash_file_path in FLAGS.hash_file:
    logging.info(f'Loading data from {hash_file_path}')
    language_name = os.path.basename(hash_file_path)[:-4]
    histograms[language_name] = load_haash_histogram_from_file(hash_file_path)

  logging.info('Finished loading data, generating matrix.')

  duplication_matrix = []
  for language_name_x in histograms:
    duplication_matrix_row = []
    for language_name_y in histograms:
      if language_name_x == language_name_y:
        duplication_matrix_row.append(
            calculate_duplication(histograms[language_name_x]))
      else:
        duplication_matrix_row.append(
            calculate_overlap(histograms[language_name_x],
                              histograms[language_name_y]))
    duplication_matrix.append(duplication_matrix_row)

  logging.info('Finished generating data, generating figure.')

  languages = list(histograms.keys())
  figure = plotly.express.imshow(
      duplication_matrix, text_auto=True, x=languages, y=languages)

  plotly.io.kaleido.scope.mathjax = None

  figure.write_image(FLAGS.output_file)


if __name__ == '__main__':
  csv.field_size_limit(sys.maxsize)

  app.run(main)
