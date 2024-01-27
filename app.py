from flask import Flask, render_template, request, redirect, flash, session
from config import Db
from class_acciones import Acciones
from class_usuarios import Usuarios
from class_universidad import Universidad

app = Flask(__name__)
app.secret_key = "abc1234"
#RUTA RAIZ
@app.route("/")
def index():
    if Acciones().red_login() == 1:
        return redirect('inicio')
    else:
        return render_template('index.html', titulo='IUTA', login=0)
#RITA DESTRUIR SESSION

# pdf_notas
@app.route("/pdf_notas")
def pdf_notas():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            return redirect("/admin_carreras")
        elif session['role_david_pro_flask'] == 2:
            return redirect("/inicio")
        else:
            id_al = session['id_alum_pro_flask']
            id_al = str(id_al)
            nom_al = session['nomb_alum_pro_flask']

            res_materias = Db().fetchall("SELECT materias.id_materia, materias.descripcion, notas_alumnos.nota1, notas_alumnos.nota2, notas_alumnos.nota3, notas_alumnos.nota_f FROM notas_alumnos INNER JOIN materias ON notas_alumnos.id_materia = materias.id_materia  WHERE notas_alumnos.id_alumno = '"+ id_al +"'")
            nom_al = session['nomb_alum_pro_flask']
            Acciones().pdf_alu(res_materias, nom_al)
            return redirect('/alumnos')
    else:
        return redirect('/')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
@app.route('/login', methods=['POST'])
def login():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            return redirect("/admin_carreras")
        else:
            return redirect("/inicio")
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        resultado = Db().fetchone("SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s", (usuario, contrasena))
        if resultado == True:
            res2 = Db().fetchall("SELECT * FROM usuarios WHERE usuario = '"+ usuario +"' AND contrasena = '"+ contrasena +"'")
            for r in res2:
                role = r[4]
                id_us = r[0]
                nomb_us = r[5]
            if role == 3:
                id_us = str(id_us)
                res3 = Db().fetchall("SELECT id_alumno FROM alumnos WHERE id_usuario = '"+ id_us +"'")
                for r2 in res3:
                    id_alu = r2[0]
                session['id_alum_pro_flask'] = id_alu
            session['role_david_pro_flask'] = role
            session['id_david_pro_flask'] = id_us
            session['nomb_alum_pro_flask'] = nomb_us

        if resultado:
            return redirect('/inicio')
        else:
            return render_template('index.html', titulo='IUTA', error_login=1) 
    return render_template('index.html')
#RUTA INICIO
@app.route("/inicio")
def inicio():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            return redirect("/admin_carreras")
        elif session['role_david_pro_flask'] == 3:
            return redirect("/alumnos")
        else:
            mostra_nota_alum = Db().fetchall("SELECT notas_alumnos.id_not_alm, carrera.descripcion, semestre.descripcion, materias.descripcion, notas_alumnos.id_alumno, notas_alumnos.nota1, notas_alumnos.nota2, notas_alumnos.nota3, notas_alumnos.nota_f FROM usuarios INNER JOIN notas_alumnos ON usuarios.id_usuario = notas_alumnos.id_profesor INNER JOIN carrera ON notas_alumnos.id_carrera = carrera.id_carrera INNER JOIN semestre ON notas_alumnos.id_semestre = semestre.id_semestre INNER JOIN materias ON notas_alumnos.id_materia = materias.id_materia WHERE id_usuario = "+ str(session['id_david_pro_flask']) +"")
            
            print(mostra_nota_alum)
            return render_template('inicio.html', titulo='IUTA - Inicio', opc_nav=1, mostra_nota_alum=mostra_nota_alum, nombre=session['nomb_alum_pro_flask'])
    else:
        return redirect('/')
#SUBIR NOTAS
@app.route("/subir_nota/<int:id>")
def subir_nota(id):
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            return redirect("/admin_carreras")
        elif session['role_david_pro_flask'] == 3:
            return redirect("/alumnos")
        else:
            sub_nota = Db().fetchall("SELECT id_not_alm, nota1, nota2, nota3 FROM notas_alumnos WHERE id_not_alm = '"+ str(id) +"'")
            return render_template('subir_nota.html', titulo='IUTA - subir notas', sub_nota=sub_nota)
    else:
        return redirect('/')
