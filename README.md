# cbot-cm-trunks-consumer-megafon

Данный сервис-бот "слушает" очередь RabbitMQ на предмет сообщений содержащих информацию о транках, и записывает эти данные в БД

Для запуска необходимо указать/изменить все переменные среды на нужные  

Убедиться в работе RabbitMQ, MySQL

Запустить build `docker build -t trunks-consumer-build .`  
Запустить docker `docker run -it --rm --name trunks-consumer-bot trunks-consumer-build`

