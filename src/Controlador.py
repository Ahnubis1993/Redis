from redis import ResponseError
from Modelo import Coche
from Utilidades import confirmation
import redis
import pickle


def closeConnection():

    '''
    Cierra la conexion a la BBDD cuando se sale del programa pulsando 0
    '''

    try:
        r.close()
        print("Conexion a Redis cerrada correctamente.")
    except Exception as e:
        print("Error al cerrar la conexion a Redis:", e)


def checkCar():

    '''
    Comprueba que hay coches en la BBDD
    :return: devuelve true si hay coches y false si no haya coches en la BBDD
    '''

    try:
        cars = r.keys('coche:*')
        if(cars):
            return True
        else:
            return False
    except ResponseError as re:
        print("Error al consultar todos los coches debido a:", re)

def checkCarPlateNumber(plateNumber):

    '''
    Comprueba que no hay coches con una matricula repetida en la BBDD
    :param plateNumber: matricular a comprobar
    :return true si esta repetida y false si no lo esta
    '''

    try:
        carsKeys = r.keys(f'coche:*')
        for carKey in carsKeys:
            carSerialized = r.get(carKey)
            car = pickle.loads(carSerialized)
            if(car.matricula==plateNumber):
                return True

        return False
    except ResponseError as re:
        print("Error al buscar coche por matricula:", re)
        
def checkLastId():
    try:
        cars = r.keys(f'coche:*')
        lastcar = cars[0].decode('utf-8')
        id = lastcar.split(':')[1]
        return int(id)
    except ResponseError as re:
            print("Error al buscar el id del ultimo coche:", re)

def createCar(plateNumber, brand, model, color):

    '''
    Crea un coche con los parametros introducidos en la vista, para ellos depende del modelo coche (Objeto)
    :param matricula: atributo del coche
    :param marca: atributo del coche
    :param modelo: atributo del coche
    :param color: atributo del coche
    '''

    try:
        car = Coche(plateNumber, brand, model, color)
        if(checkCarPlateNumber(plateNumber)):
            print("Ya existe un coche con la matricula "+plateNumber)
        else:
            r.set(f'coche:{car.id}', pickle.dumps(car))
            print("Coche", car.id, "insertado correctamente.")
    except ResponseError as re:
        print("Error al crear el coche debido a:", re)

def deleteCar(car):

    '''
    Borrar un coche mediante el uso del metodo busqueda, para ello el metodo busqueda devolvera un coche
    y obtendremos su id (unico) para borrarlo de la BBDD
    :param car: coche a borrar
    '''

    try:
        if(car):
            if confirmation("¿Quieres eliminar el coche: "+str(car.id)+"? (S/N): "):
                r.delete(f'coche:{car.id}')
                print("Coche:" + str(
                    car.id) + ", matricula:" + car.matricula + ", marca:" + car.marca + ", modelo:" + car.modelo + ", color:" + car.color+". Eliminado correctamente.")
            else:
                print("Coche:" + str(car.id) + ", no eliminado.")
        else:
            print("No se ha encontrado el coche que has buscado, eliminacion cancelada.")
    except ResponseError as re:
        print("Error de consulta borrado de coche debido a:", re)

