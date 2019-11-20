# Progamação Paralela e Distribuída
## Sistema proposto - Caça-niquel

### Descrição
 
- Será desenvolvido um 'Jogo de Dados - Caça-níquel' em Python. 

- Cliente insere um 'NOME' ao iniciar o sistema, em seguida tem disponível as opções 'VER RANKING' e 'INICIAR PARTIDA'.
- Ao iniciar a partida o cliente se conecta através de socket, enviando o 'NOME' e acontece o jogo. 
- Ao 'VER RANKING' o cliente se conecta através do socket, enviando 'RANKING' e recebendo o ranking geral.
- Antes do servidor ser iniciado, é disponibilizado as seguintes opções: 'THREADING' OU 'PROCESSOS'; Em ambas as opções o servidor fica constantemente ouvindo aguardando requisições. Se receber uma requisição com 'NOME' faz o sorteio dos dados retorna os 'NÚMEROS SORTEADOS', e a 'PONTUAÇÃO TOTAL'; Mas se a requisição chegar com 'RANKING' retorna um ranking geral do jogo.
