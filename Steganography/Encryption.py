from accessify import private

class Encryption:
    ''' Класс шифрования
    '''

    @private
    def open_file(self: object) -> None:
        ''' Чтение данных из файла
        '''
        with open(self.origin_file_name, 'rb') as f:
            self.origin_image_data = f.read()
    
    @private
    def copy_header(self: object) -> None:
        ''' Перенос шапки изображения в новый файл
        1. Шапка - 54 байта
        '''
        for i in range(0, self.header_size):
            self.new_image_data.append(self.origin_image_data[i])
            self.bytes_counter += 1

    @private
    def hide_int(self: object, curr_hide_int: int) -> None:
        ''' Шифрование длины сообщения
        1. Длина сообщения (число) - 2 байта
        2. Преобразуем каждый байт цвета в двоичный вид
        3. Меняем последний бит
        4. Преобразовываем обратно в число
        '''
        curr_hide_binary = '{:016b}'.format(curr_hide_int)    

        for i in range(0, 16):
            curr_image_binary = '{0:08b}'.format(self.origin_image_data[self.bytes_counter])
            new_image_binary = curr_image_binary[:len(curr_image_binary)-1] + curr_hide_binary[i] 
            new_image_int = int(new_image_binary, 2)
            self.new_image_data.append(new_image_int)
            self.bytes_counter += 1

    @private
    def hide_char(self: object, curr_hide_byte: str) -> None:
        ''' Шифрование символа сообщения
        1. Символ сообщения - 2 байта
        2. Преобразуем каждый байт цвета в двоичный вид
        3. Меняем последний бит
        4. Преобразуем обратно в число
        '''
        curr_hide_binary = '{0:016b}'.format(ord(curr_hide_byte))

        for i in range(0, len(curr_hide_binary)):
            curr_image_binary = '{0:08b}'.format(self.origin_image_data[self.bytes_counter])
            new_image_binary = curr_image_binary[:len(curr_image_binary)-1] + curr_hide_binary[i] 
            new_image_int = int(new_image_binary, 2)
            self.new_image_data.append(new_image_int)
            self.bytes_counter += 1

    @private
    def ceasear(self: object, text: str) -> str:
        ''' Шифр Цезаря (шифрование)
        '''
        SHIFT = 5
        N = 65535

        res = ''
        for c in text:
        
            c_index = ord(c)
            new_index = (c_index + SHIFT) % N

            new_unicode = new_index
            new_character = chr(new_unicode)
            res += new_character

        return res

    @private
    def do_hide(self: object) -> None:
        ''' Шифрование сообщения
        1. Шифруем длину сообщения
        2. Шифруем сообщение посимвольно
        '''
        self.hide_msg = self.ceasear(self.hide_msg)

        self.hide_int(len(self.hide_msg))      
        for i in range(0, len(self.hide_msg)):
            self.hide_char(self.hide_msg[i])

    @private
    def copy_rest(self: object) -> None:
        ''' Копирование неиспользованных данных
        в новое изображение
        '''
        left_data = self.origin_image_data[self.bytes_counter:]
        for left_byte in left_data:
            self.new_image_data.append(left_byte)      

    @private
    def write_file(self: object) -> None:
        ''' Сохранение нового изображения
        '''
        with open(self.new_file_name, 'wb') as out:                            
            new_image_bytes = bytearray(self.new_image_data)
            out.write(new_image_bytes)

    def run(self: object) -> None:
        ''' Запуск шифрования
        '''
        self.open_file()
        self.copy_header()
        self.do_hide()
        self.copy_rest()
        self.write_file()

    def __init__(self: object, origin_file_name: str, new_file_name: str, hide_msg: str) -> None:
        ''' Поля класса
        '''
        self.origin_file_name = origin_file_name
        self.new_file_name = new_file_name
        self.hide_msg = hide_msg
        self.bytes_counter = 0
        self.origin_image_data = ''
        self.new_image_data = []
        self.header_size = 54