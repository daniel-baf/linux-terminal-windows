# DANIEL EDUARDO BAUTISTA FUENTES
# 2121323
from compiler.analyzer import exec_compile


def main():
    print("INICIO DE APLICACION, EMULANDO COMANDOS DE LINUX")
    print("EJECUTA Man para ver los comandos")
    while True:
        str_input = input("~$ ")

        print(exec_compile(str_input))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
