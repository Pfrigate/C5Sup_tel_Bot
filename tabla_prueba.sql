create table prueba1(
hostname varchar(255),
modelo varchar(255),
serie varchar(255),
inventario varchar(255),
posicion_fisica varchar(255),
usuario varchar(255)
)
create table Bitacora(
    ID int NOT NULL auto_increment,
    piso varchar(255),
    area varchar(255),
    nombre_usuario varchar(255),
    tipo_usr varchar(255),
    actividad varchar(255),
    medio varchar(255),
    comentario varchar(255),
    PRIMARY KEY (ID)
);

LOAD DATA INFILE 'C:/Users/admin/Desktop/Bot_Telegram/prueba1.csv'
INTO TABLE prueba1
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';