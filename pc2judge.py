import logging
import pkg_resources
import requests
import cgi
import socket
import sys
from urlparse import urlparse

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

#log = logging.getLogger(__name__)

#test222 = str(log)
class Pc2JudgeBlock(XBlock):
    has_score = True
    icon_class = 'problem'
    """A simple block: just show some fixed content."""
    href = String(help="URL of the video page at the provider", default=None, scope=Scope.content)
    maxwidth = Integer(help="Maximum width of the video", default=800, scope=Scope.content)
    maxheight = Integer(help="Maximum height of the video", default=450, scope=Scope.content)
    watched = Integer(help="How many times the student has watched it?", default=0, scope=Scope.user_state)
    
    def student_view(self, context):  # pylint: disable=W0613
        #HOST, PORT = "localhost", 9994
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.runtime.publish(self, 'grade', {
                'value': 1,
                'max_value': 2,
            })
        html_str = pkg_resources.resource_string(__name__, "static/html/Pc2Judge.html")
        frag = Fragment(unicode(html_str).format(self=self))
        frag.add_css("""
            .Pc2Judge {
                border: solid 1px #888; padding: 3px;
            }
            """)
        #sock.connect((HOST, PORT))
        #sock.sendall(test222)
        #sock.close()
        
        
        frag.initialize_js('Pc2JudgeBlock')
        return frag
    
        
    def studio_view(self, context):
        html_str = pkg_resources.resource_string(__name__, "static/html/Pc2Judge2.html")
        frag = Fragment(unicode(html_str).format(self=self))
        frag.add_css("""
            .Pc2Judge2 {
                border: solid 1px #888; padding: 3px;
            }
            """)
        js_str = pkg_resources.resource_string(__name__, "static/js/Pc2Judge.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('Pc2JudgeBlock')
        return frag

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
