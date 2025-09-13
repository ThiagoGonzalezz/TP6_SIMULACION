import pandas as pd
import numpy as np
from fitter import Fitter

# -------------------------------
# 1. Cargar dataset
# -------------------------------
glovo_datos = pd.read_excel("orders_details.xlsx", sheet_name='orders_details')
glovo_datos['order_date'] = pd.to_datetime(glovo_datos['order_date'], format="%d/%m/%Y %H:%M")

# -------------------------------
# 2. Clasificar ciudades en zonas
# -------------------------------
urbanas = ["Mumbai","Delhi","Bangalore","Kolkata","Chennai","Hyderabad","Pune","Ahmedabad","Surat","Jaipur","Lucknow","Kanpur","Nagpur","Patna","Indore","Vadodara","Bhopal","Agra","Jodhpur","Coimbatore","Mysore","Rajkot"]
semiurbanas = ["Meerut","Ghaziabad","Gurgaon","Panvel","Kottayam","Karimnagar","Saharsa","Katni","Bhiwandi","Aizawl","Secunderabad","Anantapuram","Bahraich","Belgaum","Amravati","Aurangabad","Kishanganj","Sonipat","Durg","Nandyal","Faridabad","Shivpuri","Buxar","Rourkela","Kochi","Ramgarh","Rampur","Gulbarga","Parbhani","Tiruvottiyur","Ongole","Jaipur","Pudukkottai","Satna","Bhiwani","Sasaram","Bilaspur","Thoothukudi","Guna","Ranchi","Jalgaon","Hindupur","Hapur","Warangal","Danapur","Raiganj","Dewas","Deoghar","Howrah","Bhind","Arrah","Visakhapatnam","Shimoga","Hospet","Dhanbad","Udupi","Mangalore","Nagercoil","Kurnool","Farrukhabad","Jalna","Singrauli","Etawah","Bhubaneswar","Panipat","Ambala","Ludhiana","Tenali","Bardhaman","Berhampur","Akola","Bhilai","Jorhat","Bettiah","Bikaner","Saharanpur","Sikar","Nagaon","Navi Mumbai","Hajipur","Uluberia","Junagadh","Solapur","Alwar","South Dumdum","Ujjain","Dindigul","Hubli–Dharwad","Bhatpara","Rajahmundry","Gandhinagar","Khora","Maheshtala","Malegaon","Chittoor","Berhampore","Anand","Indore","Imphal","Narasaraopet","Ambarnath","Fatehpur","Thrissur","Thiruvananthapuram","Guntakal","Jammu","Amritsar","Erode","Panihati","Tadipatri","Allahabad","Patna","Bhimavaram","Phusro","Delhi","Vellore","Khandwa","Guntur","Kollam","Chandrapur","Baranagar","Agartala","Ozhukarai","Machilipatnam","Rajpur Sonarpur","Dehradun","Kirari Suleman Nagar","Varanasi","Srikakulam"]
rurales = ["Hosur","Sambalpur","Katihar","Motihari","Siwan","Tezpur","Raiganj","Danapur","Buxar","Bhind","Arrah","Katni","Rampur","Ramgarh","Kochi","Nandyal","Hapur","Shivpuri","Farrukhabad","Singrauli","Tenali","Bhiwani","Guna","Hindupur","Dewas","Deoghar","Dindigul","Bhatpara","Khora","Malegaon","Narasaraopet","Ambarnath","Bhagalpur","Motihari","Sangli-Miraj & Kupwad","Raebareli","Orai","Haridwar","Muzaffarnagar","Asansol","Jehanabad","Amroha","Kadapa","Pali","Tinsukia","Sirsa","Chinsurah","Siwan","Ichalkaranji","Nanded","Bulandshahr","Darbhanga","Phagwara","Miryalaguda","Yamunanagar","Bidhannagar","Kumbakonam","Nellore","Naihati","Dhule","Mango","Nizamabad","Bally","Pallavaram","Bihar Sharif"]

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

# -------------------------------
# 3. Calcular intervalos entre pedidos
# -------------------------------
glovo_datos = glovo_datos.sort_values(by="order_date")
glovo_datos["Time_Between_Orders"] = glovo_datos.groupby("zone")["order_date"].diff().dt.total_seconds() / 60
glovo_datos = glovo_datos.dropna(subset=["Time_Between_Orders"])

# -------------------------------
# 4. Separar días hábiles / no hábiles
# -------------------------------
glovo_datos["is_weekend"] = glovo_datos["order_date"].dt.dayofweek >= 5

# -------------------------------
# 5. Ajustar distribuciones con Fitter
# -------------------------------
fdps_fitter = {}

for zone in ["Urbana","Semiurbana","Rural"]:
    fdps_fitter[zone] = {}
    for is_weekend, label in zip([False, True], ["HABIL","NO_HABIL"]):
        subset = glovo_datos[(glovo_datos["zone"]==zone) & (glovo_datos["is_weekend"]==is_weekend)]["Time_Between_Orders"]
        if len(subset) > 1:
            f = Fitter(subset, distributions=['expon', 'gamma', 'lognorm', 'norm', 'beta'])
            f.fit()
            fdps_fitter[zone][label] = f

# -------------------------------
# 6. Función para generar intervalos según fdp ajustada
# -------------------------------
def generate_interval(zone, is_weekend):
    label = "NO_HABIL" if is_weekend else "HABIL"
    f = fdps_fitter.get(zone, {}).get(label, None)
    if f is None:
        return None
    # Tomamos la mejor distribución ajustada
    best_dist = list(f.fitted_param.keys())[0]
    params = f.fitted_param[best_dist]
    
    # Generamos un valor aleatorio según la distribución ajustada
    if best_dist == "expon":
        return np.random.exponential(scale=params[0])
    elif best_dist == "gamma":
        return np.random.gamma(shape=params[0], scale=params[2])
    elif best_dist == "lognorm":
        return np.random.lognormal(mean=params[1], sigma=params[0])
    elif best_dist == "norm":
        return np.random.normal(loc=params[0], scale=params[1])
    elif best_dist == "beta":
        # beta está entre 0 y 1, escalamos según rango de datos
        a, b, loc, scale = params
        return np.random.beta(a, b) * scale + loc
    else:
        return None

# -------------------------------
# 7. Ejemplo de uso
# -------------------------------
intervalo = generate_interval("Urbana", False)  # Día hábil, zona Urbana
print("Intervalo generado (minutos):", intervalo)
