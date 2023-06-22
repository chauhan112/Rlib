#include "mytable.h"
#include <QTableView>
#include <QStandardItemModel>

MyTable::MyTable()
{
    table.setModel(&model);
}

void MyTable::setHeaders(QStringList arr){
    for(int i =0 ; i < arr.size(); i++){
        model.setHorizontalHeaderItem(i, new QStandardItem(arr[0]));
    }
}

MyTable::~MyTable(){

}

void MyTable::addRows(QList<QStringList> listOfRows){
    for(int i =0 ; i < listOfRows.size(); i++)
        addRow(listOfRows[i]);
}

void MyTable::addRow(QStringList row){
    int size = row.size();
    if(colNr == -1) colNr = size;
    if(size != colNr)
        throw "Inconsistent row size";
    QList<QStandardItem *> items;
    for (int j = 0; j < row.size(); j++) {
        items.append(new QStandardItem(row[j]));
    }
    model.appendRow(items);
}

QTableView* MyTable::getWidget(){
    return &table;
}

QStringList MyTable::data(int rowNr){
    QString format = "item(%1,%2)";
    if(rowNr == -1)
        format = "item%1\nitem%2";
    QStringList arr;
    for (int j = 0; j < 9; j++) {
        arr.append(format.arg(rowNr).arg(j));
    }
    return arr;
}

QStringList MyTable::data(){
    return data(-1);
}

QList<QStringList> MyTable::datas(){
    return datas(10);
}

QList<QStringList> MyTable::datas(int totalRows){
    QList<QStringList> arr;
    for (int j = 0; j < totalRows; j++) {
        arr.append(data(j));
    }
    return arr;
}
