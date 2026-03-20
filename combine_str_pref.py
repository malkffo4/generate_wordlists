'''
if select 1 file, encode with base64
else, combine file
'''
import base64

def merge_with_add(file1:str, file2:str, symbol):
    with open(file2, 'r') as f2_list_r:
        f2_list = f2_list_r.readlines()
        with open(file1, 'r') as f1_list_r:
            f1_list = f1_list_r.readlines()

            for f2 in f2_list:
                f2 = f2[:-1]
                for f1 in f1_list:
                    f1 = f1[:-1]
                    print(f'{f1}{symbol}{f2}')

def encode_list(file:str):
    with open(file) as f:
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]
            
            encoded = base64.b64encode(bytes(line, 'utf-8'))
            print(encoded.decode("utf-8"))

def main():
    import sys

    if len(sys.argv) == 4:
        merge_with_add(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 2:
        encode_list(sys.argv[1])
    else:
        print(f'{sys.argv[0]} file1 file2 symbol')
        print(f'{sys.argv[0]} file')
    
if __name__ == '__main__':
    main()