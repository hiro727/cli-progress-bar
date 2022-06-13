import argparse
import parse, info

def main():
  parser = argparse.ArgumentParser()

  subparsers = parser.add_subparsers(help='Choose a command')

  parse_parser = subparsers.add_parser('parse', help='"parse" help')
  parse_parser.add_argument('mode', help='parse mode can be one of "basic", "long" or "error"')
  parse_parser.add_argument('--enable_logging', action='store_true', help='enable file logging')
  parse_parser.set_defaults(func=parse.run)

  info_parser = subparsers.add_parser('info', help='"info" help')
  info_parser.add_argument('-formatter', help='type of progress bar formatter. one of "left" or "dots"')
  info_parser.set_defaults(func=info.run)

  args = parser.parse_args()
  args.func(args)


if __name__ == '__main__':
  main()
