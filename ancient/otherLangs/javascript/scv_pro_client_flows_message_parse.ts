// SCVisitor/pro-tool/Business Logic/ClientFlows/messages/messageParser

interface IMessage {
    getContent();
    set_content(content);
    get_original_msg();
}

interface Attachment {
    id: number;
    fileSize: number;
    mimType: string;
    name: string;
    filePath: string;
    fileHandle: string;
    previewPath: string;
}

type StateNValue = { // see the model: Data/Models/model/StateNValue
    show: boolean;
    value: any;
     attachment?: Attachment 
}

type SenderDetail = {
    type:string;
    moreInfo: any;
}

type MessageComponent = { // equivalent model at: Data/Models/view/MessageComponent
    state: StateNValue;
    senderType: SenderDetail;
    time: string;
}

type CallInvitationStruct = { // equivalent model at: Data/Models/view/CallInvitationView
    active: boolean;
    roomId: string;
    show: boolean;
}

enum InformativeMessageType { // equivalent model at: CustomSC:Data/Models/enums/InformativeMessageType
    ChatHasEnded = "ChatHasEnded",
    InvitingToCall =  "InvitingToCall",
    CallCancelled = "CallCancelled",
    JoinedCall = "JoinedCall",
    RejectedCall = "RejectedCall",
    CallHasEnded= "CallHasEnded",
    CallExpired = "CallExpired"
}

type InformativeMessageComponent = { // equivalent model at: Data/Models/view/InformativeMessage
    show: boolean;
    value: string;
    type: InformativeMessageType; 
}


type UIInputDataForOneMessageElement = { // equivalent model at: Data/Models/view/OneMessageElementView
    scrollDate: StateNValue;
    message: MessageComponent;
    informative: InformativeMessageComponent;
    botMsg: StateNValue;
    callInfo: CallInvitationStruct;
}

const informativeTypeDefault = {show:false, value:"", type: InformativeMessageType.ChatHasEnded}
const stateNValueDefault = { show: false, value: "" }
const messageDefault = { state: { show: false, value: "" , attachment: null }, senderType: {type:"", moreInfo: {}}, time: "" }
const callInviteDefault: CallInvitationStruct = {active: false, roomId:"", show: false}
class Utils {
    public static getDateRelative(date) {
        let dateToday = new Date().toDateString();
        let longDateYesterday = new Date();
        longDateYesterday.setDate(new Date().getDate() - 1);
        let dateYesterday = longDateYesterday.toDateString();
        let today = dateToday.slice(0, dateToday.length - 5);
        let yesterday = dateYesterday.slice(0, dateToday.length - 5);

        const wholeDate = new Date(date).toDateString();

        const wholeDateComma = wholeDate.toString().replace(/(?<=\d) /, ", ");

        let messageDateString = wholeDate.slice(4, wholeDate.length - 5);


        if (new Date(date).getFullYear() === new Date().getFullYear()) {
            if (messageDateString === today) {
                return "Today";
            } else if (messageDateString === yesterday) {
                return "Yesterday";
            } else {
                return messageDateString;
            }
        } else {
            return wholeDateComma;
        }
    }
    public static clockTime(date) {
        var today = new Date(date);
        var hours = today.getHours()
        var ampm = hours >= 12 ? ' PM' : ' AM';
        hours = hours % 12;
        hours = hours ? hours : 12;
        var hh = String(hours);
        var min = String(today.getMinutes()).padStart(2, '0');
        return hh + ':' + min + ampm;
    }
    public static get_user_with_id(userId, users){
        if (userId){
            for (let user of users){
                if (user.id == userId && user.nickName) return user.nickName
            }
        }
        return "A"
    }
}

class TextMessage implements IMessage {
    crude_content: any;
    parsed_obj: UIInputDataForOneMessageElement | "";
    users: any;
    constructor() {
        this.parsed_obj = "";
    }
    set_users(users){
        this.users = users
    }
    set_content(content) {
        this.crude_content = content
    }
    getContent() {
        if (this.parsed_obj !== "") {
            return this.parsed_obj
        }
        this.parsed_obj = {
            scrollDate: { ...stateNValueDefault },
            informative: { ...informativeTypeDefault },
            botMsg: { show: false, value: {} },
            message: {
                state: { show: true, value: this.crude_content.message, attachment: this.crude_content.attachment },            
                senderType: {type: this.crude_content.senderType, moreInfo: {name: Utils.get_user_with_id(this.crude_content.senderId, this.users)}},
                time: Utils.clockTime(this.crude_content.messageSentTime)
            },
            callInfo: {...callInviteDefault}
        };

        return this.parsed_obj
    }
    get_original_msg() { return this.crude_content }
    
}

