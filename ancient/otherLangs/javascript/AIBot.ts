//AIAssistant/BusinessLogic/GlobalFlows/app

// UIState:navs[{id, name}], {settingPage{title, id, unselected, filesToDisplay{filename, index, filePathOnDisk}, saveBtnActive, deleteBtnActive}}
// QuadrantCollection{id, name, companyId}
// TrainFiles{id, fileSize, mimeType, filename, filePath, aiBot{id, name, companyId}}
// controller{infos{newly_created, old_deleted_files, files_from_table, all_bots, new_bots}}
   
class HashMapDataStructure {
    data: any = {};
    add(key, value, overwrite = false){  
        if (!overwrite && this.exists(key)){
            return
        }
        this.data[key] = value
    }
    deleteKey(key){
        if (this.exists(key)){
            delete this.data[key]
        }
    }
    exists(key){
        return this.data.hasOwnProperty(key)
    }
    read(key){
        return this.data[key]
    }
    readAllKeys(){
        return Object.keys(this.data)
    }
    create_new(){
        return new HashMapDataStructure()
    }
    clear(){
        for (let member in this.data) delete this.data[member];
    }
    size(){
        return this.readAllKeys().length
    }
}

class UIUpdate{
    app: any;
    async update_files_uploaded(action?: (outp) => void, botId?: number){ 
        if (!botId){
            botId = this.app.ui.aiUi.settingPage.id
        }  
        let response = await this.app.controller.fileops.model.run(["readBotFiles", false, botId])
        if (response) {
            this.app.controller.infos.old_deleted_files.clear()
            let controller = this.app.controller
            controller.infos.files_from_table.clear()
            for (const element of response.result.out) {
                controller.infos.files_from_table.add(element.filename, element, true) 
            } 
            this.update_files()
            if (action) {
                action(response);
            }  
        }
    }

    update_files(){
        let res = [];
        let controller = this.app.controller

        for (const eleme of controller.infos.files_from_table.readAllKeys()) {
            let element= controller.infos.files_from_table.read(eleme)
            if (!controller.infos.old_deleted_files.exists(element.filename)){
                res.push({'filename': element.filename, 'index': element.filename, "filePathOnDisk": element.filePath}) 
            }
        } 
        for (const elem of controller.infos.newly_created.readAllKeys()) {
            let element= controller.infos.newly_created.read(elem)
            res.push({'filename': element.info.name, 'index': element.info.name})
        } 
        this.app.ui.aiUi.settingPage.filesToDisplay = res
    }

    update_save_button(){
        if (this.app.ui.aiUi.settingPage.id === "new"){
            this.app.ui.aiUi.settingPage.saveBtnActive = !this.app.controller.infos.files_from_table.exists(this.app.ui.aiUi.settingPage.title) 
            this.app.ui.aiUi.settingPage.saveBtnActive = this.app.ui.aiUi.settingPage.saveBtnActive && this.app.ui.aiUi.settingPage.title.trim() !== ""
        }else{
            let inst = this.app.model.read(this.app.ui.aiUi.settingPage.id)
            if (inst){
                this.app.ui.aiUi.settingPage.saveBtnActive = (this.app.ui.aiUi.settingPage.title.trim() !== "" && inst.data.title !== this.app.ui.aiUi.settingPage.title.trim())
            }
            this.app.ui.aiUi.settingPage.saveBtnActive = this.app.ui.aiUi.settingPage.saveBtnActive || (this.app.controller.infos.newly_created.readAllKeys().length > 0)
            this.app.ui.aiUi.settingPage.saveBtnActive = this.app.ui.aiUi.settingPage.saveBtnActive || (this.app.controller.infos.old_deleted_files.readAllKeys().length > 0)
            this.app.ui.aiUi.settingPage.saveBtnActive = this.app.ui.aiUi.settingPage.saveBtnActive && (!this.app.controller.infos.files_from_table.exists(this.app.ui.aiUi.settingPage.title))
        }
    }

    trigger_change(){
        this.app.ui.aiTriggeredChange ++;
    }

    update_page(inst){
        let idd =inst.read("id")
        let title = inst.read("title")
        if (this.app.ui.aiUi.settingPage.id !== idd || this.app.ui.aiUi.settingPage.unselected !== false) { 
            this.app.ui.aiUi.settingPage.title = title 
            this.app.ui.aiUi.settingPage.id = idd
            this.app.ui.aiUi.settingPage.unselected = false
            this.app.controller.infos.newly_created.clear()
            this.app.controller.infos.old_deleted_files.clear()
            this.app.ui.aiUi.settingPage.filesToDisplay = []
            this.app.ui.aiUi.settingPage.deleteBtnActive = true 
            this.app.ui.aiUi.settingPage.saveBtnActive = false 
        }
    }
    async fetch_bots(){
        let response = await this.app.controller.fileops.model.run(["readBots", false, 0])
        if (response?.result?.out){
            this.app.controller.infos.all_bots.clear()
            for (const element of response.result.out) {
                this.app.controller.infos.all_bots.add(element.name, element, true)
            }
            this.load_bots()
        }
    }
    load_bots(){
        let res = []
        for (const elem of this.app.controller.infos.all_bots.readAllKeys()) {
            let element = this.app.controller.infos.all_bots.read(elem)
            res.push({name: element.name, id: element.id})
        }

        for (const elem of this.app.controller.infos.new_bots.readAllKeys()) {
            let element = this.app.controller.infos.new_bots.read(elem)
            res.push({name: element.name, id: element.id})
        }

        this.app.ui.aiUi.navs = res
        this.trigger_change()  
    }

}

