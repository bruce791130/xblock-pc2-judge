function Pc2JudgeBlock(runtime, element) {
 document.cookie = "studentid=; expires=Thu, 01 Jan 1970 00:00:00 UTC";
 document.cookie = "problem=; expires=Thu, 01 Jan 1970 00:00:00 UTC";   
 var v =  document.getElementById("edx").value;
 var v2 =  document.getElementById("edx2").value;
 
 setCookie("studentid", v, 30);
 setCookie("problem", v2, 30);
       
document.getElementById("iframe1").src = "http://acnlab.openedx.tw/correct.html?id="+v+"&problem="+v2;
	   
//location.href ="http://acnlab.openedx.tw/pc2.html?id="+"ffff"; 
//window.location="http://www.w3schools.com/"+"js/js_input_examples.asp"


    
}
function setCookie(cname,cvalue,exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname+"="+cvalue+"; "+expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
