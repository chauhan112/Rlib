import java.io.File
class FileDB{
    companion object{
        fun createFile(name:String, content:String=""){ 
            var file = File(name) 
            file.writeText(content)
        } 
        fun getFileContent(name:String) :String {
            return File(name).inputStream().readBytes().toString(Charsets.UTF_8)
        }
        fun rename(oldName:String, newName:String):Boolean{
            var oldFile = File(oldName)
            var newFile = File(newName)
            return oldFile.renameTo(newFile)
        }
        fun size(name:String): Long{
            return File(name).length()
        }
        fun delete(fileOrfolder:String) {
            File(fileOrfolder).deleteRecursively()
        }
    }
}
