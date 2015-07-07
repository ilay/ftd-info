import urllib2, json
from xml.dom.minidom import parse
from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/ftd.json')
def renderJSON():
    source = urllib2.urlopen('https://tcgbusfs.blob.core.windows.net/blobfs/GetFTDDamData.xml')
    dom = parse(source)

    list = []
    for dam in dom.getElementsByTagName('Dam_Info'):
        Organization05_Id = dam.getElementsByTagName('Organization05_Id')[0].firstChild.nodeValue
        Dam_Id = dam.getElementsByTagName('Dam_Id')[0].firstChild.nodeValue
        Dam_Info_Date = dam.getElementsByTagName('Dam_Info_Date')[0].firstChild.nodeValue
        Dam_Info_WaterLevel = dam.getElementsByTagName('Dam_Info_WaterLevel')[0].firstChild.nodeValue
        Dam_Info_InFlow = dam.getElementsByTagName('Dam_Info_InFlow')[0].firstChild.nodeValue
        Dam_Info_OutFlow = dam.getElementsByTagName('Dam_Info_OutFlow')[0].firstChild.nodeValue
        Dam_Info_Capacity = dam.getElementsByTagName('Dam_Info_Capacity')[0].firstChild.nodeValue

        damDict = {
            'Organization05_Id': Organization05_Id,
            'Dam_Id': Dam_Id,
            'Dam_Info_Date': Dam_Info_Date,
            'Dam_Info_WaterLevel': Dam_Info_WaterLevel,
            'Dam_Info_InFlow': Dam_Info_InFlow,
            'Dam_Info_OutFlow': Dam_Info_OutFlow,
            'Dam_Info_Capacity': Dam_Info_Capacity
        }
        list.append(damDict)

    result = json.dumps(list)

    return result


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
