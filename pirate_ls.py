import glob
from rich import print
from rich.console import Console
from rich.table import Table
from rich import print
from rich.columns import Columns
from rich.panel import Panel
from rich import print
from pwd import getpwuid
from grp import getgrgid
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
    vis = listato[4]
    if tipo == 'File':
        tipo = '\U0001F4C4'
        return f"[b][green]{name}[/b]\n[yellow]{tipo} [bold magenta]{permessi} {vis}\n[medium_violet_red]size: {misura} "
    else:
        tipo = "\U0001F4C1"
        return f"[b]{name}[/b]\n[red]{tipo} [bold magenta]{permessi} {vis}\n[medium_violet_red]size: {misura}"

def get_list(listato,vis):
    dz=[]
    for l in listato:
        file_name = l
        file_stats = os.stat(file_name)
        permission = oct(file_stats.st_mode)[-3:]
        misura = file_stats [stat.ST_SIZE]
        if stat.S_ISDIR(file_stats[stat.ST_MODE]):
            tipo = 'Directory'
            dz.append([file_name, tipo, permission, misura, vis])
        else:
            tipo = 'File'
            dz.append([file_name, tipo, permission, misura, vis])
    return dz

def get_file_ownership(filename):
    return (
        getpwuid(os.stat(filename).st_uid).pw_name,
        getgrgid(os.stat(filename).st_gid).gr_name
    )

def Tabella():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name")
    table.add_column("User", style="cyan")
    table.add_column("Group", style="#FF7F1D")
    table.add_column("Type", style="#0FA4FF")
    table.add_column("Permission", style="navajo_white3")
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
        permission_ = stat.filemode(file_stats.st_mode)
        ug = get_file_ownership(l)

        file_info = {
            'fname': file_name,
            'fsize': file_stats [stat.ST_SIZE],
            'f_lm': time.strftime("%d/%m/%Y, %H:%M:%S",time.localtime(file_stats[stat.ST_MTIME])),
            'f_la': time.strftime("%d/%m/%Y, %H:%M:%S",time.localtime(file_stats[stat.ST_ATIME])),
            'f_ct': time.strftime("%d/%m/%Y, %H:%M:%S",time.localtime(file_stats[stat.ST_CTIME]))
        }

        table.add_row( testa + "%(fname)s" % file_info + culo, ug[0], ug[1] ,isdir, permission + ' ' + permission_, "%(fsize)s bytes" % file_info, "%(f_lm)s" % file_info, " %(f_la)s" % file_info, " %(f_ct)s" % file_info)

    console.print(table)

def Tree():
    dz = get_list(lista,'\U0001F440')
    dz2 = get_list(lista2,'\U0001F47B')
    dz.extend(dz2)

    user_renderables = [Panel(get_content(z), expand=True) for z in dz]
    console.print(Columns(user_renderables))

try:
    if sys.argv [1] == '-l':
        lista =sorted(glob.glob('.*'))
        Tabella()
    elif sys.argv [1] == '-t':
        lista =sorted(glob.glob('*'))
        lista2 =sorted(glob.glob('.*'))
        Tree()
    else:
        print(":pirate_flag:",'[bold spring_green3] Usage: [/bold spring_green3][italic dark_orange3]pls [/italic dark_orange3]or [italic dark_orange3]pls -l[/italic dark_orange3] or [italic dark_orange3]pls -t[/italic dark_orange3]')
except:
    lista =sorted(glob.glob('*'))
    Tabella()
