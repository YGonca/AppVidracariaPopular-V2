from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import sys
import sqlite3
import uuid

def window():
    def addContact():
        if lineEditName.text() != "" and lineEditAddress.text() != "" and lineEditPhone.text() != "" \
        and textEditDescription.toPlainText() != "":   
            cursor.execute("INSERT INTO contacts VALUES (?, ?, ?, ?, ?)", (lineEditName.text(), lineEditAddress.text(), lineEditPhone.text(), textEditDescription.toPlainText(), uuid.uuid4().hex))
            connection.commit()

            addToLayout()
            entryReset()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("A Vidraçaria Popular")
            msg.setText("Favor, preencha informações")
            msg.exec_()

    def updateContact():
        if invisibleId.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle("A Vidraçaria Popular")
            msg.setText("Favor, selecionar o Nome")
            msg.exec_()
        elif lineEditName.text() != "" and lineEditAddress.text() != "" and lineEditPhone.text() != "" \
            and textEditDescription.toPlainText() != "":
            cursor.execute(f"UPDATE contacts SET name = '{lineEditName.text()}' WHERE id = '{id}'")
            cursor.execute(f"UPDATE contacts SET address = '{lineEditAddress.text()}' WHERE id = '{id}'")
            cursor.execute(f"UPDATE contacts SET phone = '{lineEditPhone.text()}' WHERE id = '{id}'")
            cursor.execute(f"UPDATE contacts SET description = '{textEditDescription.toPlainText()}' WHERE id = '{id}'")
            connection.commit()
            msg = QMessageBox()
            msg.setWindowTitle("A Vidraçaria Popular")
            msg.setText("Sucesso ao atualizar Cliente!")
            msg.exec_()

            entryReset()
            addToLayout()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("A Vidraçaria Popular")
            msg.setText("Favor, preencha informações")
            msg.exec_()
    
    def deleteContact():
        if lineEditName.text() != "" and lineEditAddress.text() != "" and lineEditPhone.text() != "" \
            and textEditDescription.toPlainText() != "" and id != "":
            msg = QMessageBox()
            msg.setWindowTitle("A Vidraçaria Popular")
            msg.setText("Quer mesmo apagar?")
            msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            result = msg.buttonClicked.connect(popupButtonDelete)
            msg.exec_()
            if result:
                cursor.execute(f"DELETE FROM contacts WHERE id = '{id}'")
                connection.commit()
                addToLayout()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("A Vidraçaria Popular")
            msg.setText("Favor, selecionar o Nome")
            msg.exec_()

    def popupButtonDelete(i):
        if i.text() == "Yes":
            return True
        return False

    def entryReset():
        lineEditName.setText("")
        lineEditAddress.setText("")
        lineEditPhone.setText("")
        textEditDescription.setText("")
        invisibleId.setText("")

    def buttonClicked(identity:str):
        cursor.execute(f"SELECT name, address, phone, description FROM contacts WHERE id = '{identity}'")
        list_contacts = cursor.fetchall()

        lineEditName.setText(list_contacts[0][0])
        lineEditAddress.setText(list_contacts[0][1])
        lineEditPhone.setText(list_contacts[0][2])
        textEditDescription.setText(list_contacts[0][3])
        invisibleId.setText(identity)

    win.setObjectName("MainWindow")
    win.resize(1500, 1000)
    win.setWindowTitle("A Vidraçaria Popular")

    scroll = QScrollArea(win)
    widget = QWidget()
    vBox = QVBoxLayout()    

    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    scroll.setGeometry(1000, 90, 400, 680)

    label = QLabel(win)
    label.setGeometry(220, 0, 1000, 71)
    label.setText("A Vidraçaria Popular")
    label.setFont(QFont("Times new roman",50))

    invisibleId = QLabel(win)
    invisibleId.setHidden(True)
    invisibleId.setText("")

    lineEditName = QLineEdit(win)
    lineEditName.setGeometry(20, 90, 860, 40)
    lineEditName.setFont(QFont("Times new roman",15))
    lineEditName.setText("")
    lineEditName.setToolTip("Nome")
    lineEditName.setPlaceholderText("Nome")

    lineEditAddress = QLineEdit(win)
    lineEditAddress.setGeometry(20, 150, 860, 40)
    lineEditAddress.setFont(QFont("Times new roman",15))
    lineEditAddress.setText("")
    lineEditAddress.setToolTip("Endereço")
    lineEditAddress.setPlaceholderText("Endereço")

    lineEditPhone = QLineEdit(win)
    lineEditPhone.setGeometry(20, 210, 860, 40)
    lineEditPhone.setFont(QFont("Times new roman",15))
    lineEditPhone.setText("")
    lineEditPhone.setToolTip("Telefone")
    lineEditPhone.setPlaceholderText("Telefone")

    textEditDescription = QTextEdit(win)
    textEditDescription.setGeometry(20, 270, 860, 500)
    textEditDescription.setFont(QFont("Times new roman",15))
    textEditDescription.setText("")
    textEditDescription.setToolTip("Descrição")

    pushButtonAdd = QPushButton(win)
    pushButtonAdd.setGeometry(20, 800, 120, 50)
    pushButtonAdd.setFont(QFont("Times new roman",20))
    pushButtonAdd.setText("Adicionar")
    pushButtonAdd.clicked.connect(addContact)

    pushButtonReset = QPushButton(win)
    pushButtonReset.setGeometry(150, 800, 120, 50)
    pushButtonReset.setFont(QFont("Times new roman",20))
    pushButtonReset.setText("Resetar")
    pushButtonReset.clicked.connect(entryReset)

    pushButtonUpdate = QPushButton(win)
    pushButtonUpdate.setGeometry(20, 900, 120, 50)
    pushButtonUpdate.setFont(QFont("Times new roman",20))
    pushButtonUpdate.setText("Atualizar")
    pushButtonUpdate.clicked.connect(updateContact)

    pushButtonDelete = QPushButton(win)
    pushButtonDelete.setGeometry(150, 900, 120, 50)
    pushButtonDelete.setFont(QFont("Times new roman",20))
    pushButtonDelete.setText("Apagar")
    pushButtonDelete.clicked.connect(deleteContact)

    def addToLayout():
        clearLayout(vBox)
        cursor.execute("SELECT name, phone, id FROM contacts ORDER BY name")
        list_contact = cursor.fetchall()

        for i, list in enumerate(list_contact):
            pushButton = QPushButton(f"{list[0]} - {list[1]}")
            pushButton.setFont(QFont("Times new roman",14))
            pushButton.clicked.connect(lambda state, identity=list[2]: buttonClicked(identity))
            vBox.addWidget(pushButton)
        widget.setLayout(vBox)

    def clearLayout(layout:QVBoxLayout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    clearLayout(item.layout())

    addToLayout()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":  
    app = QApplication(sys.argv)
    win = QMainWindow()

    connection = sqlite3.connect("BancoDeDadosPyQt5.db")
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM contacts ORDER BY name")
    except sqlite3.OperationalError as error:
        print(error)
        sql_command = """CREATE TABLE contacts (
            name VARCHAR(30),
            address VARCHAR(30),
            phone VARCHAR(30),
            description VARCHAR(30),
            id VARCHAR(32) )"""
        cursor.execute(sql_command)

    window()