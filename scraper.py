import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime

# Open CSV file for writing
with open('player_info.csv', mode='w', encoding='utf-8') as file:
    # Create writer object using python
    writer = csv.writer(file)
    
    # Writing headers to CSV file as per requirement
    writer.writerow(['Name', 'Full_name','Date_of_Birth','Age','City','Country','Position', 'Dead', 'Current_Club', 'Player_Id', 'Scarping_TimeStamp','Appearance'])
    
     # Open CSV file containing player URLs
    with open('playersURLs.csv', 'r') as url_file:
        reader = csv.reader(url_file)
        
        # Loop over each row in the CSV file
        for row in reader:
            # Extract the URL
            url = row[0]
            
            # Send the GET request
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            infobox = soup.find('table', class_='infobox vcard')

            # Find the name of the player
            name_element = soup.find("h1", class_="firstHeading")
            name = name_element.text.strip() if name_element else None
            
            # Find the full name of the player
            if infobox:
                full_name_element = infobox.find('th', string='Full name')
                full_name = full_name_element.find_next('td').text.strip() if full_name_element else None
            else:
                full_name = None
            
            #Find the date of birth in xxxx-xx-xx    
            infobox = soup.find('table', class_='infobox vcard')
            age_new = soup.find('table', {"class":"noprint ForceAgeToShow"})
            age = age_new.find_next('span').text.strip() if age_new else None
            
            #formatting the date
            try:
                dob_string = infobox.find('span', {'class': 'bday'}).text
                dob_datetime = datetime.strptime(dob_string, '%Y-%m-%d')
                dob_formatted = datetime.strftime(dob_datetime, '%Y-%m-%d')
            except:
                dob_formatted = ''
            
            #find the age in numbers example '25'    
            if dob_formatted:
                dob_datetime = datetime.strptime(dob_formatted, '%Y-%m-%d')
                today = datetime.today()
                age = today.year - dob_datetime.year - ((today.month, today.day) < (dob_datetime.month, dob_datetime.day))
            else:
                age = None
            
            # Find city and country of birth of the player
            birthplace_element = infobox.find('th', string='Place of birth')
            if birthplace_element:
                birthplace = birthplace_element.find_next('td').text.strip()
                birthplace_parts = birthplace.split(', ')
                if len(birthplace_parts) == 2:
                    city_of_birth = birthplace_parts[0]
                    country_of_birth = birthplace_parts[1]
                elif len(birthplace_parts) == 1:
                    city_of_birth = birthplace_parts[0]
                    country_of_birth = None
                else:
                    city_of_birth = None
                    country_of_birth = None
            else:
                city_of_birth = None
                country_of_birth = None
            
            # Find position of the player
            position = infobox.find('td', {'class': 'role'}).text.strip() if infobox.find('td', {'class': 'role'}) else None
           
            #Find current club of the player
            current_club_element = infobox.find('th', string='Current team')
            current_club = current_club_element.find_next('td').text.strip() if current_club_element else None
            
            #Find dead or alive status
            dead_element = infobox.find('th', string='Died')
            dead = 'Dead' if dead_element else 'Alive'
            
            #Find player ID
            player_id = url.split('/')[-1]
            
            # Find current club of the player
            current_club_element = infobox.find('th', string='Current team')
            current_club = current_club_element.find_next('td').text.strip() if current_club_element else None
            
            #get current date and time
            now = datetime.now()
            # format the date and time as a string
            scraping_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            
            #get the number of appearances of the player
            infobox = soup.find('table', class_='infobox vcard')
            current_club_element = infobox.find('th', string='Current team')
            current_club = current_club_element.find_next('td').text.strip() if current_club_element else None
            # Find the row(s) that contain the player's appearances for the current team
            appearances_rows = infobox.find_all('td')
            
            if not appearances_rows:
                appearances = None
            else:
                for row in appearances_rows:
                    next_td = row.find_next('td')
                    if next_td and next_td.text.strip().isdigit():
                        appearances = next_td.text.strip()
                        break
                else:
                    appearances = None
                                         
            #writing scraped data into the csv file
            writer.writerow([name, full_name,dob_formatted,age,city_of_birth, country_of_birth,position, dead, current_club, player_id, scraping_timestamp,appearances])
            