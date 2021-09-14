import os
import pathlib
import datetime
import hashlib
from name_format import rename as suffix_increment

'''
Move photos to dir based on YYYY/MM taken.
Automatically create dir if doesn't exist.
Hashes files with duplicate file name to 
determine if contents is same - if not rename
with prefix and move to correct dir.
'''

def check_dir(root, y, m):
    # Check if dir exists, create if not.
    o = []
    try:
        assert os.path.isdir(root+str(y))
        o.append(f'/{y} Exists')
    except AssertionError:
        o.append(f'Making directory: {y}')
        os.mkdir(root+str(y))
    try:
        assert os.path.isdir(root+str(y)+'\\'+str(m))
        o.append(f'/{y}/{m} Exists')
    except AssertionError:
        o.append(f'Making directory: {y}/{m}')
        os.mkdir(root+str(y)+'\\'+str(m))
    return o

def hasher(f1, f2):
    # Create hash of both files, add to set,
    # if set has two items, files not duplicate.
    
    buf = 65536
    md5 = hashlib.md5()
    cmpr = set()
    
    f = f1
    for _ in range(2):
        with open(f, 'rb') as f:
            while True:
                data = f.read(buf)
                if not data:
                    break
                md5.update(data)
        cmpr.add(md5.hexdigest())
        f = f2
    if len(cmpr) == 2:
        return False  # Return false if 2 different hashes therefore files dif.
    else:
        return True

def get_ym(f):
    f = pathlib.Path(f)
    timestamp = f.stat().st_mtime
    date = datetime.datetime.fromtimestamp(timestamp)
    y = date.year
    m = date.month
    
    if y < 10:
        y = '0' + str(y)
    if m < 10:
        m = '0' + str(m)

    return str(y), str(m)
    
def main(d, allowed_ft, hashing):
    target_root = os.path.dirname(d)  # Full path to folders where photos are stored
    dupes = []
    for root, dirs, files in os.walk(d):
        for name in files:
            fn, ext = os.path.splitext(root+name)
            if type(allowed_ft) == list:
                if ext.lstrip('.') not in allowed_ft:
                    yield f'Skipping: {name}'
                    yield f'Dissalowed FileType: {ext}'
                    continue
            full_path = f'{root}/{name}'
            y, m = get_ym(full_path)
            target_root = f'{target_root}/'
            for i in check_dir(target_root, y, m):
                yield i
            dest = target_root + y + '/' + m + '/'
            try:
                yield f'Moving {name} to {y}/{m}'
                os.rename(full_path, dest + name)
                if hashing:
                    yield f'Hashing not required: {name}'           
            except FileExistsError:
                c = 1
                if hashing:
                    yield 'Hashing to determine if duplicate'
                    if hasher(full_path, dest + name):
                        dupes.append([name, (y,m)])
                        yield f'Skipping {name} due to hash verified duplicate in {y}/{m}'
                        continue

                yield 'File name clash - adding suffix'
                while not suffix_increment(root, full_path, name.rstrip(ext), ext, c):
                    c += 1
                main(d, allowed_ft, hashing)  # Horrible way of doing it as iterating through twice.