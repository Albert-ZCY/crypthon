import sys
import os
from crypt import *

class Config():
    def __init__(self, argv):
        self.argv = argv[1:]
        self.helpinf = """
        ####################################################
        Crypthon v0.5.0
        (c) 2021 PointCode Corporation (a) author Albert Z.

        Commands with Arguments:
            help                  get extra help information

            encrypt *filename*      encrypt the certain file

                -ni             (defult) ues system assigned
                                    cryption, CAN BE DIRECTLY 
                                RUNED BUT CANNOT BE DECRIPTED

                -ti                 use three-itme cryption,
                                        CAN BE DECRIPTED BUT 
                                        CANNOT BE DIRECTLY RUN

                -fi                  use four-item cryption,
                                        CAN BE DECRIPTED BUT 
                                        CANNOT BE DIRECTLY RUN

            decrypt *filename*      decrypt the certain file

                -ti                  use three-itme cryption
                -fi                   use four-item cryption

            run *filename*         directly run the certain, 
                                        file without decrypting

                            THE         END
        ####################################################
        """
        self.parseCommand()

    def parseCommand(self):
        self.com = []
        self.arg = []
        for item in self.argv:
            if item.startswith('-'):
                self.arg.append(item)
            else:
                self.com.append(item)
        if self.com:
            if self.com[0] != 'help':
                self.opath = self.com[1]
                ofile = open(self.opath, 'r')
                self.content = ofile.read()
                ofile.close()
            self.call()
        else:
            self.quit('Not enough commands. Help Information:\n'+self.helpinf)

    def call(self):
        if self.com[0] == 'help':
            print(self.helpinf)
        elif self.com[0] == 'encrypt':
            if '-fi' in self.arg:
                self.mode = 'CBC'
                print('Please *input* and *remember* the values below.')
                self.head = input('crypt-head: ')
                self.key = input('crypt-key: ')
                self.iv = input('crypt-iv-key: ')
                if self.head and self.key and self.iv:
                    self.crypt = AbstractCrypt(self.mode, self.head, self.key, self.iv)
                    self.content = self.crypt.encrypt(self.content)
                    self.spath = self.opath.replace('.py', '.crp')
                    sfile = open(self.spath, 'w')
                    sfile.write(self.content)
                    sfile.close()
                else:
                    self.quit('Invalid input.')
            elif '-ti' in self.arg:
                self.mode = 'ECB'
                print('Please *input* and *remember* the values below.')
                self.head = input('crypt-head: ')
                self.key = input('crypt-key: ')
                if self.head and self.key:
                    self.crypt = AbstractCrypt(self.mode, self.head, self.key)
                    self.content = self.crypt.encrypt(self.content)
                    self.spath = self.opath.replace('.py', '.crp')
                    sfile = open(self.spath, 'w')
                    sfile.write(self.content)
                    sfile.close()
                else:
                    self.quit('Invalid input.')
            else:
                self.mode = 'CBC'
                self.head = 'CrypthonEncript'
                self.key = 'pcadm2021'
                self.iv = 'pointcode'
                self.crypt = AbstractCrypt(self.mode, self.head, self.key, self.iv)
                self.content = self.crypt.encrypt(self.content)
                self.spath = self.opath.replace('.py', '.crp')
                sfile = open(self.spath, 'w')
                sfile.write(self.content)
                sfile.close()

        elif self.com[0] == 'decrypt':
            if '-fi' in self.arg:
                self.mode = 'CBC'
                print('Please *input* the values below.')
                self.head = input('crypt-head: ')
                self.key = input('crypt-key: ')
                self.iv = input('crypt-iv-key: ')
                if self.head and self.key and self.iv:
                    try:
                        self.crypt = AbstractCrypt(self.mode, self.head, self.key, self.iv)
                        self.content = self.crypt.decrypt(self.content)
                        self.spath = self.opath.replace('.crp', '.py')
                        sfile = open(self.spath, 'w')
                        sfile.write(self.content)
                        sfile.close()
                    except:
                        self.quit('Incrrect key values or arguments.')
                else:
                    self.quit('Invalid input.')
            elif '-ti' in self.arg:
                self.mode = 'ECB'
                print('Please *input* the values below.')
                self.head = input('crypt-head: ')
                self.key = input('crypt-key: ')
                if self.head and self.key:
                    try:
                        self.crypt = AbstractCrypt(self.mode, self.head, self.key)
                        self.content = self.crypt.decrypt(self.content)
                        self.spath = self.opath.replace('.crp', '.py')
                        sfile = open(self.spath, 'w')
                        sfile.write(self.content)
                        sfile.close()
                    except:
                        self.quit('Incrrect key values or arguments.')
                else:
                    self.quit('Invalid input.')

        elif self.com[0] == 'run':
            self.dir = os.path.dirname(self.opath)
            self.pre = f'''
import sys

sys.path[0] = "{self.dir}"\n'''
            try:
                self.mode = 'CBC'
                self.head = 'CrypthonEncript'
                self.key = 'pcadm2021'
                self.iv = 'pointcode'
                self.crypt = AbstractCrypt(self.mode, self.head, self.key, self.iv)
                self.content = self.crypt.decrypt(self.content)

                self.code = self.pre + self.content
            except:
                self.quit('Four-item crypted or three-item crypted files cannot be directly run. Please use the key values to decrypt them first.')
            else:
                exec(self.code)
        else:
            self.quit('Not an allowed command')

    def quit(self, info):
        print('fatal: '+info)
        sys.exit(0)


if __name__ == '__main__':
    main = Config(sys.argv)
