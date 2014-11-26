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
from xblock.fields import Boolean, DateTime, Scope, String, Float, Integer
from xblock.fragment import Fragment


class Pc2JudgeBlock(XBlock):
    has_score = True
    icon_class = 'problem'
   
    weight = Float(
        display_name="Problem Weight",
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
    zscore= Float(
        #display_name="Maximum score",
        help=("Maximum grade score given to assignment by staff."),
        values={"min": 0, "step": .1},
        default=43,
        scope=Scope.settings
    )
    """A simple block: just show some fixed content."""
    href = String(help="URL of the video page at the provider", default=None, scope=Scope.content)
    maxwidth = Integer(help="Maximum width of the video", default=800, scope=Scope.content)
    maxheight = Integer(help="Maximum height of the video", default=450, scope=Scope.content)
    watched = Integer(help="How many times the student has watched it?", default=0, scope=Scope.user_state)
    def max_score(self):
        return self.zscore
    def student_view(self, context=None):  # pylint: disable=W0613
        HOST, PORT = "140.115.51.242", 9994
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #test = str(self.runtime.anonymous_student_id)
        #self.zxscore = 84
        #test=str(self.max_score())
        self.score2 = 90
        self.score_published2 = True
        self.score_approved2 = True
        test=str(self.score2)
        if  self.score_published2 and self.score_approved2:
            self.runtime.publish(self, 'grade', {
                'value':  self.score2,
                'max_value': self.max_score()
            })
           
            self.score_published2 = True
            self.score_approved2 = True
            
        #self.runtime.publish(self, 'progress', {'value':  self.score2,'max_value': self.max_score(),})
        html_str = pkg_resources.resource_string(__name__, "static/html/Pc2Judge.html")
        frag = Fragment(unicode(html_str).format(self=self))
        frag.add_css("""
            .Pc2Judge {
                border: solid 1px #888; padding: 3px;
            }
            """)
        sock.connect((HOST, PORT))
        #sock.sendall(test)
        sock.sendall(test)
        sock.close()
        
        
        frag.initialize_js('Pc2JudgeBlock')
        return frag
        
    def pc2(self, data, suffix=''): 
        """
        Called when submitting the form in Studio.
        """
        self.maxheight = 10
        HOST, PORT = "localhost", 9994
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.score2 = 90
        test222 = str(self.score2)
        if  self.score_published2 and self.score_approved2:
            self.runtime.publish(self, 'grade', {
                'value':  self.score2,
                'max_value': self.max_score()
            })
        sock.connect((HOST, PORT))
        sock.sendall(test222)
        sock.close()
        
        
        return {'status': 'ok'}   
        
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
