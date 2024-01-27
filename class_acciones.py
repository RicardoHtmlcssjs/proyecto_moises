from flask import session
from fpdf import FPDF
from config import Db
class Acciones():
    #mostrar tabla 
    def tabla(self, sql):
        result = Db().fetchall(sql)
        return result
    #validar input si esta vacio
    def val_inp_vacio(self, val):
        text = len(val)
        if text == 0:
            return 0
        else:
            return 1
    #mostrar mensaje
    def mensaje(self, color, txt):
        result = "<div class='alert alert-"+ color +" text-center my-1'><strong>"+ txt +"</strong></div>"
        return result
    # redireccion por no haber creado la session
    def red_login(self):
        if 'id_david_pro_flask' in session:
            re = 1
        else:
            re = 0
        return re
    def pdf_alu(self, res_materias, nom_al):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Notas de "+ nom_al +"", ln=1, align="C")
        pdf.cell(200, 20, txt="Materia               Nota1               Nota2               Nota3               Nota final", ln=1)
        for res1 in res_materias:
            pdf.cell(200, 20, txt=""+ str(res1[1]) +"             "+ str(res1[2]) +"                "+ str(res1[3]) +"               "+ str(res1[4]) +"               "+ str(res1[5]) +"", ln=1)
        pdf.output("notas_"+ str(nom_al) +".pdf")
        return 1