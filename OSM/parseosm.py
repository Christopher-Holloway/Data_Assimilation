from __future__ import print_function

from imposm.parser import OSMParser
import optparse
from pprint import pprint
from elasticsearch import Elasticsearch, TransportError
from datetime import datetime, date
import glob
import time

class Node(object):

    def __init__(self, osmid, tags, refs):
        self.osmid = osmid
        # Don't allow dots in field names
        clean_tags = [{k.replace(".", ":"): v} for k, v in tags.iteritems()]
        self.tags = clean_tags
        self.location = [refs[0], refs[1]]
        self.lat = refs[1]
        self.lng = refs[0]


class OSMScraper(object):
    """
    OSMScraper - Reads in a pdb file, indexes in ES
    """
    processed = 0
    files_processed = []
    mappings = {
        'node': {
            "dynamic_templates": [
                {
                    "tags_exceptions": {
                        "path_match": "tags.*",
                        "match": "(name.*)",
                        "match_pattern": "regex",
                        "mapping": {
                            "store": "no",
                            "type": "multi_field",
                            "fields": {
                                "{name}": {"type": "string", "index": "not_analyzed"},
                                "analyzed": {"type": "string", "index": "analyzed"}
                            }
                        }
                    }
                },
                {
                    "tags_default": {
                        "path_match": "tags.*",
                        "mapping": {"index": "not_analyzed", "store": "no"}
                    }
                }
            ],
            'properties': {
                "location": { "type": "geo_point" },
                "osmid": {"type": "string", "index": "not_analyzed"}
            }
        },
    }

    settings = {
        "settings": {},
        "mappings": mappings
    }

    # Choose from: http://wiki.openstreetmap.org/wiki/Map_Features
    categories = [
        #'aeroway',
        'amenity',
        #'barrier',
        'building',
        'emergency',
        #'public_transport', # Better bus stops
        #'highway', # Includes bus stops, highway phones, rest areas
        #'landuse',
        'military',
        #'office', # Maybe....
        'place', #City, Country, State, Region, etc.... definitely
        'power',
    ]

    def __init__(self, opts):
        self.es_client = Elasticsearch(opts.esendpoint)
        if opts.deleteindex:
            print('Deleting index "{}" before processing'.format(opts.index))
            self.es_client.indices.delete(index=opts.index, ignore=404)

        try:
            print('Recreating index "{}"'.format(opts.index))
            self.es_client.indices.create(index=opts.index, body=self.settings, ignore=400)
        except TransportError as te:
            print(te.info)

        # Set list of files we already processed so we can pick up where we left off (more or less...)
        if opts.resume:
            try:
                osmstatus = open('osm.status', 'r')
                files = osmstatus.read()
                self.files_processed = str.splitlines(files)
                print("Resuming from previous run, already processed these files: {}".format(self.files_processed))
                osmstatus.close()
            except IOError as e:
                print("No status file exists, starting from scratch")

        self.opts = opts

    def ways(self, ways):
        # Callback for ways
        # TODO: Update the mapping to be a geoshape? Or maybe just store the other IDs, and then we
        # can do an ES multiget to get that actual shape.... except we won't be able to search by
        # location in this case

        # refs - A list of longs (ids) of the nodes it comprises
        for osmid, tags, refs in ways:
            print("Refs: {}".format(refs))
            print("Tags: {}".format(tags))
            print("OSM ID: {}".format(osmid))

    def nodes(self, nodes):
        for osmid, tags, refs in nodes:
            self.processed = self.processed + 1
            print("Processed {} records...".format(self.processed), end='\r')
            # If there is overlap between the tags and our categories
            if(not set(tags.keys()).isdisjoint(self.categories)):
                node = Node(osmid, tags, refs)
                #print "Node: {}".format(node.__dict__)
                try:
                    self.es_client.index(index=self.opts.index, doc_type='node', body=node.__dict__, id=osmid)
                except TransportError as te:
                    print("Exception indexing record: {}, info: {}".format(node, te.info))

    def save_progress(self):
        with open('osm.status', 'w') as osmstatus:
            osmstatus.write("\n".join(self.files_processed))

    def add_file_processed(self, filename):
        self.files_processed.append(filename)

def parse(opts):
    scraper = OSMScraper(opts)
    if opts.filename is not None:
        print('Processing file {}'.format(opts.filename))
        parse_file(opts.filename, scraper)
    else:
        file_list = glob.glob(opts.directory + '*.pbf')
        print('Processing directory {}, with {} files'.format(opts.directory, len(file_list)))

        #Sorting is necessary to keep track of our progress in this directory
        list.sort(file_list)
        if opts.resume:
            file_list = [item for item in file_list if item not in scraper.files_processed]
            print("Picking up where we left off, so actually processing {} files".format(len(file_list)))

        for filename in file_list:
            parse_file(filename, scraper)
            scraper.processed = 0


def parse_file(filename, scraper):
    """
    parse_file
    """
    print('Started parsing file: {}'.format(filename))
    p = OSMParser(concurrency=4, nodes_callback=scraper.nodes)
    start_time = time.clock()
    p.parse(filename)
    proc_time = time.clock()-start_time

    # Add file to processed list, and update the progress file
    scraper.add_file_processed(filename)
    scraper.save_progress()
    print(u"\n \u2713 Processed {} records in {} seconds".format(scraper.processed, proc_time))


if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option('-f', '--file',
        action="store", dest="filename",
        help="File to parse (PBF Format)")

    parser.add_option('-d', '--dir',
        action="store", dest="directory",
        help="Directory containing PBF/XML/ files")

    parser.add_option('-i', '--index',
        action="store", dest="index",
        help="Elasticsearch Index", default="osm")

    parser.add_option('-e', '--endpoint',
        action="store", dest="esendpoint",
        help="Elasticsearch endpoint", default="localhost:9200")

    categories = [
        'aeroway',
        'amenity',
        'barrier',
        'building',
        'emergency',
        'public_transport', # Better bus stops
        #'highway', # Includes bus stops, highway phones, rest areas
        'landuse',
        'military',
        'office', # Maybe....
        'place', #City, Country, State, Region, etc.... definitely
        'power',
    ]

    parser.add_option('-c', '--categories',
        action="store", dest="categories",
        help="Categories to pull from OSM", default=categories)

    parser.add_option('-x', action="store_true", dest="deleteindex",
        help="If present will delete existing index", default=False)

    parser.add_option('-r', action="store_true", dest="resume",
        help="Resume where the last run left off. This checks osm.status to see if it's processed each file before.", default=False)

    options, args = parser.parse_args()

    if options.filename is not None and options.directory is not None:
        parser.error("Specify either filename or directory, not both")

    parse(options)