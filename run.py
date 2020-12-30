# Importing libraries
import argparse
import processes

args_lst = tuple(processes.getArgs().args[2:])
conf_lst = ' '.join(args_lst)
n_conf = len(args_lst)


# def str2bool(v):
# 	'''Converts a valid input to its corresponding boolean value'''
#     if isinstance(v, bool):
#        return v
#     if v.lower() in ('yes', 'true', 't', 'y', '1'):
#         return True
#     elif v.lower() in ('no', 'false', 'f', 'n', '0'):
#         return False
#     else:
#         raise argparse.ArgumentTypeError('Boolean value expected')


def nonNegativeInt(x):
	'''Ensures input argument is a positive integer'''
	try:
		n = int(x)
		if (n < 0):
			raise argparse.ArgumentTypeError('Positive integer expected')
		else:
			return n
	except ValueError:
		raise argparse.ArgumentTypeError('Integer expected')


def formatter(prog):
	'''Custom Help Formatter: https://docs.python.org/3/library/argparse.html#formatter-class'''
	return argparse.HelpFormatter(prog=prog, indent_increment=2, max_help_position=35, width=130)


def commandLineArg():
	'''Handles command-line arguments'''
	parser = argparse.ArgumentParser(
		prog='GestureBasedDriving',
		description='Game Playing using Gestures!',
		epilog=None,
		formatter_class=formatter,
		prefix_chars='-',
		argument_default=None,
		add_help=True,
		allow_abbrev=True
	)

	parser.add_argument(
		'-dr',
		'--displayRunning',
		action='store_true',
		default=False,
		help='Display the Running Processes Paths.'
	)

	parser.add_argument(
		'-de',
		'--displayEnlisted',
		action='store_true',
		default=False,
		help='Display the Enlisted Processes Paths.'
	)

	# parser.add_argument(
	# 	'-a',
	# 	dest='--add',
	# 	action='store',
	# 	nargs='*',
	# 	default=None,
	# 	type=str,
	# 	choices=None,
	# 	help='Add Process Paths to Collection ("space-separated & in double-quotes")'
	# )

	parser.add_argument(
		'-a',
		'--add',
		action='store',
		nargs=1,
		default=0,
		type=nonNegativeInt,
		choices=None,
		metavar='val',
		help='Number of Process Paths to be added to Collection.'
	)

	parser.add_argument(
		'-rm',
		'--remove',
		action='store_true',
		default=False,
		help='Remove Process Path(s) from Collection.'
	)

	parser.add_argument(
		'-e',
		'--edit',
		action='store_true',
		default=False,
		help='Edit Process Path(s) in Collection.'
	)

	parser.add_argument(
		'-dc',
		'--default_configuration',
		action='store_true',
		default=False,
		help='Display Default Configuration'
	)

	parser.add_argument(
		'-c',
		'--configure',
		action='store',
		nargs=n_conf,
		default=0,
		type=float,
		metavar=args_lst,
		help='Run with Manual Configuration. Place "-1" to skip.'
	)

	return parser.parse_args(args=None, namespace=None)


if __name__ == '__main__':
	args = commandLineArg()

	key, value, cnt = None, None, 0
	for arg_key, arg_value in vars(args).items():
		if not arg_value:
			continue
		elif ((type(arg_value) is list) and (len(arg_value) == 1)):
			arg_value = arg_value[0]

		cnt += 1
		if (cnt < 2):
			key, value = arg_key, arg_value
		else:
			raise argparse.ArgumentTypeError('Only one optional argument expected at a time')

	# if not cnt:
	# 	raise argparse.ArgumentTypeError('No functionality selected. Refer to -h/--help for more details')

	processes.handleArg(key=key, value=value)