class Confirmation:
    def doUWantToContinue(message = "do you want to continue?"):
        val = input(message)
        if(len(val) == 0):
            return False
        if('y' in val[0].lower()):
            return True
        return False