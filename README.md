# Парсер для интернет-магазина "Metro"

Парсер собирает данные о продуктах в необходимой категории интернет магазина - **Metro** и записывает данные в csv файл для удобства чтения и хранения.
Для работы парсера необходимо скачать и установить браузер - **Firefox**:
```
https://www.mozilla.org/ru/firefox/new/
```

Можно изменить желаемую категорию продуктов для парсинга. Для этого необходимо указать категорию товаров, а так же подкатегорию, продукты которой, необходимо спарсить.
Пример:
```
CATEGORY  =  'Сладости, чипсы, снеки'

SUBCATEGORY  =  'Шоколад и батончики'
```
Наименования категорий и подкатегорий необходимо брать из каталога на сайте **Metro**:
```
'https://online.metro-cc.ru'
```
Данные собираются в csv файл в директории **data**. Название файла соответствует наименованию подкатегории.
Все товары, которых нет в наличии не попадают в конечный набор данных.

Пример данных одного товара:
```
id;name;brand;link;actual_price;old_price
658363;Стейк Мираторг Prime Рибай из мраморной говядины охлажденный, 390г;МИРАТОРГ;/products/stejk-miratorg-ribaj-prime-390g;2039;2399
```
```
{
'id': 658363,
'name': 'Стейк Мираторг Prime Рибай из мраморной говядины охлажденный, 390г',
'brand': 'МИРАТОРГ',
'link': 'https://online.metro-cc.ru/products/stejk-miratorg-ribaj-prime-390g',
'actual_price': 2039,
'old_price': 2399
}
```
