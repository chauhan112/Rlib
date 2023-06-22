#include <QVBoxLayout>
#include <QApplication>
#include "mytable.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QWidget w;
    w.setLayout(new QVBoxLayout);

    MyTable tab;
    tab.setHeaders(MyTable::data());
    tab.addRows(MyTable::datas());

    w.layout()->addWidget(tab.getWidget());
    w.show();
    return a.exec();
}
