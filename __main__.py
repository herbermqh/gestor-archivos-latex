import os
from os.path import exists
import re
import subprocess
import click
import shutil
from pathlib import Path, PurePath
from appdirs import user_config_dir
from shutil import copy
import platform
import pyperclip
import subprocess
from conans import ConanFile, AutoToolsBuildEnvironment
from conans.tools import download, untargz, check_sha1, replace_in_file, environment_append
# required pip install conan_package_tools


# type directory: \capitulo
#definiendo funcion capitulo.
def capitulo(name_chapter,root_dir):
    #Deteminar el directorio de main.tex y establecer en variable root_dir_main
    root_dir_main = Path(root_dir)
    #verificar si existe el archivo name_chapter en el directorio root_dir_main utilizando pathlib
    if exists(root_dir_main/name_chapter):
        #si existe, entonces, imprimir "el capitulo ya se encuentra creado"
        # finalizar el if
        print("Capitulo ya existe")
        #si no existe, entonces, crear el capitulo
    else:
        #Dar atras en el directorio /root_dir_main y establecer este directorio en "root_dir_subject"
        root_dir_subject = Path(root_dir_main).parent
        #Dar 2 paso atras en el directorio /root_dir_main y establecer este directorio en "root_dir_latex"
        root_dir_latex = Path(root_dir_subject).parent
        #copiar la carpeta root_dir_latex/plantillas/LibroProyecto/CAPITULO con sus subdirectorios en el directorio root_dir_main cambiando de nombre a name_chapter
        shutil.copytree(root_dir_latex/'plantillas'/'LibroProyecto'/'CAPITULO',root_dir_main/name_chapter)
        #establer en variable root_dir_main_chapter el directorio root_dir_main/name_chapter
        root_dir_main_chapter = Path(root_dir_main/name_chapter)
        #cambiar el nombre del archivo TEORIA-.tex por TEORIA-name_chapter.tex en el directorio root_dir_main_chapter
        os.rename(root_dir_main_chapter/'TEORIA-.tex',root_dir_main_chapter/f'TEORIA-{name_chapter}.tex')
        #cambiar el nombre del archivo PR-.tex por PR-name_chapter.tex en el directorio root_dir_main_chapter.
        os.rename(root_dir_main_chapter/'PR-.tex',root_dir_main_chapter/f'PR-{name_chapter}.tex')
        #cambiar el nombre del archivo PP-.tex por PP-name_chapter.tex en el directorio root_dir_main_chapter.
        os.rename(root_dir_main_chapter/'PP-.tex',root_dir_main_chapter/f'PP-{name_chapter}.tex')
        #cambiar el nombre de la carpeta IMAGES-TEORIA por IMAGES-TEORIA-name_chapter en el directorio root_dir_main_chapter.
        os.rename(root_dir_main_chapter/'IMAGES-TEORIA',root_dir_main_chapter/f'IMAGES-TEORIA-{name_chapter}')
        #cambiar el nombre del archivo FOMRULARIO-.tex por FORMULARIO-name_chapter.tex en el directorio root_dir_main_chapter.
        os.rename(root_dir_main_chapter/'FORMULARIO-.tex',root_dir_main_chapter/f'FORMULARIO-{name_chapter}.tex')
        #cambiar el nombre del archivo RESUMEN-.tex por RESUMEN-name_chapter.tex en el directorio root_dir_main_chapter.
        os.rename(root_dir_main_chapter/'RESUMEN-.tex',root_dir_main_chapter/f'RESUMEN-{name_chapter}.tex')
        #crear archivo "/root_dir_main_chapter/TEORIA-name_chapter.latexmain"
        Path(root_dir_main_chapter/f'TEORIA-{name_chapter}.latexmain').touch()
        Path(root_dir_main_chapter/f'PR-{name_chapter}.latexmain').touch()
        Path(root_dir_main_chapter/f'PP-{name_chapter}.latexmain').touch()
        Path(root_dir_main_chapter/f'FORMULARIO-{name_chapter}.latexmain').touch()
        Path(root_dir_main_chapter/f'RESUMEN-{name_chapter}.latexmain').touch()
        print("Capitulo creado exitosamente")

            

