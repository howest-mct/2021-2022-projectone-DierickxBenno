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
    def get_most_recent():
        print("meest recente data werkt niet, voorlopig gwn gebruiken als placeholder")
        sql = "SELECT d.waarde, d.sensorid, s.eenheid from data d JOIN sensor s ON s.sensorid = d.sensorid GROUP BY sensorid"
        data = Database.get_rows(sql)
        return data

    #stappen toevoegen