#SUBIENDO NOTAS
@app.route("/subiendo_notas", methods=['POST'])
def subiendo_notas():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 2:
            if request.method == 'POST':
                id_alm = request.form['id']
                nota_1 = request.form['nota_1']
                nota_1 = int(nota_1) 
                nota_2 = request.form['nota_2']
                nota_2 = int(nota_2) 
                nota_3 = request.form['nota_3']
                nota_3 = int(nota_3) 
                nota_fi = (nota_1 + nota_2 + nota_3) / 3 
                ins_nota = Db().inserttar("UPDATE notas_alumnos SET nota1='"+ str(nota_1) +"', nota2='"+ str(nota_2) +"', nota3='"+ str(nota_3) +"', nota_f='"+ str(nota_fi) +"' WHERE id_not_alm = '"+ str(id_alm) +"'")
                return redirect("/inicio")
            else:
                return redirect('/inicio')
        elif session['role_david_pro_flask'] == 1:
            return redirect("/admin_carreras")
        else:
            return redirect("/alumnos")
    else:
        return redirect("/")
# ALUMNOS
@app.route("/alumnos")
def alumnos():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            return redirect("/admin_carreras")
        elif session['role_david_pro_flask'] == 2:
            return redirect("/inicio")
        else:
            id_alu = session['id_alum_pro_flask']
            id_alu = str(id_alu)
            mate_vis = Db().fetchall("SELECT notas_alumnos.id_not_alm, usuarios.usuario, carrera.descripcion, semestre.descripcion, materias.descripcion FROM notas_alumnos INNER JOIN usuarios ON notas_alumnos.id_profesor = usuarios.id_usuario INNER JOIN carrera ON notas_alumnos.id_carrera = carrera.id_carrera INNER JOIN semestre ON notas_alumnos.id_semestre = semestre.id_semestre INNER JOIN materias ON notas_alumnos.id_materia = materias.id_materia WHERE id_alumno = '"+ id_alu +"'")
            
            return render_template('alumnos.html', titulo='IUTA - Alumnos', opc_nav=1, mate_vis=mate_vis)
    else:  
        return redirect("/")
#ruta administrador profesores
@app.route("/admin_profesores")
def admin_profesores():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            res_profe = Acciones().tabla("SELECT * FROM usuarios WHERE id_role = 2")
            return render_template('admin_profesores.html', titulo='Profesores', opc_nav=1, res_profe=res_profe)
        elif session['role_david_pro_flask'] == 2:
            return redirect("/inicio")
        else:
            return redirect("/alumnos")
    else:
        return redirect("/")
#ruta editar profesor
@app.route("/editar_profesor/<int:id>")
def editar_profesor(id):
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            id = str(id)
            most_profe = Acciones().tabla("SELECT * FROM usuarios WHERE id_usuario = "+id+"")
            return render_template("editar_profesor.html", titulo='Editar profesores', most_profe=most_profe)
        elif session['role_david_pro_flask'] == 2: 
            return redirect("/inicio")
        else:
            return redirect("/alumnos")
    else:
        return redirect("/")
#actualizar profesor
@app.route("/actualizar_profesor", methods=['POST'])
def actualizar_profesor():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            if request.method == 'POST':
                id_pro = request.form['id']
                nombre = request.form['nombre'] 
                cedula = request.form['cedula']
                usuario = request.form['usuario']
                email = request.form['email']
                res = Usuarios().actualizar_profesor(id_pro, nombre, cedula, usuario, email)
                id = str(id_pro)
                if res == 0:
                    most_profe = Acciones().tabla("SELECT * FROM usuarios WHERE id_usuario = "+id+"")
                    return render_template("editar_profesor.html", titulo='Editar profesor', most_profe=most_profe, error_login=1, color="danger", text="Algun campo esta vacio")
                elif res == 1:
                    most_profe = Acciones().tabla("SELECT * FROM usuarios WHERE id_usuario = "+id+"")
                    return render_template("editar_profesor.html", titulo='Editar profesores', most_profe=most_profe, error_login=1, color="danger", text="Algun registro existe", opc_nav=1)
                elif res == 2:
                    Db().actualizar("UPDATE usuarios SET usuario = %s, email = %s, nombre = %s, ci = %s WHERE id_usuario = %s", (usuario, email, nombre, cedula, id))
                    return redirect('/admin_profesores')
            else:
                return render_template('editar_profesor.html', titulo='IUTA - Actualizar profesor', color='danger', text='Ha ocurrido un error', opc_nav=1)
        elif session['role_david_pro_flask'] == 2:
            return redirect("/inicio")
        else:
            return redirect("/alumnos")
    else:
        return redirect("/")
