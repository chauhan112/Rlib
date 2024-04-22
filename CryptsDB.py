import random
import string


class CryptsDB:
    def generatePassWord(length = 10):
        password_characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(password_characters) for i in range(length))

    def generateRandomName(length = 15):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

    def generateUniqueId():
        import uuid
        return uuid.uuid4().hex

    def encrypt(inpFile, outFile, password, size = 128 * 1024):
        import pyAesCrypt
        pyAesCrypt.encryptFile(inpFile, outFile, password, size)

    def decrypt(inpFile, outFile, password, size = 128 * 1024):
        import pyAesCrypt
        pyAesCrypt.decryptFile(inpFile, outFile, password, size)
    
    def generateRandomWord():
        from wonderwords import RandomWord
        w = RandomWord()
        return w.word()
    def generateRandomSentence():
        from wonderwords import RandomSentence
        s = RandomSentence()
        return s.sentence()