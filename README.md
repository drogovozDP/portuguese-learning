# portuguese-learning

```bash
cp .env.example .env
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Example dict structure:

```txt
# Неправильные глаголы на -er
ver | видеть # test
eu vejo | я вижу
tu vês | ты видишь
ele/ela/você vê | он/она видит
nós vemos | мы видим
eles/elas/vocês veem | они видят
---
ler | читать
eu  leio | я читаю
tu lês | ты читаешь
ele/ela/vocē lê | он/она читает
nós lemos | мы читаем
eles/elas/vocēs leem | они читают
```
