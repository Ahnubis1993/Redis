def confirmation(message):
    """
    Solicita al usuario una confirmacion mediante un mensaje.

    :param mensaje (str): El mensaje que se mostrara al usuario.
    :returns True si la respuesta es afirmativa, False si es negativa.
    """

    valid = False
    opt = False
    while (not valid):
        response = input(message).strip().lower()
        if (response.startswith("s")):
            opt = True
            valid = True
        elif (response.startswith("n")):
            opt = False
            valid = True
        else:
            print("Opcion incorrecta.")

    return opt