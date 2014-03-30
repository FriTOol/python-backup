#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gzip
import os
import time
import tarfile
from ftplib import FTP

try:
    from config import main_config
except ImportError:
    print('File "./config.py" not found.')
    exit()

UPLOADS_FILES = []


def get_database_list(config):
    """ Getting a list of databases to create a dump """
    if config['backups_targets']['databases'] == '__ALL__':
        databases = []
        database_list_command = config['mysql']['commands']['show_databases'].format(
            config['mysql']['user'],
            config['mysql']['password'],
            config['mysql']['host']
        )
        for database in os.popen(database_list_command).readlines():
            database = database.strip()
            if database not in config['backups_targets']['databases_excludes']:
                databases.append(database)
        return databases
    else:
        return config['backups_targets']['databases']


def database_backup(config):
    """ Creating a database dump """
    databases = get_database_list(config)
    for database in databases:
        print('MySQL Dump: ' + database)
        sql_backup_name = database + '_' + time.strftime('%Y-%m-%d') + '.sql'
        sql_backup_path = os.path.abspath(config['backups_dir'] + sql_backup_name)

        code = os.system(
            config['mysql']['commands']['dump'].format(
                config['mysql']['user'],
                config['mysql']['password'],
                database,
                sql_backup_path
            )
        )
        if code != 0:
            os.unlink(sql_backup_path)
        else:
            gz_sql_backup_path = sql_backup_path + '.gz'
            sql_file = open(sql_backup_path, 'rb')
            gz_sql_file = gzip.open(gz_sql_backup_path, 'wb')
            gz_sql_file.writelines(sql_file)
            sql_file.close()
            gz_sql_file.close()
            os.unlink(sql_backup_path)
            UPLOADS_FILES.append(gz_sql_backup_path)


def backup_files(config):
    """ Create an archive folder """
    for path in config['backups_targets']['dirs']:
        print('Архивация директории: ' + path)
        backup_name = config['backups_dir'] + os.path.basename(os.path.abspath(path)) + \
            '_' + time.strftime('%Y-%m-%d') + '.tar.bz2'

        with tarfile.open(backup_name, "w:gz") as tar:
            tar.add(
                name=path,
                arcname=os.path.abspath(path),
                exclude=lambda file: file in config['backups_targets']['dirs_excludes']
            )
        UPLOADS_FILES.append(backup_name)


def upload_backups(upload_files, config):
    """ Uploading files on the FTP server """
    for file in upload_files:
        print('Загрузка файла: ' + file)
        try:
            ftp = FTP()
            ftp.connect(config['ftp']['host'], 21)
            ftp.login(config['ftp']['user'], config['ftp']['password'])
            ftp.cwd(config['ftp']['dir_destination'])
            ftp.storbinary('STOR ' + os.path.basename(os.path.abspath(file)), open(file, 'rb'))
        except Exception as e:
            print(type(e))
            print(e.args)
            print(e)
            break
        else:
            ftp.quit()
            if config['delete_files_after_uploading']:
                os.unlink(file)


def main(config):
    config['backups_dir'] = os.path.abspath(config['backups_dir']) + os.sep
    if not os.path.exists(config['backups_dir']):
        print('Create folder ' + config['backups_dir'])
        os.mkdir(config['backups_dir'])

    database_backup(config)
    backup_files(config)
    upload_backups(UPLOADS_FILES, config)


if __name__ == '__main__':
    main(main_config)