# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/2/29

"""
下面的都是针对http://www.csrc.gov.cn/pub/zjhpublic/旧的网站写的脚本
但由于网站不太稳定容易会有问题
"""

show_origin_png_script = """
function main(splash, args)
    assert(splash:go(args.url))
    splash:wait(0.1)
    return splash:png()
end
"""

show_origin_html_script = """
function main(splash, args)
    assert(splash:go(args.url))
    splash:wait(0.1)
    return splash:html()
end
"""

click_bt1_script = """
function main(splash, args)
    assert(splash:go(args.url))
    splash:set_viewport_full()
    splash:wait(0.1)
    splash:runjs("document.getElementById('832').click()")
    splash:wait(0.1)
    return splash.png()
end
"""

click_bt1_bt2_script = """
function main(splash, args)
    assert(splash:go(args.url))
    splash:set_viewport_full()
    splash:wait(0.1)
    splash:runjs("document.getElementById('832').click()")
    splash:wait(0.1)
    splash:runjs("document.getElementById('3236').click()")
    splash:wait(0.2)
    return splash.png()
end
"""

click_bt1_bt2_bt3_script = """
function main(splash, args)
    assert(splash:go(args.url))
    splash:set_viewport_full()
    splash:wait(0.1)
    splash:runjs("document.getElementById('832').click()")
    splash:wait(0.1)
    splash:runjs("document.getElementById('3236').click()")
    splash:wait(0.2)
    splash:runjs("document.getElementById('3237').childElements()[0].click()")
    splash:wait(1.5)
    return splash.png()
end
"""

get_page_html_script = """
function main(splash, args)
    assert(splash:go(args.url))
    splash:set_viewport_full()
    splash:wait(0.1)
    splash:runjs("document.getElementById('832').click()")
    splash:wait(0.1)
    splash:runjs("document.getElementById('3236').click()")
    splash:wait(0.2)
    splash:runjs("document.getElementById('3237').childElements()[0].click()")
    splash:wait(1.5)
    return splash.html()
end
"""

get_page_redirect_script = """
function main(splash, args)
    splash:set_user_agent('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 OPR/46.0.2597.57')
    assert(splash:go(args.url))
    splash:set_viewport_full()
    splash:wait(0.1)
    splash:runjs("document.getElementById('832').click()")
    splash:wait(0.1)
    splash:runjs("document.getElementById('3236').click()")
    splash:wait(0.2)
    splash:runjs("document.getElementById('3237').childElements()[0].click()")
    splash:wait(1.5)
    local getFramesUrl = splash:jsfunc([[
       function test() {
          return window.frames[0].document.URL;
        }
    ]]);
    return {url = getFramesUrl()}
end
"""

get_child_ms_script = """
function main(splash, args)
    assert(splash:go(args.url))
    splash:set_viewport_full()
    splash:wait(0.5)
    local get_href = splash:jsfunc([[
        function () {
        var container = document.querySelector("#documentContainer");
        var as = container.querySelectorAll("a");
        var attrList = []
        for(var i = 0, len = as.length; i < len; i++){
            attrList.push({"href": as[i].href, "text": as[i].text});
           }
        return attrList;
        }
    ]])
    return {attrs = get_href()}
end
"""

click_next_page_script = """
function main(splash, args)
    splash:set_user_agent('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 OPR/46.0.2597.57')
    assert(splash:go(args.url))
    splash:set_viewport_full()
    splash:wait(0.1)
    splash:runjs("document.getElementById('832').click()")
    splash:wait(0.1)
    splash:runjs("document.getElementById('3236').click()")
    splash:wait(0.2)
    splash:runjs("document.getElementById('3237').childElements()[0].click()")
    splash:wait(1.5)
    splash:runjs("window.frames[0].document.querySelector('.nav_go_next > a').click();");
      splash:wait(1.5)
    return {png = splash:png()}
end
"""

