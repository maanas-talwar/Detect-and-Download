'''
        Author: Maanas Talwar
        Purpose: Temporary file to test scrapping
'''

from plugins.postgresql_plugin.code import postgresql

if __name__ == '__main__':
    a = postgresql()
    a.check_which_released()
