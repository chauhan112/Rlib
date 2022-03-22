#ifndef MYTABLE_H
#define MYTABLE_H
#include <QTableView>
#include <QStandardItemModel>

class MyTable
{
public:
    MyTable();
    ~MyTable();
    void setHeaders(QStringList arr);
    void addRows(QList<QStringList> arrayOfRows);
    void addRow(QStringList row);
    static QStringList data(int rowNr);
    static QStringList data();
    static QList<QStringList> datas();
    static QList<QStringList> datas(int totalRowNr);
    QTableView* getWidget();
public:
    QTableView table;
    QStandardItemModel model;
    int colNr = -1;

};

#endif // MYTABLE_H
