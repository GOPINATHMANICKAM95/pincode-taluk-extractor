from bs4 import BeautifulSoup
import requests
import pandas as pd
def extract_taluk_info(pincode):
    url = "https://pincode.net.in/" + pincode
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            taluk_tag = soup.find('b', string="Postal Taluk")
            taluk = taluk_tag.next_sibling.strip() if taluk_tag else "Not available"
            taluk = taluk.replace(':- ', '')
        except AttributeError:
            taluk = "Not available"
    else:
        taluk = "Not available"
    return taluk

# Read the CSV file into a DataFrame
df = pd.read_csv("sample.csv")

# Convert the pincode column to string
df["Pincode"] = df["Pincode"].apply(lambda x: str(x))

# Initialize a list to store taluk information
taluks = []

# Loop through each pincode and extract the taluk information
for pin in df["Pincode"]:
    taluk = extract_taluk_info(pin)
    taluks.append(taluk)

# Add the extracted taluk information to the DataFrame
df["Taluk"] = taluks

# Save the updated DataFrame back to a CSV file
df.to_csv("updated_sample.csv", index=False)
