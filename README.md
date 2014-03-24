Python-Backup
=============
Python script to backup databases and files.

Installation
------------

1. Rename the file config.example.py to config.py.

2. Customize configs:

**backups_dir** - local directory for storing archives
**delete_files_after_uploading** - delete local files after uploading on the FTP server

Targets backup (**backups_targets**):

**databases** - the list of databases to create a list damp. If you specify a string instead of a list "\_\_ALL\_\_" then all databases will be backup

**databases_excludes** - a list of databases that you want to exclude for backup. (Use for 'databases': '\_\_ AL_\_')

**dirs** - a list of absolute paths to folders for which you want to backup

**dirs_excludes** - a list of absolute paths to folders that should be excluded from backups

3.Run:

```
python backup.py 
```