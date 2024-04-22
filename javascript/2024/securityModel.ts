 
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
    values(){
        let res = []
        for (let member in this.data){
            res.push(this.data[member])
        }
        return res
    }
}

class SecurityGroupModel {
    key = "securityGroups"
    model: HashMapDataStructure = new HashMapDataStructure();
    read(){
        let x = localStorage.getItem(this.key)
        if (!x) {
            this.model.data = {}
        } else { this.model.data = JSON.parse(x) }
        return this.model.values() 
    }
    overwrite(id, value){
        value.id = id
        this.model.add(id, value, true)
        localStorage.setItem(this.key, JSON.stringify(this.model.data)) 
    } 
    create(value){
        this.overwrite((new Date()).getTime(), value)
    }
    read_with_id(id){
        return this.model.read(id)
    }
    delete_security(id){
        this.model.deleteKey(id)
        localStorage.setItem(this.key, JSON.stringify(this.model.data))  
    }
} 