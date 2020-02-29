# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/2/29


show_origin_html_script = """
function main(splash, args)
    assert(splash:go(args.url))
    splash:wait(0.1)
    return splash:png()
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
    assert(splash:go(args.url))
    splash:set_viewport_full()
    splash:wait(0.1)
    splash:runjs("document.getElementById('832').click()")
    splash:wait(0.1)
    splash:runjs("document.getElementById('3236').click()")
    splash:wait(0.2)
    splash:runjs("document.getElementById('3237').childElements()[0].click()")
    splash:wait(1.5)
    local data1 = splash:evaljs("document.getElementById('DataList')")
    print(data1)
    dataList = splash:select('#DataList')
    return dataList
end
"""

test_script = """
function main(splash, args)
    assert(splash:go(args.url))
    local get_div_count = splash:jsfunc([[
    function () {
        var body = document.body;
        var divs = body.getElementsByTagName('div');
        return divs.length;
        }
    ]])
    local div_count = get_div_count()
    return div_count
end
"""

