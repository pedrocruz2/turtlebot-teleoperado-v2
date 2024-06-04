Para Rodar esse projeto é necessário ter o python instalado e as dependências:
- rclpy
- opencv-python
- websockets
- flask
Todas elas estão citadas no arquivo requirements.txt, para instalar elas deve-se rodar o comando ```pip install -r requirements.txt``` na diretória raiz desse projeto.

Com todas as dependências instaladas, primeiro é necessário instanciar o servidor de websocket rodando em um terminal o comando ```python3 server.py```

Em Outro terminal, é preciso rodar outros 2 comandos.
O primeiro é ``` export FLASK_APP=page_server``` e depois ```flask run```, ambos na diretória raiz do projeto.
