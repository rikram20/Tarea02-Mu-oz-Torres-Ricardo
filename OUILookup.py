#Diego Fernandez
#Ricardo Muñoz

import sys #modulo para interactuar con el sistema y obtener argumentos de linea de comandos
import getopt #modulo para analizar y manejar argumentos de linea de comandos de manera sencilla
import requests #modulo para hacer solicitudes HTTP a APIs y obtener datos de la web
import time #modulo para medir el tiempo y calcular duraciones, como el tiempo de respuesta

def obtener_fabricante(direccion_de_la_mac):
    """Funcion que busca el fabricante de una MAC usando una API."""
    tiempo_inicial = time.time()  # marca el tiempo de inicio
    try:
        url = f"https://api.maclookup.app/v2/macs/{direccion_de_la_mac}" #clave api
        respuesta = requests.get(url)
        respuesta.raise_for_status() #verifica si hubo un error en la solicitud
        datos = respuesta.json()
        tiempo_final = time.time() #marca el tiempo de fin
        tiempo_respuesta = int((tiempo_final - tiempo_inicial) * 1000) #convierte a milisegundos

        #python3 OUILookup.py

        #Caso MAC que esté en la base de datos
        #python3 OUILookup.py --mac 98:06:3c:92:ff:c5

        #Caso MAC que no esté en la base de datos
        #python3 OUILookup.py --mac 98:06:3f:92:ff:c5

        #Caso fabricantes de las MAC disponibles en la tabla arp
        #python3 OUILookup.py --arp

        #verifica si la busqueda tuvo exito y si se tiene un fabricante
        if datos.get("exito") and datos.get("compañia"):
            print(f"MAC direccion : {direccion_de_la_mac}")
            print(f"Fabricante      : {datos['compañia']}")
        else:
            print(f"MAC direccion : {direccion_de_la_mac}")
            print("Fabricante     : Fabricante no detectado")

        print(f"Tiempo de respuesta: {tiempo_respuesta}ms")

    except requests.RequestException as e:
        print("Error al hacer la consulta:", e)

def buscar_mac(direccion_de_la_mac):
    """"Funcion que muestra el fabricante de una MAC especifica."""
    obtener_fabricante(direccion_de_la_mac)

def buscar_arp():
    """Funcion que muestra una lista de MACs y sus fabricantes."""
    #MACs simuladas en la tabla ARP
    tabla_arp = {
        "00:01:97:bb:bb:bb": "Cisco",
        "b4:b5:fe:92:ff:c5": "Hewlett Packard",
        "00:E0:64:aa:aa:aa": "Samsung",
        "AC:F7:F3:aa:aa:aa": "Xiomi"
    }
    print("IP/MAC/Fabricante:")
    for mac, fabricante in tabla_arp.items():
        print(f"{mac} / {fabricante}")

def main(argv):
    direccion_de_la_mac = None
    buscar_arp_bandera = False

    try:
        opciones, args = getopt.getopt(argv, "hm:a", ["help", "mac=", "arp"])
    except getopt.GetoptError:
        print('Uso: OUILookup.py --mac <mac> | --arp | [--help]')
        print('--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.')
        print('--arp: muestra los fabricantes de los host disponibles en la tabla arp.')
        print('--help: muestra este mensaje y termina.')
        sys.exit(2)

    for opcion, arg in opciones:
        if opcion in ("-h", "--help"):
            print('Uso: OUILookup.py --mac <mac> | --arp | [--help]')
            print('--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.')
            print('--arp: muestra los fabricantes de los host disponibles en la tabla arp.')
            print('--help: muestra este mensaje y termina.')
            sys.exit()
        elif opcion in ("-m", "--mac"):
            direccion_de_la_mac = arg
        elif opcion in ("-a", "--arp"):
            buscar_arp_bandera = True

    #llama a la funcion correcta dependiendo de los parametros
    if direccion_de_la_mac:
        buscar_mac(direccion_de_la_mac)
    elif buscar_arp_bandera:
        buscar_arp()
    else:
        print('Uso: OUILookup.py --mac <mac> | --arp | [--help]')
        print('--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.')
        print('--arp: muestra los fabricantes de los host disponibles en la tabla arp.')
        print('--help: muestra este mensaje y termina.')
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])