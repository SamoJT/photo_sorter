# Photo Sorter
### A Simple GUI tool for organising photos based on date taken. 
\
**Rename:**  Files in the chosen directory are renamed based on their 'Modified' date with the following schema - Photo No. is increased incrementally:
<pre>
  Day | Month | Year | Photo No. | Ext
   01  -  01   -  19  _  000     . JPG
</pre>
\
**Move, Both:** Files are moved (or both renamed then moved) from the chosen directory.
The program will create new directories in the parent of the current chosen directory ( . . / )\
\
Example of if 'Both' is chosen. \
*Note:* dir_of_photos would be empty.
<pre>
USER
└── Pictures
    ├── dir_of_photos   
    │   ├── 1.jpg
    │   └── 2.jpg
    └── 2021               - Generated
        ├── 01             - Generated
        │   └── 1_001.jpg  - Moved & Renamed
        └── 02             - Generated
            └── 2_001.jpg  - Moved & Renmaed
</pre>
\
Files can be hashed using MD5 if a FileExistsError is thrown - any files determined to be duplicate are left in the source directory.

---
Made using:
Python 3 and Tkinter