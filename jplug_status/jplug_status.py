from __future__ import with_statement
import web
import json

urls = ("/", "render_index",
		"/query","query"
		)
app = web.application(urls, globals())
render = web.template.render('templates')

def tail(basepath,fname,count):
	with open(basepath+fname, "r") as f:
		f.seek (0, 2)           # Seek @ EOF
		fsize = f.tell()        # Get Size
		f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
		lines = f.readlines()       # Read to end
		lines = lines[-count:]
		return lines

class render_index:
	def GET(self):
		return render.index()
		
class query:
	
	def POST(self):
		data = web.data()
		query_data=json.loads(data)
		jplug_id=query_data["jplug_id"]
		try:
			lines=tail("/var/www/",jplug_id,10)
			out=""
			for line in lines:
				out= out+line+"_"
			file_tail=out
		except:
			file_tail="Less than 10 entries in file or file does not exist"
		web.header('Content-Type', 'application/json')
		return json.dumps({"data":file_tail})
			
		

if __name__ == "__main__":
    app.run()
