from extract import extract_data
from transform import transform_data
from load import load_data

#Funcion de ETL
def etl():
    #Extraccion de la data
    data_extraxted = extract_data()
    #Transformacion de la data
    data_transformed = transform_data(data_extraxted)
    #Carga de la data
    load_data(data_transformed)
    print("Proceso finalizado...")

#Prueba del etl
#etl()