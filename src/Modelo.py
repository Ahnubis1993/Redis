class Coche:

    '''
    Objeto Coche que se usara para introducir en la BBDD
    Tiene una clase unica incremental, de tal forma que si se borra uno ya creado, la clave
    seguira aumentando.
    '''

    # Variable de clase para el ID autoincremental
    nextId = 1

    def __init__(self, matricula, marca, modelo, color):
        self.id = Coche.nextId
        Coche.nextId += 1
        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        self.color = color