# type directory: \cargarProblemas
def create_libroEjercicios_chapter(root_dir_latex,root_dir_name_book,name_book_chapter):
    #copiar el archivo "/root_dir_latex/plantillas/LibroEjercicios/CAPITULO.tex" en el directorio "/root_dir_name_book/" cambiando de nombre a "name_book_chapter"
    shutil.copy(root_dir_latex/'plantillas'/'LibroEjercicios'/'CAPITULO.tex',root_dir_name_book/f'{name_book_chapter}.tex')
    #crear archivo "/root_dir_name_book/name_book_chapter.latexmain"
    Path(root_dir_name_book/f'{name_book_chapter}.latexmain').touch()
    #copiar la carpeta "/roo_dir_latex/plantillas/LibroEjercicios/IMAGES-CAPITULO/" a "/root_dir_name_book/IMAGES-name_book_chapter"
    shutil.copytree(root_dir_latex/'plantillas'/'LibroEjercicios'/'IMAGES-CAPITULO',root_dir_name_book/f'IMAGES-{name_book_chapter}')

#definiendo funcion cargarProblemas(name_book,name_book_chapter,root_dir)
def cargarProblemas(name_book,name_book_chapter,root_dir):
    #Deteminar el directorio de main.tex y establecer en variable "root_dir_main"
    root_dir_main = root_dir
    #Dar 1 paso atras en el directorio /root_dir_main y establecer este directorio en "root_dir_subject"
    root_dir_subject = Path(root_dir_main).parent
    #Dar 2 paso atras en el directorio /root_dir_main y establecer este directorio en "root_dir_latex"
    root_dir_latex = Path(root_dir_subject).parent
    #Establecer el directorio /root_dir_subject/problemas-libros/name_book/ en root_dir_name_book
    root_dir_name_book = Path(root_dir_subject/'problemas-libros'/name_book)
    #Determinar si existe existe el directorio "root_dir_name_book"
    if exists(root_dir_name_book):
        #determinar si existe la el arhivo "/root_dir_name_book/name_book_chapter.tex"
        if exists(root_dir_name_book/f'{name_book_chapter}.tex'):
           print("Libro y capitulo ya existen")
            #si no existe,
        else:
            # print("El capitulo no se encuentra creado")
            #crear el capitulo
            create_libroEjercicios_chapter(root_dir_latex,root_dir_name_book,name_book_chapter)
            print("Capitulo creado exitosamente")
    else:
        # print("El libro no existe")
        #crear carpeta "/root_dir_name_book/"
        os.mkdir(root_dir_name_book)
        #copiar "/root_dir_latex/plantillas/LibroEjercicios/main.tex" a "/root_dir_name_book/name_book.tex"
        shutil.copy(root_dir_latex/'plantillas'/'LibroEjercicios'/'main.tex',root_dir_name_book/f'{name_book}.tex')
        #crear archivo "/root_dir_name_book/name_book.latexmain"
        Path(root_dir_name_book/f'{name_book}.latexmain').touch()
        #crear el capitulo
        create_libroEjercicios_chapter(root_dir_latex,root_dir_name_book,name_book_chapter)
        print("Libro y capitulo creados exitosamente")

