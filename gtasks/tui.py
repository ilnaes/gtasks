import sys
import tty
import termios


buffer = ['0', '0']


def csi(s):
    sys.stdout.write('\x1b['+s)


def main():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin)

    while True:
        sys.stdout.write(buffer[0] + '\r\n' + buffer[1] + '\r\n')

        char = sys.stdin.read(1)
        if ord(char) == 17:
            break

        csi('2A')
        csi('J')

        buffer[0], buffer[1] = buffer[1], str(ord(char))

    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


if __name__ == '__main__':
    main()
