import logging
import time
import random
import progress_bar as pb

logger = logging.getLogger("PARSE")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
logger.addHandler(ch)


def run(args):
  logger.info("running parser")

  if args.enable_logging:
    fh = logging.FileHandler('log.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

  if args.mode == 'basic':
    run_basic_task()
  elif args.mode == 'long':
    run_long_task()
  elif args.mode == 'error':
    run_error_task()

def run_basic_task():
  for task in ["A", "B", "C"]:
    progress = pb.ProgressBar(logger, name=f"TASK-{task}")

    for i in range(10):
      logger.info(f"Working on Task {i + 1} of 10.", extra={"progress": i*10})
      logger.debug("debug info")
      logger.debug("more debug info")
      logger.debug("a lot of debug info")
      time.sleep(0.5)

    progress.complete()



def run_long_task():
  long_task = "TASK-LONG"
  formatter = pb.ProgressBarFormatterDots(done_msg="Finally Completed!")
  progress = pb.ProgressBar(logger, name=long_task, formatter=formatter)

  time.sleep(5)
  logger.info("Preparing Data", extra={"progress": 20})
  logger.debug("debugging data preparation")
  time.sleep(5)
  logger.info("Validating Data", extra={"progress": 40})
  logger.debug("debugging data validation")
  time.sleep(5)
  logger.info("Processing Data", extra={"progress": 60})
  logger.debug("debugging data processing")
  time.sleep(10)

  progress.complete()


def run_error_task():
  for index, task in enumerate(["A", "B", "C", "D", "E", "F"]):
    progress = pb.ProgressBar(logger, name=f"TASK-{task}")
    try:
      failure_timing = random.randrange(10) if index % 2 == 0 else -1
      for i in range(10):
        logger.debug('some details')
        if i == failure_timing:
          logger.error("bad bad bad")
          raise RuntimeError(f"oops something failed at task {i}")
        logger.info(f"Still working hard on task {i + 1}", extra={"progress": i*10})
        time.sleep(0.5)
      progress.complete()
    except RuntimeError as e:
      progress.fail(e)



