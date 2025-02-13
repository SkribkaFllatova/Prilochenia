#!/bin/bash 
 
db_user="skribkafilatova" 
db_name="lab2" 
db_pass="lab2" 
 
migration_dir="E:\Skribka-Filatova\Prilochenia\lab2" #Задали путь к директории с SQL-файлами миграций
 
run_sql() { 
    if [ -f "$1" ]; then 
        if [[ "$1" == *.sql ]]; then 
            PASSWORD=$db_pass /c/Program\ Files/PostgreSQL/15/bin/psql.exe -U $db_user -d $db_name -f "$1" -t
        else 
            echo "Данный файл'$1' не является .sql" 
            exit 1 
        fi 
    else 
        echo "Данный файл '$1' не существует" 
        exit 1 
    fi 
} 
#Определили функцию run_sql, которая принимает один аргумент (путь к SQL-файлу).  
#Функция проверяет:
   #Существует ли файл (-f "$1")
   #Является ли файл файлом SQL (.sql с помощью [[ "$1" == .sql ]]).
   #Если оба условия истинны, запускает psql для выполнения SQL-запроса из файла. -t опция подавляет вывод заголовков столбцов
   #В противном случае выводит сообщение об ошибке и завершается, указывая на ошибку
 
run_sql_c() { 
    PASSWORD=$db_pass /c/Program\ Files/PostgreSQL/15/bin/psql.exe -U $db_user -d $db_name -c "$1" -t
} 
#Определили функцию run_sql_c, которая принимает один аргумент (SQL-запрос)

run_sql_c "CREATE TABLE IF NOT EXISTS migrations ( 
    id SERIAL PRIMARY KEY, 
    migration_name VARCHAR(255) UNIQUE NOT NULL, 
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);"
#Выполнили создание таблицы migrations (если она не существует) для отслеживания примененных миграций

applied_migrations=$(run_sql_c "SELECT migration_name FROM migrations;")
#Выполнили запрос к таблице migrations для получения списка уже примененных миграций. Результат записывается в переменную applied_migrations

echo "Файлы, которые уже были мигрированы: $applied_migrations" #Вывод списка уже примененных миграций

for migration_file in "$migration_dir"/*.sql; do #Цикл перебирает все файлы с расширением .sql в указанной директории
    migration_name=$(basename "$migration_file") #Далее извлекается имя файла миграции без пути
    if echo "$applied_migrations" | grep "$migration_name"; then #Проверяется, присутствует ли имя текущей миграции в списке уже примененных миграций
        echo "Миграция применена: $migration_name" #Выводится сообщение, если миграция уже применена
    else
        echo "Применение миграции: $migration_name" #Выводится сообщение о начале применения миграции
        run_sql "$migration_file" #Выполняется SQL-скрипт миграции
        run_sql_c "INSERT INTO migrations (migration_name) 
                   SELECT '$migration_name'
                   WHERE NOT EXISTS (SELECT 1 FROM migrations 
                   WHERE migration_name = '$migration_name');"
    fi
done
#Добавляется запись о примененной миграции в таблицу migrations. WHERE NOT EXISTS предотвращает дублирование записей, если миграция каким-то образом уже добавлена