import glob
from rich.console import Console
from rich.table import Table
import os
import stat
import time
import sys

console = Console()
try:
    if sys.argv [1] == '-l':
        lista = glob.glob('.*')
    else:
        print(' Usage: pls or pls -l')
except:
    lista = glob.glob('*')


table = Table(show_header=True, header_style="bold magenta")
table.add_column("Name", style="green")
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
        testa = '[bold magenta]'
        culo = '[/bold magenta]'
    else:
        isdir= 'File'
        testa = '[yellow]'
        culo = '[/yellow]'

    permission = oct(file_stats.st_mode)[-3:]

    file_info = {
        'fname': file_name,
        'fsize': file_stats [stat.ST_SIZE],
        'f_lm': time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(file_stats[stat.ST_MTIME])),
        'f_la': time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(file_stats[stat.ST_ATIME])),
        'f_ct': time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(file_stats[stat.ST_CTIME]))
    }

    table.add_row( testa + "%(fname)s" % file_info + culo, isdir, permission, "%(fsize)s bytes" % file_info, "%(f_lm)s" % file_info, " %(f_la)s" % file_info, " %(f_ct)s" % file_info)


console.print(table)
