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
    def insert_data(p_waarde, p_eenheidid):
        sql = 'INSERT INTO historiek (waarde, eenheidid, tijdstip) VALUES (%s,%s, current_time());'
        params = [p_waarde, p_eenheidid]
        Database.execute_sql(sql, params)

    @staticmethod
    def add_location(longitude, latitude):
        sql = "INSERT INTO historiek (waarde, eenheidid, tijdstip) VALUES (%s,3, current_time()); INSERT INTO historiek (waarde, eenheidid, tijdstip) VALUES (%s,4, current_time());"
        params = [latitude, longitude]
        Database.execute_sql(sql, params)

    #get most recent data
    @staticmethod
    def get_most_recent_data():
        sql = """
        SELECT h.eenheidid, waarde, eenheid from historiek h 
	    JOIN eenheden e ON h.eenheidid = e.eenheidid
        where h.historiekid in (select max(historiekid) from historiek group by eenheidid order by historiekid)
        ORDER BY h.tijdstip desc"""
        data = Database.get_rows(sql)
        return data

    @staticmethod 
    def get_total_steps():
        sql="""SELECT SUM(waarde) AS `waarde` from historiek
where eenheidid = 2 and date_format(tijdstip, "yyyy-mm-dd") = date_format(now(), "yyyy-mm-dd");"""
        data = Database.get_one_row(sql)
        return data
    
    #get historiek waarden
    def get_historiek():
        sql = """SELECT h.eenheidid, waarde, tijdstip, eenheid FROM historiek h
 join eenheden e on e.eenheidid = h.eenheidid
 where h.eenheidid in (1,5,6,7)
order by historiekid asc"""
        data = Database.get_rows(sql)