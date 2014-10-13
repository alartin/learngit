from flask import Flask
import requests
import untangle
import os
from jinja2 import Template
app = Flask(__name__)
wechatxml = '''<xml>
                 <ToUserName><![CDATA[{{ toUser }}]]></ToUserName>
                 <FromUserName><![CDATA[{{ fromUser }}]]></FromUserName>
                 <CreateTime>12345678</CreateTime>
                 <MsgType><![CDATA[text]]></MsgType>
                 <Content><![CDATA[{{ content }}]]></Content>
               </xml>'''
template = Template(wechatxml)

@app.route('/')
def index():
   # Query europe pmc restful api and sort by date
   r = requests.get("http://www.ebi.ac.uk/europepmc/webservices/rest/search/query=hadoop%20sort_date:y&resulttype=core")
   obj = untangle.parse(r.text.encode('utf-8'))
   #response = ''
   latest = obj.responseWrapper.resultList.result[0]
   title = latest.title.cdata
   authors = latest.authorString.cdata
   affiliation = latest.affiliation.cdata
   journal = latest.journalInfo.journal.title.cdata
   date = latest.journalInfo.dateOfPublication.cdata
   abstract = latest.abstractText.cdata
   #for result in obj.responseWrapper.resultList.result:
   #    title = result.title.cdata      
   #    print title
   #    response = response + os.linesep + title + os.linesep + os.linesep
   #result = obj.responseWrapper.resultList.result       
   #return response
   response = title + os.linesep + authors + os.linesep + affiliation + os.linesep + journal + os.linesep + date + os.linesep + abstract 
   return template.render(toUser='User', fromUser='BIIT', content=response)
   

if __name__ == '__main__':
    app.run()
