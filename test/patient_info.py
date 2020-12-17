from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import Qt
from __manifest__ import path_separator, load_properties
import database_manager as sqlite

class Patient_info(QtWidgets.QMainWindow):
    def __init__(self):
        super(Patient_info, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'patient_info.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.patient_info.setAlignment(QtCore.Qt.AlignCenter)


        config = load_properties()
        self.patient_dni = config.get('PatientsSection', 'selectedPatient')
        doctor = config.get('UsersSection', 'currentuser')

        sql_con = sqlite.sqlite_connector()
        self.patient_info.setText("Paciente: "+sql_con.get_patient_name(doctor, self.patient_dni))
        sql_con.close()
        sql_con = sqlite.sqlite_connector()
        data = sql_con.get_patient_times(self.patient_dni)
       
        
        self.model = TableModel(data)
        
        self.info_table.setModel(self.model)

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self.horizontalHeaders = [''] * 6

        self.setHeaderData(0, Qt.Horizontal, "Fecha y hora")
        self.setHeaderData(1, Qt.Horizontal, "Segmento 1")
        self.setHeaderData(2, Qt.Horizontal, "Segmento 2")
        self.setHeaderData(3, Qt.Horizontal, "Segmento 3")
        self.setHeaderData(4, Qt.Horizontal, "Tiempo total")
        self.setHeaderData(5, Qt.Horizontal, "Clasificación total")
        self._data = [["N/A"]]
        if(data):
            self._data = data

    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                self.horizontalHeaders[section] = data
                return True
            except:
                return False
        return super().setHeaderData(section, orientation, data, role)
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self.horizontalHeaders[section]
            except:
                pass
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])