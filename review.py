import splunklib.client as client
import utils, sys, StringIO, json, time, datetime
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-D", type="int", dest="days", default=0)
parser.add_option("-M", type="int", dest="minutes", default=0)
parser.add_option("-H", type="int", dest="hours", default=0)
parser.add_option("--delete", action="store_true", dest="delete", default=False)
parser.add_option("-f", action="store_true", dest="force", default=False)
parser.add_option("-q", action="store_true", dest="quiet", default=False)
parser.add_option("--host", dest="host", default="localhost")
parser.add_option("--port", dest="port", type="int", default=8089)
parser.add_option("--username", dest="username", default="admin")
parser.add_option("--password", dest="password", default="changeme")

(options, args) = parser.parse_args()

search_time = time.time() - (options.days * 86400 + options.hours * 3660 + options.minutes * 60)

query_string = "{\"time\" : {\"$lt\" : %i}}" % search_time

query = {"query":query_string} 

print "Current time %s, finding review records older than %s" % (str(datetime.datetime.fromtimestamp(time.time())), str(datetime.datetime.fromtimestamp(search_time))       )
print
                                  
service = client.connect(host=options.host, port=options.port, username=options.username, password=options.password, owner="nobody", app="SA-ThreatIntelligence")

response = service.get("storage/collections/data/incident_review", **query )

buffer = StringIO.StringIO()
print >> buffer, response.body
records = buffer.getvalue()
parsed_records = json.loads(records)

rec_num = 0;

if not options.quiet:

	for rec in parsed_records:
		rec_num = rec_num + 1
		print "= %i ====================================" % rec_num
		for field in sorted(rec):
			if field[0] == "_": continue
			if field == "time":
				print "%s = %s" % (field, datetime.datetime.fromtimestamp(rec[field]))
			else:
				print "%s = %s" % (field, rec[field])
		print
else:
	for rec in parsed_records:
		rec_num = rec_num + 1
print "Total %i records found." % rec_num
print
if options.delete:
	if rec_num == 0:
		print "Nothing to delete."
		sys.exit()
	if options.force:
		confirm = "y"
	else: 
		confirm = raw_input("Enter Y to confirm delete: ")
	if confirm.lower() == "y":
		service.delete("storage/collections/data/incident_review", **query)
		print "%i records deleted." % rec_num
	else:
		print "Delete cancelled."
		print
