import pathlib
import datetime
import os

#######################################
# Renames photos to defined standard: #
#  Day | Month | Year | Photo No.     #
#  01  |  01   |  19  |    000        #
#######################################


def get_taken(file_path):
    # Get date photo was taken and format it
    
    f = pathlib.Path(file_path)
    timestamp = f.stat().st_mtime
    date = datetime.datetime.fromtimestamp(timestamp)
    d, m, y = str(date.day), str(date.month), str(date.year)
    
    if len(d) != 2:
        d = '0' + d
    if len(m) != 2:
        m = '0' + m
    y = y[2:4]
    return(f'{d}-{m}-{y}_')

def rename(d, old, new, ext, c):
    try:
        new = f'{d}\\{new}{str(f"{c:003d}")}{ext}'
        os.rename(old, new)
        return True
    except:
        return False
    
def main(d):
    tot = 0
    for root, dirs, file in os.walk(d):
        if tot == 0:
            yield f'{len(dirs)} subdirectories'
            
        for name in file:
            full_path = os.path.join(root, name)
            c = 1
            date = get_taken(full_path)
            fn, ext = os.path.splitext(full_path)
            while not rename(root, full_path, date, ext, c):
                c += 1
            tot += 1
        yield f'Renamed {tot} files'
    return