#FORMULARIO AGREGAR UN PROFESOR
@app.route("/crear_profesor")
def crear_profesor():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            return render_template('crear_profesor.html', titulo='IUTA - crear profesor', opc_nav=1)
        elif session['role_david_pro_flask'] == 2:
            return redirect("/inicio") 
        else:
            return redirect("/alumnos")
    else:
        return redirect("/")

#INSERTAR REGISTRO DE AGREGAR PROFESOR
@app.route("/creando_profesor", methods=['POST'])
def creando_profesor():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            if request.method == 'POST':
                nombre = request.form['nombre'] 
                cedula = request.form['cedula']
                usuario = request.form['usuario']
                email = request.form['email']
                contrasena = request.form['contrasena']
                res = Usuarios().agregar_profesor(nombre, cedula, usuario, email, contrasena)
                if res == 0:
                    return render_template('crear_profesor.html', titulo='IUTA - Crear profesor', opc_nav=1, error_login=1, color='danger', text='Algun campo esta vaio')
                elif res == 1:
                    Db().inserttar("INSERT INTO usuarios (ci, contrasena, email, fec_hor_reg, id_role, nombre, usuario) VALUES ("+ cedula +" ,  '"+contrasena+"' ,  '"+ email +"' , now(), 2,'"+ nombre +"', '"+ usuario +"')")
                    return redirect('/admin_profesores')
                else:
                    select_role = Acciones().tabla("SELECT * FROM roles")
                    return render_template('crear_profesor.html', titulo='IUTA - Crear profesor', opc_nav=1, select_role=select_role, error_login=1, color='danger', text=res)   
            else:
                return render_template('crear_profesor.html', titulo='IUTA - Crear profesor', opc_nav=1, error_login=1, color='danger', text='Ha ocurrido un error')
        elif session['role_david_pro_flask'] == 2:
            return redirect("/inicio")
        else:
            return redirect("/alumnos")
    else:
        return redirect("/")

#ruta administrador carreras
@app.route("/admin_carreras")
def admin_carreras():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            res_carrera = Acciones().tabla("SELECT * FROM carrera")
            return render_template('admin_carreras.html', titulo='IUTA - Carreras', opc_nav=1, res_carrera=res_carrera)
        elif session['role_david_pro_flask'] == 2:
            return redirect("/inicio")
        else:
            return redirect("/alumnos")
    else:
        return redirect("/")

#ruta editar carrera
@app.route("/editar_carrera/<int:id>")
def editar_carrera(id):
    id = str(id)
    most_carr = Acciones().tabla("SELECT * FROM carrera WHERE id_carrera = "+id+"")
    return render_template("editar_carrera.html", opc_nav=1, titulo='IUTA - Editar carrera', most_carr=most_carr) 

#ACTUALIZAR CARRERA
@app.route("/actualizar_carrera", methods=['POST'])
def actualizar_carrera():
   if request.method == 'POST':
        id = request.form['id']
        descripcion = request.form["descripcion"]
        res = Universidad().actualizar_carrera(id, descripcion)
        id = str(id)
        if res == 0:
            most_carr = Acciones().tabla("SELECT * FROM carrera WHERE id_carrera = "+id+"")
            return render_template("editar_carrera.html", opc_nav=1, titulo='IUTA - Editar carrera', most_carr=most_carr, error_login=1, color="danger", text="Algun campo esta vacio")
        elif res == 1:
            most_carr = Acciones().tabla("SELECT * FROM carrera WHERE id_carrera = "+id+"")
            return render_template("editar_carrera.html", titulo='IUTA - Editar carrera', most_carr=most_carr, error_login=1, color="danger", text="Algun registro existe", opc_nav=1)
        elif res == 2:
            Db().actualizar("UPDATE carrera SET descripcion = %s WHERE id_carrera = %s", (descripcion, id))
            return redirect('/admin_carreras')

#FORMULARIO AGREGAR CARRERA
@app.route("/crear_carrera")
def crear_carrera():
    return render_template('crear_carrera.html', titulo='IUTA - Crear carrera', opc_nav=1)
# INSERTANDO REGISTRO DE CARRERA
@app.route("/creando_carrera", methods=['POST'])
def creando_carrera():
    if request.method == 'POST':
        descripcion = request.form['descripcion'] 
        res = Universidad().agregar_carrera( descripcion)
        if res == 0:
            return render_template('crear_carrera.html', titulo='IUTA - Crear carrera', opc_nav=1, error_login=1, color='danger', text='Algun campo esta vaio')
        elif res == 1:
            Db().inserttar("INSERT INTO carrera (descripcion) VALUES ('"+ descripcion +"')")
            return redirect('/admin_carreras')
        else:
            return render_template('crear_carrera.html', titulo='IUTA - Crear carrera', opc_nav=1, select_role=select_role, error_login=1, color='danger', text=res)
        
        
    else:
        return render_template('crear_carrera.html', titulo='IUTA - Crear carrera', opc_nav=1, error_login=1, color='danger', text='Ha ocurrido un error')

