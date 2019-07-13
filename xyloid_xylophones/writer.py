import sys

try:
    filename = sys.argv[1]
except IndexError:
    print('need filename')
    sys.exit(1)

f = open(filename, 'wb')
val = input('> ')

while val.strip() != '':
    try:
        val = bytes([int(val)])
        f.write(val)
    except ValueError:
        print('unable to write, please try again')
    val = input('> ')

f.close()
