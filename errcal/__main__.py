from . import app
import docopt, cherrypy, os

if( __name__ == "__main__"):
	args = docopt.docopt(app.__doc__)
	cherrypy.config.update(
		{
		"server.socket_host": args["--address"],
		"server.socket_port": int(args["--port"]),
		"tools.staticdir.on": True,
		"tools.staticdir.dir": os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/")
		})
	server = app.CalServer()
	cherrypy.quickstart(server)
	
