 class ListDBJs {
    static checkFileExistence(fileName, fileList) {
        for (let i = 0; i < fileList.length; i++) {
            if (fileList[i] === fileName) {
                return true;
            }
        }
        return false;
    }
}
