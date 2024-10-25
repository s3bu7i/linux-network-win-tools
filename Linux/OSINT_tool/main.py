import requests
import whois
import socket
import sqlite3
import json
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime


class OSINTTool:

    def __init__(self):
        self.session = requests.Session()
        self.data_folder = "data"
        self.database = os.path.join(self.data_folder, "osint_results.db")
        self.init_database()

    def init_database(self):
        """
        Initialize the SQLite database and create tables if they don't exist.
        """
        # Create the data folder if it doesn't exist
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
            print(f"Data folder '{self.data_folder}' created.")

        # Connect to the database
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS osint_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    query TEXT,
                    result TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
        print("Database initialized and ready.")

        # Run the main menu
        self.main_menu()

    def main_menu(self):
        """
        Display the main menu to select functionality.
        """
        while True:
            print("\nPlease select an option:")
            print("1. Domain Information")
            print("2. IP Geolocation")
            print("3. Email Validation")
            print("4. Social Media Username Lookup")
            print("5. Google Search")
            print("6. View Previous Results")
            print("7. Exit")
            choice = input("Enter your choice (1-7): ")

            if choice == '1':
                domain = input("Enter the domain (e.g., example.com): ")
                self.domain_info(domain)
            elif choice == '2':
                ip = input("Enter the IP address (e.g., 8.8.8.8): ")
                self.ip_geolocation(ip)
            elif choice == '3':
                email = input(
                    "Enter the email address (e.g., user@example.com): ")
                self.email_validation(email)
            elif choice == '4':
                username = input(
                    "Enter the social media username (e.g., johndoe): ")
                self.social_media_lookup(username)
            elif choice == '5':
                query = input("Enter the search query: ")
                self.google_search(query)
            elif choice == '6':
                self.view_previous_results()
            elif choice == '7':
                print("Exiting the OSINT Tool. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def save_results(self, osint_type, query, content):
        """
        Save results to the SQLite database and as a text file.
        """
        # Save to the SQLite database
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO osint_data (type, query, result) VALUES (?, ?, ?)
            """, (osint_type, query, content))
            conn.commit()
        print(f"Results saved to database under {osint_type}.")

        # Save to a text file
        filename = f"{
            self.data_folder}/{osint_type}_{query.replace(' ', '_')}.txt"
        with open(filename, 'w') as file:
            file.write(f"Type: {osint_type}\n")
            file.write(f"Query: {query}\n")
            file.write(f"Result:\n{content}\n")
        print(f"Results also saved as a text file: {filename}")

    def domain_info(self, domain):
        """
        Fetch WHOIS data for a domain.
        """
        try:
            whois_data = whois.whois(domain)
            result = f"\nWHOIS Information for domain: {domain}\n{whois_data}"
            print(result)
            self.save_results("Domain Information", domain, str(whois_data))
        except Exception as e:
            print(f"Error fetching WHOIS data: {e}")

    def ip_geolocation(self, ip):
        """
        Fetch IP geolocation information using an external API.
        """
        try:
            response = self.session.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            if data['status'] == 'fail':
                print("Invalid IP or unable to fetch geolocation data.")
                return

            result = (
                f"\nIP Geolocation Information for IP: {ip}\n"
                f"Country: {data['country']}\n"
                f"City: {data['city']}\n"
                f"ISP: {data['isp']}\n"
                f"Latitude: {data['lat']}\n"
                f"Longitude: {data['lon']}\n"
            )
            print(result)
            self.save_results("IP Geolocation", ip, json.dumps(data))
        except Exception as e:
            print(f"Error fetching geolocation data: {e}")

    def email_validation(self, email):
        """
        Basic email format validation and checking if it's a real domain.
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Invalid email format.")
            return

        domain = email.split("@")[1]
        try:
            socket.gethostbyname(domain)
            result = f"\nThe domain {domain} exists for the email: {email}."
            print(result)
            self.save_results("Email Validation", email, result)
        except socket.gaierror:
            result = f"\nThe domain {
                domain} does not exist for the email: {email}."
            print(result)
            self.save_results("Email Validation", email, result)

    def social_media_lookup(self, username):
        """
        Check username existence on popular social media platforms.
        """
        platforms = {
            "Twitter": f"https://twitter.com/{username}",
            "Instagram": f"https://www.instagram.com/{username}",
            "Facebook": f"https://www.facebook.com/{username}",
            "LinkedIn": f"https://www.linkedin.com/in/{username}"
        }

        result = f"\nSocial Media Lookup Results for username: {username}\n"
        for platform, url in platforms.items():
            response = self.session.get(url)
            if response.status_code == 200:
                result += f"[+] {username} exists on {platform}: {url}\n"
            else:
                result += f"[-] {username} does not exist on {platform}.\n"

        print(result)
        self.save_results("Social Media Lookup", username, result)

    def google_search(self, query, num_results=5):
        """
        Perform a Google search and return the top results.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        }
        try:
            response = self.session.get(
                f"https://www.google.com/search?q={query}&num={num_results}", headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = []
            for item in soup.find_all('h3'):
                if item.text:
                    search_results.append(item.text)
            result = f"\nGoogle Search Results for query: {query}\n"
            for idx, res in enumerate(search_results, start=1):
                result += f"{idx}. {res}\n"

            print(result)
            self.save_results("Google Search", query, result)
        except Exception as e:
            print(f"Error performing Google search: {e}")

    def view_previous_results(self):
        """
        Display previously saved results.
        """
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM osint_data ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            print("\nPrevious Results:")
            for row in rows:
                print(f"\nID: {row[0]}, Type: {row[1]}, Query: {row[2]}")
                print(f"Result: {row[3]}")
                print(f"Timestamp: {row[4]}")
                print("-" * 50)


# Start the OSINT tool
if __name__ == "__main__":
    osint_tool = OSINTTool()
    osint_tool.main_menu()
