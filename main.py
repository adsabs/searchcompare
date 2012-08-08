
import os
from flask import Flask, g, render_template
from flaskext.htmlbuilder import html, render
from urllib import urlencode
from urllib2 import urlopen
from lxml.etree import fromstring
import flask_sijax
import config

sijax_path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

app = Flask(__name__)
app.debug = config.DEBUG
app.config['SIJAX_STATIC_PATH'] = sijax_path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

def results2html(results):
    return render([
            html.div(id=result['bibcode'])(
                html.p(html.strong("%s (%s)" % (result['bibcode'], result['score']))),
                html.p(result['title'])
            ) for result in results
        ])
    
def classic_search(q):
    params = urlencode({'text': q, 'data_type': 'XML'})
    search_url = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?" + params
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
    return (results2html(results), root.attrib.get('selected'))
    
def solr_search(q):
    params = urlencode({'q': q, 'wt': 'python', 'rows': 200, 'fl': "bibcode,title,score"})
    search_url = "http://adsate:8987/solr/collection1/select?" + params
    u = urlopen(search_url)
    resp = eval(u.read())
    return (results2html(resp['response']['docs']), resp['response']['numFound'])

class SearchHandler(object):
    
    @staticmethod
    def search_classic(obj_resp, q):
        results_html,total_hits = classic_search(q)
        obj_resp.html('#results-classic', results_html)
        obj_resp.script("$('#meta-classic').text('Total Hits: %s')" % total_hits)
        
    @staticmethod
    def search_solr(obj_resp, q):
        results_html,total_hits = solr_search(q)
        obj_resp.html('#results-solr', results_html)
        obj_resp.script("$('#meta-solr').text('Total Hits: %s')" % total_hits)
#        obj_resp.alert('solr search: %s' % q)
        
@flask_sijax.route(app, '/')
def main(name=None):
    if g.sijax.is_sijax_request:
        g.sijax.register_object(SearchHandler)
        return g.sijax.process_request()
    return render_template('main.html', name=name)

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT)