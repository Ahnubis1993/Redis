from Controlador import createCar, printAllCars, searchCarByAttribute, checkCar, deleteCar, modifyCarByAttribute, closeConnection
from Utilidades import confirmation

def mainMenu():

    '''
    Invoca al menu principal. Cada opcion elegida por el usuario realizara una operacion en concreta
    '''

    opt = None
    while(opt != "0"):
        print("\n╔══════════════════════════════════╗")
        print("║         Concesionario            ║")
        print("╠══════════════════════════════════╣")
        print("║ 1. Crear un coche                ║")
        print("║ 2. Eliminar un coche             ║")
        print("║ 3. Buscar un coche               ║")
        print("║ 4. Modificar un coche            ║")
        print("║ 5. Mostrar todos los coches      ║")
        print("║ 0. Salir                         ║")
        print("╚══════════════════════════════════╝")
        opt = input("Elige una opcion: ").strip()

        if opt == "1":
            createMenu()
        elif opt == "2":
            deleteMenu()
        elif opt == "3":
            searchMenu(False)
        elif opt == "4":
            modifyMenu()
        elif opt == "5":
            printAll()
        elif opt == "0":
            closeConnection()
            print("¡Hasta luego!")
        else:
            print("Opcion no valida. Intentalo de nuevo.")


def createMenu():

    '''
    Crea los atributos del coche mediante unas restricciones, cada atributo tiene las suyas propias.
    Ademas el usuario dispone de 5 intentos para crear el coche, en caso contrario, fallara el alta.
    Independiente del resultado (si se realiza el alta, como si no) se pide al usuario si quiere introducir uno nuevo
    '''

    print("\n╔════════════════════════════════╗")
    print("║        Crear un coche          ║")
    print("╚════════════════════════════════╝")

    exit = False
    valid = False

    while(not exit):
        attempts = 5
        while attempts > 0:
            print("\nIntroduce la matricula (4 digitos y 3 letras): ")
            plateNumber = input().strip().upper()
            if len(plateNumber) == 7 and plateNumber[:4].isdigit() and plateNumber[4:].isalpha():
                attempts = 0
                valid = True
            else:
                attempts -= 1
                print("** La matricula debe tener 4 digitos seguidos de 3 letras. Intentalo de nuevo.")

        if(valid):
            valid = False
            valid_brands = ["Tesla", "Audi", "Seat", "Golf", "Ford"]
            attempts = 5
            while attempts > 0:
                print("\nIntroduce la marca (Tesla, Audi, Seat, Golf, Ford): ")
                brand = input().strip().capitalize()
                if brand in valid_brands:
                    attempts = 0
                    valid = True
                else:
                    attempts -= 1
                    print("Marca no valida. Intentalo de nuevo.")

            if(valid):
                print("\nIntroduce el modelo: ")
                model = input().strip().capitalize()

                print("Introduce el color: ")
                color = input().strip().capitalize()

                createCar(plateNumber, brand, model, color)
            else:
                print("Coche no dado de alta correctamente, has introducido una marca con la que no trabajamos.")

        else:
            print("Coche no dado de alta correctamente, has introducido mal la matricula.")

        if not confirmation("¿Quieres crear otro coche?: (S/N)"):
            exit = True


def deleteMenu():

    '''
    Usa el metodo serachMenu del controlador, para buscar por cualquier atributo el coche a borrar.
    En caso que se haya encontrado el coche, se eliminar d ela BBDD.
    '''

    if checkCar():
        print("\n╔═══════════════════════════════════╗")
        print("║       Eliminar un vehiculo        ║")
        print("╚═══════════════════════════════════╝")

        print("Redireccionando a la busqueda de coche a borrar.")
        car = searchMenu(True)
        deleteCar(car)
    else:
        print("No hay coches en la BBDD, primero debes crear uno para eliminar un coche.")


