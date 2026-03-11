import sys
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from db_connect import db, cursor

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('sneaker_shop.ui', self)
    self.id = 0

    self.sneakers_shop.setColumnWidth(0, 50)
    self.sneakers_shop.setColumnWidth(1, 150)
    self.sneakers_shop.setColumnWidth(2, 150)
    self.sneakers_shop.setColumnWidth(3, 100)
    self.sneakers_shop.setColumnWidth(4, 180)

    self.show_all_sneakers()
    self.btn_add.clicked.connect(self.insert_sneakers)
    self.sneakers_shop.cellClicked.connect(self.selected_row)
    self.btn_update.clicked.connect(self.update_sneakers)
    self.btn_delete.clicked.connect(self.delete_sneakers)
    self.btn_clear.clicked.connect(self.clear)
    self.btn_search.clicked.connect(self.search_sneakers)

  def insert_sneakers(self):
    brand = self.txt_brand.text()
    name = self.txt_name.text()
    year = (self.txt_year.text())
    price = (self.txt_price.text())

    sql = 'insert into sneakers(brand, name, year, price) values(?, ?, ?, ?)'
    values = (brand, name, year, price)

    rs = cursor.execute(sql, values)
    db.commit()
    if rs.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Insert sneakers successful!')
      self.show_all_sneakers()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to insert sneakers!')

    self.clear()

  def show_sneakers(self, sneakers):
      n = len(sneakers)
      self.sneakers_shop.setRowCount(n)
      row = 0
      for sneaker in sneakers: 
        self.sneakers_shop.setItem(row, 0, QTableWidgetItem(str(sneaker[0])))
        self.sneakers_shop.setItem(row, 1, QTableWidgetItem(sneaker[1]))
        self.sneakers_shop.setItem(row, 2, QTableWidgetItem(sneaker[2]))
        self.sneakers_shop.setItem(row, 3, QTableWidgetItem(str(sneaker[3])))
        self.sneakers_shop.setItem(row, 4, QTableWidgetItem(str(sneaker[4])))

        row +=1
  def show_all_sneakers(self):
        sql = 'select * from sneakers'
        sneakers = cursor.execute(sql).fetchall()

        self.show_sneakers(sneakers)

  def selected_row(self):
    row = self.sneakers_shop.currentRow()
    self.id = self.sneakers_shop.item(row, 0).text()
    self.txt_brand.setText(self.sneakers_shop.item(row, 1).text())
    self.txt_name.setText(self.sneakers_shop.item(row, 2).text())
    self.txt_year.setText(self.sneakers_shop.item(row, 3).text())
    self.txt_price.setText(self.sneakers_shop.item(row, 4).text())

    self.btn_update.setEnabled(True)
    self.btn_delete.setEnabled(True)
    self.btn_add.setEnabled(False)

    self.txt_brand.setEnabled(False)
    self.txt_name.setEnabled(False)
    self.txt_year.setEnabled(False)

  def update_sneakers(self):
    price = int(self.txt_price.text())
    sql = 'update sneakers set Price = ? where id = ?'
    values = (price, self.id)

    row = cursor.execute(sql, values)
    db.commit()

    if row.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Update sneakers successful!')
      self.show_all_sneakers()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to update sneakers!')
    self.clear()

  def delete_sneakers(self):
    sql = 'delete from sneakers where id = ?'
    values = (self.id, )

    row = cursor.execute(sql, values)
    db.commit()

    if row.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Delete sneakers successful!')
      self.show_all_sneakers()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to delete sneakers!')
    self.clear()

  def clear(self):
    self.txt_brand.setText('')
    self.txt_name.setText('')
    self.txt_year.setText('')
    self.txt_price.setText('')
    
    self.txt_brand.setEnabled(True)
    self.txt_name.setEnabled(True)
    self.txt_year.setEnabled(True)

    self.sneakers_shop.clearSelection()

    self.btn_add.setEnabled(True)
    self.btn_update.setEnabled(False)
    self.btn_delete.setEnabled(False)

    self.show_all_sneakers()

  def search_sneakers(self):
    name = self.txt_search.text()
    sql = 'select * from sneakers where brand like ?'
    values = (f'%{name}%', )

    sneakers = cursor.execute(sql, values).fetchall()
    self.show_sneakers(sneakers)

    self.txt_search.setText('')

  def show_all_sneakers(self):
    sql = 'select * from sneakers'
    sneakers = cursor.execute(sql).fetchall()

    self.show_sneakers(sneakers)


if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()

