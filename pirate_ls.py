import glob
from rich.console import Console
from rich.table import Table
from rich import print
from rich.columns import Columns
from rich.panel import Panel
from rich import print
import json
import os
import stat
import time
import sys

console = Console()

class App(dict):
    def __str__(self):
        return json.dumps(self)

def get_content(listato):
    name = f"{listato[0]}"
    tipo = f"{listato[1]}"
    permessi = f"{listato[2]}"
    misura = f"{listato[3]}"
    if tipo == 'File':
        return f"[b][green]{name}[/b]\n[yellow]{tipo} [bold magenta]{permessi}\n[medium_violet_red]size: {misura} "
    else:
        return f"[b]{name}[/b]\n[red]{tipo} [bold magenta]{permessi}\n[medium_violet_red]size: {misura}"


def Tabella():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Type", style="cyan")
    table.add_column("Permission", style="navajo_white3",  justify="center")
    table.add_column("Size", style="red")
    table.add_column("Last Modified", style="yellow")
    table.add_column("Last Accessed", style="bright_green")
    table.add_column("Creation Time", style="medium_violet_red")

    for l in lista:
        file_name = l
        file_stats = os.stat(file_name)

        if stat.S_ISDIR(file_stats[stat.ST_MODE]):
            isdir= 'Directory'
            testa = '[yellow]'
            culo = '[/yellow]'
        else:
            isdir= 'File'
            testa = '[bold magenta]'
            culo = '[/bold magenta]'

        permission = oct(file_stats.st_mode)[-3:]

        file_info = {
            'fname': file_name,
            'fsize': file_stats [stat.ST_SIZE],
            'f_lm': time.strftime("%m/%d/%Y, %H:%M:%S",time.localtime(file_stats[stat.ST_MTIME])),
            'f_la': time.strftime("%m/%d/%Y, %H:%M:%S",time.localtime(file_stats[stat.ST_ATIME])),
            'f_ct': time.strftime("%m/%d/%Y, %H:%M:%S",time.localtime(file_stats[stat.ST_CTIME]))
        }

        table.add_row( testa + "%(fname)s" % file_info + culo, isdir, permission, "%(fsize)s bytes" % file_info, "%(f_lm)s" % file_info, " %(f_la)s" % file_info, " %(f_ct)s" % file_info)

    console.print(table)

def Tree():
    dz=[]
    for l in lista:
        file_name = l
        file_stats = os.stat(file_name)
        permission = oct(file_stats.st_mode)[-3:]
        misura = file_stats [stat.ST_SIZE]
        if stat.S_ISDIR(file_stats[stat.ST_MODE]):
            tipo = 'Directory'
            dz.append([file_name, tipo, permission, misura])

        else:
            tipo = 'File'
            dz.append([file_name, tipo, permission, misura])
    
    user_renderables = [Panel(get_content(z), expand=True) for z in dz]
    console.print(Columns(user_renderables))

try:
    if sys.argv [1] == '-l':
        lista = glob.glob('.*')
        Tabella()
    elif sys.argv [1] == '-t':
        lista = glob.glob('*')
        Tree()
    else:
        print(' Usage: pls or pls -l or pls -t')
except:
    lista = glob.glob('*')
    Tabella()
