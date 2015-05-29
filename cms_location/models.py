from django.utils import timezone
from django.db import models

class CmsCountry(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)

    def delete(self):
        self.is_active = False
        self.date_deactivated = timezone.now()
        self.save(update_fields=['is_active','date_deactivated'])

class CmsUSState(models.Model):
    us_states_id = models.AutoField(primary_key=True)
    us_state_name = models.CharField(max_length=255)
    us_state_abbreviation = models.CharField(max_length=2,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)

    def delete(self):
        self.is_active = False
        self.date_deactivated = timezone.now()
        self.save(update_fields=['is_active','date_deactivated'])

    def load_all_usstates(self,country):
        if country.country == 'United States':
            us_states_list = CmsUSState.objects.filter(is_active=True)
            return us_states_list

class CmsUSZIPCode(models.Model):
    us_zip_code_id = models.AutoField(primary_key=True)
    us_zip_code = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)

    def delete(self):
        self.is_active = False
        self.date_deactivated = timezone.now()
        self.save(update_fields=['is_active','date_deactivated'])

    def check_if_zip_code_exists(self,zipcode):
        if zipcode == CmsUSZIPCode.objects.filter(us_zip_code=zipcode):
            return True
        else:
            return False

class CmsCity(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255)
    us_zip_code = models.ForeignKey(CmsUSZIPCode,related_name="city_us_zip_code",null=True,blank=True)
    us_state = models.ForeignKey(CmsUSState,related_name="city_us_state",null=True,blank=True)
    country = models.ForeignKey(CmsCountry,related_name="city_country")
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)

    def delete(self):
        self.is_active = False
        self.date_deactivated = timezone.now()
        self.save(update_fields=['is_active','date_deactivated'])

class CmsGeographicTarget(models.Model):
    geographic_target_id = models.AutoField(primary_key=True)
    geographic_countries_flag = models.BooleanField(default=False)
    geographic_countries = 	models.ManyToManyField(CmsCountry, related_name="geographic_countries",blank=True) #foreign key to Countries
    geographic_states_flag = models.BooleanField(default=False)
    geographic_states = models.ManyToManyField(CmsUSState,related_name="geographic_states",blank=True)
    geographic_zip_codes_flag = models.BooleanField(default=False)
    geographic_zip_codes = models.ManyToManyField(CmsUSZIPCode, related_name="geographic_zip_codes",blank=True)
    geographic_cities_flag = models.BooleanField(default=False)
    geographic_cities = models.ManyToManyField(CmsCity, related_name="geographic_cities",blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_deactivated = models.DateTimeField(blank=True,null=True)
    is_active = models.BooleanField(default=True)

    def delete(self):
        self.is_active = False
        self.date_deactivated = timezone.now()
        self.save(update_fields=['is_active','date_deactivated'])