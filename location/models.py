from django.db import models

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Countries cannot be deleted.')

class USState(models.Model):
    us_states_id = models.AutoField(primary_key=True)
    us_state_name = models.CharField(max_length=255)
    us_state_abbreviation = models.CharField(max_length=2,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('USStates cannot be deleted.')


class USZIPCode(models.Model):
    us_zip_code_id = models.AutoField(primary_key=True)
    us_zip_code = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('USZIPCodes cannot be deleted.')


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255)
    us_zip_code = models.ForeignKey(USZIPCode,related_name="city_us_zip_code",null=True,blank=True)
    us_state = models.ForeignKey(USState,related_name="city_us_state",null=True,blank=True)
    country = models.ForeignKey(Country,related_name="city_country")
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('Cities cannot be deleted.')


class GeographicTarget(models.Model):
    geographic_target_id = models.AutoField(primary_key=True)
    geographic_countries_flag = models.BooleanField(default=False)
    geographic_countries = 	models.ManyToManyField(Country, related_name="geographic_countries",blank=True,null=True) #foreign key to Countries
    geographic_states_flag = models.BooleanField(default=False)
    geographic_states = models.ManyToManyField(USState,related_name="geographic_states",blank=True,null=True)
    geographic_zip_codes_flag = models.BooleanField(default=False)
    geographic_zip_codes = models.ManyToManyField(USZIPCode, related_name="geographic_zip_codes",blank=True,null=True)
    geographic_cities_flag = models.BooleanField(default=False)
    geographic_cities = models.ManyToManyField(City, related_name="geographic_cities",blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)
    is_active = models.BooleanField(default=True)

    def delete(self):
        '''disabling delete'''
        raise NotImplementedError('GeographicTargets cannot be deleted.')
