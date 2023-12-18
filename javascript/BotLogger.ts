enum BotStatus{
    Started,
    Completed, 
    Abandoned
}

class BotInfoManager{
    botStatus: any = {};
    update_bot_status(botId: number, status: string){
        if (!this.botStatus.hasOwnProperty(botId)){
            this.botStatus[botId] = {status: status}
        }else {
            this.botStatus[botId].status = status
        }
        this.write_locally()
    }
    update_time(botId: number){
        if (!this.botStatus.hasOwnProperty(botId)){
            this.botStatus[botId] = {startedTime: new Date()}
        }else {
            this.botStatus[botId].startedTime = new Date()
        }
        this.write_locally()
    }
    write_locally(){
        localStorage.setItem('botStatus', JSON.stringify(this.botStatus))
    }
    read_locally(){
        let x = localStorage.getItem("botStatus")
        if (!x){
            this.botStatus = {}
        }else {this.botStatus = JSON.parse(x) }
        
    }
    get_status_with_botId(botId: number): BotStatus{
        this.read_locally()
        return this.botStatus[botId].status
    }
    get_all_ended_bots(){
        this.read_locally()
        let res = Object.keys(this.botStatus).filter(botId => this.botStatus[botId].status === BotStatus[BotStatus.Completed])
        let parsed: number[] = []
        for (let ele of res) {
            let inv = parseInt(ele)
            parsed.push(inv)
        }
        return parsed
    }
    update_interacted_status(botId, value:boolean=true){
        if (!this.botStatus.hasOwnProperty(botId)){
            this.botStatus[botId] = {interacted: value}
        }else this.botStatus[botId].interacted = value
        this.write_locally()
    }
    get_status(){
        this.read_locally()
        return this.botStatus
    }
    logStepInfo(step, botId){
        this.write_locally_last_step_status("step", step)
        this.write_locally_last_step_status("botId", botId)
    }
    private write_locally_last_step_status(key, value){
        let x = this.get_last_step_info()
        if (!x){
            x = {}
        }
        x[key] = value
        localStorage.setItem('lastBotStepInfo', JSON.stringify(x))
    }
    
    get_last_step_info(){
        let x = localStorage.getItem("lastBotStepInfo")
        if (!x){
            return x
        }
        return JSON.parse(x)
    }
    update_badge_count(count) {
        this.write_locally_last_step_status("badgeCount", count)
    }

    getTime(key) {
        let val = this.get_last_step_info()
        if (val && val.hasOwnProperty(key))
            return val[key] 
        return -1
    }
    logTime(key, value){
        this.write_locally_last_step_status(key, value)
    }
}


console.log("bot status logger")
$this.out = new BotInfoManager() 

