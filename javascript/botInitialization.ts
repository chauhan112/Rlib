//SCVisitor/Citizen-tool/flows/botStepExecution
enum BotStatus {
    Started,
    Completed,
    Abandoned
}

class RefreshTimer {
    timer: any;
    private callback: any;
    private duration: number; // number of seconds
    logger: any;
    key: string;

    start(logIt = true) {
        this.clear();
        this.timer = setTimeout(this.callback, this.duration);
        let nowTime = Date.now()
        if (logIt) this.logger.logTime(this.key, nowTime);
    }

    get_rem_time() {
        let startedTime = this.logger.getTime(this.key)
        return Date.now() - startedTime;
    }
    canItBeLoaded() {
        let startedTime = this.logger.getTime(this.key)
        let dur = Date.now() - startedTime;
        if (dur > this.duration * 1000) {
            return false;
        }
        return true;
    }
    clear() {
        clearTimeout(this.timer)
    }
    set_callback(callback) {
        this.callback = callback;
    }
    set_duration(duration) {
        this.duration = duration;
    }
    set_logger(logger) {
        this.logger = logger;
    }
    set_key(key: string) {
        this.key = key;
    }
}

class BotStepManager {
    convId: number;
    totalBotSteps: number;
    parsedSteps: any;
    currentBotId: number;
    flowGlobalSteps: any;
    flowGlobalUpdatemessages: any;
    flowGlobalEscalatetoagent: any;
    flowGlobalGetnextbot: any;
    visitorRef: string;
    parentRef: string;
    timeout: number;
    logger: any;

    setTimeoutPeriod(milisec) {
        this.timeout = milisec
    }
    setBotId(botId) {
        this.currentBotId = botId
    }
    setConversationId(convID) {
        this.convId = convID
    }
    setParsedSteps(steps) {
        this.parsedSteps = steps
        this.totalBotSteps = steps.length
    }
    setStepsRunner(runner) {
        this.flowGlobalSteps = runner
    }
    setMessageUpdater(updater) {
        this.flowGlobalUpdatemessages = updater
    }
    setEscalator(escalator) {
        this.flowGlobalEscalatetoagent = escalator
    }
    setNextBotInstance(ins) {
        this.flowGlobalGetnextbot = ins
    }
    setVisitorRef(ref) {
        this.visitorRef = ref
    }
    setParentRef(ref) {
        this.parentRef = ref
    }
    set_logger(logger) {
        this.logger = logger
    }
    repeatSteps(curStepNr) {
        let steCon = this.getAndUpdateStep(curStepNr)
        if (steCon.content.type == "UInput") {
            this.setInputStatus(steCon)
        } else if (steCon.content.type == "QReply") {
            VariableService.global.view.bottom.disableTextField = true
            VariableService.global.view.bottom.textInputPlaceholder = "Select an option above"
            VariableService.global.view.window.chatBottomState = "Open"
            VariableService.global.view.window.hideBorderBottom = false
            VariableService.global.botModel.expecting.type = "None"
        } else {
            VariableService.global.botModel.expecting.type = "None"
            VariableService.global.view.window.chatBottomState = "Close"
            VariableService.global.view.window.hideBorderBottom = true
        }
        if (this.hasThisStepRun(curStepNr)) {
            let rf = new RefreshTimer()
            rf.set_logger(this.logger)
            rf.set_key("StepTimer")
            let timePrefix = -1
            let totalRunTime = rf.get_rem_time()
            // console.log("total run time: " + totalRunTime);
            timePrefix = steCon.parsed.timeout - totalRunTime;
            if (timePrefix < 500) {
                timePrefix = 500;
            }
            this.stepRunSuceeded(steCon, curStepNr, timePrefix)
        } else {
            this.flowGlobalSteps.run([VariableService.global.botModel.currentBotId, this.visitorRef, this.parentRef, this.convId, true,
            this.parsedSteps, steCon, VariableService.global.view.widgetV1.widgetState == "Open"]).then((response: any) => {
                if (VariableService.global.view.widgetV1.widgetState === "Close") {
                    VariableService.global.view.widgetV1.badgeNotify++;
                    this.logger.update_badge_count(VariableService.global.view.widgetV1.badgeNotify)
                }
                this.stepRunSuceeded(steCon, curStepNr);
            }, (error: { [key: string]: any }) => {
                console.error('flowGlobalSteps.run Error', error);
            });
        }
    }

