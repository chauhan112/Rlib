// SCVisitor/pro-tool/Business Logic/ClientFlows/botSteps/parseSteps

let DEFAULT_TIMEOUT = 1.5 * 1000 // 10 sec

interface IStepType {
    parse(): any;
    getNextStep();// returns array of size 2, [0] = step, [1]= substep 
    getNextStepForTimeOut();//return long 
    set_next_step(step, substep);
}
class TextStepType implements IStepType {
    content: any
    parsed: any // json format
    current_step: number
    private next_step: number[]
    constructor() {
        this.content = null
        this.parsed = null
        this.next_step = [-1, -1]
    }
    set_content(steps) {
        this.content = steps
        this.parse()
    }
    set_next_step(step, substep) {
        this.next_step = [step, substep]
    }
    parse() {
        if (this.parsed) { return this.parsed }
        let stp = -1
        if (this.content.data.hasOwnProperty("goToIndex")) {
            stp = this.content.data.goToIndex
        }
        let obj = {
            type: this.content.type,
            isQuickReply: false,
            isInputReply: false,
            isTextReply: true,
            isActionReply: false,
            QReplyOptions: [],
            UInputData: "",
            textData: this.content.data.text.trim(),
            timeout: DEFAULT_TIMEOUT,
            Step: stp
        }
        this.parsed = obj
        this.set_next_step(obj.Step, 0)
        return this.parsed
    }
    getNextStep() {
        return this.next_step
    }
    getNextStepForTimeOut() {
        return this.getNextStep()
    }
}
class QReplyStepType implements IStepType {
    content: any
    parsed: any // json format
    current_step: number
    private next_step: number[]
    constructor() {
        this.content = null
        this.parsed = null
        this.next_step = [-1, -1]
    }
    set_content(steps) {
        this.content = steps
        this.parse()
    }
    set_next_step(step, substep) {
        this.next_step = [step, substep]
        for (let opt of this.parsed.QReplyOptions) {
            if (!opt.hasOwnProperty("stepIndex")) {
                opt.stepIndex = -1
            }
            if (opt.stepIndex == -1) {
                opt.stepIndex = step
            }
        }
    }
    getNextStep() {
        return this.next_step
    }
    getNextStepForTimeOut() {
        return this.getNextStep()
    }
    parse() {
        if (this.parsed) { return this.parsed }
        let content = this.content.data.text
        if (content) {
            content = content.trim()
        }
        this.parsed = {
            type: this.content.type,
            isQuickReply: true,
            isInputReply: false,
            isTextReply: false,
            isActionReply: false,
            QReplyOptions: this.content.data.options,
            UInputData: "",
            textData: content,
            timeout: 1000 * 60 * 60 * 2, // default timeout 2 hr
            Step: -1
        }
        this.set_next_step(this.parsed.Step, 0)
        return this.parsed
    }

}
class UInputStepType implements IStepType {
    content: any
    parsed: any // json format
    current_step: number
    private next_step: number[]
    next_step_for_timeout: number[]
    constructor() {
        this.content = null
        this.parsed = null
        this.next_step = [-1, -1]
        this.next_step_for_timeout = [-1, 0]
    }
    set_content(steps) {
        this.content = steps
        this.parse()
    }
    set_next_step(step, substep) {
        this.next_step = [step, substep]
    }