def searchCarByAttribute(attribute, value, uniqueResult):

    '''
    Busca un coche por atributo especifico. Tambien tiene un valor boolean uniqueResult para saber si
    se esta invocando al metodo desde el propio busqueda o desde el metodo eliminar o modificar.
    En cuyo ultimos casos devolvera el coche encontrado para realizar operaciones sobre el mismo.
    Antes de realizar la operacion de borrado, comprueba que se haya encontrado el coche.
    :param attribute: atributo a buscar en el coche
    :param value: el valor del atributo
    :param uniqueResult: se usa para mostrar todos los resultados o elegir uno si hay varios
    :return: el coche encontrado (se devuelve en algunos metodos (delete y modify))
    '''

    try:
        # Obtener todas las claves que coinciden con el patron "coche:*"
        carsKey = r.keys('coche:*')
        carsFounded = []

        # Iterar sobre todas las claves y recuperar los coches
        for carKey in carsKey:
            # Recuperar el objeto serializado del coche
            carSerialized = r.get(carKey)
            car = pickle.loads(carSerialized)

            # Verificar si el atributo y el valor coinciden
            if getattr(car, attribute, None) == value:
                carsFounded.append(car)

        if(carsFounded):
            # Mostramos los coches en caso que haya
            print("Se encontraron los siguientes coches:")
            for index, car in enumerate(carsFounded, start=1):
                print(f"{index}. Matricula: {car.matricula}, Marca: {car.marca}, Modelo: {car.modelo}, Color: {car.color}.")

            # Si el resultado es True, sirve para delte, modify, devuelve coche
            if(uniqueResult):

                if len(carsFounded) > 1:
                    print("Hay mas de un coche que cumple con los criterios especificados.")
                    exit = False
                    while not exit:
                        choice = input("Selecciona el numero del coche que deseas seleccionar: ").strip()
                        if choice.isdigit() and 1 <= int(choice) <= len(carsFounded):
                            exit = True
                            return carsFounded[int(choice) - 1]
                        else:
                            print("Seleccion no valida.")
                else:
                    return carsFounded[0]
        else:
            print("No se encontraron coches con "+attribute+" "+value+".")

    except ResponseError as re:
        print("Error al buscar coches por atributo debido a:", re)


def modifyCarByAttribute(id, attribute, value):

    '''
    Es invocado desde la vista una vez se ha insertado un atributo nuevo correcto.
    Para llevar a cabo esta modificacion, se busca y obtiene el coche por id, y luego emdiante
    el metodo setattr (objeto, atributo, valorDelAtributo).
    :param id: del coche a localizar
    :param attribute: atributo a cambiar
    :param value: valor del atributo
    '''

    try:
        # Verificar si la clave del coche existe en Redis
        if r.exists(f'coche:{id}'):
            if(attribute == "matricula" and checkCarPlateNumber(value) ):
                print("Ya existe un coche con la matricula "+value) 
            else:
                # Obtener el valor de la clave
                carSerialized = r.get(f'coche:{id}')
                car = pickle.loads(carSerialized)

                # Modificar el atributo del coche dinamicamente
                setattr(car, attribute, value)

                # Guardar el coche modificado de nuevo en Redis
                r.set(f'coche:{id}', pickle.dumps(car))
                print("Coche modificado correctamente.")

    except ResponseError as re:
        print("Error al intentar modificar el campo "+attribute+" del coche.")


def printAllCars():

    '''
    Muestra todos los coches de la BBDD con todos sus atributos
    '''

    try:
        # Obtener todas las claves que coinciden con el patron "coche:*"
        carKeys = r.keys('coche:*')
        if carKeys:
            # Se invierte la lista porque redis nos la da al reves
            carKeys = list(reversed(carKeys))
            
            # Iterar sobre todas las claves y recuperar los coches
            for carKey in carKeys:
                # Recuperar el objeto serializado del coche
                carSerialized = r.get(carKey)
                car = pickle.loads(carSerialized)
                print("Coche:"+str(car.id)+", matricula: "+car.matricula+", marca: "+car.marca+", modelo: "+car.modelo+", color: "+car.color+".")

        else:
            print("No hay coches en la BBDD.")
    except ResponseError as re:
        print("Error de lectura de coches debido a:", re)
        

# Conectar a Redis

'''
Conexion con la base de datos de redis. Se mantiene fuera de una funcion para que se ejecute nada mas empezar el programa
'''

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    print("Conexion a la BBDD Redis establecida correctamente.")
    Coche.nextId = checkLastId()+1
except ConnectionError as ce:
    print("Error de conexion a Redis:", ce)
except ResponseError as re:
    print("Error de respuesta de Redis:", re)
except TimeoutError as te:
    print("Tiempo de espera agotado:", te)
except Exception as e:
    print("Error inesperado:", e)
