import socket
import http.server
import socketserver
import os


def my_ip():
    """This function returns the IP address of the computer."""

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        my_socket.connect(('10.255.255.255', 1))
        this_ip = my_socket.getsockname()[0]
    except Exception:
        this_ip = '127.0.0.1'
    finally:
        my_socket.close()
    return this_ip


def create_share_page(to_share, file_name):
    """This function transforms its input into a web page with both a link
       and an input box with accompanying button that copies its contents into
       the clipboard.
    """

    with open(file_name, 'w') as file:
        file.write('<!DOCTYPE html>\n')
        file.write('<html>\n    <head>\n')
        file.write('            <meta name="viewport" content='
                   '"width=device-width, initial-scale=2.0">\n')
        file.write('            <link rel="icon" href="data:,">\n')
        file.write('    </head>\n\n')
        file.write('    <body>\n')
        file.write('        <div>\n')
        file.write('            <a href="')
        file.write(to_share)
        file.write('">Link:  ')
        file.write(to_share)
        file.write('</a>\n')
        file.write('        </div>\n        <br>\n\n')
        file.write('        <div>\n')
        file.write('            <input id="txt" value="')
        file.write(to_share)
        file.write('"/>\n')
        file.write('            <button class="button" id="btn">'
                   'Copy</button>\n')
        file.write('        </div>\n\n\n')
        file.write("        <script>\n")
        file.write("            const txt = document.querySelector('#txt')\n")
        file.write("            const btn = document.querySelector('#btn')\n")
        file.write("            const copy = (text) => {\n")
        file.write("                const textarea = document.createElement"
                   "('textarea')\n")
        file.write("                document.body.appendChild(textarea)\n")
        file.write("                textarea.value = text\n")
        file.write("                textarea.select()\n")
        file.write("                document.execCommand('copy')\n")
        file.write("                textarea.remove()\n")
        file.write("            }\n\n")
        file.write("            btn.addEventListener('click', (e) => {\n")
        file.write("                copy(txt.value)\n")
        file.write("            }\n")
        file.write("        </script>\n")
        file.write('    </body>\n</html>')


def start_server():
    """Starts up a simple webserver and informs the user where to find its
       content.
    """
    httpd = None
    print(f'Enter this address into browser:\nhttps://{my_ip()}:8000/')
    print('Press Ctrl-C when finished to stop server')
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    try:
        httpd = socketserver.TCPServer(("", port), handler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        httpd.server_close()


def get_info():
    """Asks the user for the info they want to share."""
    to_share = input("Paste/input text to share:\n")
    file_name = input("Name of file if you wish to save"
                      "(blank for default):\n")

    if file_name == "":
        file_name = "index"
    file_name += ".html"
    return to_share, file_name


def main():
    start = (get_info())
    create_share_page(*start)
    start_server()

    # Deletes the created file if the user chose the default option
    if start[1] == 'index.html':
        os.remove(start[1])


if __name__ == '__main__':
    main()
