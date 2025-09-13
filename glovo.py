from fitter import Fitter
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
# Asignar zona a cada fila en el DataFrame
glovo_datos["zone"] = glovo_datos["area"].apply(assign_zone)


# fdp de distancias de los 3 tipos de zonas ---> Habria que dividir por zonas  
fdp = Fitter(glovo_datos['distance_km'])


for zona in ["Urbana", "Semiurbana", "Rural"]:
    datos_zona = glovo_datos[glovo_datos["zone"] == zona]["distance_km"].dropna()
    if not datos_zona.empty:
        print(f"\nFDP para zona: {zona}")
        fdp = Fitter(datos_zona)
        fdp.fit()
        fdp.summary()



#fdp = intervalo entre arribos

for zona in ["Urbana", "Semiurbana", "Rural"]:
    datos_zona = glovo_datos[glovo_datos["zone"] == zona].copy()
    if not datos_zona.empty:
        # Asegúrate de que la columna de tiempo sea tipo datetime
        datos_zona["order_date"] = pd.to_datetime(datos_zona["order_date"])
        # Ordena por tiempo
        datos_zona = datos_zona.sort_values("order_date")
        # Calcula la diferencia entre pedidos consecutivos
        intervalos = datos_zona["order_date"].diff().dropna().dt.total_seconds() / 60  # en minutos
        print(f"\nIntervalos entre arribos para zona: {zona}")


#fdp = tiempo de entrega --> minuto/distancia (? 



