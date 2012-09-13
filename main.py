
import os
from flask import Flask, g, render_template
from flaskext.htmlbuilder import html, render
from urllib import urlencode
from urllib2 import urlopen, quote
from lxml.etree import fromstring
import flask_sijax
import config

sijax_path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

app = Flask(__name__)
app.debug = config.DEBUG
app.config['SIJAX_STATIC_PATH'] = sijax_path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

class SearchResults(object):
    def __init__(self):
        self.url = None
        self.results = None
        self.total_hits = None
        
    def results2html(self):
        return render_template('result-list.html', results=self.results)
    
def classic_search(q):
    
    search_url = "http://adsabs.harvard.edu/cgi-bin/topicSearch?" \
                + ("q=%s&qtype=NEW&db_key=AST&db_key=PRE&arxiv_sel=astro-ph&arxiv_sel=gr-qc&data_type=XML" % quote(q))
    app.logger.debug("classic search: %s" % search_url)
    u = urlopen(search_url)
    root = fromstring(u.read())
    ns = {'ads': 'http://ads.harvard.edu/schema/abs/1.1/abstracts'}
    results = [] 
    for rec in root.getchildren():
        results.append({
            'bibcode': rec.find('ads:bibcode', ns).text,
            'title': rec.find('ads:title', ns).text,
            'score': rec.find('ads:score', ns).text
            })
    sr = SearchResults()
    sr.url = search_url
    sr.results = results
    sr.total_hist = root.attrib.get('selected')
    return sr
    
def solr_search(q):
    params = urlencode({'q': q, 'wt': 'python', 'rows': 200, 'fl': "bibcode,title,score,pubdate_sort",
                        'fq': 'database:ASTRONOMY', 'sort': 'pubdate_sort desc'})
    search_url = "http://adsate:8987/solr/collection1/select?" + params
    app.logger.debug("solr search: %s" % search_url)
    u = urlopen(search_url)
    resp = eval(u.read())
    # remove records with bad pubdates
    app.logger.debug(str(resp['response']['docs'][0]))
    results = filter(lambda x: int(x['pubdate_sort']) < 20140000, resp['response']['docs'])
    sr = SearchResults()
    sr.url = search_url
    sr.results = results
    sr.total_hist = resp['response']['numFound']
    return sr

class SearchHandler(object):
    
    @staticmethod
    def search_classic(obj_resp, q):
        results = classic_search(q)
        obj_resp.html('#results-classic', results.results2html())
        obj_resp.script("$('#meta-classic').text('Total Hits: %s')" % results.total_hits)
        
    @staticmethod
    def search_solr(obj_resp, q):
        results = solr_search(q)
        obj_resp.html('#results-solr', results.results2html())
        obj_resp.script("$('#meta-solr').text('Total Hits: %s')" % results.total_hits)
        
@flask_sijax.route(app, '/')
def main(name=None):
    if g.sijax.is_sijax_request:
        g.sijax.register_object(SearchHandler)
        return g.sijax.process_request()
    return render_template('main.html', name=name)

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT)
