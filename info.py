import logging


logger = logging.getLogger("INFO")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
logger.addHandler(ch)


def run(args):
  print(args)
  if args.formatter == 'dots':
    print('yes?')
    logger.info("""Format info-level messages with
    TASK_NAME: 0...10...20...30
    %(message)
    with a progress bar starting at '0...' and ending at '...100'
    Moves onto the next line only when progress bar completes/fails
    """)
  elif args.formatter == 'left':
    logger.info("""Format info-level messages with
    [ 80%] TASK_NAME %(message)
    with a progress bar starting at '[  0%]' and ending at '[100%]'
    Moves onto the next line only when progress bar completes/fails
    """)
    pass
  else:
    logger.error("Unknown formatter type. only 'dots' and 'left' are supported")
