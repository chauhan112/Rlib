#pragma once
#include <QString>
#include <iostream>
#include <QDebug>

struct Range {
    int left;
    int right;

    void merge(Range r){
        if(this->left > r.left) this->left = r.left;
        if(this->right > r.right) this->right = r.right;
    }

    bool intersects(Range r){
        if(r.right >= right) return r.left <= right;
        return left <= r.right;
    }

    void print() {
        qDebug() <<"("<< left << "," << right << ")";
    }

    QString string() {
        QString k;
        k = "(" + QString::number(left) + "," + QString::number(right) + ")";
        return k;
    }

    int distance(Range r){
        if(r.right >= right) return r.left - right;
        return left - r.right;
    }
};

class utils{
public:
    static QString strip(QString regex, QString word);
    static QString pathBasename(QString filepath);
    static QStringList getStringFromMaps(QString line, QVector<Range> maps);
    static bool hasPattern(QString regex, QString text);
    static QStringList filter(QString regex, QStringList l);
    static QStringList filesWithExtension(QString ext,QString path);
    static QString getFileContent(QString filename);
    static QVector<Range> getPositionSearchWithRegex(QString reg , QString text);
    static QStringList listEverythingInDir(QString path);
    static QStringList  listDirFiles(QString dirPath);
    static QString getNameWithHelpOfDialogPrompt(QWidget* instance, QString header);
    static QString join(QString, QStringList);
    static QString selectFileForReading(QWidget* instance, QString header);
};
