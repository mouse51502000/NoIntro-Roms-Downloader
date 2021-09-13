import os
import PySimpleGUI as sg
import common_functions as common
from urllib.parse import quote
from urllib.request import urlopen
from http.client import HTTPResponse


_base_url = "https://archive.org"


def download_files(platform_id: str, filenames: list, output_folder: str, cb_progressbar: sg.ProgressBar, cb_statusbar: sg.StatusBar, cb_text_status: sg.Text, cb_function):
  def download(filename: str):
    filename_quoted = quote(filename)
    full_url = f"{_base_url}/download/{platform_id}/{filename_quoted}"
    output_stream = open(file=os.path.join(output_folder, filename), mode="wb")
    file_request: HTTPResponse = urlopen(full_url)
    file_length = file_request.length
    buffer_length = int(file_length / 10)
    position = 0
    
    while True:
      bytes_read = file_request.read(buffer_length)
      output_stream.write(bytes_read)
      output_stream.flush()
      position += len(bytes_read)
      cb_progressbar.update(position, file_length)
      cb_text_status.update(f"{common.length_to_unit_string(position)} / {common.length_to_unit_string(file_length)}")
      if len(bytes_read) < buffer_length: break
    
    file_request.close()
    output_stream.close()
    while not file_request.closed and not output_stream.closed: pass

  count = 0
  max = len(filenames)
  for filename in filenames:
    count+=1
    cb_progressbar.update(0, 0)
    cb_text_status.update("0Kb / 0Kb")
    cb_statusbar.update(f"Downloading... ({filename[:20]}{'...' if len(filename) > 20 else ''}) ({count}/{max})")
    download(filename)
  cb_function(max)
