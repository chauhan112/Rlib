class VideoDB:
    def size(filename):
        import subprocess 
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)

class YoutubeDB:
    def getSubtitleForVideoId(videoId, original = False):
        from youtube_transcript_api import YouTubeTranscriptApi

        sub = YouTubeTranscriptApi.get_transcript(videoId)
        if(original):
            return sub
        text = ""

        for line in sub:
            text += ' ' + line['text']
        return text

class AudioDB:
    def playWith():
        class Temp:
            def data(data, framerate):
                return Audio(data,rate=framerate)
            def url(uri):
                return Audio(url=uri)
            def path(filePath):
                return Audio(filename=filePath)
            
        return Temp
    
    def examples():
        class Temp:
            def TestAudio():
                from IPython.display import Audio
                return Audio("http://www.nch.com.au/acm/8k16bitpcm.wav")
            
            def manuallyCreatedAudio():
                import numpy as np
                class Te:
                    framerate = 44100
                    def audioData():
                        t = np.linspace(0,5,Te.framerate*5)
                        data = np.sin(2*np.pi*220*t) + np.sin(2*np.pi*224*t)
                        return data, framerate
                    
                    def audioDataWithChannels():
                        dataleft = np.sin(2*np.pi*220*t)
                        dataright = np.sin(2*np.pi*224*t)
                        return [dataleft, dataright], framerate
                return Te
        
        return Temp

class CategorizeVideoIntoDifferentSizes(IOps):
    def __init__(self, files, target_folder= None):
        self.files = files
        self._outfolder = target_folder
    def execute(self):
        from OpsDB import OpsDB
        import os
        from Path import Path
        
        sizes = {f: VideoDB.size(f) for f in self.files}
        sizesInMin = {f:sizes[f]/60 for f in sizes}
        sizes_group = OpsDB.group(sizesInMin, lambda x: round(sizesInMin[x]//5) )
        for val in  sizes_group:
            flder = 'less_than_'+ str(val*5)
            if not os.path.exists(flder):
                os.mkdir(flder)
            for f in sizes_group[val]:
                try:
                    Path.move().files([f], to+os.sep + flder)
                except Exception as e:
                    print(e)