#IMPRIMIR PDF DE CARRERAS
@app.route("/imprimir_pdf_carreras")
def imprimir_pdf_carreras():
    text = "texto completo"

    pdf = MuPDF()
    pdf.add_page(title, text)
    pdf.save("document.pdf")

    return render_template("pdf_carreras.html", text=text)
#ruta administrador semestre
@app.route("/admin_semestre")
def admin_semestre():
    res_semestre = Acciones().tabla("SELECT * FROM semestre")
    return render_template('admin_semestre.html', titulo='IUTA - Semestres', opc_nav=1, res_semestre=res_semestre)

@app.route("/crear_semestre")
def crear_semestre():
    res_semestre = Acciones().tabla("SELECT * FROM semestre")
    for res1 in res_semestre:
        ult_seme = res1[1]
    nuev_seme = int(ult_seme) + 1
    if nuev_seme < 8:
        nuev_seme = str(nuev_seme)
        Db().inserttar("INSERT INTO semestre (descripcion) VALUES ('"+ nuev_seme +"')")
        return redirect('/admin_semestre')
    else:
        return render_template('admin_semestre.html', titulo='IUTA - Semestres', opc_nav=1, res_semestre=res_semestre, error=1, color='danger', text='No esta permitido crear mas de 7 semestres')

#ruta administrador materias
@app.route("/admin_materias")
def admin_materias():
    res_materias = Acciones().tabla("SELECT materias.id_materia, materias.descripcion, carrera.descripcion, semestre.descripcion, usuarios.nombre FROM materias INNER JOIN carrera ON materias.id_carrera = carrera.id_carrera INNER JOIN semestre ON materias.id_semestre = semestre.id_semestre INNER JOIN usuarios ON materias.id_profesor = usuarios.id_usuario ORDER BY semestre.descripcion")
    return render_template('admin_materias.html', titulo='IUTA - Materias', opc_nav=1, res_materias=res_materias)
# 
#FORMULARIO AGREGAR CARRERA
@app.route("/crear_materia")
def crear_materia():
    res_carreras = Acciones().tabla("SELECT * FROM carrera")
    res_semestres = Acciones().tabla("SELECT * FROM semestre")
    res_profesores = Acciones().tabla("SELECT * FROM usuarios WHERE id_role = 2")
    return render_template('crear_materia.html', titulo='IUTA - Crear materia', opc_nav=1, res_carreras=res_carreras, res_semestres=res_semestres, res_profesores=res_profesores)


#
@app.route("/creando_materia", methods=['POST'])
def creando_materia():
    if request.method == 'POST':
        materia = request.form['materia'] 
        carrera = request.form['carrera']
        semestre = request.form['semestre']
        profesor = request.form['profesor']
        carrera = str(carrera)
        semestre = str(semestre)
        profesor = str(profesor)
        print(carrera)
        res = Universidad().agregar_materia(materia)
        if res == 0:
            return render_template('crear_materia.html', titulo='IUTA - Crear materia', opc_nav=1, error_login=1, color='danger', text='Algun campo esta vaio')
        elif res == 1:
            Db().inserttar("INSERT INTO materias (descripcion, id_carrera, id_semestre, id_profesor) VALUES ('"+ materia +"' ,  '"+ carrera +"' ,  '"+ semestre +"', '"+ profesor +"')")
            print("Registro exitoso")
            return redirect('/admin_materias')
        else:
            return render_template('crear_materia.html', titulo='IUTA - Crear materi', opc_nav=1,  error_login=1, color='danger', text="Ha ocurrido un error")
    else:
        return render_template('crear_profesor.html', titulo='IUTA - Crear profesor', opc_nav=1, error_login=1, color='danger', text='Ha ocurrido un error')

#RUTA ADMINISTRADOR ALUMNOS
@app.route("/admin_alumnos")
def admin_alumnos():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            res_alumnos = Acciones().tabla("SELECT * FROM usuarios WHERE id_role = 3")
            return render_template('admin_alumnos.html', titulo='Alumnos', opc_nav=1, res_alumnos=res_alumnos)
        elif session['role_david_pro_flask'] == 2:
            return redirect("/inicio")
        else:
            return redirect("/alumnos")
    else:
        return redirect("/")

