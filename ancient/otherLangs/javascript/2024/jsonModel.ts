class LocalStorageJSONModel {
    key: string = "LocalStorageModel";
    data: any;
    constructor() {
        this.data = this.readFormStorage()
    }
    addEntry(location: string[], value: any) {
        let x = this.data
        for (let i = 0; i < location.length; i++) {
            let key = location[i]
            if (!x.hasOwnProperty(key)) {
                let data;
                data = {}
                if (i == (location.length - 1)) data = value
                x[key] = data
            }
            x = x[key]
        }
        this.writeToStorage()
    }
    deleteEntry(location: string[]) {
        let newLoc = location.slice(0, location.length - 1)
        let data = this.readEntry(newLoc)
        let lastKey = location[location.length - 1]
        delete data[lastKey]
        this.writeToStorage()
    }
    updateEntry(location: string[], value: any) {
        let newLoc = [...location];
        let lastKey = newLoc.pop();
        let vals = this.readEntry(newLoc);
        vals[lastKey] = value;
        this.writeToStorage();
    }
    readEntry(location: string[]) {
        let x = this.data
        for (let i = 0; i < location.length; i++) {
            let key = location[i]
            x = x[key]
        }
        return x
    }
    private readFormStorage() {
        let x = localStorage.getItem(this.key);
        if (x) return JSON.parse(x)
        return {}
    }
    private writeToStorage() {
        localStorage.setItem(this.key, JSON.stringify(this.data))
    }
    get_keys(location: string[]){
        return Object.keys(this.readEntry(location))
    }
    exists(location: string[]){
        try{
            let val = this.readEntry(location)
            return true
        }catch{ 
            return false
        }
    }
}