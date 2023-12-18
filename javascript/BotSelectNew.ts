interface IFilterBot {
    apply(bots: any[]): any;
}
class ActiveBots implements IFilterBot {
    apply(bots: any[]) {
        let res: any[] = []
        for (let bot of bots) {
            if (bot.status === "ACTIVE") res.push(bot)
        }
        return res
    }
}
class BotSkipper implements IFilterBot {
    skipping_bots: number[] = []

    apply(bots: any[]) {
        let res: any[] = []
        for (let bot of bots) {
            if (this.skipping_bots.indexOf(bot.id) === -1) res.push(bot)
        }
        return res
    }
    set_skipping_bots(bots: number[]) {
        this.skipping_bots = bots
    }
}
class OnceInteractedNeverRunAgainBot implements IFilterBot {
    botStatus: any = {};

    apply(bots: any[]) {
        let res: any[] = []
        for (let bot of bots) {
            if (bot.schedule.frequency === "AllTime") {
                let botInfo = this.botStatus["" + bot.id]
                if (!botInfo) {
                    res.push(bot)
                } else if (botInfo && !botInfo.interacted) {
                    res.push(bot)
                }
            }
        }
        return res
    }
    set_bot_status(botStatus: any) {
        this.botStatus = botStatus
    }
}
class EveryFixedIntervalRunningBot implements IFilterBot {
    botStatus: any;
    interval: number;
    apply(bots: any[]) {
        let res: any[] = []
        for (let bot of bots) {
            if (bot.schedule.frequency === "Every2Hours") {
                let botInfo = this.botStatus["" + bot.id]
                if (!botInfo){
                    res.push(bot)
                }else if (this.get_time_difference(botInfo.startedTime) >= this.interval) {
                    res.push(bot)
                }else if (!botInfo.interacted) {
                    res.push(bot)
                }
            }
        }
        return res
    }
    private get_time_difference(dateAndTime: string): number {
        let date = new Date(dateAndTime)
        let now = new Date()
        return Math.abs(date.getTime() - now.getTime())
    }
    set_bot_status(botStatus: any) {
        this.botStatus = botStatus
    }
    set_time_interval(timeInMiliSec: number) {
        this.interval = timeInMiliSec
    }
}
class OnceStartedNeverRunAgainBot implements IFilterBot {
    botStatus: any = {};

    apply(bots: any[]) {
        let res: any[] = []
        for (let bot of bots) {
            if (bot.schedule.frequency === "OneTime") {
                let botInfo = this.botStatus["" + bot.id]
                if (!botInfo) {
                    res.push(bot)
                }
            }
        }
        return res
    }
    set_bots_status(status: any) {
        this.botStatus = status
    }
}
class BotFrequencyCondition implements IFilterBot {
    filters: any[] = [];
    apply(bots: any[]) {
        let res: any[] = []
        for (let filter of this.filters) {
            res = res.concat(filter.apply(bots))
        }
        return res
    }
    add_filter(filter: any) {
        this.filters.push(filter)
    }
}
class TriggerFilteringCondition implements IFilterBot {
    visitorInfo: any;
    remainingTimeSpent: number = 0;
    apply(bots: any[]) {
        return this.timespent_on_url_condition(
            this.current_page_url(
                this.filter_for_visits(bots)
            )
        )
    }
    private filter_for_visits(bots: any[]) {
        let totalVisits = this.visitorInfo.totalVisits
        let res: any[] = []
        for (let bot of bots) {
            if (bot.triggers.selectedCondition.indexOf("Total Visits on URL") === -1) {
                res.push(bot)
                continue
            }
            let visitCountDefined = bot.triggers.totalVisits.times
            if (bot.triggers.totalVisits.rule == "more than" && totalVisits > visitCountDefined) {
                res.push(bot)
            } else if (bot.triggers.totalVisits.rule == "less than" && totalVisits < visitCountDefined) {
                res.push(bot)
            }

        }
        return res
    }

    private timespent_on_url_condition(bots: any[]) {
        let res: any[] = []
        for (let bot of bots) {
            if (bot.triggers.selectedCondition.indexOf("Time Spent on URL") === -1) {
                res.push(bot)
                continue
            }
            let timeSpentUnitDefined = bot.triggers.timeSpent.unit
            let timeSpentValueDefined = bot.triggers.timeSpent.value
            let currentUserTimeSpent = this.visitorInfo.timespent
            this.update_timespent(timeSpentValueDefined - currentUserTimeSpent)
            if (timeSpentUnitDefined == "seconds" && currentUserTimeSpent > timeSpentValueDefined) {
                res.push(bot)
            } else if (timeSpentUnitDefined == "minutes") {
                let timeInMinutes = currentUserTimeSpent / 60
                this.update_timespent((timeSpentValueDefined - timeInMinutes) * 60)
                if (timeInMinutes > timeSpentValueDefined) {
                    res.push(bot)
                }
            } else if (timeSpentUnitDefined == "hours") {
                let convertToHour = currentUserTimeSpent / 3600 
                this.update_timespent((timeSpentValueDefined - convertToHour) * 3600)
                if (convertToHour > timeSpentValueDefined) {
                    res.push(bot)
                }
            }
        }
        return res
    }

