import psycopg2


def connect_and_load_data(scrappedData):
  hostname = 'localhost'
  database = 'concerts'
  username = 'postgres'
  password = 'password'
  port_id = 5432
  connection = None
  cursor = None

  try: 
    connection = psycopg2.connect(
      host = hostname,
      dbname = database,
      user = username,
      password = password,
      port = port_id
    )

    cursor = connection.cursor()

    
    create_table = ''' CREATE TABLE IF NOT EXISTS events (
      date varchar(400),
      time varchar(400),
      location varchar(800),
      works varchar(200),
      title varchar(200),
      artists varchar(800),
      imageLink varchar(800)
    )
    '''

    cursor.execute(create_table)

  

    for row in scrappedData:
      insert_script = 'INSERT INTO events (date, time, location, works, title, artists, imageLink) VALUES (%s, %s, %s, %s, %s, %s, %s)'
      cursor.execute(insert_script, row)
    

    connection.commit()

  except Exception as error:
    print(error)

  finally: 
    if cursor is not None:
      cursor.close()
    if connection is not None:
      connection.close()