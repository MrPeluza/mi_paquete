from .cursos import cursos
def horas_totales():
    return sum(curso.duracion for curso in cursos)
