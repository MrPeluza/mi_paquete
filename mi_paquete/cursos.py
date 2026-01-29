class curso:
    def __init__(self, nombre, duracion):
        self.nombre = nombre
        self.duracion = duracion

    def __repr__(self):
        return f"{self.nombre} [{self.duracion} horas]"

cursos = [
    curso("Python", 25),
    curso("Javascript", 30),
    curso("HTML", 20)
]

def listar_cursos():
    for curso in cursos:
        print(curso)