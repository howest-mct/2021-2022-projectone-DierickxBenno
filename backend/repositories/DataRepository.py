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
        location = []
        sql = "INSERT INTO historiek (waarde, eenheidid, tijdstip) VALUES (%s,3, current_time());"
        params = [latitude]
        Database.execute_sql(sql, params)
        sql = "INSERT INTO historiek (waarde, eenheidid, tijdstip) VALUES (%s,4, current_time());"
        params = [longitude]
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
        where eenheidid = 2 and date_format(tijdstip, "%Y-%m-%d") = date_format(now(), "%Y-%m-%d");"""
        data = Database.get_one_row(sql)
        return data
    
    @staticmethod
    def set_hue(p_hue):
        sql  = """
        UPDATE historiek 
        set waarde = %s,
        tijdstip = now()
        where actieid = 5"""
        params = [p_hue]
        data = Database.execute_sql(sql, params)
        return data
    
    @staticmethod
    def get_hue():
        sql = "SELECT waarde FROM historiek WHERE actieid = 5"
        data = Database.get_one_row(sql)
        return data

    #get historiek waarden
    @staticmethod
    def get_historiek(p_interval):
        sql = """SELECT h.eenheidid, waarde as `y`, unix_timestamp(tijdstip)*1000 as `x`, eenheid FROM historiek h
        join eenheden e on e.eenheidid = h.eenheidid
        where h.eenheidid in (1,2,5,6,7) and tijdstip between date_sub(now(),INTERVAL 1 %s) and now()
        order by historiekid asc"""
        params=(p_interval)
        data = Database.get_rows(sql)
        return data
