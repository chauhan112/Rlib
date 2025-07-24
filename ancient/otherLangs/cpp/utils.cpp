#include "utils.h"
#include <QString>
#include <QDebug>
#include <QTextStream>
#include <QFile>
#include <QDirIterator>
#include <QRegularExpression>
#include <QFileDialog>

QString utils::getFileContent(QString filename){
    QString text;
    QFile file(filename);
    if(!file.open(QFile::ReadOnly | QFile::Text)){
        qDebug() << "cant open file";
        return text;
    }
    QTextStream in(&file);
    text = in.readAll();
    return text;
}

QStringList utils::listEverythingInDir(QString path){
    QStringList lists ;
    QDirIterator it(path, QDirIterator::Subdirectories);
    while (it.hasNext()) {
        lists.push_back(it.next());
    }
    return lists;
}

QVector<Range> utils::getPositionSearchWithRegex(QString reg , QString text){
    QRegExp rx( "("+ reg+ ")");
    QStringList list;
    int pos = 0;
    QVector<Range> k;
    while ((pos = rx.indexIn(text, pos)) != -1) {
        int wordSize =rx.matchedLength();
        Range temp{pos, pos + wordSize};
        pos += wordSize;
        k.push_back(temp);
    }
    return k;
}

QStringList  utils::listDirFiles(QString dirPath){
    QDir directory(dirPath);
    QStringList files = directory.entryList(QStringList() << "*.*" ,QDir::Files);
    for (int i = 0; i < files.size(); i++) {
        files[i].push_front(dirPath + "/");
    }
    return files;
}

QStringList utils::filesWithExtension(QString ext, QString path){
    QStringList files;
    QStringList allFiles = utils::listDirFiles(path);
    if(ext[0] != ".") ext.prepend('.');

    for (int i = 0; i < allFiles.size(); i++) {
        QString file = allFiles[i];

        if(file.endsWith(ext)) files.push_back(file);

    }
    return files;
}

QStringList utils::filter(QString regex, QStringList l){
    QStringList r;

    foreach (QString k, l) {
        if(utils::hasPattern(regex, k))
            r.push_back(k);
    }
    return r;
}

bool utils::hasPattern(QString reg, QString text){
    QRegularExpression re(reg);
    QRegularExpressionMatch match = re.match(text);
    return match.hasMatch();
}

QStringList utils::getStringFromMaps(QString line, QVector<Range> maps){
    QStringList rresult;
    foreach (Range r, maps) {
        int s = r.right - r.left;
        rresult.push_back(line.mid(r.left, s));
    }
    return rresult;
}

QString utils::pathBasename(QString filepath){
    QStringList lists = filepath.split("/");
    if(lists.length() == 0) return "";
    return lists[lists.length()-1];
}

QString utils::strip(QString regex, QString word){
    word = word.remove(QRegExp("^((" + regex+ ")+)"));
    word = word.remove(QRegExp("((" + regex+ ")+)$"));
    return word;
}

QString utils::getNameWithHelpOfDialogPrompt(QWidget* instance, QString header){
    QString name = QFileDialog::getSaveFileName(instance, header, "", "All Files (*)");
    return name;
}

QString utils::selectFileForReading(QWidget* instance, QString header){
    QString name = QFileDialog::getOpenFileName(instance,header,"", "All Files (*)");
    return name;
}

QString utils::join(QString connector, QStringList l){
    QString r ="";
    bool first = true;
    foreach (QString val, l) {
        if(first){
            r += val;
            first = false;
            continue;
        }
        r += connector + val;
    }
    return r;
}
