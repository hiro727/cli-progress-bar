import logging
import time
import math
import itertools


spinner = itertools.cycle(['-', '/', '|', '\\'])

move_left = "\x1b[80D"
move_up = "\x1b[1A"
clear_line = "\x1b[K"


class ProgressBarFormatter(logging.Formatter):
  def __init__(self, start_msg="Processing", done_msg="Completed", *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._cur_val = 0
    self._max_val = 100
    self._prev_num_lines = 0
    self._task_name = ""
    self._start_msg = start_msg
    self._done_msg = done_msg
    self._completed = False

  @property
  def clear_text(self):
    # clear previous output
    return f"{move_left}{move_up}{clear_line}" * (self._prev_num_lines)

  @property
  def task_name(self):
    if self._task_name == "":
      return ""
    else:
      return self._task_name + ": "

  @task_name.setter
  def task_name(self, val):
    self._task_name = val

  @property
  def percentage(self):
    return math.floor(self._cur_val / self._max_val * 100)

  def format(self, record):
    record.message = record.getMessage()
    if hasattr(record, "progress"):
      self._cur_val = record.progress

    if self._cur_val == self._max_val:
      text = self.text(self._done_msg)
      self._prev_num_lines = 0
      self._completed = True
    else:
      text = self.text(record.message)
      self._prev_num_lines = text.count('\n') + 1 # logger auto-adds one line break at the end.
    return text

  def start(self, logger):
    self._completed = False
    self._prev_num_lines = 0
    logger.info(self._start_msg, extra={"progress": 0})

  def complete(self, logger):
    if self._completed:
      return
    logger.info(self._done_msg, extra={"progress": self._max_val})

  def fail(self, logger, e):
    if self._completed:
      return
    logger.info(f"Error {e}. see logs for details")


class ProgressBarFormatterLeft(ProgressBarFormatter):
  def text(self, msg):
    percentage = str(self.percentage).rjust(3) + "%" # pad with empty spaces
    return self.clear_text + f"[{percentage}]" + " " + self.task_name + msg

class ProgressBarFormatterDots(ProgressBarFormatter):
  def text(self, msg):
    percentage = self.percentage
    progress = "0"
    for i in range(0, math.floor(percentage/10)):
      progress = f"{progress}...{(i + 1) * 10}"

    return self.clear_text + self.task_name + " " + progress + "\n" + msg

class ProgressBar(object):
  def __init__(self, logger, name, formatter=None):
    self._handler = next(h for h in logger.handlers if isinstance(h, logging.StreamHandler))

    self._logger = logger
    self._new_handler = self._handler is None
    if self._new_handler:
      self._handler = logging.StreamHandler()
      self._logger.addHandler(self._handler)

    self._old_formatter = self._handler.formatter
    self._old_level = self._handler.level

    self._formatter =  ProgressBarFormatterLeft() if formatter is None else formatter
    self._formatter.task_name = name
    self._handler.setFormatter(self._formatter)
    self._handler.setLevel(logging.INFO)
    self._formatter.start(self._logger)

  def _clean(self):
    if self._new_handler:
      self._logger.removeHandler(self._handler)
      self._logger = None
    self._handler.setLevel(self._old_level)
    self._handler.setFormatter(self._old_formatter)

  def complete(self):
    self._formatter.complete(self._logger)
    self._clean()

  def fail(self, e):
    self._formatter.fail(self._logger, e)
    self._clean()

