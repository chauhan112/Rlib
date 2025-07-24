class JFileDB:
    def getCodeToCreateFile():
        print( """
            public void createFile(filename, content) {
                FileOutputStream fos = new FileOutputStream(filename);
                fos.write(content.getBytes());
                fos.flush();
                fos.close();
            }
        """)
    
    def getFileContent():
        print("String content = Files.readString(path, StandardCharsets.US_ASCII);")