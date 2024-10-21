import re
import os

# Definir los servicios y precios
servicios = {
    1: ("Lavado básico", 5000),
    2: ("Lavado + Planchado", 8000),
    3: ("Lavado de edredón", 12000),
    4: ("Lavado + Desinfección", 10000),
    5: ("Lavado Industrial (grandes)", 15000)
}

# Variables globales
clientes_atendidos = 0
clientes_con_descuento = 0
ventas_totales = 0
cantidad_servicios = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
ventas_por_servicio = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}  # Almacena el total generado por cada servicio

# Función para limpiar la consola
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para mostrar el menú
def mostrar_menu(cliente_numero):
    limpiar_consola()
    print("\n" + "="*40)
    print("            LIMPIO YA - LAVANDERÍA            ")
    print("="*40)
    print(f"           MENÚ DE SERVICIOS (Cliente {cliente_numero})           ")
    print("="*40)
    print(" [1] Lavado básico                        ")
    print(" [2] Lavado + Planchado                   ")
    print(" [3] Lavado de edredón                    ")
    print(" [4] Lavado + Desinfección                ")
    print(" [5] Lavado Industrial (grandes)          ")
    print(" [6] Cerrar Pedido                        ")
    print(" [7] Salir del Sistema                    ")
    print("="*40 + "\n")

# Función para validar la entrada del usuario
def validar_entrada(opcion):
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 7:
        print("Entrada no válida, intente de nuevo.")
        opcion = input("Seleccione una opción del menú: ")
    return int(opcion)

# Función para validar el formato del correo electrónico
def validar_email(email):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(patron, email):
        return True
    else:
        print("Correo no válido, intente de nuevo.")
        return False

# Función para obtener el correo del cliente (si desea recibir promociones)
def obtener_email():
    desea_promocion = input("¿El cliente desea recibir promociones? (s/n): ").lower()
    if desea_promocion == 's':
        email = input("Ingrese el correo electrónico del cliente: ")
        while not validar_email(email):
            email = input("Ingrese el correo electrónico válido del cliente: ")
        return email
    return None

# Función para procesar el pedido de un cliente
def procesar_pedido_cliente(cliente_numero):
    global clientes_atendidos, clientes_con_descuento, ventas_totales
    total_cliente = 0
    total_sin_descuento = 0
    cliente_tiene_descuento = False
    cliente_servicios = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    while True:
        mostrar_menu(cliente_numero)
        opcion = validar_entrada(input(f"Cliente {cliente_numero}, seleccione una opción (o 6 para cerrar el pedido): "))
        if opcion == 6:
            break
        elif opcion == 7:
            # Guardar los valores antes de salir solo si el cliente ha comprado algo
            if total_sin_descuento > 0:
                tiene_tarjeta = input(f"¿El cliente {cliente_numero} tiene una tarjeta de fidelización? (s/n): ").lower()
                if tiene_tarjeta == 's':
                    cliente_tiene_descuento = True
                    total_cliente = total_sin_descuento * 0.9
                else:
                    total_cliente = total_sin_descuento

                ventas_totales += total_cliente
                clientes_atendidos += 1
                if cliente_tiene_descuento:
                    clientes_con_descuento += 1

                for servicio, cantidad in cliente_servicios.items():
                    cantidad_servicios[servicio] += cantidad
                    ventas_por_servicio[servicio] += cantidad * servicios[servicio][1]

            totalizar_caja()
            exit()
        servicio_nombre, servicio_precio = servicios[opcion]
        cantidad = int(input(f"¿Cuántos {servicio_nombre} desea el cliente {cliente_numero}? "))
        total_sin_descuento += servicio_precio * cantidad
        cliente_servicios[opcion] += cantidad

    tiene_tarjeta = input(f"¿El cliente {cliente_numero} tiene una tarjeta de fidelización? (s/n): ").lower()
    if tiene_tarjeta == 's':
        cliente_tiene_descuento = True
        total_cliente = total_sin_descuento * 0.9
    else:
        total_cliente = total_sin_descuento

    ventas_totales += total_cliente
    clientes_atendidos += 1
    if cliente_tiene_descuento:
        clientes_con_descuento += 1
    
    for servicio, cantidad in cliente_servicios.items():
        cantidad_servicios[servicio] += cantidad
        ventas_por_servicio[servicio] += cantidad * servicios[servicio][1]

    print(f"\n--- Total del cliente {cliente_numero} ---")
    if cliente_tiene_descuento:
        print(f"Total sin descuento: ${total_sin_descuento:.2f}")
        print(f"Total con descuento: ${total_cliente:.2f}")
    else:
        print(f"Total a pagar: ${total_cliente:.2f}\n")

    cliente_email = obtener_email()
    if cliente_email:
        print(f"Correo registrado para promociones: {cliente_email}")
    else:
        print("El cliente no desea recibir promociones.\n")

# Función para totalizar caja
def totalizar_caja():
    global clientes_atendidos, clientes_con_descuento, ventas_totales, cantidad_servicios, ventas_por_servicio
    print("\n" + "="*40)
    print("            TOTALIZACIÓN DE LA CAJA            ")
    print("="*40)
    print(f"Total de clientes atendidos: {clientes_atendidos}")
    print(f"Clientes con descuento: {clientes_con_descuento}")
    print(f"Total de ventas generadas: ${ventas_totales:.2f}\n")

    print("Cantidad de servicios vendidos y su contribución:")
    for servicio, cantidad in cantidad_servicios.items():
        if cantidad > 0:
            monto_servicio = ventas_por_servicio[servicio]
            porcentaje_ventas = (monto_servicio / ventas_totales) * 100
            print(f"{servicios[servicio][0]}: {cantidad} vendidos, total generado: ${monto_servicio:.2f}, "
                  f"representa el {porcentaje_ventas:.2f}% de las ventas generales.")
    
    print("\n" + "="*40)
    print("            FIN DE LA TOTALIZACIÓN            ")
    print("="*40 + "\n")
    
    # Preguntar si desea abrir una nueva sesión o salir del sistema
    nueva_sesion = input("¿Desea abrir una nueva sesión? (s/n): ").lower()
    if nueva_sesion == 's':
        # Reiniciar todos los contadores
        clientes_atendidos = 0
        clientes_con_descuento = 0
        ventas_totales = 0
        cantidad_servicios = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        ventas_por_servicio = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        main()
    else:
        print("Saliendo del sistema...")
        exit()

# Bucle principal del sistema
def main():
    global clientes_atendidos, clientes_con_descuento, ventas_totales, cantidad_servicios, ventas_por_servicio
    while True:
        cliente_numero = clientes_atendidos + 1
        print(f"\n--- Nuevo Cliente {cliente_numero} ---")
        procesar_pedido_cliente(cliente_numero)
        
        # Volver al menú principal después de procesar el pedido del cliente
        mostrar_menu(cliente_numero)

# Asegura que el código se ejecute solo si el archivo se ejecuta directamente
if __name__ == "__main__":
    main()