class BotMessage implements IMessage {
    crude_content: any;
    parsed_obj: UIInputDataForOneMessageElement | "";
    constructor() {
        this.parsed_obj = "";
    }
    set_content(content) {
        this.crude_content = content
    }
    getContent() {
        if (this.parsed_obj !== "") {
            return this.parsed_obj
        }
        let parsed_content = JSON.parse(this.crude_content.message)
        this.parsed_obj = { scrollDate: { ...stateNValueDefault }, informative: { ...informativeTypeDefault }, botMsg: { show: false, value: {} },
            message: { 
                state: { show: false, value: "" }, 
                senderType: {type: this.crude_content.senderType, moreInfo: {name:"BOT"}},
                time: Utils.clockTime(this.crude_content.messageSentTime) 
            },
            callInfo: {...callInviteDefault}
        };
        
        if (parsed_content.hasOwnProperty("isEndStep")){
            this.parsed_obj.informative = {show: true, value: parsed_content.textData, type: InformativeMessageType.ChatHasEnded}
        }else if (parsed_content.type === "Text" || parsed_content.type === "Email" || parsed_content.type === "PhoneNumber" || parsed_content.type === "FreeText"
                        || parsed_content.type === "Escalate" || parsed_content.type === "AI_BOT" ){ 
            this.parsed_obj.message.state = {show:true, value: parsed_content.textData}
        }else if (parsed_content.type === "QReply"){
            this.parsed_obj.botMsg = { show: false, value: parsed_content.QReplyOptions } // false because only last quick reply needs to be activated
            this.parsed_obj.message.state = {show:true, value: parsed_content.textData}
        }
        
        return this.parsed_obj
    }

    
    get_original_msg() { return this.crude_content }

}

class CallInvitationMessge implements IMessage{
    crude_content: any;
    parsed_obj: UIInputDataForOneMessageElement | "";
    users: any;
    constructor() {
        this.parsed_obj = "";
    }
    set_users(users){
        this.users = users
    }
    getContent() {
        if (this.parsed_obj !== "") {
            return this.parsed_obj
        }
        let msg = new TextMessage()
        msg.set_content(this.crude_content)
        msg.set_users(this.users)
        this.parsed_obj = msg.getContent()
        this.parsed_obj.callInfo.active = !this.hasExired(this.crude_content.messageSentTime)
        this.parsed_obj.callInfo.roomId = this.crude_content.roomId
        this.parsed_obj.callInfo.show = true
        this.parsed_obj.message.state.show = false
        this.parsed_obj.message.state.attachment = null
        this.parsed_obj.message.senderType.type = "USER"
        return this.parsed_obj;
    }
    private hasExired(time:string): boolean { 
        let nowTime = new Date();
        let messageTime = new Date(time);
        return (nowTime.getTime() - messageTime.getTime() > 5*60*1000)
    }
    set_content(content: any) {
        this.crude_content = content;
    }
    get_original_msg() {
        return this.crude_content;
    }
    get_informative_part(){
        let msg = new InformativeMessage()
        msg.set_content(this.crude_content)
        let obj = msg.getContent()
        obj.informative.value = Utils.get_user_with_id(this.crude_content.senderId, this.users) + " is inviting you to a call";
        return msg;
    }
    deactivate(){
        let val = this.getContent()
        val.callInfo.active = false;
    }

}

class InformativeMessage implements IMessage {
    crude_content: any;
    parsed_obj: UIInputDataForOneMessageElement | "";
    roomId: string;
    constructor() {
        this.parsed_obj = "";
    }
    set_content(content) {
        this.crude_content = content
    }
    getContent() {
        if (this.parsed_obj !== "") {
            return this.parsed_obj
        }
        this.roomId = "";
        let show = this.crude_content.informativeMessageId === "CONVERSATION_CLOSED";
        let msg = ""
        let info = this.crude_content.informativeMessage
        let typ = InformativeMessageType.ChatHasEnded
        if (this.crude_content.informativeMessageId === "CONVERSATION_CLOSED"){
            show = true
            msg = "This conversation has ended"
        }else if(this.crude_content.informativeMessageId === "CONVERSATION_ASSIGNED"){
            show = true
            msg = info.assignToUser + " joined the conversation"
        }else if (this.crude_content.informativeMessageId === "CALL_REJECTED_VISITOR"){
            show = true
            typ = InformativeMessageType.RejectedCall;
            msg = "You rejected the call at " + Utils.clockTime(this.crude_content.messageSentTime)
            this.roomId = this.crude_content.roomId
        }else if (this.crude_content.informativeMessageId === "CALL_INVITATION_VISITOR"){
            show = true
            typ = InformativeMessageType.InvitingToCall;
        }else if (this.crude_content.informativeMessageId === "CALL_JOINED_VISITOR"){
            show = true
            msg = "You joined the call at " + Utils.clockTime(this.crude_content.messageSentTime)
            typ = InformativeMessageType.JoinedCall;
            this.roomId = this.crude_content.roomId
        }else if (this.crude_content.informativeMessageId === "CALL_ENDED_VISITOR" || this.crude_content.informativeMessageId === "CALL_ENDED_AGENT"){
            show = true
            msg = "The call ended at " + Utils.clockTime(this.crude_content.messageSentTime)
            typ = InformativeMessageType.CallHasEnded;
            this.roomId = this.crude_content.roomId
        }else if (this.crude_content.informativeMessageId === "CALL_INVITATION_EXPIREDVISITOR"){ 
            show = true
            msg = "The call invitation expired"
            typ = InformativeMessageType.CallExpired;
            this.roomId = this.crude_content.roomId
        }   
        this.parsed_obj = {
            scrollDate: { ...stateNValueDefault },
            informative: { show: show, value: msg, type: typ},
            botMsg: { show: false, value: {} },
            message: { ...messageDefault },
            callInfo: {...callInviteDefault}
        };
        return this.parsed_obj
    }
    get_original_msg() { return this.crude_content }
    get_room_id() { return this.roomId }
}

