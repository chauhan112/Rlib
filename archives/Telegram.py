from Path import Path
from archives.coronaUpdate import get_country_confirmed_infected, getMessage
from OpsDB import IOps
class IController:
    def __init__(self):
        self.replyMsg = ""

    def getReply(self, message):
        print(self.__class__.__name__)
        return self._getReply(message)

    def continueToNext(self):
        return self.replyMsg != ""

    def _getReply(self, message):
        raise NotImplementedError()

class CCoronaInfo(IController):
    def _getReply(self, message):
        self.replyMsg = ""
        if(message.lower() == "corona"):
            countries = ["nepal", "germany", "india", "usa", "japan"]
            msg = ""
            for country in countries:
                msg += country + "\n"
                msg += getMessage(country)
                msg += "\n\n"
            self.replyMsg = msg
        return self.replyMsg
class DefaulController(IController):
    def _getReply(self, message):
        return 'invalid function'

class MainController:
    controllers = [ CCoronaInfo(), DefaulController() ]

    def getReply(msg):
        reply = ""
        for con in MainController.controllers:
            reply += con.getReply(msg)
            if(con.continueToNext()):
                break
        return reply
class ExtractHeaderFromTelegramMessageHtml(IOps):
    def __init__(self, html):
        self.set_file(html)
        self._forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    def set_file(self, html):
        self._html = html
    def execute(self):
        from htmlDB import htmlDB
        from FileDatabase import File
        val = htmlDB.getParsedData(File.getFileContent(self._html))
        found = val.find_all('div', class_="page_header")
        found = found[0]
        title = found.div.div.string.strip()
        for ch in self._forbidden_chars:
            title = title.replace(ch, "")
        return title
class RenameAllTelegramFolderExportedMessage(IOps):
    def set_folder(self, folder):
        self._path = folder
    def execute(self):
        exported_chrts =list(filter(lambda x: "ChatExport" in x, os.listdir(self._path)))
        eh = ExtractHeaderFromTelegramMessageHtml(None)
        for chat in exported_chrts:
            msg_file = os.sep.join([self._path, chat, 'messages.html'])
            if os.path.exists(msg_file):
                eh.set_file(msg_file)
                title = eh.execute()
                self._rename_folder(self._path + os.sep + chat, self._path + os.sep + title)
            
    def _rename_folder(self, old, new):
        os.rename(old, new)

class TBot:
    instance = None
    
    def start():
        if(TBot.instance is not None):
            print("a bot is already running")
        else:
            TBot._setup()
        return TBot.instance
    
    
    def _setup():
        from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
        from jupyterDB import jupyterDB
        import logging
        from telegram.ext import InlineQueryHandler
        
        class Temp:
            def start(update, context):
                update.message.reply_text("type something to get started")
                
            def _help(update, context):
                update.message.reply_text("help funcs")

            def handle(update, context):
                text = str(update.message.text).lower()
                update.message.reply_text(MainController.getReply(text))

            def tech(update ,context):
                msg = ' '.join(context.args).upper()
                context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

            def error(update, context):
                print(f"Update {update} caused error {context.error}")
                
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                             level=logging.INFO)

        k = jupyterDB.pickle().read("crypts")
        updater = Updater(k['logger token'], use_context=True)
        dp  = updater.dispatcher
        dp.add_handler(CommandHandler("start", Temp.start))
        dp.add_handler(CommandHandler('tech', Temp.tech))
        dp.add_handler(CommandHandler("help", Temp._help)) 
        dp.add_handler(MessageHandler(Filters.text, Temp.handle))
        dp.add_error_handler(Temp.error)
        updater.start_polling()
        updater.idle()
        TBot.instance = updater