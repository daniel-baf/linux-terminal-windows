import re
import subprocess
from os import system
from colorama import Fore, Back, init

# Initialize colorama
init(autoreset=True)

STATIC_COMMANDS = ['pwd', 'date', 'time', 'exit', 'clear', 'Man', 'uname -a']  # table of static commands
DYNAMIC_COMMANDS = ['cd', 'ls', 'rm', 'mkdir', 'rmdir']  # table of dynamic commands

LS_OPTIONS = ['-a', '-l']  # ls options for windows

STATIC_WIN_EQUIVALENTS = ['cd', 'date', 'time', 'exit', 'cls', 'man',
                          'ver']  # items used to cast a command to a windows command


# Init compile process of input
def exec_compile(command):
    global STATIC_COMMANDS, DYNAMIC_COMMANDS  # global references
    # check if input is a static command
    if any(STATIC_COMMANDS in command for STATIC_COMMANDS in STATIC_COMMANDS) or 'uname' in command:
        return run_static_command(command)
    # check if input is a dynamic command
    elif any(DYNAMIC_COMMANDS in command for DYNAMIC_COMMANDS in DYNAMIC_COMMANDS):
        return run_dynamic_command(command)
    # no valid command
    else:
        return 'Error: Command not found.'


# execute a dynamic command with switch statement
def run_dynamic_command(command):
    global DYNAMIC_COMMANDS  # global reference
    # check if command is at dynamic pool
    if any(DYNAMIC_COMMANDS in command for DYNAMIC_COMMANDS in DYNAMIC_COMMANDS):
        if 'cd' in command:
            return run_file_command(command, 'cd')
        elif 'ls' in command:
            return run_ls(command)
        elif 'rmdir' in command:
            return run_file_command(command, 'rmdir')
        elif 'rm' in command:
            return run_file_command(command, 'rm')
        elif 'mkdir' in command:
            return run_file_command(command, 'mkdir')
    else:
        return 'Error: Command not found.'


# exec commands related to file or directories
def run_file_command(command, dynamic_command):
    # <command> <file> | <dir>?
    if re.fullmatch(r'^\s*{}\s+([a-zA-Z0-9_./-]+\s*)$'.format(dynamic_command), command):
        return run_powershell_command(command)
    else:
        return 'Error: Command not found.'


# custom ls -> dir function
def run_ls(command):
    if re.fullmatch(r'^\s*ls(\s+-[al])?\s*$', command):
        return run_powershell_command(command)

    else:
        return 'Error: Command not found.'


# run static commands
def run_static_command(command):
    general_pattern = r'^\s*(\w+)\s*$'  # <STATIC_COMMAND>
    uname_pattern = r'^\s*uname\s*-a\s*$'  # <UNAME> <-A>
    if re.fullmatch(uname_pattern, command):
        return run_cmd_command('ver')

    elif re.fullmatch(general_pattern, command):
        expression = re.fullmatch(general_pattern, command)
        c_split = expression.group(1)
        command_index = STATIC_COMMANDS.index(c_split)
        output_command = STATIC_WIN_EQUIVALENTS[command_index]

        if c_split == 'Man':
            return print_menu()
            # return "hola"
        elif c_split == "exit":
            return exit()
        return run_cmd_command(output_command)
    return 'Error: Command not found.'


# invokes powershell
def run_powershell_command(command):
    # result = subprocess.run(["powershell", "-Command", command], capture_output=True).stdout
    result = subprocess.run(["powershell", "-Command", command], stdout=subprocess.PIPE, text=True)
    return result.stdout


# invokes cmd
def run_cmd_command(command):
    return system(command)


