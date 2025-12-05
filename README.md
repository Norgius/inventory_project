# Разработчикам бэкенда

Проект включает несколько API enpoints для работы с пользователями, их инвентарём и продуктами.

## Как развернуть local-окружение

### Необходимое ПО

Для запуска ПО вам понадобятся консольный Git, Make, Docker и Docker Compose. Инструкции по их установке ищите на официальных сайтах:

- [Git SCM](https://git-scm.com/)
- [GNU Make](https://www.gnu.org/software/make/)
- [Get Started with Docker](https://www.docker.com/get-started/)

Для тех, кто использует Windows необходимы также программы **git** и **git bash**. В git bash надо добавить ещё команду make:

- Go to [ezwinports](https://sourceforge.net/projects/ezwinports/files/)
- Download make-4.2.1-without-guile-w32-bin.zip (get the version without guile)
- Extract zip
- Copy the contents to C:\ProgramFiles\Git\mingw64\ merging the folders, but do NOT overwrite/replace any exisiting files.

Все дальнейшие команды запускать из-под **git bash**.

### Подготовка файла .env

Для локального развертывания приложения необходимо создать в корне проекта файл `.env`. Сейчас можете оставитье его пустым:

```shell
$ touch .env
```

## Работа с кодом с использованием docker

Склонируйте репозиторий.

Сначала скачайте и соберите докер-образы с помощью Docker Сompose:

```shell
$ docker compose pull --ignore-buildable
$ docker compose build
```

Запустите докер-контейнеры и не выключайте:

```shell
$ docker compose up
```

Примените миграции

```shell
$ make migrate
```

API доступно по адресу [127.0.0.1:8000/api/v1/redoc](http://127.0.0.1:8000/api/v1/redoc).

### Команды для быстрого запуска с помощью make

Для часто используемых команд Docker Compose подготовлен набор альтернативных коротких команд `make`.

Полный набор доступных команд `make` и их скриптов можно найти в файле [Makefile](Makefile). Тот же список доступных команд можно вывести в консоль через встроенную справку:

```shell
$ make help
Cписок доступных команд:
lint                           Проверяет линтерами код в репозитории
format                         Запуск автоформатера
makemigrations                 Создаёт новые файлы миграций Alembic
migrate                        Применяет новые миграции Alembic
test                           Запуск тестов
```

### Как запустить тесты

В проекте используются автотесты [pytest](https://docs.pytest.org/). Можно запустить их командой:

```shell
make test
```
