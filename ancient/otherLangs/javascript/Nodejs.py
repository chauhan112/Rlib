from Path import Path
from FileDatabase import File
import os
from WordDB import WordDB
from ListDB import ListDB
class Nodejs:
    def createNodejsFolderStructure(path = None):
        nodejs_folder_structure = ['routes',
            'middlewares',
            'modules',
            'node_modules',
            {'public': ['javascripts', 'stylesheets', 'images']},
            'views']
        nodejsFiles = ['app.js', {'public':'index.html'}]
        if(path is None):
            path ="unnamed"
        Path.createFolderStructure({os.path.basename(path):nodejs_folder_structure})
        File.createFileStructure(nodejsFiles, path)

    def basicInstall():
        print("npm install express")
        print("npm install -D nodemon")
        print("add to script in the package.json 'dev':'nodemon *.js'")
        print("npm run dev")

    def helloWorldExpress():
        lines = ["const express = require('express')",
            "const app = express()","const port = 3000",
            "app.get('/', (req, res) => res.send('<h1>Hello World!</h1>'))",
            "app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))"]
        for line in lines:
            print(line)

    def syntax(word=None):
        from Database import Database
        synts = {
            'import path' : "const path = require('path')",
            'run dev' : "npm run dev",
            "serve static page": """app.use(express.static("./websockets"));"""
        }
        return Database.dbSearch(Database.dicDB(synts), word)
