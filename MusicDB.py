class MusicDB:
    def helloWorldMusic():
        return "\n".join(['live_loop :guit do',
                '  with_fx :echo, mix: 0.3, phase: 0.25 do',
                '    sample :guit_em9, rate: 0.5',
                '  end',
                '  #  sample :guit_em9, rate: -0.5',
                '  sleep 8',
                'end',
                '',
                'live_loop :boom do',
                '  with_fx :reverb, room: 1 do',
                '    sample :bd_boom, amp: 10, rate: 1',
                '  end',
                '  sleep 8',
                'end'])
    
    def playMP3File(filepath):
        from IPython.display import display, HTML, Audio
        return Audio(filename= filepath, autoplay=True)