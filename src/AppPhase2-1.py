import sys

from module import FileInput
from module import FileOutput
from module import Elgamal
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')


def main():
    bit_size = int(config['config_elgamal']["bit_size"])
    random_file_path = config['random_file']['path']
    input_file_path = config['input_file']['path']
    cipher_file_path = config['cipher_file']['path']
    output_file_path = config['output_file']['path']
    public_key_path = config['public_key']['path']
    private_key_path = config['private_key']['path']

    #Set Up
    key = Elgamal.elgamalKeyGen(bit_size=bit_size, random_file=random_file_path)
    FileOutput.saveKeyTofile(key=key, public_key_path=public_key_path, private_key_path=private_key_path)

    #Encrypt
    public_key = FileInput.readPublicKeyFromFile(public_key_path=public_key_path)
    binary_input_file = FileInput.readBinaryFromFile(input_file_name=input_file_path)
    print(f"input length: {len(binary_input_file)}")
    cipher_text = Elgamal.elgamalEncrypt(p=public_key.p, g=public_key.g, y=public_key.y, binary_data=binary_input_file)
    FileOutput.writeBinaryToFileHandlePostPadding(binary_data=cipher_text, output_file_path=cipher_file_path)

    #Decrypt
    private_key = FileInput.readPrivateKeyFromFile(private_key_path=private_key_path)
    binary_cipher_text_read_from_file = FileInput.readBinaryFromFileHandlePostPadding(input_file_name=cipher_file_path,
                                                                                      block_size=bit_size)
    message = Elgamal.elgamalDecrypt(u=private_key.u, p=private_key.p, binary_cipher_text=binary_cipher_text_read_from_file)
    FileOutput.writeBinaryToFile(binary_data=message, output_file_path=output_file_path)


if __name__ == "__main__":
    main()
