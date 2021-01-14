from PyQt5 import QtWidgets, uic, QtCore, QtGui
import database_manager as sqlite

import sys


from __manifest__ import calculate_imc, path_separator, load_properties, photo_to_blob, load_doctors

class Edit_patient(QtWidgets.QMainWindow):
    def __init__(self, patient_dni="123123123"):
        super(Edit_patient, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'newPatient.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.patient_dni = patient_dni
        self.titulo.setText("EDITAR PACIENTE")
        self.set_editable_text(False) # Desactivem la edició

        self.fase.setPlaceholderText("Escala de Hoehn-Yahr")
        self.fase.addItems(["1", "1.5", "2", "2.5", "3", "4", "5"])

        self.medicos.setPlaceholderText("Selecciona un médico")
        load_doctors(self.medicos)

        self.newPatientButton.setText("Editar usuario")
        self.fotoCaraButton.setText("Editar foto")
        self.fotoCuerpoButton.setText("Editar foto")
        self.newPatientButton.clicked.connect(self.edit_mode) 
        

        self.load_data() # Carreguem les dades

        self.pes.editingFinished.connect(self.write_imc);
        self.altura.editingFinished.connect(self.write_imc)
    
    
    def load_data(self):
        self.cancelarButton.hide()
        self.guardarButton.hide()
        self.newPatientButton.show()


        sql_con = sqlite.sqlite_connector()
        data = sql_con.get_patient_data(self.patient_dni)
        sql_con.close()

        self.dni.setText(data[0])
        self.nom.setText(data[1])
        self.cognom.setText(data[2])
        self.direccio.setText(data[4])
        self.telefon.setText(data[5])
        self.mail.setText(data[6])
        self.sip.setText(data[7])
        self.altura.setText(data[8])
        self.pes.setText(data[9])
        self.naiximent.setDate(QtCore.QDate.fromString(data[10],"dd/MM/yyyy"))
        if(data[11] != 'M'):
            self.mujer.setChecked(True)
        self.diagnostic.setDate(QtCore.QDate.fromString(data[12],"dd/MM/yyyy"))
        self.fase.setCurrentIndex(data[13])
        self.imc.setText(data[14])
        self.grasa.setText(data[15])
        self.medicacio.setText(data[16])
        
        self.fotoCara.setPixmap(self.blob_to_pixmap(data[17]))
        if(self.fotoCara.pixmap()):
            print(self.fotoCara.pixmap())
        self.fotoCuerpo.setPixmap(self.blob_to_pixmap(data[18]))

    def blob_to_pixmap(self, binary):
        outPixmap = QtGui.QPixmap()
        outPixmap.loadFromData(binary)
        return outPixmap

    def edit_mode(self):
        self.set_editable_text(True) # Activem la edició

        self.newPatientButton.hide()
        self.guardarButton.show()
        self.guardarButton.clicked.connect(self.save_edit)
        self.cancelarButton.show()
        self.cancelarButton.clicked.connect(self.load_data)
    
    def save_edit(self):
        self.set_editable_text(False) # Desactivem l'edició

        sql_con = sqlite.sqlite_connector()

        if (len(self.dni.text()) < 9):  # Major que 9 no pot ser perque està controlat a l'interfície
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Introduce un DNI válido.")
        if(self.nom.text() == ""):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Es obligatorio introducir un nombre.")
        else:
            try:
                sql_con.add_patient(self.dni.text(), self.nom.text(), self.cognom.text(), self.medicos.itemData(self.medicos.currentIndex()), self.direccio.text(),
                                    self.telefon.text(), self.mail.text(), self.sip.text(), self.altura.text(), self.pes.text(),
                                    self.naiximent.text(), self.hombre.isChecked(), self.diagnostic.text(), self.fase.currentIndex(),
                                    self.imc.text(), self.grasa.text(), self.medicacio.toPlainText(), photo_to_blob(self.fotoCara.pixmap()),
                                    photo_to_blob(self.fotoCuerpo.pixmap()))
                QtWidgets.QMessageBox.information(self, 'Paciente modificado', "¡El paciente ha sido modificado con éxito!")
                self.newPatientButton.setText("Editar usuario")
                self.newPatientButton.clicked.disconnect(self.save_edit)
                self.newPatientButton.clicked.connect(self.edit_mode)
            except sqlite.sqlite3.IntegrityError:
                QtWidgets.QMessageBox.critical(self, 'ERROR', "Ya existe un paciente con este DNI")
            finally:
                sql_con.close()

    def write_imc(self):
        self.imc.setText(calculate_imc(self.pes.text(), self.altura.text()))
        self.grasa.setText(self.imc.text()+"%")

    def set_editable_text(self, mode):
        self.dni.setReadOnly(not mode)
        self.nom.setReadOnly(not mode)
        self.cognom.setReadOnly(not mode)
        self.direccio.setReadOnly(not mode)
        self.telefon.setReadOnly(not mode)
        self.mail.setReadOnly(not mode)
        self.sip.setReadOnly(not mode)
        self.altura.setReadOnly(not mode)
        self.pes.setReadOnly(not mode)
        self.naiximent.setReadOnly(not mode)
        self.hombre.setCheckable(not mode)
        self.mujer.setCheckable(not mode)
        self.diagnostic.setReadOnly(not mode)
        self.medicacio.setReadOnly(not mode)

        if(mode):
            self.fotoCaraButton.show()
            self.fotoCuerpoButton.show()
        else:
            self.fotoCaraButton.hide()
            self.fotoCuerpoButton.hide()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Edit_patient()# Llancem el login
    app.exec_() # Start the application