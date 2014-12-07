import logging
import pkg_resources
import requests
import cgi
import socket
import sys
from urlparse import urlparse
from lxml import etree
from pkg_resources import resource_string


from xmodule.x_module import XModule
from xmodule.raw_module import RawDescriptor
from xblock.core import Scope, String
from xmodule.annotator_mixin import get_instructions
from xmodule.annotator_token import retrieve_token
from xblock.fragment import Fragment
from xblock.run_script import run_script
import textwrap

from xblock.core import XBlock
from xblock.fields import Boolean, DateTime, Scope, String, Float, Integer,ScopeIds
from xblock.fragment import Fragment
import xblock.runtime

class Pc2JudgeBlock(XBlock):
    has_score = True
    icon_class = 'problem'
   
    weight = Float(
        display_name="Problem Weight",
        default=1,
        help=("Defines the number of points each problem is worth. "
              "If the value is not set, the problem is worth the sum of the "
              "option point values."),
        values={"min": 0, "step": .1},
        scope=Scope.settings
    )
    score2 = Float(
        display_name="Grade score",
        default=10,
        help=("Grade score given to assignment by staff."),
        values={"min": 0, "step": .1},
        scope=Scope.user_state
    )
    score_published2 = Boolean(
        display_name="Whether score has been published.",
        help=("This is a terrible hack, an implementation detail."),
        default=True,
        scope=Scope.user_state
    )

    score_approved2 = Boolean(
        display_name="Whether the score has been approved by an instructor",
        help=("Course staff may submit grades but an instructor must approve "
              "grades before they become visible."),
        default=True,
        scope=Scope.user_state
    )
    zcore895= Float(
        #display_name="Maximum score",
        help=("Maximum grade score given to assignment by staff."),
        values={"min": 0, "step": .1},
        default=10,
        scope=Scope.settings
    )
    """A simple block: just show some fixed content."""
    edxid = String(help="URL of the video page at the provider", default=None, scope=Scope.user_state)
    maxwidth = Integer(help="Maximum width of the video", default=800, scope=Scope.user_state)
    problemtext = Integer(help="Maximum width of the video", default=0, scope=Scope.user_state)
    maxheight = Integer(help="Maximum height of the video", default=450, scope=Scope.user_state)
    watched = Integer(help="How many times the student has watched it?", default=0, scope=Scope.user_state)
    def max_score(self):
        return self.zcore895
    def student_view(self, context=None):  # pylint: disable=W0613
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
        
    def pc2(self, data, suffix=''): 
        """
        Called when submitting the form in Studio.
        """
        
        #HOST, PORT = "140.115.51.242", 9994
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.score2 = 90
        test = str(self)
       
        event_data = {'value': self.weight, 'max_value': self.weight,}
        self.runtime.publish(self, 'grade',event_data)
        #sock.connect((HOST, PORT))
        #sock.sendall(test)
        #sock.close()
        
        
        return {'status': 'ok'}   
        
    def studio_view(self, context):
        html_str = pkg_resources.resource_string(__name__, "static/html/Pc2Judge_edit.html")
        problemtext = self.problemtext or ''
        frag = Fragment(unicode(html_str).format(problemtext=problemtext))

        js_str = pkg_resources.resource_string(__name__, "static/js/Pc2Judge_edit.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('Pc2JudgeEditBlock')

        return frag

    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.problemtext = data.get('problemtext')
        

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
