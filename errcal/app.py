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
from cherrypy.lib import file_generator
from .calculation import *
from .conversion import *
import docopt, json, os, numpy
from decimal import Decimal
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO


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


		result = [{
			"samples": samples,
			"min": min(samples),
			"max": max(samples),
			"modus": modus(samples),
			"avg": avg(samples),
			"average_absolute_error": average_absolute_error(samples),
			"relative_error": relative_error(samples) } for samples in many_samples]

		tolerances = [float(tol) for tol in  json.loads(tolerances)] if tolerances else [0 for i in result]

		for i, res in enumerate(result):
			if(tolerances[i]):
				aar = res["average_absolute_error"] + avg(many_samples[i])  * (float(tolerances[i])  / 100)
				res["average_absolute_error"] = aar

		return formats[dtype](result)


	@cherrypy.expose
	def plot(self, many_samples, xes, tolerances = None, xerr_abs = 0, xerr_rel = 0):
		many_samples = json.loads(many_samples)
		many_samples = [[float(sample) for sample in samples] for samples in many_samples]
		xes = [float(x) for x in json.loads(xes)]
		try:
			xerr_abs = float(xerr_abs)
		except:
			xerr_abs = 0
		try:
			xerr_rel = float(xerr_rel)/100
		except:
			xerr_rel = 0

		result = [{
			"samples": samples,
			"min": min(samples),
			"max": max(samples),
			"modus": modus(samples),
			"avg": avg(samples),
			"average_absolute_error": average_absolute_error(samples),
			"relative_error": relative_error(samples) } for samples in many_samples]

		tolerances = [float(tol)/100 for tol in json.loads(tolerances)] if tolerances else [0 for i in result]
		tolerances = numpy.array(tolerances)

		for i, res in enumerate(result):
			if(tolerances[i]):
				aar = res["average_absolute_error"] + avg(many_samples[i])  * (float(tolerances[i])  / 100)
				res["average_absolute_error"] = aar

		plt.xkcd()
		f, (scatter, curves1) = plt.subplots(2, sharex=True, sharey=True)
		f.set_size_inches(20, 40)

		colors = [v for k,v in sorted(matplotlib.colors.cnames.items(), key = lambda y:y[0]) 
				if not "white" in k]

		scatter.set_title("Scatter Plot")
		for i, (x, samples) in enumerate(zip(xes, [res["samples"] for res in result])):
			scatter.scatter([x for i in samples], samples, 
					color=colors[i % len(colors)],
					marker = "o", edgecolors = "black")
		
		X = numpy.array(xes)
		Y = numpy.array([res["avg"] for res in result])

		y_rel_error = numpy.array([res["relative_error"] for res in result])
		y_abs_error = numpy.array([res["average_absolute_error"] for res in result])



		curves1.set_title("Errorbar of avg")
		c1 = curves1.errorbar(X, Y, xerr = X*xerr_rel + xerr_abs, yerr = Y*(tolerances + y_rel_error) + y_abs_error )
		c2, = curves1.plot(X, [res["min"] for res in result])
		c3, = curves1.plot(X, [res["max"] for res in result])
		c4, = curves1.plot(X, [res["modus"] for res in result])

		curves1.legend((c1, c2, c3, c4), ("average with errorbars", "min", "max", "modus"))

		buf = BytesIO()
		plt.savefig(buf, format = "png")
		buf.seek(0)
		cherrypy.response.headers['Content-Type'] = "image/png"
		return file_generator(buf)

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
	