# UMSA-FIS-1-2008-I-A-cpf
# type directory: \cargarExamen
#definiendo función cargarExamen(name_exam,root_dir)
def cargarExamen(name_exam,root_dir):
    #Deteminar el directorio de main.tex y establecer en variable "root_dir_main"
    root_dir_main = root_dir
    #Dar 2 pasos hacia atras en el directorio "/root_dir_main" y establecer este directorio en "root_dir_latex"
    root_dir_subject = Path(root_dir_main).parent
    root_dir_latex = Path(root_dir_subject).parent
    #Hacer un split de name_exam en la lista
    name_exam_split = name_exam.split('-')
    university = name_exam_split[0]
    subject = name_exam_split[1]
    partial = name_exam_split[2]
    year = name_exam_split[3]
    semester = name_exam_split[4]
    row = name_exam_split[5]
    other = name_exam_split[6]
        
    #Construir nombre del directorio padre del examan de acuerdo a las variables university, subject, partial, year, semester, row, other, y establecer en variable name_parent_exam
    name_parent_exam = f'{university}_{subject}_{semester}_{other}' if partial == "" else f'{university}_{subject}_{partial}_{semester}_{other}'
    
    #Definir directorio padre del examen "/roo_dir_latex/materia/problemas-examenes/name_parent_exam" y establecer en variable root_dir_parent_examan
    root_dir_parent_exam = Path(root_dir_subject/'problemas-examenes'/name_parent_exam)

    #Existe el directorio "/root_dir_parent_examen"
    if exists(root_dir_parent_exam):
        #si existe, entonces no crear carpeta.
        pass
    else:
        #no existe, entonces crear carpeta en "/root_dir_parent_examen".
        os.mkdir(root_dir_parent_exam)
        
    # Tipos examen carpeta examen:
    #universidad_examen_añoExamenSemestreExamen_examenPertenciente
    #universidad_exam_parcial_añoExamenSemestreExamen_examPerteneciente
    #universidad_exam_parcial_añoexamenSemestreExamen_FilaExamen_examPerteneciente 

    #Construir nombre del examen y establecer en variable name_exam_internal de acuerdo a las variables university, subject, partial, year, semester, row, other
    if row == "":
        if partial == "":
            name_exam_internal = f'{university}_{subject}_{year}{semester}_{other}'
        else:
            name_exam_internal = f'{university}_{subject}_{partial}_{year}{semester}_{other}'
    else:
        name_exam_internal = f'{university}_{subject}_{partial}_{year}{semester}_{row}_{other}'

    #Definir directorio examen "/roo_dir_latex/materia/problemas-examenes/name_parent_exam/name_exam_internal" y establecer en variable root_dir_exam
    root_dir_exam = Path(root_dir_parent_exam/name_exam_internal)

    #Existe el directorio "/root_dir_exam"?
    if exists(root_dir_exam):
        #si existe, entonces no crear carpeta.
        print("Examen ya existe")
    else:
        #no existe, entonces crear carpeta en "/root_dir_exam".
        #copiar carpeta "/roo_dir_latex/plantillas/Examen" a "/root_dir_exam"
        shutil.copytree(root_dir_latex/'plantillas'/'Examen',root_dir_exam)
        #cambiar el nombre del arhivo "/root_dir_exam/main.tex" a "/root_dir_exam/name_exam_internal.tex"
        os.rename(root_dir_exam/'main.tex',root_dir_exam/f'{name_exam_internal}.tex')
        #cambiar el nombre del arhivo "/root_dir_exam/main.latexmain" a "/root_dir_exam/name_exam_internal.latexmain"
        os.rename(root_dir_exam/'main.latexmain',root_dir_exam/f'{name_exam_internal}.latexmain')
        #cambiar MATERIA en el archivo "/root_dir_exam/name_exam_internal.tex" por subject
        replace_in_file(root_dir_exam/f'{name_exam_internal}.tex','MATERIA',subject)
        replace_in_file(root_dir_exam/f'{name_exam_internal}.tex','SEMESTRE',semester)
        replace_in_file(root_dir_exam/f'{name_exam_internal}.tex','ANO',year)
        replace_in_file(root_dir_exam/f'{name_exam_internal}.tex','FILA',row)
        print("Examen creado existosamente")
# type directory: \cargarPractica
def cargarPractica(name_practice,root_dir):
    root_dir_main = root_dir
    root_dir_subject = Path(root_dir_main).parent
    root_dir_latex = Path(root_dir_subject).parent
    root_dir_practice = Path(root_dir_subject/'problemas-practicas'/name_practice)
    if exists(root_dir_practice):
        print("Practica ya existe")
    else:
        shutil.copytree(root_dir_latex/'plantillas'/'Practica',root_dir_practice)
        os.rename(root_dir_practice/'main.tex',root_dir_practice/f'{name_practice}.tex')
        os.rename(root_dir_practice/'main.latexmain',root_dir_practice/f'{name_practice}.latexmain')
        print("Practica creada existosamente")

# type directory: \usarproblema

# type directory: \usarexamen

# type directory: \usarpractica

# syntax: python -m archive-gestor-tex [create|edit] "line_name" root_dir
# syntax: python -m gestor-archivos-latex create "\capitulo[2]{HEBER}" C:\Users\heber\Documents\LaTeX\fisica\prueba\FisicaPre.tex
# syntax: python C:\Users\heber\Documents\gestor-archivos-latex\__main__.py create "\capitulo[2]{HEBER}" C:\Users\heber\Documents\LaTeX\fisica\prueba\FisicaPre.tex
@click.group()
def cli():
    pass


