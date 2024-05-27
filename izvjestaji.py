import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import matplotlib.pyplot as plt

# Inicijalizacija Firebasea
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://evidencijaprepoznavanjemlica-default-rtdb.europe-west1.firebasedatabase.app/"
})

def fetch_monthly_arrivals(student_id):
    ref = db.reference(f'Studenti/{student_id}/dolasci')
    arrival_data = ref.get()

    if arrival_data is None:
        arrival_data = {}

    monthly_arrivals = {}

    for date_str, arrivals in arrival_data.items():
        for time_id, arrival in arrivals.items():
            if 'arrival_time' in arrival:
                arrival_datetime = datetime.strptime(arrival['arrival_time'], "%Y-%m-%d %H:%M:%S")
                month_str = arrival_datetime.strftime("%Y-%m")
                if month_str in monthly_arrivals:
                    monthly_arrivals[month_str] += 1
                else:
                    monthly_arrivals[month_str] = 1

    return monthly_arrivals

def plot_monthly_arrivals(monthly_arrivals):
    months = list(monthly_arrivals.keys())
    arrivals = list(monthly_arrivals.values())

    plt.figure(figsize=(10, 5))
    plt.bar(months, arrivals, color='green')
    plt.xlabel('Mjesec')
    plt.ylabel('Broj dolazaka')
    plt.title('Mjesečni broj dolazaka')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def fetch_hourly_arrivals(student_id):
    ref = db.reference(f'Studenti/{student_id}/dolasci')
    arrival_data = ref.get()

    if arrival_data is None:
        arrival_data = {}

    hourly_arrivals = [0] * 24

    for date_str, arrivals in arrival_data.items():
        for time_id, arrival in arrivals.items():
            if 'arrival_time' in arrival:
                arrival_datetime = datetime.strptime(arrival['arrival_time'], "%Y-%m-%d %H:%M:%S")
                hour = arrival_datetime.hour
                hourly_arrivals[hour] += 1

    return hourly_arrivals

def plot_hourly_arrivals(hourly_arrivals):
    hours = list(range(24))
    arrivals = hourly_arrivals

    plt.figure(figsize=(10, 5))
    plt.bar(hours, arrivals, color='orange')
    plt.xlabel('Sat')
    plt.ylabel('Broj dolazaka')
    plt.title('Broj dolazaka po satima')
    plt.xticks(hours)
    plt.tight_layout()
    plt.show()

def fetch_weekly_arrivals(student_id):
    ref = db.reference(f'Studenti/{student_id}/dolasci')
    arrival_data = ref.get()

    if arrival_data is None:
        arrival_data = {}

    weekly_arrivals = [0] * 7

    for date_str, arrivals in arrival_data.items():
        for time_id, arrival in arrivals.items():
            if 'arrival_time' in arrival:
                arrival_datetime = datetime.strptime(arrival['arrival_time'], "%Y-%m-%d %H:%M:%S")
                weekday = arrival_datetime.weekday()
                weekly_arrivals[weekday] += 1

    return weekly_arrivals

def plot_weekly_arrivals(weekly_arrivals):
    days = ['Ponedjeljak', 'Utorak', 'Srijeda', 'Četvrtak', 'Petak', 'Subota', 'Nedjelja']
    arrivals = weekly_arrivals

    plt.figure(figsize=(10, 5))
    plt.bar(days, arrivals, color='purple')
    plt.xlabel('Dan u tjednu')
    plt.ylabel('Broj dolazaka')
    plt.title('Broj dolazaka po danima u tjednu')
    plt.tight_layout()
    plt.show()

def fetch_total_arrivals():
    ref = db.reference('Studenti')
    students_data = ref.get()

    total_arrivals = {}

    for student_id, student_info in students_data.items():
        dolasci = student_info.get('dolasci', {})
        total_arrivals[student_id] = sum(len(day_arrivals) for day_arrivals in dolasci.values())

    return total_arrivals

def plot_total_arrivals(total_arrivals):
    students = list(total_arrivals.keys())
    arrivals = list(total_arrivals.values())

    plt.figure(figsize=(15, 5))
    plt.bar(students, arrivals, color='red')
    plt.xlabel('Student ID')
    plt.ylabel('Ukupan broj dolazaka')
    plt.title('Ukupan broj dolazaka po studentu')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def fetch_yearly_arrivals():
    ref = db.reference('Studenti')
    students_data = ref.get()

    yearly_arrivals = {}

    for student_id, student_info in students_data.items():
        dolasci = student_info.get('dolasci', {})
        for date_str, arrivals in dolasci.items():
            for time_id, arrival in arrivals.items():
                if 'arrival_time' in arrival:
                    arrival_datetime = datetime.strptime(arrival['arrival_time'], "%Y-%m-%d %H:%M:%S")
                    year_str = arrival_datetime.strftime("%Y")
                    if year_str in yearly_arrivals:
                        yearly_arrivals[year_str] += 1
                    else:
                        yearly_arrivals[year_str] = 1

    return yearly_arrivals

def plot_yearly_arrivals(yearly_arrivals):
    years = list(yearly_arrivals.keys())
    arrivals = list(yearly_arrivals.values())

    plt.figure(figsize=(10, 5))
    plt.bar(years, arrivals, color='cyan')
    plt.xlabel('Godina')
    plt.ylabel('Ukupan broj dolazaka')
    plt.title('Ukupan broj dolazaka po godini')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Glavni dio koda

student_id = "321654"  # Zamijenite s odgovarajućim ID-jem studenta

# Mjesečni dolasci
monthly_arrivals = fetch_monthly_arrivals(student_id)
plot_monthly_arrivals(monthly_arrivals)

# Dolasci po satima
hourly_arrivals = fetch_hourly_arrivals(student_id)
plot_hourly_arrivals(hourly_arrivals)

# Tjedni dolasci
weekly_arrivals = fetch_weekly_arrivals(student_id)
plot_weekly_arrivals(weekly_arrivals)

# Ukupan broj dolazaka po studentu
total_arrivals = fetch_total_arrivals()
plot_total_arrivals(total_arrivals)


