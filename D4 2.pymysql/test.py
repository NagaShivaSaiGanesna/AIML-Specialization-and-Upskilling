import pymysql
def get_connection():
    return pymysql.connect(
        host=secret['host'],
        user=secret['user'],
        password=secret['password'],
        port=int(secret['port'])
    )
def run():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO ProdMainDataStaging.Logs_Data_Ingestion (Pipeline_Name, File_Name, Ingestion_Date_Time)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, ('Incentives_ETL_Ingestion', file['FileName'], Pipeline_Start_Datetime))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as log_file_error:
            print(f"Error logging file ingestion: {log_file_error}")

