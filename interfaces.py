import requests

def console_interface(host = 'localhost', port=9000):
    session = requests.Session()
    CONTINUE = True
    while CONTINUE:
        entrada = input("Você: ")
        if entrada.startswith('!'):
            pass
        else:
            dest = "http://{}:{}/message".format(host, port)
            data = {
                'message' : entrada
            }
            response = session.post(dest, json=data)
            if response.status_code == 200:
                answer = response.json()
                message = answer['response']
                print("Bot: %s" % message)

if __name__ == '__main__':
    console_interface()