@cli.command(help='Crear archivos latex')
@click.argument('line_name')
@click.argument('root_dir')
def create(line_name,root_dir):
    # elinar espacios vacios antes y despues de line_name y root_dir
    line_name = line_name.strip()
    root_dir = Path(root_dir.strip())
    print(line_name)
    # determinar el tipo de comando latex en line_name
    # Por medio de regex determinar el primer cadena de caracteres [a-zA-Z] des pues de \ y establecer en la variable "type_comand_latex"
    type_comand_latex = re.search(r'\\(\w+)(\[|\{)',line_name).group(1)

    # si type_comand_latex es capitulo, entonces, llamar al funcion capitulo()
    if type_comand_latex == "capitulo":
        #determinar el nombre del capitulo "name_chapter" por medio de split line_name y establecer en la variable "name_chapter" 
        name_chapter = re.search(r'\{([a-zA-Z0-9_-]+)\}',line_name).group(1)
        #llamar a la funcion capitulo(name_chapter,root_dir)
        capitulo(name_chapter,root_dir)
    
    # si type_comand_latex es cargarProblemas, entonces, llamar al funcion cargarProblemas()
    elif type_comand_latex == "cargarProblemas":
        #determinar el nombre del libro "name_book" por medio de split line_name y establecer en la variable "name_book" 
        name_book = re.search(r'\{([a-zA-Z0-9_-]+)\}',line_name).group(1)
        #determinar segunda búaqueda nombre del ejercicio "name_exercise" por medio de split line_name y establecer en la variable "name_exercise". Second match
        name_book_chapter = re.search(r'\}\{([a-zA-Z0-9_-]+)\}',line_name).group(1)
        #llamar a la funcion cargarProblemas(name_book,name_book_chapter,root_dir)
        cargarProblemas(name_book,name_book_chapter,root_dir)

    # si type_comand_latex es cargarExamen, entonces, llamar al funcion cargarExamen()
    elif type_comand_latex == "cargarExamen":
        #determinar el nombre del libro "name_book" por medio de split line_name y establecer en la variable "name_book" 
        name_exam = re.search(r'\{([a-zA-Z0-9_-]+)\}',line_name).group(1)
        #llamar a la funcion cargarExamen(name_exam,root_dir)
        cargarExamen(name_exam,root_dir)

    # si type_comand_latex es cargarPractica, entonces, llamar al funcion cargarPractica()
    elif type_comand_latex == "cargarPractica":
        #determinar el nombre del libro "name_book" por medio de split line_name y establecer en la variable "name_book" 
        name_practice = re.search(r'\{([a-zA-Z0-9_-]+)\}',line_name).group(1)
        #llamar a la funcion cargarPractica(name_practice,root_dir)
        cargarPractica(name_practice,root_dir)
    else:
        print("Comando LaTeX no reconocido")
    #determinar el nombre de la practica establecer en name_practice
    #llamar a la función cargarPractica(name_practice)

    #imprimir "operaciones exitosa"


@cli.command(help='Editar archivo latex')
@click.argument('line_name')
@click.argument('root_dir')
def edit(line_name,root_dir):
    print("No implementado")

@cli.command(help="prembulo precompilado")
@click.argument('root_archive')
def compilepreamble(root_archive):
    root_archive = Path(root_archive.strip())
    #determinar el directorio del archivo root_archive.tex y establecer en la variable "root_dir"
    root_dir = Path(root_archive).parent
    #determinar el nombre del carpeta root_dir y establecer en la variable "name_dir"
    name_dir = root_dir.name
    #establecer el directorio "/root_dir/precompile.bat" y establecer en la variable "root_dir_precompile"
    #determina si estoy en windows o linux
    if os.name == 'nt':
        root_dir_precompile = Path(root_dir/'precompile.bat')
    else:
        root_dir_precompile = Path(root_dir/'precompile.sh')
    #verificar si en el arhivo /root_archive.tex existe la cadena "\endofdump"
    #si existe, entonces, llamar a la funcion precompile(root_dir,name_dir,root_dir_precompile)
    if Path(root_archive).read_text().find("\\endofdump") != -1:
        #ir a la carpeta root_dir y ejecutar el archivo root_dir_precompile
        os.chdir(root_dir)
        subprocess.call(root_dir_precompile)
    else:
        # entrar al archivo /root_archive.tex y escribir la cadena "\endofdump" al final del archivo "root_archive" y luego guardar y salir.
        with open(root_archive, 'a') as f:
            f.write("\\endofdump")
        f.close()
        #crea el arhivo /root_dir/precompile.bat en root_dir
        with open(root_dir_precompile, 'w') as f:
            f.write('xelatex-dev.exe -synctex=1 -interaction=nonstopmode --enable-write18 -shell-escape -ini -jobname="'+name_dir+'" "&xelatex-dev" mylatexformat.ltx "'+root_archive+'"')
        # ir a la carpeta root_dir y ejecutar el archivo precompile.bat
        os.chdir(root_dir)
        subprocess.call(root_dir_precompile)
        # entrar al arhivo /root_archive.tex y escribir la cadena "%&name_dir" en la linea cero y luego saltar a la linea siguiente
        with open(root_archive,'r') as f:
            lines = f.readlines()
            lines.insert(0,'%&'+name_dir+'\n')
            with open(root_archive,'w') as f:
                f.writelines(lines)
        f.close()

if __name__ == "__main__":
    cli()




