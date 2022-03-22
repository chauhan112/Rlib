class StringDB{
    companion object{
        fun regSearch(regex:String, content:String):MutableList<String>{
            val matches = Regex(regex).findAll(content)
            return matches.map { it.value}.toMutableList()
        }
        fun tokenize(content:String):MutableList<String>{
            return StringDB.regSearch("\\w+", content)
        }
        fun split(regex:String, content:String):MutableList<String>{
            val separate1 = content.split(regex.toRegex()).map { it.trim() }
            return separate1.toMutableList()
        }
    }
}