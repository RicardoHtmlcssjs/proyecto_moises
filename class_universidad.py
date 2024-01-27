from config import Db
from class_acciones import Acciones

class Universidad():
    def actualizar_carrera(self, id, descripcion):
        id = str(id)
        if Acciones().val_inp_vacio(descripcion) == 0:
            return 0
        else:
            datos_act = Acciones().tabla("SELECT * FROM carrera WHERE id_carrera = "+id+"")
            for d1 in datos_act:
                desc_act = d1[1]
            todos_pro = Acciones().tabla("SELECT * FROM carrera")
            cont = 0
            for res_def in todos_pro:
                rr = res_def[1]
                if res_def[1] == descripcion:
                    if res_def[1] != desc_act:
                        cont = cont + 1
            if cont >= 1:
                return 1
            else:
                return 2  
    def agregar_carrera(self, descripcion):
        if Acciones().val_inp_vacio(descripcion) == 0:
            return 0
        else:
            cont = 0
            exis_carr = Acciones().tabla("SELECT * FROM carrera")
            for pro1 in exis_carr:
                if pro1[1] == descripcion:
                    return "La carrera ya existe"
            return 1
    def agregar_materia(self, materia):
        if Acciones().val_inp_vacio(materia) == 0:
            return 0
        else:
            cont = 0
            exis_mate = Acciones().tabla("SELECT * FROM materias")
            for pro1 in exis_mate:
                if pro1[1] == materia:
                    return "La materia ya existe"
            return 1