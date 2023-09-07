"""A tool for generating histograms from a CSV file."""

import logging
import os

import pandas

import plotly.express
import plotly.subplots
import plotly.graph_objects

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_multi_string('data_path', None, 'The path to the data file.')
flags.DEFINE_string('output_path', None,
                    'The path to a folder to write the histograms to.')
flags.DEFINE_integer('num_bins', 20,
                     'The number of bins to use for the histograms.')
flags.DEFINE_multi_string(
    'sub_plot_sections', None,
    'The column names to include in a subplot diagram. There must be eight '
    'sections specified. If this flag is set, only one plot will be generated.')

flags.mark_flag_as_required('data_path')
flags.mark_flag_as_required('output_path')


def main(_):
  data_frames = []
  languages = []

  for data_path in FLAGS.data_path:
    logging.info(f'Loading data from {data_path}')
    data_frame = pandas.read_csv(data_path)
    data_frame.drop(['name'], axis=1, inplace=True)
    language_name = os.path.basename(data_path)[:-4]
    languages.append(language_name)
    data_frame.insert(0, 'language', [language_name] * len(data_frame))
    data_frames.append(data_frame)

  data_frame = pandas.concat(data_frames)

  logging.info('Finished loading data, generating histograms.')

  if FLAGS.sub_plot_sections is None:
    for column in data_frame:
      figure = plotly.express.histogram(
          data_frame,
          x=column,
          color='language',
          nbins=FLAGS.num_bins,
          log_y=True,
          barmode='overlay')
      figure.write_image(os.path.join(FLAGS.output_path, f'{column}.png'))
      logging.info(f'Finished generating figure for {column}')
    return

  # TODO(boomanaiden154): More elegant support for multiple languages
  # with a subplot figure.
  subplot_figure = fig = plotly.subplots.make_subplots(
      rows=2, cols=4, subplot_titles=FLAGS.sub_plot_sections)

  for index, sub_plot_section in enumerate(FLAGS.sub_plot_sections):
    column = (index % 4) + 1
    row = int(index / 4 + 1)

    for language_index, language in enumerate(languages):
      data_frame_subset = data_frame[data_frame['language'] == language]
      to_show_legend = True if index == 0 else False
      subplot_figure.add_trace(
          plotly.graph_objects.Histogram(
              x=data_frame_subset[sub_plot_section].to_numpy(),
              nbinsx=FLAGS.num_bins,
              name=language,
              marker_color=plotly.colors.qualitative.Plotly[language_index],
              showlegend=to_show_legend),
          col=column,
          row=row)
      subplot_figure.update_yaxes(type="log", col=column, row=row)

  subplot_figure.update_layout(
      width=2200, height=1000, barmode='stack', font=dict(size=30), bargap=0)
  subplot_figure.update_annotations(font_size=40)

  logging.info('Writing image to file')

  subplot_figure.write_image(
      os.path.join(FLAGS.output_path, 'subplot_figure.pdf'))


if __name__ == '__main__':
  app.run(main)
