# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/3/2

get_redirect_url_script = """
function main(splash, args)
    assert(splash:go(args.url))
    splash:set_viewport_full()
    splash:wait(0.1)
    splash:runjs("document.querySelector('.left_nav > ul > li:nth-child(1) > a').click()");
    splash:wait(0.5)
    local next_url = splash:evaljs("document.URL")
    return {parse_url=parse_url,
            next_url=next_url}
end
"""


get_next_url_script = """
function main(splash, args)
    assert(splash:go(args.url))
    splash:set_viewport_full()
    splash:wait(0.1)
    local get_next_url = splash:jsfunc([[
        function test() {
            var a = document.querySelector('.nav_go_next > a');
            if (a == null)
                return a;
            return a.href;
            }
        ]]);
    return {parse_url=args.url,
            next_url=get_next_url()}
end
"""
