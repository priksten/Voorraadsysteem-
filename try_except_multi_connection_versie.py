import asyncio
import json
import mysql.connector
from article_database import increase_inventory, decrease_inventory, check_existence
from writing_to_txt import write_to_log_file, write_to_log_database_offline

async def handle_client(reader, writer):
    """Deze coroutine handelt een verbinding met een client af"""
   
    while True:
        data = await reader.read(1024)
        if not data:
            break
        barcode = json.loads(data.decode())

        adres = writer.get_extra_info('peername')
        if adres: 
            ip_adres = adres[0]
            port = adres[1]
                
            print("Verbinding vanuit IP adres " + str(ip_adres) + " en poort " + str(port))

        if barcode[1] == "+":
            try:
                existence = check_existence("magazijn", barcode[0])
                if existence == True:
                    increase_inventory("magazijn", "voorraad", str(barcode[0]))
                    write_to_log_file(ip_adres, str(barcode[0]), barcode[1], existence)
                    writer.write(b'Barcode ontvangen en voorraad succesvol aangepast in database\n')
                else:
                    writer.write(b'De ontvangen barcode komt niet voor in onze database\n')
                    write_to_log_file(ip_adres, str(barcode[0]), barcode[1], existence)
            except mysql.connector.errors.DatabaseError:
                print("Kan geen verbinding maken met de database. \nStart de databaseserver")
                write_to_log_database_offline(ip_adres, str(barcode[0]), barcode[1])
                writer.write(b'Kan geen verbinding maken met de database. \nStart de databaseserver\n') 
        elif barcode[1] == "-":
            try: 
                existence = check_existence("magazijn", barcode[0])
                if existence == True:
                    decrease_inventory("magazijn", "voorraad", str(barcode[0]))
                    write_to_log_file(ip_adres, str(barcode[0]), barcode[1], existence)
                    writer.write(b'Barcode ontvangen en voorraad succesvol aangepast in database\n')
                else:
                    writer.write(b'De ontvangen barcode komt niet voor in onze database\n')
                    write_to_log_file(ip_adres, str(barcode[0]), barcode[1], existence)
            except mysql.connector.errors.DatabaseError:
                print("Kan geen verbinding maken met de database. \nStart de databaseserver")
                write_to_log_database_offline(ip_adres, str(barcode[0]), barcode[1])
                writer.write(b'Kan geen verbinding maken met de database. \nStart de databaseserver\n')    
        await writer.drain()

    writer.close()

async def start_server():
    """Deze coroutine start de barcode server"""
    server = await asyncio.start_server(
        handle_client, '0.0.0.0', 65432
    )
    async with server:
        print("Server is gestart en luistert naar barcodes.")
        await server.serve_forever()

async def main():
    """Hoofdprogramma om de server te starten"""
    await start_server()

# Start de asyncio event loop
asyncio.run(main())