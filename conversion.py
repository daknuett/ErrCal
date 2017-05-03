#!/usr/bin/python3

from ljson import Table, Header
from ljson.convert.csv import table2csv
from io import StringIO
import json

def data2ljson(result):
	header = Header(
		{
			"samples": {"type": "json", "modifiers": []},
			"min": {"type": "float", "modifiers": []},
			"max": {"type": "float", "modifiers": []},
			"avg": {"type": "float", "modifiers": []},
			"modus": {"type": "float", "modifiers": []},
			"average_absolute_error": {"type": "float", "modifiers": []},
			"relative_error": {"type": "float", "modifiers": []}
		})

	
	table = Table(header, result)
	fout = StringIO()
	table.save(fout)
	fout.seek(0)
	return fout.read()

def data2csv(result):
	header = Header(
		{
			"samples": {"type": "json", "modifiers": []},
			"min": {"type": "float", "modifiers": []},
			"max": {"type": "float", "modifiers": []},
			"avg": {"type": "float", "modifiers": []},
			"modus": {"type": "float", "modifiers": []},
			"average_absolute_error": {"type": "float", "modifiers": []},
			"relative_error": {"type": "float", "modifiers": []}
		})

	
	table = Table(header, result)
	fout = StringIO()
	table2csv(table, fout)
	fout.seek(0)
	return fout.read()

def data2json(result):
	return json.dumps(result)
