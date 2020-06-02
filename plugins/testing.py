'''
        Author: Maanas Talwar
        Purpose: testing the function of plugins

'''

from postgresql.code import postgresql

if __name__ == '__main__':
    print('*****  Start Execution  *****')

    a = postgresql()
    a.update_json()

    print('*****  End Execution  *****')