#FORMULARIO AGREGAR UN PROFESOR
@app.route("/crear_alumno")
def crear_alumno():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            carrera = Db().fetchall("SELECT * FROM carrera")
            semestre = Db().fetchall("SELECT * FROM semestre")
            return render_template('crear_alumno.html', titulo='IUTA - crear alumno', opc_nav=1, carrera = carrera, semestre = semestre)
        elif session['role_david_pro_flask'] == 2:
            return redirect("/inicio")
        else:
            return redirect("/alumnos")
    else:
        return redirect("/")

#INSERTAR REGISTRO DE AGREGAR PROFESOR
@app.route("/creando_alumno", methods=['POST'])
def creando_alumno():
    if Acciones().red_login() == 1:
        if session['role_david_pro_flask'] == 1:
            if request.method == 'POST':
                nombre = request.form['nombre'] 
                cedula = request.form['cedula']
                usuario = request.form['usuario']
                email = request.form['email']
                contrasena = request.form['contrasena']
                carrera = request.form['carrera']
                semestre = request.form['semestre']
                res = Usuarios().agregar_profesor(nombre, cedula, usuario, email, contrasena)
                if res == 0:
                    return render_template('crear_alumno.html', titulo='IUTA - Crear alumno', opc_nav=1, error_login=1, color='danger', text='Algun campo esta vaio')
                elif res == 1:
                    Db().inserttar("INSERT INTO usuarios (ci, contrasena, email, fec_hor_reg, id_role, nombre, usuario) VALUES ("+ cedula +" ,  '"+contrasena+"' ,  '"+ email +"' , now(), 3,'"+ nombre +"', '"+ usuario +"')")
                    tt = Db().fetchall("SELECT id_usuario FROM usuarios")
                    for x in tt:
                        iid = x[0]
                    carrera = str(carrera)
                    semestre = str(semestre)
                    iid = str(iid)
                    Db().inserttar("INSERT INTO alumnos (id_carrera, id_semestre, id_usuario) VALUES ('"+ carrera +"', '"+ semestre +"', '"+ iid +"')")
                    res_materias = Acciones().tabla("SELECT materias.id_materia, materias.descripcion, carrera.id_carrera, carrera.descripcion, semestre.id_semestre, semestre.descripcion, usuarios.id_usuario, usuarios.nombre FROM materias INNER JOIN carrera ON materias.id_carrera = carrera.id_carrera INNER JOIN semestre ON materias.id_semestre = semestre.id_semestre INNER JOIN usuarios ON materias.id_profesor = usuarios.id_usuario WHERE carrera.id_carrera = '"+ carrera +"' AND semestre.id_semestre = '"+ semestre +"'")
                    
                    estu = Db().fetchall("SELECT id_alumno FROM alumnos")
                    for res1 in estu:
                        id_estu_act = res1[0]
                    
                    for res2 in res_materias:
                        id_profesor = res2[6]
                        id_materia = res2[0]
                        id_profesor = str(id_profesor)
                        id_materia = str(id_materia)
                        id_estu_act = str(id_estu_act)

                        Db().inserttar("INSERT INTO notas_alumnos (id_profesor, id_alumno, id_carrera, id_semestre, id_materia, nota1, nota2, nota3, nota_f) VALUES ('"+ id_profesor +"', '"+ id_estu_act +"', '"+ carrera +"', '"+ semestre +"', '"+ id_materia +"', 0, 0, 0, 0)")
                    return redirect('/admin_alumnos')
                    
                else:
                    # select_role = Acciones().tabla("SELECT * FROM roles")
                    carrera = Db().fetchall("SELECT * FROM carrera")
                    semestre = Db().fetchall("SELECT * FROM semestre")
                    return render_template('crear_alumno.html', titulo='IUTA - Crear alumno', opc_nav=1, error_login=1, color='danger', text=res, carrera=carrera, semestre=semestre)   
            else:
                return render_template('crear_profesor.html', titulo='IUTA - Crear profesor', opc_nav=1, error_login=1, color='danger', text='Ha ocurrido un error')
        elif session['role_david_pro_flask'] == 2:
            return redirect("/inicio")
        else:
            return redirect("/alumnos")
    else:
        return redirect("/")

    
#INICIAR EL SERVIDOR
if __name__ == '__main__':
    app.run(port=5000, debug=True)