import java.io.File

class PathDB{
    companion object{
        fun listDir(dirname:String, fileTyp:String=".", walk:Boolean=true):MutableList<String>{
            var res:MutableList<String> = mutableListOf<String>()
            if(!walk){
                File(dirname).listFiles().asList().forEach { res.add(it.toString())}
            }else{
                var dirs= File(dirname).walkTopDown()
                for (item in dirs){
                    res.add(item.toString())
                }
            }
            if(fileTyp != "."){
                var rs= res.filter { it.lowercase().endsWith("."+fileTyp)}
                res = rs.toMutableList()
            }
            return res
        }
        fun join(arr:MutableList<String>):String{
            return arr.joinToString(File.separator)
        }
        fun dirname(name:String):String{
            return File(name).parent
        }
        fun basename(name:String):String{
            return File(name).name
        }
    }
}