def searchMenu(uniqueResult):

    '''
    Busca un coche mediante cualquier atributo del mismo, para ello el usuario debe elegir el atributo a buscar
    y despues insertar el campo que crea. El metodo searchCarByAttribute del controlador se hara cargo.
    Si el objeto se encuentra en la BBDD, se muestra, o si hay varios, tambien.
    :param uniqueResult: valor boolean para saber si se esta invocando al metodo desde busqueda o desde otreo metodo
    :return: el coche en caso que lo invoque el metodo eliminar o modificar
    '''

    if checkCar():
        print("\n╔════════════════════════════════╗")
        print("║         Buscar un coche        ║")
        print("╚════════════════════════════════╝")
        car = None
        exit = False
        while not exit:
            print("\nSelecciona el atributo por el cual buscar: ")
            print("1. Matricula")
            print("2. Marca")
            print("3. Modelo")
            print("4. Color")
            option = input().strip()

            if option == "1":
                print("\nIntroduce la matricula: ")
                plateNUmber = input().strip().upper()
                if len(plateNUmber) == 7 and plateNUmber[:4].isdigit() and plateNUmber[4:].isalpha():
                    car = searchCarByAttribute("matricula", plateNUmber, uniqueResult)
                else:
                    print("La matricula que has introducido es incorrecta.")
            elif option == "2":
                print("\nIntroduce la marca (Tesla, Audi, Seat, Golf, Ford): ")
                valid_brands = ["Tesla", "Audi", "Seat", "Golf", "Ford"]
                brand = input().strip().capitalize()
                if brand in valid_brands:
                    car = searchCarByAttribute("marca", brand, uniqueResult)
                else:
                    print("La marca que has introducido es incorrecta.")
            elif option == "3":
                print("\nIntroduce el modelo: ")
                model = input().strip().capitalize()
                car = searchCarByAttribute("modelo", model, uniqueResult)
            elif option == "4":
                print("\nIntroduce el color: ")
                color = input().strip().capitalize()
                car = searchCarByAttribute("color", color, uniqueResult)
            else:
                print("Opcion no valida. Intentalo de nuevo.")

            if not confirmation("¿Quieres buscar un coche nuevo? (S/N): "):
                exit = True
                return car
    else:
        print("No hay coches en la BBDD, primero debes crear uno para buscar un coche.")

def modifyMenu():

    '''
    Primero busca un coche mediante el metodo searchMenu. Si se encuentra el coche que se desea modificar
    se pregunta al usuario mediante u menu el atributo a modificar, para introducir uno nuevo y cambiarlo.
    '''

    if checkCar():
        print("\n╔════════════════════════════════╗")
        print("║       Modificar un coche       ║")
        print("╚════════════════════════════════╝")

        car = searchMenu(True)

        if(car):

            exit = False
            while not exit:
                print("\nSelecciona el atributo a modificar del coche: ")
                print("1. Matricula")
                print("2. Marca")
                print("3. Modelo")
                print("4. Color")
                option = input().strip()

                if option == "1":
                    print("\nIntroduce una nueva matricula: ")
                    plateNUmber = input().strip().upper()
                    if len(plateNUmber) == 7 and plateNUmber[:4].isdigit() and plateNUmber[4:].isalpha():
                        modifyCarByAttribute(car.id, "matricula", plateNUmber)
                    else:
                        print("La matricula que has introducido es incorrecta.")
                elif option == "2":
                    print("\nIntroduce nueva marca (Tesla, Audi, Seat, Golf, Ford): ")
                    valid_brands = ["Tesla", "Audi", "Seat", "Golf", "Ford"]
                    brand = input().strip().capitalize()
                    if brand in valid_brands:
                        modifyCarByAttribute(car.id, "marca", brand)
                    else:
                        print("La marca que has introducido es incorrecta.")
                elif option == "3":
                    print("\nIntroduce nuevo modelo: ")
                    model = input().strip().capitalize()
                    modifyCarByAttribute(car.id, "modelo", model)
                elif option == "4":
                    print("\nIntroduce nuevo color: ")
                    color = input().strip().capitalize()
                    modifyCarByAttribute(car.id, "color", color)
                else:
                    print("Opcion no valida. Intentalo de nuevo.")

                if not confirmation("¿Quieres modificar algun atributo mas del coche? (S/N): "):
                    exit = True

        else:
            print("No se ha encontrado el coche que has buscado, modificacion cancelada.")

    else:
        print("No hay coches en la BBDD, primero debes crear uno para modificar un coches.")

def printAll():

    '''
    Muestra todos los coches que hay en la BBDD, para ello invoca al metodo printAllCars del controlador.
    :return:
    '''

    if checkCar():
        print("\n╔════════════════════════════════╗")
        print("║         Coches                 ║")
        print("╚════════════════════════════════╝")
        printAllCars()
    else:
        print("No hay coches en la BBDD, primero debes crear uno para ver los coches.")
