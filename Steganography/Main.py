import Decryption as Dec
import Encryption as Enc

if __name__ == "__main__":
    INPUT_FILEPATH = 'Lab_6\input\Безымянный.bmp'
    OUTPUT_FILEPATH = 'Lab_6\output\Безымянный.bmp'
    TEXT = "Привет, мир!"

    encryption = Enc.Encryption(INPUT_FILEPATH, OUTPUT_FILEPATH, TEXT)
    encryption.run()
    print('Шифрование выполнено успешно!')

    decryption = Dec.Decryption(OUTPUT_FILEPATH)
    decry_msg = decryption.run()
    print('Расшифрованное сообщение: "' + decry_msg + '".')