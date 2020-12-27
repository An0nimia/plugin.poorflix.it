#!/usr/bin/python

from os import listdir, path
from importlib import import_module

host_files = listdir(
	path.dirname(
		path.realpath(__file__)
	)
)

host_files.remove("__init__.py")
hosts = {}
dnw = []

for a in host_files:
	if a.endswith(".py"):
		library_name = a[:-3]

		if library_name.endswith("_dnw"):
			dnw.append(library_name[:-4])
			continue

		library = import_module("hosts.%s" % library_name)
		hosts[library_name] = library