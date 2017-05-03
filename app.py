#!/usr/bin/python3

"""
Web application for error calculation.

Usage:
	error_calculation.app [options]

Options:
        -p <port> --port=<port>            The port for the web-service [default: 8087]
        -a <address> --address=<address>   The address of the web-service [default: 0.0.0.0]

	

"""

import cherrypy
from .calculation import *
from .conversion import *
import docopt, json, os
from decimal import Decimal


formats = {"ljson": data2ljson,
	"csv": data2csv,
	"json": data2json}

class CalServer(object):
	def __init__(self):
		pass

	@cherrypy.expose
	def index(self):
		raise cherrypy.HTTPRedirect("/index.html")
	@cherrypy.expose
	def calculate_all(self, samples, tolerance = None):
		samples = json.loads(samples)
		samples = [float(sample) for sample in samples]

		result = {
			"samples": samples,
			"min": min(samples),
			"max": max(samples),
			"modus": modus(samples),
			"avg": avg(samples),
			"average_absolute_error": average_absolute_error(samples),
			"relative_error": relative_error(samples)
		}

		if(tolerance):
			aar = result["average_absolute_error"] + avg(samples) * (float(tolerance) / 100)
			result["average_absolute_error"] = aar


		return json.dumps(result, indent = "\t")
	@cherrypy.expose
	def download(self, many_samples, tolerances = None, dtype = "ljson"):
		if(not dtype in formats):
			return "ERROR: unsupported format: {}".format(dtype)
		many_samples = json.loads(many_samples)
		many_samples = [[float(sample) for sample in samples] for samples in many_samples]


		tolerances = json.loads(tolerances)

		result = [{
			"samples": samples,
			"min": min(samples),
			"max": max(samples),
			"modus": modus(samples),
			"avg": avg(samples),
			"average_absolute_error": average_absolute_error(samples),
			"relative_error": relative_error(samples) } for samples in many_samples]

		for i, res in enumerate(result):
			if(tolerances[i]):
				aar = res["average_absolute_error"] + avg(many_samples[i])  * (float(tolerances[i])  / 100)
				res["average_absolute_error"] = aar

		return formats[dtype](result)




if( __name__ == "__main__"):

	args = docopt.docopt(__doc__)
	cherrypy.config.update(
		{
		"server.socket_host": args["--address"],
		"server.socket_port": int(args["--port"]),
		"tools.staticdir.on": True,
		"tools.staticdir.dir": os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/")
		})
	server = CalServer()
	cherrypy.quickstart(server)
	
