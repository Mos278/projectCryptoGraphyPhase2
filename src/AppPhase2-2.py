from module import FileInput
from module import FileOutput
from module import Elgamal
from module import HashFunction
from module import ConvertDataType
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
    public_key_receiver_path = config['public_key_receiver']['path']
    private_key_path = config['private_key']['path']

    # Set Up
    key = Elgamal.elgamalKeyGen(bit_size=bit_size, random_file=random_file_path)
    FileOutput.saveKeyTofile(key=key, public_key_path=public_key_path, private_key_path=private_key_path)

    # get Key
    public_key = FileInput.readPublicKeyFromFile(public_key_path=public_key_path)
    public_key_receiver = FileInput.readPublicKeyFromFile(public_key_path=public_key_receiver_path)
    private_key = FileInput.readPrivateKeyFromFile(private_key_path=private_key_path)


    # Encrypt
    binary_input_file = FileInput.readBinaryFromFile(input_file_name=input_file_path)
    print(f"input length: {len(binary_input_file)}")
    sign_message_text = Elgamal.elgamalSignature(binary_data=binary_input_file, p=public_key.p,
                                                 g=public_key.g, u=private_key.u)

    sign_cipher_text = Elgamal.elgamalEncrypt(p=public_key_receiver.p, g=public_key_receiver.g,
                                              y=public_key_receiver.y, binary_data=sign_message_text)

    FileOutput.writeBinaryToFileHandlePostPadding(binary_data=sign_cipher_text, output_file_path=cipher_file_path)


    # Decrypt
    binary_sign_cipher_text_read_from_file = FileInput.readBinaryFromFileHandlePostPadding(
        input_file_name=cipher_file_path, block_size=len(ConvertDataType.intToBinary(public_key.p)))

    sign_message_text = Elgamal.elgamalDecrypt(u=private_key.u, p=public_key.p,
                                     binary_cipher_text=binary_sign_cipher_text_read_from_file)

    verify, message = Elgamal.elgamalVerification(
        sign_text=sign_message_text, p=public_key_receiver.p, g=public_key_receiver.g,
        y=public_key_receiver.y)

    FileOutput.writeBinaryToFile(binary_data=message, output_file_path=output_file_path)
    print(f"Verify Signature: {verify}")


if __name__ == "__main__":
    main()  # encrypt - sign cipher text and decrypt - verify signature