class FileOps{
    model: any;
    app: any 
    async delete_a_file(fildId, filename){
        await this.model.run(["deleteFile", false, {fileId: fildId, filename: filename}])
    }

    async read_bot_files(botId) {
        let response = await this.model.run(["readBotFiles", false, botId])
        return response.result.out
    }

    async delete_a_bot(botId){
        let files = await this.read_bot_files(botId)
        for (const element of files) {
            await this.delete_a_file(element.id, element.filePath)
        } 
        await this.model.run(["deleteBot", false, botId])
        this.app.controller.apiTool.delete(this.app.ui.aiUi.settingPage.title)
        await this.app.ui_parser.fetch_bots()
        this.app.ui.aiUi.settingPage.id = null
        this.app.ui.aiUi.settingPage.unselected =true
        this.app.ui_parser.trigger_change()
    }

    async read_bots(){
        let response = await this.app.controller.fileops.model.run(["readBots", false, 0])
        return response?.result?.out
    }
    async create_new_bot(name){
        let response = await this.model.run(["createBot", false, name])
        return response.result.out.id
    }

    async add_a_bot_file(fileInfo, botId){
        await this.app.controller.fileops.model.run(["uploadFile", false, {file: fileInfo, botId:botId}])
    }
}  
 
class AppController{
    apiTool: any
    infos: any = {}; 
    app: any;
    fileops: any;
    private changed: boolean = true;

    async save_to_table(){
        this.app.ui.aiUi.settingPage.isLoading = true
        this.app.ui_parser.trigger_change()
        if (this.app.ui.aiUi.settingPage.id === "new"){
            let botid = await this.fileops.create_new_bot(this.app.ui.aiUi.settingPage.title)
            let app = this.app
            app.ui.aiUi.settingPage.id = botid
            app.controller.infos.new_bots.clear()
            setTimeout(() => { 
                this.update_files_and_train_bot(botid) 
            }, 1000)
            app.ui.aiUi.settingPage.id = null
            app.ui.aiUi.settingPage.unselected =true 
            app.ui_parser.fetch_bots()
        }else{            
            this.update_files_and_train_bot(this.app.ui.aiUi.settingPage.id) 
        }
    }  
    
    async update_files_and_train_bot(botId){
        this.changed = false
        let filesInfo = this.app.controller.infos.newly_created.readAllKeys().map((file) => this.app.controller.infos.newly_created.read(file).info)
        
        for (const element of filesInfo) {
            try {  await this.fileops.add_a_bot_file(element, botId) }
            catch(e){
                let result = e.message; // error under useUnknownInCatchVariables 
                console.log(result) 
            }
            this.changed = true
        }  
        
        let files = this.app.controller.infos.old_deleted_files.readAllKeys().map((file) => this.app.controller.infos.old_deleted_files.read(file))
        for (const element of files) {
            await this.fileops.delete_a_file(element.id, element.filePath)
            this.changed = true
        } 
        this.app.controller.infos.newly_created.clear()
        this.app.controller.infos.old_deleted_files.clear()
        this.update_navs(botId) 
    } 

    update_navs(botId){ 
        if(this.changed){
            this.app.ui_parser.update_files_uploaded((response) => {
                let files = response.result.out.map((x) => {return {filename: x.filePath}})
                let chatbotName = this.app.ui.aiUi.settingPage.title
                this.apiTool.update(chatbotName, files)
                this.app.ui_parser.update_save_button()
                this.app.ui.aiUi.settingPage.isLoading = false
                this.app.ui_parser.trigger_change()  
            }, botId) 
        }else{
            this.app.ui.aiUi.settingPage.isLoading = false
            this.app.ui_parser.trigger_change()   
        }

    } 
}

class APItool{
    update(chatbotName, files){
        fetch("https://k8-lcap-255-105.ect-telecoms.de/chatbot/db-exists/", {
            method: "POST", 
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "chatbot_name": chatbotName,
            }),
        }).then(response => {return response.json()}).then((res) => {
            if (res.exists){
                this.retrain(chatbotName, files)
            }else{
                this.create(chatbotName, files)
            }
        })
    }
    create(chatbotName, files){
        fetch("https://k8-lcap-255-105.ect-telecoms.de/chatbot/create-chatbot/", {
            method: "POST", 
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "chatbot_name": chatbotName,
                "files": files
            }),
        })
    }
    retrain(chatbotName, files){
        fetch("https://k8-lcap-255-105.ect-telecoms.de/chatbot/update-chatbot/", {
            method: "POST", 
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "chatbot_name": chatbotName,
                "files": files
            }),
        })
    }
    delete(chatbotName){
        fetch("https://k8-lcap-255-105.ect-telecoms.de/chatbot/delete-chatbot/", {
            method: "POST", 
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "chatbot_name": chatbotName
            }),
        })
    } 
}   
 
class Application{
    ui: any;
    controller: any;
    model: any;
    ui_parser: any;
} 

  
this.inst = new Application()
this.inst.controller =  new AppController()
this.inst.model = new HashMapDataStructure()
this.inst.ui_parser = new UIUpdate() 

this.inst.ui_parser.app = this.inst
this.inst.controller.app = this.inst 
this.inst.controller.apiTool = new APItool()
this.inst.controller.fileops = new FileOps()
this.inst.controller.fileops.app = this.inst  