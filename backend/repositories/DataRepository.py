from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    # add _data
    @staticmethod
    def insert_data(p_waarde, p_sensorid):
        sql = 'INSERT INTO data (waarde, sensorid, tijdstip) VALUES (%s, %s, current_time())'
        params = [p_waarde, p_sensorid]
        Database.execute_sql(sql, params)

    @staticmethod
    def add_location(longitude, latitude):
        sql = "INSERT INTO locatie (latitude, longitude, tijdstip) VALUES (%s,%s, current_time())"
        params = [latitude, longitude]
        Database.execute_sql(sql, params)

    

    #get most recent data
    @staticmethod
    def get_most_recent_sensor():
        sql = """
        SELECT round(d.waarde, 1) as `waarde`, (d.sensorid), s.eenheid from data d 
JOIN sensor s ON s.sensorid = d.sensorid 
where dataid in(select max(dataid) from data group by sensorid order by dataid)
ORDER BY d.tijdstip desc;"""
        data = Database.get_rows(sql)
        return data

    @staticmethod
    def get_most_recent_location():
        sql = """
        Select latitude, longitude from locatie
        Order BY tijdstip desc
        LIMIT 1"""
        data = Database.get_rows(sql)
        return data
 
    @staticmethod
    def get_most_recent_speed():
        sql = """
        Select snelheid from snelheid
        Order BY tijdstip desc
        LIMIT 1"""
        data = Database.get_rows(sql)
        return data

    @staticmethod
    def get_most_recent_steps():
        sql = """
        Select stappen from activiteit
        Order BY datum desc
        LIMIT 1"""
        data = Database.get_rows(sql)
        return data

    