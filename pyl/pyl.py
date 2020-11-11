#!/usr/bin/env python3
import argparse
import sys
import contextlib
import importlib

def run(code, files=None, filter_=None, begin=None, end=None, imports=None):
	if files is None:
		files = [sys.stdin]
	if imports is not None:
		for imp in imports:
			locals()[imp] = importlib.import_module(imp)
	if begin is not None:
		exec(begin)
	if filter_ is not None:
		filter_ = compile(filter_, "<string>", "eval")
	code = f"({code},)[-1]"
	code = compile(code, "<string>", "eval")
	for file in files:
		for i, line in enumerate(file):
			line = line.rstrip("\n")
			x = l = line
			if filter_ is not None and not eval(filter_):
				continue
			res = eval(code)
			if res is not None:
				print(res)
	if end is not None:
		exec(end)

def main():
	parser = argparse.ArgumentParser(prog="pyl")
	parser.add_argument("-b", "-H", "--begin", help="code to run at the beginning")
	parser.add_argument("-e", "--end", help="code to run at the end")
	parser.add_argument("-f", "--filter", help="code to filter lines to run")
	parser.add_argument(
		"-i", "--import", dest="imports", help="modules to import before running code"
	)
	parser.add_argument("code", nargs="?", help="code to run per line")
	parser.add_argument("files", nargs="*", default=["-"], help="list of files")
	args = parser.parse_args()
	if args.imports is None:
		imports = []
	else:
		imports = [imp.strip() for imp in args.imports.split(",")]
	if args.code is None:
		if args.filter is not None:
			args.code = "l"
		else:
			parser.error("At least one of code or filter must be provided")
	
	with contextlib.ExitStack() as stack:
		files = [
			stack.enter_context(open(file)) if file != "-" else sys.stdin for file in args.files
		]
		run(args.code, files, args.filter, args.begin, args.end, imports)

if __name__ == "__main__":
	main()