    private current_page_url(bots: any[]) {
        let res: any[] = []
        let pageUrl = this.visitorInfo.pageUrl
        for (let bot of bots) {
            if (bot.triggers.selectedCondition.indexOf("Current Page URL") === -1) {
                res.push(bot)
                continue
            }
            for (let page of bot.triggers.currentPage) {
                if (page.rule === "is" && page.url === pageUrl) {
                    res.push(bot)
                } else if (page.rule === "contains" && pageUrl.includes(page.url)) {
                    res.push(bot)
                } else if (page.rule === "starts with" && pageUrl.startsWith(page.url)) {
                    res.push(bot)
                }
            }
        }
        return res
    }

    set_visitor_info(visitorInfo: any) {
        this.visitorInfo = visitorInfo
    }
    private update_timespent(timeInSec: number) {
        if (timeInSec < this.remainingTimeSpent || this.remainingTimeSpent === 0) {
            this.remainingTimeSpent = timeInSec
        }
    }
}
class BotShowingWithDateCondition implements IFilterBot {
    apply(bots: any[]) {
        let res: any[] = []
        for (let bot of bots) {
            if (bot.schedule.stopShowing === "Never") {
                res.push(bot)
            } else {
                let currentDate = new Date();
                let givenDate = new Date(bot.schedule.dateAndTime)
                if (currentDate < givenDate) {
                    res.push(bot)
                }
            }
        }
        return res
    }
}
class BusinessHoursCondition implements IFilterBot {
    businessHoursInfo: boolean;
    apply(bots: any[]) {
        let res: any[] = []
        for (let bot of bots) {
            if (bot.schedule.showBot === "Always") {
                res.push(bot)
            } else if (bot.schedule.showBot === "During business hours") {
                if (this.businessHoursInfo) {
                    res.push(bot)
                }
            } else if (bot.schedule.showBot === "Outside business hours") {
                if (!this.businessHoursInfo) {
                    res.push(bot)
                }
            }
        }
        return res
    }
    set_business_hours(businessHoursInfo: boolean) {
        this.businessHoursInfo = businessHoursInfo
    }

}
class BotSelector {
    bots: any[];
    filters: IFilterBot[]= [];
    constructor(bots: any[]) {
        this.bots = bots
    }

    get_available_bot() {
        let filteredBots = this.bots;
        for (let filter of this.filters) {
            filteredBots = filter.apply(filteredBots)
        }
        return filteredBots.sort((a, b) => (a.priority - b.priority))
    }

    add_filter(filter: IFilterBot) {
        this.filters.push(filter)
    }
}
class Main{
    public static get_bot_selector(bots:any[], botStatus: any, isInBussinessHr: boolean, timeSpent: number, currentUrl: string, 
            visitorSession: any, timeLimit: number): [BotSelector, TriggerFilteringCondition] {
        let bs = new BotSelector(bots)

        bs.add_filter(new ActiveBots())
        
        let bfc = new BotFrequencyCondition()
        let efirb = new EveryFixedIntervalRunningBot();
        efirb.set_bot_status(botStatus)
        efirb.set_time_interval(timeLimit)
        let osnrab = new OnceStartedNeverRunAgainBot();
        osnrab.set_bots_status(botStatus)
        let oinrab = new OnceInteractedNeverRunAgainBot();
        oinrab.set_bot_status(botStatus)
        
        bfc.add_filter(efirb)
        bfc.add_filter(osnrab)
        bfc.add_filter(oinrab)
        bs.add_filter(bfc)
        
        let bhc = new BusinessHoursCondition()
        bhc.set_business_hours(isInBussinessHr)
        bs.add_filter(bhc)
        
        let tfc = new TriggerFilteringCondition()
        let visitor = { ...visitorSession, timespent:  timeSpent / 1000, pageUrl: currentUrl }
        tfc.set_visitor_info(visitor)
        bs.add_filter(tfc)
        
        bs.add_filter(new BotShowingWithDateCondition())
        
        return [bs, tfc]
    }

}

console.log("selecting a bot...")
let [bs, tfc] = Main.get_bot_selector($this.bots, $this._botsStatus, $this.isInBussinessHr, $this._timeSpent, $this._currentPageUrl, $this.visitorSession, $this._timeLimit)
let res = bs.get_available_bot()
$this.userType = "Agent"
$this.remTriggerTime = tfc.remainingTimeSpent
if (res.length > 0) {
    $this.botId = res[0].id
    $this.userType = "Bot"
}

