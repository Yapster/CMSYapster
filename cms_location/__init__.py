# import csv
# from cms_location.models import *
# from operator import itemgetter
#
# print("starting on countries")
# with open('cms_location/countries.csv', encoding="utf_8") as f:
#     reader = csv.reader(f)
#     header = reader.__next__()
#     countries = [x[1] for x in reader]
#
# print("starting on states_abbreviations")
# with open('cms_location/state_table.csv', encoding="utf_8") as f:
#     reader = csv.reader(f)
#     header = reader.__next__()
#     states = [x for x in reader]
#
# print("starting on states_abbreviations")
# with open('cms_location/state_table.csv', encoding="utf_8") as f:
#     reader = csv.reader(f)
#     header = reader.__next__()
#     states_a = [x for x in reader]
#
# print("starting on zip_codes")
# with open('cms_location/zip_code_database.csv', encoding="utf_8") as f:
#     reader = csv.reader(f)
#     header = reader.__next__()
#     zip_codes = [x[0] for x in reader]
#
# with open('cms_location/cities.csv', encoding="utf_8") as f:
#     reader = csv.reader(f)
#     header = reader.__next__()
#     cities = [x for x in reader]
#
#
#
# def create_countries():
#     print(countries)
#     for country in countries:
#         print(country)
#         CmsCountry.objects.create(country_name=country)
#
# create_countries()
#
# def create_states():
#     print(states)
#     for state in states:
#         print(state)
#         us_state_name= state[1]
#         us_state_abbreviation = state[2]
#         CmsUSState.objects.create(us_state_name=us_state_name, us_state_abbreviation=us_state_abbreviation)
#
# create_states()
#
# def create_zipcodes():
#     print(zip_codes)
#     for zipcode in zip_codes:
#         print(zipcode)
#         CmsUSZIPCode.objects.create(us_zip_code=zipcode)
#
# create_zipcodes()
#
# def create_cities():
#     print(cities)
#     for city in cities:
#         print (city)
#         country = CmsCountry.objects.get(pk=184)
#         us_zip_code = CmsUSZIPCode.objects.get(us_zip_code=city[3])
#         us_state = CmsUSState.objects.get(us_state_name=city[2].split(',')[1])
#         CmsCity.objects.create(city_name=city[1], country=country, us_zip_code=us_zip_code, us_state=us_state)
#
# create_cities()