    private hasThisStepRun(step: any) {
        let stepBotInfo = this.logger.get_last_step_info();
        return stepBotInfo && stepBotInfo.step && stepBotInfo.step[0] === step[0] && stepBotInfo.step[1] === step[1] &&
            stepBotInfo.botId === VariableService.global.botModel.currentBotId
    }
    stepRunSuceeded(stepContent, currentStep, remainingTime = -1) {
        let step = currentStep[0]
        this.logger.logStepInfo(currentStep, VariableService.global.botModel.currentBotId)
        let nextStepTimeout = stepContent.getNextStepForTimeOut()
        let time2wait = stepContent.parsed.timeout
        let logIt = true;
        if (remainingTime > 0) {
            time2wait = remainingTime
            logIt = false;
        }
        this.flowGlobalUpdatemessages.run([this.convId, false, VariableService.global.visitorDetails.parentRef,
        VariableService.global.sessionManger.name]).then((response: any) => {
            VariableService.global.parsedMessages = response.result.res
            if (response.result.user.type && response.result.user.type !== "BOT") {
                this.stopBotExecution(response.result.user, "LiveAgentSession")
                this.setTimerForSession()
                return
            }
        }, (error: { [key: string]: any }) => {
            console.error('flowGlobalUpdatemessages.run Success', error);
        });

        if (stepContent.parsed.type == "Escalate") {
            this.addToEndedBots(VariableService.global.botModel.currentBotId)
            this.logger.update_bot_completed_count(VariableService.global.botModel.currentBotId)
            this.stopBotExecution()
            this.setTimerForSession()
            this.flowGlobalEscalatetoagent.run([this.parentRef, this.visitorRef, false,
            VariableService.global.botModel.currentBotId]).then((response: any) => {
                console.debug('flowGlobalEscalatetoagent.run Success', response);
            }, (error: { [key: string]: any }) => { console.error('flowGlobalEscalatetoagent.run Error', error); });
            this.resetBotSteps()
        } else if (step + 1 >= this.totalBotSteps) {
            this.addToEndedBots(VariableService.global.botModel.currentBotId)
            this.logger.update_bot_completed_count(VariableService.global.botModel.currentBotId)
            this.continueToNextBot()
        } else {
            if (VariableService.global.botModel.timer) { VariableService.global.botModel.timer.clear() }
            VariableService.global.botModel.timer = this.timerSet(() => { this.repeatSteps(nextStepTimeout) }, time2wait, "StepTimer", logIt);
        }
        VariableService.global.changeTrigger += 1
        this.setTimerForSession()
    }
    private timerSet(func, time2wait, key: string, logIt = true) {
        console.log("setting time: ", key)
        let timer = new RefreshTimer();
        timer.set_callback(func)
        timer.set_duration(time2wait)
        timer.set_logger(this.logger)
        timer.set_key(key)
        timer.start(logIt)
        return timer
    }
    private resetBotSteps() {
        localStorage.setItem("stepNumber", "0")
        localStorage.setItem("subStepNumber", "0")
    }
    private startingABot() {
        console.log("bot starting")
        VariableService.global.view.widgetV1.conversationWith = { "type": "BOT", "name": "Emma" }
        VariableService.global.view.window.chatBottomState = "Close"
        VariableService.global.botModel.expecting.type = "None"
        VariableService.global.view.window.hideBorderBottom = true
        VariableService.global.sessionManger.name = "BotRunningSession"
    }
    private stopBotExecution(agent = { "type": "AGENT", "name": "Customer Support" }, sessionName = "LiveIdleSession") {
        console.log("bot stops now")
        VariableService.global.view.widgetV1.conversationWith = agent
        VariableService.global.view.window.chatBottomState = "Open"
        VariableService.global.view.bottom.textInputPlaceholder = "Send a message..."
        VariableService.global.view.bottom.errorRegex = ""
        VariableService.global.view.bottom.disableTextField = false
        VariableService.global.view.window.hideBorderBottom = false
        VariableService.global.sessionManger.name = sessionName
        VariableService.global.botModel.expecting.type = "None"
        if (VariableService.global.botModel.timer)
            VariableService.global.botModel.timer.clear(); 
        let msgs = VariableService.global.parsedMessages
        let lastEntry = msgs[msgs.length - 1]
        if (lastEntry && VariableService.global.sessionManger.name !== "BotRunningSession") {
            if (lastEntry.botMsg.value.hasOwnProperty('length')) { lastEntry.botMsg.show = false; }
            VariableService.global.changeTrigger += 1
        }
    }
    private addToEndedBots(endedBotId) {
        this.logger.update_bot_status(endedBotId, BotStatus[BotStatus.Completed])
    }
    private getAndUpdateStep(stepNr) {
        let step = stepNr[0]
        let substep = stepNr[1];
        localStorage.setItem("stepNumber", step.toString())
        localStorage.setItem("subStepNumber", substep.toString())
        VariableService.global.botModel.currentStepNr = step
        VariableService.global.botModel.currentSubStepNr = substep
        return this.parsedSteps[step][substep]
    }
    private setInputStatus(step) {
        VariableService.global.botModel.expecting.type = step.parsed.type
        VariableService.global.botModel.expecting.nextStep = step.getNextStep()
        VariableService.global.view.bottom.errorRegex = step.parsed.regex
        VariableService.global.view.bottom.textInputPlaceholder = step.parsed.placeHolder
        VariableService.global.view.bottom.ErrorHandler.value = step.parsed.errorMsg
        VariableService.global.view.window.chatBottomState = "Open"
        VariableService.global.view.bottom.disableTextField = false
        VariableService.global.view.window.hideBorderBottom = false
    }
    private nextStepForBot(botId, step, substep) {
        let lastBotStepInfo = this.logger.get_last_step_info()
        if (lastBotStepInfo && botId === lastBotStepInfo.botId) return [step, substep]
        return [0, 0]
    }
    continueToNextBot(stepNr = 0, subStepNr = 0) {
        this.flowGlobalGetnextbot.run([this.convId, this.visitorRef, this.parentRef, false, this.logger.get_status()]).then((response: any) => {
            let steps = response.result.botSteps
            if (response.result.botTriggerRemainingTime !== null && response.result.botTriggerRemainingTime > 0) {
                setTimeout(() => { this.checkTrigger() }, response.result.botTriggerRemainingTime * 1000);
            }
            if (response.result.botId !== null) {
                [stepNr, subStepNr] = this.nextStepForBot(response.result.botId, stepNr, subStepNr)
                VariableService.global.botModel.parsedBots = steps
                this.setParsedSteps(VariableService.global.botModel.parsedBots)
                this.startingABot()
                this.logger.update_bot_status(response.result.botId, BotStatus[BotStatus.Started])
                this.logger.update_bot_started_count(response.result.botId)
                this.logger.update_time(response.result.botId)
                if (VariableService.global.botModel.timer) { VariableService.global.botModel.timer.clear(); }
                VariableService.global.botModel.timer = this.timerSet(() => { this.repeatSteps([stepNr, subStepNr]) }, 1000, "StepTimer", false);
                VariableService.global.botModel.currentBotId = response.result.botId
                this.logger.update_interacted_status(VariableService.global.botModel.currentBotId, VariableService.global.view.widgetV1.widgetState === "Open")
            } else {
                if (response.result.assignedUser){
                    this.stopBotExecution({ type: "AGENT", name: response.result.assignedUser }, "LiveAgentSession")
                    this.setTimerForSession(false)
                }else { 
                    // when it goes to customer support, timer is set to check for new bots every one min # 60*1000
                    this.stopBotExecution()
                    VariableService.global.sessionManger.botConversation = this.timerSet(() => { this.botSessionEnds() }, 60*1000, "SessionTimer", false);
                }
                VariableService.global.changeTrigger += 1
            }
        }, (error: { [key: string]: any }) => {
            console.error('flowGlobalGetnextbot.run Error', error);
        });
    }
    checkTrigger() {
        if (VariableService.global.sessionManger.name === "LiveIdleSession") {
            this.continueToNextBot(0, 0);
        }
    }
    botSessionEnds() {
        console.log("bot session ends");
        if (VariableService.global.sessionManger.botConversation) { VariableService.global.sessionManger.botConversation.clear(); }
        if (VariableService.global.sessionManger.name === "BotRunningSession")
            this.addToEndedBots(VariableService.global.botModel.currentBotId)
        VariableService.global.sessionManger.name = "LiveIdleSession"
        this.continueToNextBot()
        this.resetBotSteps()
    }
    start() {
        if (VariableService.global.botModel.timer) { VariableService.global.botModel.timer.clear(); }
        console.log("clearing timeout")
        let stepO = parseInt(localStorage.getItem("stepNumber"))
        let substepO = parseInt(localStorage.getItem("subStepNumber"))
        VariableService.global.botModel.timer = this.timerSet(() => { this.repeatSteps([stepO, substepO]) }, 1000, "StepTimer", false);
    }
    setTimerForSession(reset = true) {
        if (VariableService.global.sessionManger.botConversation) { VariableService.global.sessionManger.botConversation.clear(); }
        console.log("bot session timeout in (s)", this.timeout / 1000)

        if (reset) { VariableService.global.sessionManger.botConversation = this.timerSet(() => { this.botSessionEnds() }, this.timeout, "SessionTimer"); }
        else {
            let rf = new RefreshTimer()
            rf.set_logger(this.logger)
            rf.set_key("SessionTimer")
            let timePrefix = -1
            let totalRunTime = rf.get_rem_time()
            timePrefix = this.timeout - totalRunTime;
            console.log("total session run time: ", totalRunTime, this.timeout);
            let logIt = false;
            if (timePrefix < 500) {
                timePrefix = 500;
                logIt = true;
            }
            VariableService.global.sessionManger.botConversation = this.timerSet(() => { this.botSessionEnds() }, timePrefix, "SessionTimer", logIt);
        }
    }
}

let bsm = new BotStepManager()
bsm.setConversationId(VariableService.global.convHistory.id)
bsm.setVisitorRef(VariableService.global.visitorDetails.visitorRef)
bsm.setParentRef(VariableService.global.visitorDetails.parentRef)
bsm.setStepsRunner(new FlowGlobalSteps())
bsm.setMessageUpdater(new FlowGlobalUpdatemessages())
bsm.setEscalator(new FlowGlobalEscalatetoagent())
bsm.setNextBotInstance(new FlowGlobalGetnextbot())
bsm.setTimeoutPeriod(VariableService.config.sessionTimeoutInX) // 2 hr = 2*60*60*1000 // 3 min = 3* 60 * 1000
VariableService.global.botModel.instance = bsm  