    set_next_step_for_timeout(step) {
        this.next_step_for_timeout = [step, 0]
    }
    getNextStep() {
        return this.next_step
    }
    getNextStepForTimeOut() {
        return this.next_step_for_timeout
    }
    parse() {
        if (this.parsed) { return this.parsed }
        let inputExpireStep = -1
        if (this.content.data.hasOwnProperty("stepIndex")) {
            inputExpireStep = this.content.data.stepIndex
        }
        let beforeInputExpireStep = -1
        if (this.content.data.hasOwnProperty("goToIndex")) {
            beforeInputExpireStep = this.content.data.goToIndex
        }

        let typeFixer = { // check InputType data model
            'email': 'Email',
            'phone': 'PhoneNumber',
            'freeinput': 'FreeText',
            'AI_BOT': "AI_BOT"
        }
        // let regexChecker = {
        //     'email': /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
        //     'phone': /(\+\d{1,3}\s?)?((\(\d{3}\)\s?)|(\d{3})(\s|-?))(\d{3}(\s|-?))(\d{4})(\s?(([E|e]xt[:|.|]?)|x|X)(\s?\d+))?\s*$/,
        // }

        // let regexChecker = {
        //     'email': /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
        //     'phone': /^\d{1,14}$/,
        // }
        let regexChecker = {
            'email': /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
            'phone': /^[+]{0,1}[0-9]{5,14}$/,
        }


        let errorMsgMap = {
            'email': "Oops the email is not valid. Maybe you are missing @ or a .com.",
            'phone': "Please enter valid phone number"
        }

        let placeHolderMap = {
            'email': "email@example.com",
            'phone': "Enter your phone number",
            'freeinput': 'Send a message…',
            'AI_BOT': "Make your query here"
        }
        let content = this.content.data.text
        if (content) {
            content = content.trim()
        }
        let typ = this.content.data.inputType
        let botName = ""
        if (typ == "freeinput") {
            if (content.length > 6 && content.substr(0, 6) == "AI_BOT"){
                typ = "AI_BOT"
                content = content.substr(6).trim()
                let lines = content.split("\n")
                botName = lines.shift().trim()
                content = lines.join("\n")
                content = content.trim()
            }
        }

        let obj = { // Object of array from [entity/ECT.SalesChatDM: Bot2V]
            type: typeFixer[typ],
            isQuickReply: false,
            isInputReply: true,
            isTextReply: true,
            isActionReply: false,
            QReplyOptions: [],
            UInputData: "",
            textData: content,
            timeout: this.content.data.inputExpires * 1000,
            Step: beforeInputExpireStep,
            inputExpireStep: inputExpireStep,
            saveToProfile: this.content.data.saveToProfile,
            regex: regexChecker[typ],
            errorMsg: errorMsgMap[typ],
            placeHolder: placeHolderMap[typ],
            extra: botName
        }
        this.set_next_step(obj.Step, 0)
        this.set_next_step_for_timeout(obj.inputExpireStep)
        this.parsed = obj
        return obj
    }
}

 
class EscalateToAgent implements IStepType {
    content: any
    parsed: any // json format
    current_step: number
    private next_step: number[]
    constructor() {
        this.content = null
        this.parsed = null
        this.next_step = [-1, -1]
    }
    set_content(steps) {
        this.content = steps
        this.parse()
    }
    parse() {
        if (this.parsed) { return this.parsed }
        let obj = {
            type: this.content.type,
            textData: this.content.data.text.trim(),
            timeout: this.content.data.noAgentExpires
        }
        this.parsed = obj
        return obj
    }
    getNextStep() {
        return this.next_step
    }
    getNextStepForTimeOut() {
        return this.getNextStep()
    }
    set_next_step(step: any, substep: any) {

    }
}


class Parser {
    private parseASubStep(step: any) {
        switch (step.type) {
            case "Text":
                let tst = new TextStepType()
                tst.set_content(step)
                return tst
            case "QReply":
                let qst = new QReplyStepType()
                qst.set_content(step)
                return qst
            case "UInput":
                let uist = new UInputStepType()
                uist.set_content(step)
                return uist
            case "Escalate":
                let eta = new EscalateToAgent()
                eta.set_content(step)
                return eta
        }
    }

    private parseAStep(steps: any) {
        let contents = steps.contents
        let res = [];
        for (let step of contents) {
            let parsed = this.parseASubStep(step)
            if (step.type == "QReply") {
                let title = res.pop()
                parsed.parsed.textData = title.parsed.textData;
            }
            res.push(parsed)
        }
        return res;
    }

    parse(steps) {
        let res = []
        for (let step_with_substeps of steps) {
            res.push(this.parseAStep(step_with_substeps))
        }
        return res
    }
}
class NextStepDecider {
    botSteps: any;
    set_bot_steps(parsedSteps: any) {
        this.botSteps = parsedSteps
    }
    compareArrays(arr1, arr2) {
        if (arr1.length != arr2.length) { return false }
        for (let i = 0; i < arr1.length; i++) {
            if (arr1[i] != arr2[i]) { return false }
        }
        return true
    }
    private getNext(step, substep) {
        let totalNrOfSteps = this.botSteps.length
        if ((step + 1) >= totalNrOfSteps) {
            return [0, 0]
        }
        let currentStep = this.botSteps[step]
        let totnrOfSubsteps = currentStep.length
        if ((substep + 1) >= totnrOfSubsteps) {
            return [step + 1, 0]
        }
        return [step, substep + 1]
    }

    assignNextSteps() {
        for (let i = 0; i < this.botSteps.length; i++) {
            let lstep = this.botSteps[i]
            for (let j = 0; j < lstep.length; j++) {
                let lsubSubstep = lstep[j]
                let res = this.getNext(i, j)
                let gns = lsubSubstep.getNextStep()
                if (gns[0] == -1) {
                    lsubSubstep.set_next_step(res[0], res[1])
                }
                let gnsft = lsubSubstep.getNextStepForTimeOut()
                if (lsubSubstep instanceof UInputStepType && gnsft[0] == -1) {
                    lsubSubstep.set_next_step_for_timeout(res[0])
                }
            }
        }
        if (this.botSteps.length > 0) {
            this.botSteps[this.botSteps.length - 1][0].parsed.isEndStep = true
        }
    }
}
console.log("parsing steps classes")

if (this._botSteps) {
    let p = new Parser()
    let ps = p.parse(this._botSteps)
    let nsd = new NextStepDecider()
    nsd.set_bot_steps(ps)
    nsd.assignNextSteps()
    this.out = ps
} 

