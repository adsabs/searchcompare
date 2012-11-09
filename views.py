'''
Created on Nov 9, 2012

@author: jluker
'''

from urllib import urlencode
from urllib2 import quote
from flask import Blueprint, request, g, render_template, abort
from adsabs.core.solr import SolrRequest

searchcompare_blueprint = Blueprint('searchcompare', __name__, template_folder="templates", static_folder="static")

__all__ = ['searchcompare_blueprint']

#@searchcompare_blueprint.route('/classic', methods=['GET'])
#def classic_search(q):
#    
#    search_url = "http://adsabs.harvard.edu/cgi-bin/topicSearch?" \
#                + ("q=%s&qtype=NEW&db_key=AST&db_key=PRE&arxiv_sel=astro-ph&arxiv_sel=gr-qc&data_type=XML" % quote(q))
#    app.logger.debug("classic search: %s" % search_url)
#    u = urlopen(search_url)
#    root = fromstring(u.read())
#    ns = {'ads': 'http://ads.harvard.edu/schema/abs/1.1/abstracts'}
#    results = [] 
#    for rec in root.getchildren():
#        results.append({
#            'bibcode': rec.find('ads:bibcode', ns).text,
#            'title': rec.find('ads:title', ns).text,
#            'score': rec.find('ads:score', ns).text
#            })
#    sr = SearchResults()
#    sr.url = search_url
#    sr.results = results
#    sr.total_hits = root.attrib.get('selected')
#    return sr
#    
@searchcompare_blueprint.route('/solr', methods=['GET'])
def solr_search():
    try:
        q = request.args.get('q')
    except:
        abort(400)
    req = SolrRequest(q)
    req.set_format('python')
    req.set_rows(200)
    req.set_fields(['bibcode','title','score','pubdate_sort'])
    req.set_sort('DATE', 'asc')
    req.add_filter('database', 'ASTRONOMY')
    return
#    params = urlencode({'q': q, 'wt': 'python', 'rows': 200, 'fl': "bibcode,title,score,pubdate_sort",
#                        'fq': 'database:ASTRONOMY', 'sort': 'pubdate_sort desc'})
#    search_url = "http://adsate:8987/solr/collection1/select?" + params
#    app.logger.debug("solr search: %s" % search_url)
#    u = urlopen(search_url)
#    resp = eval(u.read())
#    # remove records with bad pubdates
#    app.logger.debug(str(resp['response']['docs'][0]))
#    results = filter(lambda x: int(x['pubdate_sort']) < 20140000, resp['response']['docs'])
#    sr = SearchResults()
#    sr.url = search_url
#    sr.results = results
#    sr.total_hits = resp['response']['numFound']
#    return sr

@searchcompare_blueprint.route('/', methods=['GET'])
def index():
    """
    displays the initial interface
    """
    return render_template('main.html')
