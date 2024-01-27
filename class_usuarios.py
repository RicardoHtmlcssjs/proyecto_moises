from config import Db
from class_acciones import Acciones

class Usuarios():
    def actualizar_profesor(self, id_pro, nombre, cedula, usuario, email):
        id = str(id_pro)
        if Acciones().val_inp_vacio(nombre) == 0 or Acciones().val_inp_vacio(cedula) == 0 or Acciones().val_inp_vacio(usuario) == 0 or Acciones().val_inp_vacio(email) == 0:
            return 0

        else:
            datos_act = Acciones().tabla("SELECT * FROM usuarios WHERE id_usuario = "+id+"")
            for d1 in datos_act:
                usu_actual = d1[1]
                ema_actual = d1[3]
                nom_actual = d1[5]
                ci_actual = d1[6]
            todos_pro = Acciones().tabla("SELECT * FROM usuarios")
            cont = 0
            for res_def in todos_pro:
                if res_def[1] == usuario or res_def[3] == email or res_def[5] == nombre or res_def[6] == cedula:
                    if res_def[1] != usu_actual or res_def[3] != ema_actual or res_def[5] != nom_actual or res_def[6] != ci_actual:
                        cont = cont + 1
            if cont >= 1:
            	return 1
            else:
            	return 2
    def agregar_profesor(self, nombre, cedula, usuario, email, contrasena):
        if Acciones().val_inp_vacio(nombre) == 0 or Acciones().val_inp_vacio(cedula) == 0 or Acciones().val_inp_vacio(usuario) == 0 or Acciones().val_inp_vacio(email) == 0 or Acciones().val_inp_vacio(contrasena) == 0:
            return 0
        else:
            cont = 0
            exis_profe = Acciones().tabla("SELECT * FROM usuarios")
            for pro1 in exis_profe:
                if pro1[1] == usuario:
                    return "Usuario ya existe"
                elif pro1[3] == email:
                    return "Email ya existe"
                elif pro1[6] == cedula:
                    return "Cedula ya existe"
                elif pro1[2] == contrasena:
                    return "Contraseña ya existe"
            return 1 
                  