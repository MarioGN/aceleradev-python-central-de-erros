# Central de Erros

Sistema para centralizar registros de erros de aplicações. Projeto prático final da aceleração Python da codenation.

## Como desenvolver?

1. Clone o repositório.
2. Crie um virtualenv com Python3.8
3. Ative o virtualenv.
4. Instale as dependências.
5. Configura a instância com o .env
6. Execute os testes

```console
git clone git@github.com:MarioGN/aceleradev-python-central-de-erros.git aceleradev-central-erros
cd aceleradev-central-erros
python -m venv .central
source .central/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```


## Como fazer o deploy?

1. Crie uma instância no heroku.
2. Envie as configurações para o heroku.
3. Defina uma SECRET_KEY segura para a instância.
4. Defina DEBUG=False
5. Defina ALLOWED_HOSTS=.herokuapp.com
6. Envie o código para o heroku.

```console
heroku create minhainstancia
heroku git:remote -a minhainstancia
heroku config:set SECRET_KEY='python contrib/secret_gen.py'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=.herokuapp.com
git push heroku master --force
```