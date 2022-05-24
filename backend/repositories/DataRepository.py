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
    def insert_data(p_waarde, p_sensorid, p_activiteitid):
        sql = 'INSERT INTO data (waarde, sensorid, activiteitid, tijdstip) VALUES (%s, %s, %s, current_time())'
        params = [p_waarde, p_sensorid, p_activiteitid]
        Database.execute_sql(sql, params)