def print_menu():
    # Define the colors for the header, commands, and descriptions
    header_color = Back.BLACK + Fore.GREEN
    left_command_color = Fore.RED + Back.BLACK
    right_command_color = Fore.WHITE + Back.BLACK

    # format text with table format
    # Text with table formatting
    table_text = f'''{header_color}╔═════════════════════════════════════════════════════════════════════╗\n║          INSTRUCCIONES SOBRE EL USO DE LA APLICACIÓN                ║\n║                                                                     ║\n║   NOTA: Esta aplicación simula una consola, por lo que debes        ║\n║   tener en cuenta lo siguiente:                                     ║\n║                                                                     ║\n║   1. El comando {left_command_color}'cd' {header_color}emulará un cambio de directorio. El proceso    ║\n║      no puede ser movido, pero se trabajará sobre una ruta          ║\n║      guardada en RAM para futuras consultas.                        ║\n║                                                                     ║\n║   2. Algunos comandos no funcionan en Linux y sí en Windows, como   ║\n║      por ejemplo, {left_command_color}'ls <options>'{header_color}. Pues {left_command_color}<options>{header_color} no estan en win.   ║\n║                                                                     ║\n╟─────────────────────────────────────────────────────────────────────╢\n║                          COMANDOS                                   ║\n╟─────────────────────────────────────────────────────────────────────╢\n{header_color}║   - {left_command_color}pwd                    {right_command_color}Muestra el directorio actual. Ten en     {header_color}║\n{header_color}║                            {right_command_color}cuenta que la ruta absoluta no cambia,   {header_color}║\n{header_color}║                            {right_command_color}pero las consultas realizadas con el     {header_color}║\n{header_color}║                            {right_command_color}programa se verán reflejadas. El         {header_color}║\n{header_color}║                            {right_command_color}puntero será cambiado.                   {header_color}║\n{header_color}║                                                                     {header_color}║\n{header_color}║   - {left_command_color}date                   {right_command_color}Muestra la fecha actual.                 {header_color}║\n{header_color}║                                                                     {header_color}║\n{header_color}║   - {left_command_color}time                   {right_command_color}Muestra la hora actual en la computadora.{header_color}║\n{header_color}║                                                                     {header_color}║\n{header_color}║   - {left_command_color}exit                   {right_command_color}Sale del programa.                       {header_color}║\n{header_color}║                                                                     {header_color}║\n{header_color}║   - {left_command_color}clear                  {right_command_color}Limpia la pantalla de la consola.        {header_color}║\n{header_color}║                                                                     {header_color}║\n{header_color}║   - {left_command_color}Man                    {right_command_color}Muestra un mensaje con instrucciones e   {header_color}║\n{header_color}║                            {right_command_color}información del programa.                {header_color}║\n{header_color}║                                                                     {header_color}║\n{header_color}║   - {left_command_color}uname -a               {right_command_color}Muestra la versión del sistema operativo.{header_color}║\n{header_color}║                                                                     {header_color}║\n{header_color}║   - {left_command_color}cd <dir>               {right_command_color}Cambia el directorio sobre el que estamos{header_color}║\n{header_color}║                            {right_command_color}trabajando.                              {header_color}║\n{header_color}║                                                                     {header_color}║\n{header_color}║   - {left_command_color}ls [opt] <dir>         {right_command_color}Muestra los elementos que hay en el      {header_color}║\n{header_color}║                            {right_command_color}directorio. Estamos haciéndolo basados   {header_color}║\n{header_color}║                            {right_command_color}en Linux, por lo que el comando 'ls' no  {header_color}║\n{header_color}║                            {right_command_color}podrá ser ejecutado en Windows. Es       {header_color}║\n{header_color}║                            {right_command_color}probable que muestre un error. Windows   {header_color}║\n{header_color}║                            {right_command_color}utiliza el comando 'dir'.                {header_color}║\n{header_color}║                                                                     {header_color}║\n{header_color}║   - {left_command_color}rm [files]             {right_command_color}Borra archivos. 'files' puede ser escrito{header_color}║\n{header_color}║                            {right_command_color}como un archivo o como una ruta.         {header_color}║\n{header_color}║                                                                     {header_color}║\n{header_color}║   - {left_command_color}mkdir <dir>            {right_command_color}Crea una carpeta con el nombre de <dir>. {header_color}║\n{header_color}║                                                                     {header_color}║\n{header_color}║   - {left_command_color}rmdir <dir>            {right_command_color}Elimina la carpeta con el nombre de <dir>{header_color}║\n{header_color}║                            {right_command_color}Es probable que no permita borrar        {header_color}║\n{header_color}║                            {right_command_color}carpetas con elementos dentro.           {header_color}║\n{header_color}╟─────────────────────────────────────────────────────────────────────╢\n{header_color}║                    {left_command_color}DANIEL BAUTSITA 2121323 - URL                    {header_color}║\n{header_color}╚═════════════════════════════════════════════════════════════════════╝'''

    return table_text
