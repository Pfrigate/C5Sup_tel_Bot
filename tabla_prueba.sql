create table prueba1(
hostname varchar(255),
modelo varchar(255),
serie varchar(255),
inventario varchar(255),
posicion_fisica varchar(255),
usuario varchar(255)
)

LOAD DATA INFILE 'C:/Users/admin/Desktop/Bot_Telegram/prueba1.csv'
INTO TABLE prueba1
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';