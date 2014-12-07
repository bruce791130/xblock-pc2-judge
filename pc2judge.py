import logging
import pkg_resources
import requests
import cgi
import socket
import sys
from urlparse import urlparse


from xblock.core import XBlock
from xblock.fields import Boolean, DateTime, Scope, String, Float, Integer,ScopeIds
from xblock.fragment import Fragment

log = logging.getLogger(__name__)

class Pc2JudgeBlock(XBlock):
   
    """A simple block: just show some fixed content."""
    edxid = String(help="URL of the video page at the provider", default=None, scope=Scope.user_state)
    maxwidth = Integer(help="Maximum width of the video", default=800, scope=Scope.content)
    problemtext = String(help="Maximum width of the video", default='2', scope=Scope.content)
    maxheight = Integer(help="Maximum height of the video", default=450, scope=Scope.content)
    href = String(help="URL of the video page at the provider", default=None, scope=Scope.content)
    watched = Integer(help="How many times the student has watched it?", default=0, scope=Scope.user_state)
   
    def student_view(self, context):  # pylint: disable=W0613
        HOST, PORT = "140.115.51.227", 9876
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.problemtext=3
        studentid =str(self.runtime.anonymous_student_id)
        self.edxid = studentid 
        sock.connect((HOST, PORT))
        sock.sendall(studentid)
        sock.close()
        HOST2, PORT2 = "140.115.51.227", 9888
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect((HOST2, PORT2))
        sock2.sendall(studentid)
        ok = sock2.recv(1024).strip()
        sock2.sendall(str(self.problemtext))
        choose = sock2.recv(1024).strip()
        
        sock2.close()
        html_str = pkg_resources.resource_string(__name__, "static/html/Pc2Judge.html")
        frag = Fragment(unicode(html_str).format(edxid=self.edxid,problemtext=self.problemtext))   
       
        if(choose=="None"):
        	self.edxid = studentid 
        	
        	js_str = pkg_resources.resource_string(__name__, "static/js/Pc2Judge_1.js")
        	frag.add_javascript(unicode(js_str))
        	frag.initialize_js('Pc2JudgeBlock')
        elif(choose=="YES"):
		self.edxid = studentid 
        	
        	js_str = pkg_resources.resource_string(__name__, "static/js/Pc2Judge_2.js")
        	frag.add_javascript(unicode(js_str))
        	frag.initialize_js('Pc2JudgeBlock2')
        elif(choose=="NO"):
		self.edxid = studentid 
        	
        	js_str = pkg_resources.resource_string(__name__, "static/js/Pc2Judge_3.js")
        	frag.add_javascript(unicode(js_str))
        	frag.initialize_js('Pc2JudgeBlock3')
        #html_str = pkg_resources.resource_string(__name__, "static/html/Pc2Judge2.html")
       
        #sock.connect((HOST, PORT))
        #sock.sendall(test)
        #sock.sendall(test)
        #sock.close()
        
        
        #frag.initialize_js('Pc2JudgeBlock')
        return frag
        
    
        
    def studio_view(self, context):
        html_str = pkg_resources.resource_string(__name__, "static/html/Pc2Judge_edit.html")
        
        href = self.href or ''
        frag = Fragment(unicode(html_str).format(href=href, maxwidth=self.maxwidth, maxheight=self.maxheight))

        js_str = pkg_resources.resource_string(__name__, "static/js/Pc2Judge_edit.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('SimpleVideoEditBlock')

        return frag

    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.href = data.get('href')
        self.maxwidth = data.get('maxwidth')
        self.maxheight = data.get('maxheight')

        return {'result': 'success'}

    @staticmethod
    def workbench_scenarios():
        return [
            ("Edx-Pc2-Judge", 
              """
                <vertical_demo>
                   <pc2judge  />  
                   <html_demo><div>Rate the video:</div></html_demo>
                </vertical_demo>
             """),
        ]
