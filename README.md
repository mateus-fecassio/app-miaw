# Bot de Votação - MTV Miaw 2022
Projeto criado como tentativa a fazer Samira Close vencer o prêmio de Streamer do Ano na premiação MTV Miaw 2022.


# Tecnologias Utilizadas
- Python / Jupyter Notebook;
- Selenium;
- Threads.


# Deploy no Heroku
Esse projeto foi desenvolvido para utilizar o Heroku como servidor para votação. Para que isso fosse possível, foi preciso utilizar algumas configurações no aplicativo que foi feito deploy para que a biblioteca Selenium pudesse ser utilizada para manipulação das páginas de votação. Os passos para esse deploy, baseados nessa [fonte](https://www.andressevilla.com/running-chromedriver-with-python-selenium-on-heroku/) são:


### Passo 1:
No Heroku, abra seu App. Clique em Settings e role a página até Buildpacks. Adicione o seguinte:

- Python (Selecione o Python dos buildpacks oficiais suportados)
- Headless Google Chrome: https://github.com/heroku/heroku-buildpack-google-chrome
- Chromedriver: https://github.com/heroku/heroku-buildpack-chromedriver

### Passo 2:
Vá até a seção de configuração de variáveis. Aqui, nós adicionaremos os caminhos para o Chrome e o Chromedriver. Adicione o seguinte:

```
CHROMEDRIVER_PATH = /app/.chromedriver/bin/chromedriver
GOOGLE_CHROME_BIN = /app/.apt/usr/bin/google-chrome
```