from datetime import date, datetime
import os

def create_filename():
    """Deze functie maakt de filename voor de log-file aan"""
    work_day = str(date.today()).replace('-', '')
    filename = work_day + "_log.txt"
    
    return filename

def check_existence(folder_name, file_name):
    folder_existence = False
    log_existence = False

    folder_list = os.listdir("C:\\")
    scan_library = os.path.join("C:\\", folder_name) 

    if folder_name not in folder_list:
        os.mkdir(scan_library)
        print("scan_logs has been created")

        with open(os.path.join(scan_library, file_name), 'w') as file_object:
            pass

        folder_existence = True
        print(file_name + " has been created")
    else: 
        folder_existence = True
        # print("This folder already exists!")

           
        file_list = os.listdir(scan_library)
        
        if file_name not in file_list:             
            with open(os.path.join(scan_library, file_name), 'w') as file_object:
                pass
            
            log_existence = True
            print(file_name + " has been created")
        
        elif file_name in file_list:
            log_existence = True
            # print("The log file already exists!")
        
    return folder_existence, log_existence

def write_to_log_file(sender_ip, barcode, change_type, ex):
    """
    Deze functie schrijft na een verbinding de volgende gegevens naar de log file (log.txt):
    - IP-adress zender
    - tijdstip waarop het bericht ontvangen is van de zender
    - de barcode die is verstuurd
    - het type mutatie
    """
    if ex == True:
        date_time = str(datetime.now())
        time_received = "Tijdstip: " + date_time + "\n"
        ip_received = "IP zender: " + sender_ip + "\n"
        barcode_received = "Barcode: " + barcode + "\n"
        mutation_received = "Type verandering: " + change_type + "\n"
        process_status = "Wijziging succesvol verwerkt in de database\n"
    if ex == False:
        date_time = str(datetime.now())
        time_received = "Tijdstip: " + date_time + "\n"
        ip_received = "IP zender: " + sender_ip + "\n"
        barcode_received = "Barcode: " + barcode + "\n"
        mutation_received = "Type verandering: " + change_type + "\n"
        process_status = "Wijziging niet verwerkt in de database: barcode komt niet in de database voor\n"
    
    file_name = create_filename()
    folder, log = check_existence("scan_logs", file_name)

    log_file = os.path.join("C://scan_logs", file_name)
    with open(log_file, 'a') as file_object:
        file_object.write("\nBarcode ontvangen: \n")
        file_object.write(ip_received)
        file_object.write(time_received)
        file_object.write(barcode_received)
        file_object.write(mutation_received)
        file_object.write(process_status)
    
def write_to_log_database_offline(sender_ip, barcode, change_type):
    """
    Deze functie schrijft na een verbinding de volgende gegevens naar de log file (log.txt):
    - IP-adress zender
    - tijdstip waarop het bericht ontvangen is van de zender
    - de barcode die is verstuurd
    - het type mutatie
    """
    date_time = str(datetime.now())
    time_received = "Tijdstip: " + date_time + "\n"
    ip_received = "IP zender: " + sender_ip + "\n"
    barcode_received = "Barcode: " + barcode + "\n"
    mutation_received = "Type verandering: " + change_type + "\n"
    process_status = "Database offline: wijziging niet verwerkt in database \n"

    
    file_name = create_filename()
    folder, log = check_existence("scan_logs", file_name)

    log_file = os.path.join("C://scan_logs", file_name)
    with open(log_file, 'a') as file_object:
        file_object.write("\nBarcode ontvangen: \n")
        file_object.write(ip_received)
        file_object.write(time_received)
        file_object.write(barcode_received)
        file_object.write(mutation_received)
        file_object.write(process_status)



# file_name = create_filename()
# print(file_name)
# folder, log = check_existence("scan_logs", file_name)
# print(folder)
# print(log)

# for i in range(1, 10000):
#    write_to_log_file()

# write_to_log_file("10.0.1.152", "9781119149224", "+")
# for i in range (1, 4):
#    write_to_log_file("10.0.1.151", "9781119149224", "-")
# for i in range (1, 4):
#    write_to_log_file("10.0.1.152", "9781119149224", "+")