class ParsedMessages {
    users: any;
    session_name: any;
    set_users(users){
        this.users = users
    }
    parse(crude_messages) {
        let res: IMessage[] = []
        let updatingMessages = {}
        let lastInvited  = ""
        
        for (let i = 0; i < crude_messages.length; i++) {
            let msg = crude_messages[i]
            if (msg.senderType == "BOT") {
                let msgParsed = new BotMessage()
                msgParsed.set_content(msg)
                res.push(msgParsed)
            } else if (msg.informativeMessageId == "CALL_INVITATION_VISITOR"){
                let a = new CallInvitationMessge()
                a.set_users(this.users)
                a.set_content(msg)
                let invite = a.get_informative_part()
                let cont = a.getContent()
                if (cont.callInfo.roomId) {
                    updatingMessages[cont.callInfo.roomId] = cont;
                }else cont.callInfo.active = false;
                lastInvited = cont.callInfo.roomId
                res.push(invite)
                res.push(a)
            } else if (msg.senderType == "INFORMATIVE") {
                let msgParsed = new InformativeMessage()
                msgParsed.set_content(msg)
                msgParsed.getContent()
                let rmid = msgParsed.get_room_id()
                if (rmid && updatingMessages.hasOwnProperty(rmid)){
                    updatingMessages[rmid].callInfo.active = false;
                }
                res.push(msgParsed)
            } else {
                let a = new TextMessage()
                a.set_users(this.users)
                a.set_content(msg)
                res.push(a)
            }
        }

        this.only_activate_last_call_invite(updatingMessages, lastInvited)
        let out = this.add_scroll_time(res)
        if (out.length > 0 ){
            let lastEntry: UIInputDataForOneMessageElement = out[out.length-1]
            if (lastEntry.botMsg.value.hasOwnProperty('length') && this.session_name === "BotRunningSession"){
                lastEntry.botMsg.show = true
            }
        }
        return this.filterInactiveMessage(out)
    }
    private only_activate_last_call_invite(updatingMessages, lastInvited){
        for (let rmId in updatingMessages) {
            let val = updatingMessages[rmId]
            if (lastInvited !== rmId){
                val.callInfo.active = false;
            }
        }
    }

    add_scroll_time(msgs: IMessage[]) {
        let first = true;
        var date, lastDate = "";
        let res: UIInputDataForOneMessageElement[] = []
        for (let i = 0; i < msgs.length; i++) {
            let msg = msgs[i]
            date = Utils.getDateRelative(msg.get_original_msg().messageSentTime)
            let uidata: UIInputDataForOneMessageElement = msg.getContent()
            if (first) {
                uidata.scrollDate.show = true
                uidata.scrollDate.value = date
                lastDate = date
                first = false
                res.push(uidata)
                continue
            }
            if (lastDate != date) {
                uidata.scrollDate.show = true
                uidata.scrollDate.value = date
                lastDate = date
            }
            res.push(uidata)

        } 
        return res
    }

    filterInactiveMessage(msgs: UIInputDataForOneMessageElement[]){
        let res: UIInputDataForOneMessageElement[] = []
        for (let i = 0; i < msgs.length; i++) {
            let ele = msgs[i]
            if(ele.botMsg.show || ele.message.state.show || ele.informative.show || ele.scrollDate.show|| ele.callInfo.show ){
                res.push(ele)
            }
        }
        return res
    }

    set_session_name(session){
        this.session_name = session
    }
}

console.log("parsing the messages")
let pm = new ParsedMessages();
pm.set_users(this.users)
pm.set_session_name(this._state)
this.out = pm.parse(this._crudeMsg) 