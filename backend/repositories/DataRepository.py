from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def insert_data(p_waarde, p_sensorid):
        sql = 'INSERT INTO data (waarde, sensorid, tijdstip) VALUES (%s, %s, current_time())'
        params = [p_waarde, p_sensorid]
        Database.execute_sql(sql, params)

    #get most recent data
    @staticmethod
    def get_most_recent_sensor():
        print("meest recente data werkt niet, voorlopig gwn gebruiken als placeholder")
        sql = "SELECT d.waarde, d.sensorid, s.eenheid from data d JOIN sensor s ON s.sensorid = d.sensorid GROUP BY sensorid"
        data = Database.get_rows(sql)
        return data

    @staticmethod
    def get_most_recent_location():
        sql = """
        Select * from locatie
        Order BY tijdstip desc
        LIMIT 1"""
        data = Database.get_rows(sql)
        return data

    
    @staticmethod
    def get_most_recent_speed():
        sql = """
        Select * from snelheid
        Order BY tijdstip desc
        LIMIT 1"""
        data = Database.get_rows(sql)
        return data

    @staticmethod
    def add_location(longitude, latitude):
        sql = "INSERT INTO locatie (latitude, longitude, tijdstip) VALUES (%s,%s, current_time())"
        params = [latitude, longitude]
        Database.execute_sql(sql, params)