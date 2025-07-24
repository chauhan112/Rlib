from useful.FileDatabase import File

class ChromeDB:
    def youtubePage(links, totaltime ,number = 2, speed = 2):
        textBefore = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Video test</title>
                        <style>
                            html,body {
                                padding:0;
                                margin:0;
                                height:100%;
                            }
                            #video1{
                                float: left;
                            }
                            #video2, #video4{
                                float: right;
                            }
                        </style>
                    </head>
                    <body>"""        
        if(type(links) is not list):
            links = [links]*number
        options = {
            2: 'height = "90%"',
            4: 'height = "48%"'
        }

        if(number not in options):
            number = 2
        oneFrame = '<iframe width = "48%" {} src="https://www.youtube.com/embed/{}?start={}" allowfullscreen></iframe>'

        iframes = "".join([oneFrame.format(i,j,k) for i,j, k in list(zip([options[number]] * number , links , 
                    [int(i* (1/number) * totaltime) for i in range(number)]))])
        speedSet = """<script>
                        var i;
                        for (i = 0; i < number; i++) {{
                            document.getElementsByTagName("iframe")[i].playbackRate = {};
                        }}
                    </script>""".format(speed)
        textAfter = "</body></html>"
        File.overWrite("youtube.html", textBefore +  iframes + speedSet + textAfter)
        textBefore = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Video test</title>
                        <style>
                            html,body {
                                padding:0;
                                margin:0;
                                height:100%;
                            }
                            #video1{
                                float: left;
                            }
                            #video2, #video4{
                                float: right;
                            }
                        </style>
                    </head>
                    <body>"""        
        if(type(links) is not list):
            links = [links]*number
        options = {
            2: 'height= "100%"',
            4: 'height= "100%"'
        }
        if(number not in options):
            number = 2
        k = '<iframe width = "48%" {} src="https://www.youtube.com/embed/{}?start={}" allowfullscreen></iframe>'
        
        iframes = (k*number).format()
        speed = """<script>
                        var i;
                        for (i = 0; i < number; i++) {
                            document.getElementsByTagName("video")[0].playbackRate = {};
                        }
                    </script>"""
        textAfter = "</body></html>"