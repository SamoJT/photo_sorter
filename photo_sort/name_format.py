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
    return(f'{d}-{m}-{y}')

def rename(d, old, new, ext, c):
    try:
        new = f'{d}\\{new}_{str(f"{c:003d}")}{ext}'
        os.rename(old, new)
        return True
    except:
        return False
    
def main(d, allowed_ft):
    tot = 0
    for root, dirs, files in os.walk(d):
        if tot == 0:
            yield f'{len(dirs)} subdirectories'
        for name in files:
            full_path = os.path.join(root, name)
            fn, ext = os.path.splitext(full_path)
            if type(allowed_ft) == list:
                if ext.lstrip('.') not in allowed_ft:
                    yield f'Skipping: {name}'
                    yield f'Dissalowed FileType: {ext}'
                    continue
            c = 1
            date = get_taken(full_path)
            while not rename(root, full_path, date, ext, c):
                c += 1
            tot += 1
        yield f'Renamed {tot} files'
    return
