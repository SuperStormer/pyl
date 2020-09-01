#!/usr/bin/env python3
import argparse
import sys
import contextlib
import importlib

def run(code, files=None, filter_=None, header=None, imports=None):
	if files is None:
		files = [sys.stdin]
	if imports is not None:
		for imp in imports:
			importlib.import_module(imp)
	if header is not None:
		exec(header)
	if filter_ is not None:
		filter_ = compile(filter_, "<string>", "eval")
	code = compile(code, "<string>", "single")
	for file in files:
		for i, line in enumerate(file):
			line = line.rstrip("\n")
			x = l = line
			if filter_ is not None and not exec(filter_):
				continue
			exec(code)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-H", "--header", help="code to run at start of each line")
	parser.add_argument("-f", "-F", "--filter", help="code to filter lines to run")
	parser.add_argument(
		"-i", "-I", "--import", dest="imports", help="modules to import before running code"
	)
	parser.add_argument("code", nargs="?", help="code to run per line")
	parser.add_argument("files", nargs="*", default=["-"], help="list of files")
	args = parser.parse_args()
	if args.imports is None:
		imports = []
	else:
		imports = [imp.strip() for imp in args.imports.split(",")]
	if args.filter is not None and args.code is None:
		args.code = "l"
	with contextlib.ExitStack() as stack:
		files = [
			stack.enter_context(open(file)) if file != "-" else sys.stdin for file in args.files
		]
		run(args.code, files, args.filter, args.header, imports)

if __name__ == "__main__":
	main()
