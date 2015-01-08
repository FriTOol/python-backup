__author__ = 'fritool'

import sys

main_config = {
    # Folder for temporary storage of archives
    'backups_dir': sys.path[0] + '/backups/',

    # Delete files after uploading
    'delete_files_after_uploading': True,

    # Config MySQL
    'mysql': {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'commands': {
            # Console command to list all databases
            #
            # mysql -u {user} -p{password} -h {host} --silent -N -e "show databases"
            'show_databases': 'mysql -u {} -p{} -h {} --silent -N -e "show databases"',

            # Console command to dump the database
            'dump': 'mysqldump -u {} -p{} {} > {}'
        }
    },
    # FTP server to upload files
    'ftp': {
        'host': '192.168.0.1',
        'port': 21,
        'user': '',
        'password': '',

        # Folder on the server where the files will be uploaded
        'dir_destination': 'backup'
    },
    # Targets backup
    'backups_targets': {
        # List of databases for backup
        # In order to make a backup of all databases, you must specify the __ ALL__
        # 'databases': '__ALL__'
        #
        #
        # Or, you can list the names of databases
        # 'databases': [
        #   'test_db',
        #   'test_2',
        #   ...
        # ]
        'databases': '__ALL__',

        # Databases excludes
        'databases_excludes': [],

        # Absolute path to the folder for backup
        # 'dirs': [
        #    '/var/www/site1.com',
        #    '/var/www/site2.com'
        # ],
        'dirs': [
        ],

        # Absolute paths folders excludes
        # 'dirs_excludes': [
        #    '/var/www/site1.com/logs',
        #    '/var/www/site1.com/data/cache/',
        #    '/var/www/site2.com/vendor/',
        #    '/var/www/site2.com/composer.lock',
        # ],
        'dirs_excludes': [
        ],
    }
}