#### Запуск
```sh
docker compose build
docker compose up
```

#### Предустановленные пользователи
| username  | password |
| ------------- | ------------- |
| admin  | admin  |
| user1  | user1  |
| user2  | user2  |

#### wallet admin предоставляет 3 модели:
- Wallet holders
- Wallets
- Transactions

### Wallet holders / Держатели кошельков
это пользователи системы кошельков
у каждого из них может быть 0-N кошельков

### Wallets / Кошельки
у каждого кошелька есть:
- 1 владелец
- 1 уникальный идентификатор (uid) - с помощью них происходят транзакции средств
- баланс
- идентификатор валюты (RUB/USD)
кошельки должны/могут:
- делать переводы другим кошелькам с совпадающим идентификатором валюты
- отправлять не больше, чем есть на балансе

### Transactions / Транзакции
создаются каждый раз, когда один кошелек делает перевод другому. Собственно, транзакция - это есть процесс и совершенное действие, указывающее, что: у отправителя (Sender) уменьшился баланс на X-значение, а у получателя (Receiver) увеличился баланс на X-значение.
Не стоит пытаться создать транзакцию через django админ-панель. Все транзакции создаются через POST-запрос (application/json) следующего типа:

> http://127.0.0.1:8002/api/wallets/transactions/
```json
{
    "sender": "c842fe5e-68a8-4104-be64-de8aec121102", // uid кошелька пользователя/отправителя
    "receiver": "13c04cb5-4e3c-40eb-bca0-398324cf0ea7", // uid кошелька получателя
    "amount": "125.00", // отправляемая сумма
    "currency": "USD"   // уникальный _код валюты страны_ (ISO 4217)
}
```


Tак же через GET-запрос можно получить список всех транзакций пользователя
> http://127.0.0.1:8002/api/wallets/transactions/

Или же получив список кошельков
GET
> http://127.0.0.1:8002/api/wallets/wallets/
```json
[
    {
        "url": "http://127.0.0.1:8002/api/wallets/wallets/1/",
        "uid": "c842fe5e-68a8-4104-be64-de8aec121102",
        "holder": "user1",
        "balance": "645.00",
        "currency": "USD"
    },
    {
        "url": "http://127.0.0.1:8002/api/wallets/wallets/2/",
        "uid": "271f4f25-46da-4170-a98b-c68f200676b0",
        "holder": "user1",
        "balance": "1960.40",
        "currency": "RUB"
    }
]
```
Выбрать интересуемый нас кошелек. И получить к нему доступ через предоставленный объект поля json['url'], например 
GET
> http://127.0.0.1:8002/api/wallets/wallets/1/
```json
{
    "holder": "user1",
    "currency": "USD",
    "balance": "645.00",
    "transactions": [
        {
            "sender": "c842fe5e-68a8-4104-be64-de8aec121102",
            "receiver": "13c04cb5-4e3c-40eb-bca0-398324cf0ea7",
            "currency": "USD",
            "amount": "125.00"
        },
        {
            "sender": "c842fe5e-68a8-4104-be64-de8aec121102",
            "receiver": "13c04cb5-4e3c-40eb-bca0-398324cf0ea7",
            "currency": "USD",
            "amount": "175.00"
        }
    ]
}
```

