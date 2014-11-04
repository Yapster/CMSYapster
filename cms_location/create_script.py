# from cms_location.models import *
# import csv
#
#
# print("starting on countries")
# with open('countries.csv','Ur') as f:
#     reader = csv.reader(f)
#     header = reader.next()
#     countries = [x[1] for x in reader]
#
# print("starting on states_abbreviations")
# with open('state_table.csv','Ur') as f:
#     reader = csv.reader(f)
#     header = reader.next()
#     states = [x[1] for x in reader]
#
# print("starting on states_abbreviations")
# with open('state_table.csv','Ur') as f:
#     reader = csv.reader(f)
#     header = reader.next()
#     states_a = [x[2] for x in reader]
#
# print("starting cities")
# with open('cities.csv','Ur') as f:
#     reader = csv.reader(f)
#     header = reader.next()
#     cities = [x[2] for x in reader]
#
# print("starting on zip_codes")
# with open('zip_code_database.csv','Ur') as f:
#     reader = csv.reader(f)
#     header = reader.next()
#     zip_codes = [x[0] for x in reader]
#
#
#
# def create_countries():
#     print(countries)
#     for country in countries:
#         print(country)
#         country_name = {
#         'country':country
#         }
#         CmsCountry.objects.create(**country_name)
#
# create_countries()
#
# def create_states():
#     print(states)
#     for state in states:
#         print(state)
#         state_name = {
#         'us_state':state
#         }
#         CmsUSState.objects.create(**state_name)
#
# create_states()
#
# def create_cities():
#     print(cities)
#     for city in cities:
#         print (city)
#         country = CmsCountry.objects.get(pk=184)
#         city_name = {
#         'city':city,
#         'country':country,
#         }
#         print(city_name)
#         CmsCity.objects.create(**city_name)
#
# create_cities()
#
# def create_zipcodes():
#     print(zip_codes)
#     for zipcode in zip_codes:
#         print(zipcode)
#         zipcode_number = {
#         'us_zip_code':zipcode
#         }
#         CmsUSZIPCode.objects.create(**zipcode_number)
#
# create_zipcodes()
