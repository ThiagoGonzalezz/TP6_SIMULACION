from fitter import Fitter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

glovo_datos = pd.read_excel("orders_details.xlsx", sheet_name='orders_details')

print(glovo_datos.shape)
print(glovo_datos.head(10))
print(glovo_datos.dtypes)


# URBANA
urbanas = ["Mumbai","Delhi","Bangalore","Kolkata","Chennai","Hyderabad","Pune","Ahmedabad","Surat","Jaipur","Lucknow","Kanpur","Nagpur","Patna","Indore","Vadodara","Bhopal","Agra","Jodhpur","Coimbatore","Mysore","Rajkot"]

# SEMIURBANA
semiurbanas = ["Meerut","Ghaziabad","Gurgaon","Panvel","Kottayam","Karimnagar","Saharsa","Katni","Bhiwandi","Aizawl","Secunderabad","Anantapuram","Bahraich","Belgaum","Amravati","Aurangabad","Kishanganj","Sonipat","Durg","Nandyal","Faridabad","Shivpuri","Buxar","Rourkela","Kochi","Ramgarh","Rampur","Gulbarga","Parbhani","Tiruvottiyur","Ongole","Jaipur","Pudukkottai","Satna","Bhiwani","Sasaram","Bilaspur","Thoothukudi","Guna","Ranchi","Jalgaon","Hindupur","Hapur","Warangal","Danapur","Raiganj","Dewas","Deoghar","Howrah","Bhind","Arrah","Visakhapatnam","Shimoga","Hospet","Dhanbad","Udupi","Mangalore","Nagercoil","Kurnool","Farrukhabad","Jalna","Singrauli","Etawah","Bhubaneswar","Panipat","Ambala","Ludhiana","Tenali","Bardhaman","Berhampur","Akola","Bhilai","Jorhat","Bettiah","Bikaner","Saharanpur","Sikar","Nagaon","Navi Mumbai","Hajipur","Uluberia","Junagadh","Solapur","Alwar","South Dumdum","Ujjain","Dindigul","Hubli–Dharwad","Bhatpara","Rajahmundry","Gandhinagar","Khora","Maheshtala","Malegaon","Chittoor","Berhampore","Anand","Indore","Imphal","Narasaraopet","Ambarnath","Fatehpur","Thrissur","Thiruvananthapuram","Guntakal","Jammu","Amritsar","Erode","Panihati","Tadipatri","Allahabad","Patna","Bhimavaram","Phusro","Delhi","Vellore","Khandwa","Guntur","Kollam","Chandrapur","Baranagar","Agartala","Ozhukarai","Machilipatnam","Rajpur Sonarpur","Dehradun","Kirari Suleman Nagar","Varanasi","Srikakulam"]

# RURAL
rurales = ["Hosur","Sambalpur","Katihar","Motihari","Siwan","Tezpur","Raiganj","Danapur","Buxar","Bhind","Arrah","Katni","Rampur","Ramgarh","Kochi","Nandyal","Hapur","Shivpuri","Farrukhabad","Singrauli","Tenali","Bhiwani","Guna","Hindupur","Dewas","Deoghar","Dindigul","Bhatpara","Khora","Malegaon","Narasaraopet","Ambarnath","Tadipatri","Bhagalpur","Motihari","Sangli-Miraj & Kupwad","Raebareli","Orai","Haridwar","Muzaffarnagar","Asansol","Jehanabad","Amroha","Kadapa","Pali","Tinsukia","Sirsa","Chinsurah","Siwan","Ichalkaranji","Nanded","Bulandshahr","Darbhanga","Phagwara","Miryalaguda","Yamunanagar","Bidhannagar","Kumbakonam","Nellore","Naihati","Dhule","Mango","Nizamabad","Bally","Pallavaram","Bihar Sharif"]


def assign_zone(city):
    if city in urbanas:
        return "Urbana"
    elif city in semiurbanas:
        return "Semiurbana"
    elif city in rurales:
        return "Rural"
    else:
        return "Unknown"



glovo_datos["zone"] = glovo_datos["area"].apply(assign_zone)


glovo_datos["order_date"] = pd.to_datetime(glovo_datos["order_date"])

glovo_datos["weekday"] = glovo_datos["order_date"].dt.weekday

glovo_datos["workday"] = glovo_datos["weekday"].apply(lambda x: "Hábil" if x < 5 else "No hábil")


datos_habiles = glovo_datos[glovo_datos["workday"] == "Hábil"]
datos_nohabiles = glovo_datos[glovo_datos["workday"] == "No hábil"]


habiles_urbana = datos_habiles[datos_habiles["zone"] == "Urbana"]
habiles_semiurbana = datos_habiles[datos_habiles["zone"] == "Semiurbana"]
habiles_rural = datos_habiles[datos_habiles["zone"] == "Rural"]

nohabiles_urbana = datos_nohabiles[datos_nohabiles["zone"] == "Urbana"]
nohabiles_semiurbana = datos_nohabiles[datos_nohabiles["zone"] == "Semiurbana"]
nohabiles_rural = datos_nohabiles[datos_nohabiles["zone"] == "Rural"]

# Intervalo entre arribos - IA
for zona, df in [("Urbana", habiles_urbana), ("Semiurbana", habiles_semiurbana), ("Rural", habiles_rural)]:
    if not df.empty:
        df = df.sort_values("order_date")
        intervalos = df["order_date"].diff().dropna().dt.total_seconds() / 60  # minutos
        print(f"\nIntervalos entre arribos en días hábiles para zona {zona}:")
        print(intervalos.describe())
        if not intervalos.empty:
            fdp_ia = Fitter(intervalos)
            fdp_ia.fit()
            fdp_ia.summary(10)

# Distancia de entregas - DE
for zona, df in [("Urbana", habiles_urbana), ("Semiurbana", habiles_semiurbana), ("Rural", habiles_rural)]:
    if not df.empty and "distance_km" in df.columns:
        distancias = df["distance_km"].dropna()
        print(f"\nFDP de distancia en días hábiles para zona {zona}:")
        print(distancias.describe())
        if not distancias.empty:
            fdp_dist = Fitter(distancias)
            fdp_dist.fit()
            fdp_dist.summary(10)
            fdp_dist.plot()        # Gráfico de ajuste
            plt.title(f"FDP de distancia - zona {zona}")
            plt.show()

# VELOCIDAD/CONDUCTOR - VC            
'''
for zona, df in [("Urbana", habiles_urbana), ("Semiurbana", habiles_semiurbana), ("Rural", habiles_rural)]:
    if not df.empty and {"order_date", "actual_delivery_time", "distance_km"}.issubset(df.columns):
        # Convertir columnas de tiempo a datetime
        df = df.copy()
        df["order_date"] = pd.to_datetime(df["order_date"])
        df["actual_delivery_time"] = pd.to_datetime(df["actual_delivery_time"])
        # Calcular minutos/km
        tiempo_min = (df["actual_delivery_time"] - df["order_date"]).dt.total_seconds() / 60
        minutos_por_km = tiempo_min / df["distance_km"]
        minutos_por_km = minutos_por_km.replace([np.inf, -np.inf], np.nan).dropna()
        print(f"\nFDP de minutos/km en días hábiles para zona {zona}:")
        print(minutos_por_km.describe())
        if not minutos_por_km.empty:
            fdp_vel = Fitter(minutos_por_km)
            fdp_vel.fit()
            fdp_vel.summary(10)
            fdp_vel.plot()
            plt.title(f"FDP minutos/km - zona {zona}")
            plt.show()
'''

#TE = ACTUAL_DELIVERY_TIME - ORDER_DATE)


