from accessify import private

class Decryption:
    ''' Класс дешифрования
    '''

    @private
    def read_header(self: object) -> None:
        ''' Чтение заголовка .bmp
        '''
        self.f.read(self.header_size)

    @private
    def get_int(self: object) -> int:
        ''' Получение длины зашифрованной строки
        1. Считываем байт
        2. Преобразуем в двоичный вид
        3. Берем последний бит
        4. Переводим в число
        '''
        curr_hide_binary = ''
        for i in range(0, 16):
            curr_image_byte = self.f.read(1)
            
            if len(curr_image_byte) == 0:
                return ''
            
            curr_image_binary = '{0:08b}'.format(ord(curr_image_byte))
            curr_hide_binary += curr_image_binary[7]
        curr_hide_int = int(curr_hide_binary, 2)
        
        return curr_hide_int

    @private
    def get_char(self: object) -> str:
        ''' Получение зашифрованного сообщения
        1. Считываем байт
        2. Преобразуем в двоичный вид
        3. Берем последний бит
        4. Переводим в символ       
        '''
        curr_hide_binary = ''
        for i in range(0, 16):
            curr_image_byte = self.f.read(1)

            if len(curr_image_byte) == 0:
                return ''
                
            curr_image_binary = '{0:08b}'.format(ord(curr_image_byte))
            curr_hide_binary += curr_image_binary[7]
        curr_hide_char = chr(int(curr_hide_binary, 2))

        return curr_hide_char

    @private
    def ceasear(self: object, text: str) -> str:
        ''' Шифр Цезаря (дешифрование)
        '''
        SHIFT = 5
        N = 65535

        res = ''
        for c in text:
        
            c_index = ord(c)
            new_index = (c_index - SHIFT) % N

            new_unicode = new_index
            new_character = chr(new_unicode)
            res += new_character

        return res

    @private
    def get_hide(self: object) -> None:
        ''' Дешифровка сообщения
        '''
        curr_hide_int = self.get_int()
        for i in range(0, curr_hide_int):
            curr_hide_char = self.get_char()
            self.hide_msg += curr_hide_char
        self.f.close()
        self.hide_msg = self.ceasear(self.hide_msg)

    def run(self: object) -> str:
        ''' Запуск дешифрования
        '''
        self.read_header()
        self.get_hide()

        return self.hide_msg

    def __init__(self: object, new_file_name: str) -> None:
        ''' Поля класса
        '''
        self.new_file_name = new_file_name
        self.f = open(self.new_file_name, 'rb')
        self.hide_msg = ''
        self.header_size = 54