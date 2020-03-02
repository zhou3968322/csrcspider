function main(splash)
    assert(splash:go(splash.args.url))
    assert(splash:wait(5))
    local getFramesHtml = splash:jsfunc([[
    function test() {
        var data = [];
        for (var i = 0 ; i < window.frames.length; i++)
        {
            data.push(window.frames[i].document.documentElement.outerHTML);
        }
        return data;
        }
    ]]);

    return {
        html = splash:html(),
        frames = getFramesHtml()
        }
end