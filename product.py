import mysql.connector as mc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(821, 521)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Labels
        self.no = QtWidgets.QLabel(self.centralwidget)
        self.no.setGeometry(QtCore.QRect(40, 30, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.no.setFont(font)
        self.no.setText("NO")
        self.Barkode = QtWidgets.QLabel(self.centralwidget)
        self.Barkode.setGeometry(QtCore.QRect(40, 60, 51, 21))
        self.Barkode.setFont(font)
        self.Barkode.setText("Barkode")
        self.Nama = QtWidgets.QLabel(self.centralwidget)
        self.Nama.setGeometry(QtCore.QRect(40, 90, 41, 21))
        self.Nama.setFont(font)
        self.Nama.setText("Nama")
        self.Qty = QtWidgets.QLabel(self.centralwidget)
        self.Qty.setGeometry(QtCore.QRect(40, 120, 31, 21))
        self.Qty.setFont(font)
        self.Qty.setText("Qty")
        self.Harga = QtWidgets.QLabel(self.centralwidget)
        self.Harga.setGeometry(QtCore.QRect(40, 150, 41, 21))
        self.Harga.setFont(font)
        self.Harga.setText("Harga")
        
        # Input Fields
        self.No_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.No_Edit.setGeometry(QtCore.QRect(100, 30, 211, 20))
        self.Barkode_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.Barkode_Edit.setGeometry(QtCore.QRect(100, 60, 211, 20))
        self.Nama_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.Nama_Edit.setGeometry(QtCore.QRect(100, 90, 211, 20))
        self.Qty_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.Qty_Edit.setGeometry(QtCore.QRect(100, 120, 211, 20))
        self.Harga_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.Harga_Edit.setGeometry(QtCore.QRect(100, 150, 211, 20))
        
        # Buttons
        self.Simpan_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Simpan_Button.setGeometry(QtCore.QRect(100, 190, 61, 21))
        self.Simpan_Button.setText("SIMPAN")
        self.Edit_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Edit_Button.setGeometry(QtCore.QRect(180, 190, 61, 21))
        self.Edit_Button.setText("EDIT")
        self.Hapus_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Hapus_Button.setGeometry(QtCore.QRect(250, 190, 61, 21))
        self.Hapus_Button.setText("HAPUS")
        self.Load_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Load_Button.setGeometry(QtCore.QRect(100, 220, 61, 21))
        self.Load_Button.setText("LOAD")
        
        # Tombol Cari
        self.Cari_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Cari_Button.setGeometry(QtCore.QRect(250, 220, 61, 21))
        self.Cari_Button.setText("CARI")
        
        # Input Pencarian
        self.Cari_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.Cari_Edit.setGeometry(QtCore.QRect(100, 250, 211, 20))
        self.Cari_Edit.setPlaceholderText("Masukkan barkode atau nama")
        
        # Table
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(320, 30, 451, 251))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Barkode", "Name", "Kategori", "Qty", "Harga"])
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Connect Buttons
        self.Simpan_Button.clicked.connect(self.save_data)
        self.Load_Button.clicked.connect(self.load_data)
        self.Edit_Button.clicked.connect(self.edit_data)
        self.Hapus_Button.clicked.connect(self.delete_data)
        self.Cari_Button.clicked.connect(self.search_data)
        
    def connect_db(self):
        """Establish a database connection."""
        try:
            db = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_penjualan"  # Replace with your database name
            )
            return db
        except mc.Error as e:
            QMessageBox.critical(None, "Database Connection Error", str(e))
            return None

    def save_data(self):
        """Save data to the database."""
        db = self.connect_db()
        if db:
            cursor = db.cursor()
            try:
                query = "INSERT INTO product (id, barkode, name, kategori, qty, harga) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (
                    self.No_Edit.text(),
                    self.Barkode_Edit.text(),
                    self.Nama_Edit.text(),
                    "Kategori",  # Default value, replace if needed
                    self.Qty_Edit.text(),
                    self.Harga_Edit.text(),
                )
                cursor.execute(query, values)
                db.commit()
                QMessageBox.information(None, "Success", "Data saved successfully!")
            except mc.Error as e:
                QMessageBox.critical(None, "Error", str(e))
            finally:
                db.close()

    def load_data(self):
        """Load data from the database."""
        db = self.connect_db()
        if db:
            cursor = db.cursor()
            try:
                cursor.execute("SELECT * FROM product")
                rows = cursor.fetchall()
                self.tableWidget.setRowCount(0)
                for row_idx, row_data in enumerate(rows):
                    self.tableWidget.insertRow(row_idx)
                    for col_idx, col_data in enumerate(row_data):
                        self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            except mc.Error as e:
                QMessageBox.critical(None, "Error", str(e))
            finally:
                db.close()

    def edit_data(self):
        """Edit data in the database."""
        db = self.connect_db()
        if db:
            cursor = db.cursor()
            try:
                query = "UPDATE product SET barkode=%s, name=%s, qty=%s, harga=%s WHERE id=%s"
                values = (
                    self.Barkode_Edit.text(),
                    self.Nama_Edit.text(),
                    self.Qty_Edit.text(),
                    self.Harga_Edit.text(),
                    self.No_Edit.text(),
                )
                cursor.execute(query, values)
                db.commit()
                QMessageBox.information(None, "Success", "Data updated successfully!")
            except mc.Error as e:
                QMessageBox.critical(None, "Error", str(e))
            finally:
                db.close()

    def delete_data(self):
        """Delete data from the database."""
        db = self.connect_db()
        if db:
            cursor = db.cursor()
            try:
                query = "DELETE FROM product WHERE id=%s"
                values = (self.No_Edit.text(),)
                cursor.execute(query, values)
                db.commit()
                QMessageBox.information(None, "Success", "Data deleted successfully!")
            except mc.Error as e:
                QMessageBox.critical(None, "Error", str(e))
            finally:
                db.close()

    def search_data(self):
        """Search data in the database."""
        db = self.connect_db()
        if db:
            cursor = db.cursor()
            try:
                search_value = self.Cari_Edit.text()
                query = "SELECT * FROM product WHERE barkode LIKE %s OR name LIKE %s"
                values = (f"%{search_value}%", f"%{search_value}%")
                cursor.execute(query, values)
                rows = cursor.fetchall()
                self.tableWidget.setRowCount(0)
                for row_idx, row_data in enumerate(rows):
                    self.tableWidget.insertRow(row_idx)
                    for col_idx, col_data in enumerate(row_data):
                        self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
                if not rows:
                    QMessageBox.information(None, "Info", "Data tidak ditemukan.")
            except mc.Error as e:
                QMessageBox.critical(None, "Error", str(e))
            finally:
                db.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
