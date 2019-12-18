# Conjunto de ferramentas para medição 2
Conjunto de ferramentas automatizam o processo de processamento e controle de qualidade da medição de pontos de controle.
Essas ferramentas complementam as rotinas disponíveis em https://github.com/1cgeo/ferramentas_pto_controle, que devem ser utilizadas em conjunto!
Rotinas disponíveis neste repositório:
* 5- Gerar PPP
* 7- Atualizar banco com dados do PPP
* 8- Gerar Monografia

## Instalação
Certifique-se de ter instalado no seu computador as últimas versões do [NodeJS](https://nodejs.org/en/download/) e do [Python 3.X](https://www.python.org/downloads/)
Para instalar as dependências necessárias utilize os seguintes comandos:
```
npm install -g testcafe@0.17.2
pip install -r requirements.txt
```

### 5- Gerar PPP
Esta rotina acessa o portal do IBGE e realiza o download do processamento realizado pela plataforma de PPP do IBGE.
Os parâmetros necessários para essa rotina são:
* Navegador a ser utilizado (chrome ou firefox)
* Pasta com a estrutura de pontos de controle
* Pasta na qual será realizada o download do PPP
* Email
```
testcafe -c 3 chrome upload_ppp.js D:\2018-04-06 D:\downloads\ppp test@email.com.br
```

### 7- Atualizar banco com dados do PPP
Esta rotina atualiza o banco de dados com os dados do PPP.
Os parâmetros necessários para essa rotina são:
* Parâmetros de conexão do banco:
    * Host
    * Nome do Banco
    * Usuário
    * Senha
* Pasta com a estrutura de pontos de controle
```
python refreshFromPPP.py localhost banco_pt_controle postgres postgres D:\2018-04-06
```

### 8- Gerar Monografia
Esta rotina gera monografias baseadas no [Modelo](modelo.odt) em formato ODT.
Para utilizar esta rotina é necessário que o LibreOffice esteja instalado no computador.
Os parâmetros necessários para essa rotina são:
* Parâmetros de conexão do banco:
    * Host
    * Nome do Banco
    * Usuário
    * Senha
* Pasta com a estrutura de pontos de controle OU Pasta com várias estruturas de pontos de controle
```
python generateMono.py localhost banco_pt_controle postgres postgres D:\2018-04-06
```