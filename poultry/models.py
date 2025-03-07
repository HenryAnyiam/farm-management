from datetime import date, timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models import Sum

from poultry.utils import todays_date
from poultry.validators import *
from users.models import Organization

def get_current_time():
    return timezone.now().time()

#9
class FlockSource(models.Model):
    """
    The model represents the source of a flock in a poultry farm.

    Fields:
    - `source`: A character field representing the source of the flock.
                It is limited to a maximum length of 13 characters.
                The available choices are defined in the `FlockSourceChoices` enum.

    """

    name = models.CharField(max_length=13, choices=FlockSourceChoices.choices)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='sources', null=True)

    def clean(self):
        FlockSourceValidator.validate_source(self.name, self.organization)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)

#8
class FlockBreed(models.Model):
    """
    Model representing a breed.

    Fields:
    - `name`: A CharField representing the name of the breed.

    """

    name = models.CharField(max_length=20, choices=FlockBreedTypeChoices.choices)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='breeds', null=True)

    def __str__(self):
        return self.name

    def clean(self):
        FlockBreedValidator.validate_breed_name(self.name, self.organization)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)

#7
class HousingStructure(models.Model):
    """
    The model represents a housing structure for poultry in a farm.

    Fields:
    - `house_type`: A character field representing the type of the housing structure.
              It is limited to a maximum length of 22 characters.
              The available choices are defined in the `HousingStructureTypeChoices` enum.
    - `category`: A character field representing the category of the housing structure.
                  It is limited to a maximum length of 21 characters.
                  The available choices are defined in the `HousingStructureCategoryChoices` enum.

    Methods:
    - `clean()`: This method performs validation on the model instance.
                 It ensures that specific combinations of `type` and `category` are valid.
                 For example, if the category is "Brooder Chick House", only "Deep Litter House" and "Closed Shed"
                 structure types are allowed, and an error is raised if an invalid type is chosen.
                 Similarly, if the category is "Breeders House", the "Pasture Housing" structure type is not allowed,
                 and a validation error is raised.
    - `save(*args, **kwargs)`: This overridden method calls `clean()` to perform validation before saving the instance.

    """

    house_type = models.CharField(
        max_length=22, choices=HousingStructureTypeChoices.choices
    )
    category = models.CharField(
        max_length=21, choices=HousingStructureCategoryChoices.choices
    )
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='structures', null=True)

    def __str__(self):
        """
        Returns a string representation of the housing structure.

        """
        return f"Housing Structure #{self.id}"

    def clean(self):
        """
        Performs validation on the model instance.

        Raises:
        - `ValidationError`: If the combination of `house_type` and `category` is invalid.

        """
        HousingStructureValidator.validate_category(self.category, self.house_type)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to perform validation before saving.

        """
        self.clean()
        super().save(*args, **kwargs)

#6
class Flock(models.Model):
    """
    The model represents a flock in a poultry farm.

    Fields:
    - `source`: A foreign key to the `FlockSource` model, representing the source of the flock.
    - `breed`: A foreign key to the `FlockBreed` model, representing the breed of the flock.
    - `chicken_type`: A character field representing the type of chickens in the flock.
                      It is limited to a maximum length of 15 characters.
                      The available choices are defined in the `ChickenTypeChoices` enum.
    - `initial_number_of_birds`: A positive integer field representing the initial number of birds in the flock.
                                 It is validated to ensure it is at least 2.
    - `current_rearing_method`: A character field representing the current rearing method of the flock.
                                It is limited to a maximum length of 50 characters.
                                The available choices are defined in the `RearingMethodChoices` enum.
    - `current_housing_structure`: A foreign key to the `HousingStructure` model, representing the current housing
                                  structure for the flock.
    - `date_established`: A date field that automatically records the date when the flock was established.
    - `is_present`: A boolean field indicating if the flock is currently present. It is set to True by default.

    Properties:
    - `name`: Returns a string representing the name of the flock, including its ID and the date of establishment.
    - `age_in_weeks`: Calculates and returns the age of the flock in weeks.
    - `age_in_months`: Calculates and returns the age of the flock in months.
    - `age_in_weeks_in_farm`: Calculates and returns the age of the flock in weeks since establishment.
    - `age_in_months_in_farm`: Calculates and returns the age of the flock in months since establishment.

    """

    source = models.ForeignKey(FlockSource, on_delete=models.PROTECT, related_name="flocks")
    breed = models.ForeignKey(FlockBreed, on_delete=models.PROTECT, related_name="flocks")
    chicken_type = models.CharField(max_length=15, choices=ChickenTypeChoices.choices)
    age_in_weeks = models.PositiveIntegerField()
    initial_number_of_birds = models.PositiveIntegerField(validators=[MinValueValidator(2)])
    unit_prices = models.PositiveIntegerField()
    initial_weight = models.PositiveIntegerField(validators=[MinValueValidator(2)])
    current_rearing_method = models.CharField(max_length=50, choices=RearingMethodChoices.choices)
    current_housing_structure = models.ForeignKey(HousingStructure, on_delete=models.PROTECT, related_name="flocks")
    date_established = models.DateField(default=timezone.now)
    is_present = models.BooleanField(default=True, editable=False)
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='flocks', null=True)

    @property
    def age_in_months(self):
        """
        Calculates and returns the age of the flock in months.

        """
        age_in_days = (todays_date - timedelta(days=(self.age_in_weeks * 7))).days
        age_in_months = age_in_days // 30
        return age_in_months

    @property
    def age_in_weeks_in_farm(self):
        """
        Calculates and returns the age of the flock in weeks since establishment.

        """
        age_in_days = (todays_date - self.date_established).days
        age_in_weeks_in_farm = age_in_days // 7
        return age_in_weeks_in_farm

    @property
    def age_in_months_in_farm(self):
        """
        Calculates and returns the age of the flock in months since establishment.

        """
        age_in_days = (todays_date - self.date_established).days
        age_in_months_in_farm = age_in_days // 30
        return age_in_months_in_farm

    def __str__(self):
        """
        Returns a string representation of the flock.
        """
        return self.name

    def clean(self):
        FlockValidator.validate_chicken_type_update(self)
        FlockValidator.validate_flock_housing(self.chicken_type, self.current_housing_structure, self.age_in_weeks)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

#5
class FlockHistory(models.Model):
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    rearing_method = models.CharField(
        max_length=50, choices=RearingMethodChoices.choices
    )
    current_housing_structure = models.ForeignKey(
        HousingStructure, on_delete=models.CASCADE
    )
    date_changed = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='flock_histories', null=True)

    def __str__(self):
        return f"History for {self.flock}"

#4
class FlockMovement(models.Model):
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    from_structure = models.ForeignKey(HousingStructure, on_delete=models.CASCADE, related_name='outgoing_movements')
    to_structure = models.ForeignKey(HousingStructure, on_delete=models.CASCADE, related_name='incoming_movements')
    movement_date = models.DateField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='flock_movements', null=True)

    def clean(self):
        FlockMovementValidator.validate_flock_movement(self.flock, self.to_structure, self.from_structure)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Movement of Flock {self.flock.id} ({self.from_structure} -> {self.to_structure})'

#3
class FlockInspectionRecord(models.Model):
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    date_of_inspection = models.DateField()
    number_of_dead_birds = models.PositiveIntegerField(default=0)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='inspections', null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.flock} Inspection Report on: {self.date_of_inspection}"

    def save(self, *args, **kwargs):
        FlockInspectionRecordValidator.validate_flock_availability(self.flock)
        FlockInspectionRecordValidator.validate_number_of_dead_birds(self)
        super().save(*args, **kwargs)
        FlockInspectionRecordValidator.validate_daily_number_of_inspection_records(self.date_of_inspection)
        FlockInspectionRecordValidator.validate_inspection_record_time_separation(self.flock, self)

#2
class FlockBreedInformation(models.Model):
    """
    Model representing the information about a flock breed.

    The FlockBreedInformation model contains details such as the breed,
    chicken type, average mature weight, average egg production, and maturity age.

    Fields:
    - breed: ForeignKey to the FlockBreed model, specifying the breed of the flock.
    - chicken_type: CharField specifying the type of chicken, chosen from a set of choices.
    - date_added: DateField automatically set to the date of creation.
    - average_mature_weight_in_kgs: DecimalField specifying the average mature weight of the flock in kilograms,
      with no specific minimum value.
    - average_egg_production: PositiveIntegerField specifying the average egg production of the flock,
      with the option to be null.
    - maturity_age_in_weeks: PositiveIntegerField specifying the maturity age of the flock in weeks,
      with a minimum value of 6."""

    breed = models.ForeignKey(FlockBreed, on_delete=models.CASCADE)
    chicken_type = models.CharField(max_length=15, choices=ChickenTypeChoices.choices)
    date_added = models.DateField(auto_now_add=True)
    average_mature_weight_in_kgs = models.DecimalField(max_digits=3, decimal_places=2)
    average_egg_production = models.PositiveIntegerField(blank =True, null=True)
    maturity_age_in_weeks = models.PositiveIntegerField(validators=[MinValueValidator(8), MaxValueValidator(24)])
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='breed_information', null=True)
    
    def clean(self):
        FlockBreedInformationValidator.validate_fields(self.chicken_type, self.average_egg_production,
                                                       self.average_mature_weight_in_kgs, self.maturity_age_in_weeks)                          

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

#1
class EggCollection(models.Model):
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    date_of_collection = models.DateField(auto_now_add=True)
    time_of_collection = models.TimeField(auto_now_add=True)
    collected_eggs = models.PositiveIntegerField(default=0)
    broken_eggs = models.PositiveIntegerField(default=0)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='egg_collections', null=True)

    @property
    def picking_time(self):
        """
        Returns a string indicating whether the egg collection was done in the morning or afternoon.

        Returns:
        - str: The picking time, either 'Morning' or 'Afternoon'.

        """
        hour = self.time_of_collection.hour
        if hour < 12:
            return "Morning"
        else:
            return "Afternoon"

    def clean(self):
        EggCollectionValidator.validate_flock_eligibility(self.flock)
        EggCollectionValidator.validate_egg_collection_records_per_day(self.flock)
        EggCollectionValidator.validate_egg_collection_count(
            self.flock, self.date_of_collection, self.broken_eggs, self.collected_eggs, self.pk
        )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class FeedPurchase(models.Model):

    name = models.CharField(max_length=250)
    variety = models.CharField(max_length=250)
    form = models.CharField(max_length=20, choices=FeedTypeChoices.choices)
    chicken_type = models.CharField(max_length=15, choices=ChickenTypeChoices.choices)
    growth_stage = models.CharField(max_length=20, choices=GrowthStageChoices.choices)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    size_of_bags = models.PositiveIntegerField()
    total_bags = models.PositiveIntegerField()
    purchase_date = models.DateField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='feeds', null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)

    @property
    def total_feed_weight(self):
        return (self.size_of_bags or 1) * (self.total_bags or 1)
    
    @property
    def total_feed_left(self):
        size_of_bags = 1
        if self.size_of_bags:
            size_of_bags = self.size_of_bags
        total_bags = 1
        if self.total_bags:
            total_bags = self.total_bags
        total = self.feeding.aggregate(total=Sum('feed_weight'))['total']
        if not total:
            total = 0
        
        return (size_of_bags * total_bags) - total


class Feeding(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='feeding', null=True)
    feed_weight = models.FloatField()
    feed = models.ForeignKey(FeedPurchase, on_delete=models.PROTECT, related_name='feeding')
    water_qty = models.FloatField()
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE, related_name='feeding')
    notes = models.TextField(null=True)
    feed_date = models.DateField(default=timezone.now)
    feed_time = models.TimeField(default=get_current_time)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def clean(self):
        FeedingValidator.validate_feed_weight(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Treatment(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='treatment', null=True)
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE, related_name='treatment')
    treatment_type = models.CharField(max_length=20, choices=TreatmentTypeChoices.choices)
    details = models.CharField(max_length=250)
    dosage = models.CharField(max_length=250)
    associated_cost = models.DecimalField(max_digits=20, decimal_places=2)
    treatment_method = models.CharField(max_length=20, choices=TreatmentMethodChoices.choices)
    birds_treated = models.PositiveIntegerField()
    veterinarian = models.CharField(max_length=250)
    notes = models.TextField(null=True)
    date_administered = models.DateField(default=timezone.now)
    time_administered = models.TimeField(default=get_current_time)
    date_recorded = models.DateTimeField(auto_now_add=True)


class FlockWeight(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='weight', null=True)
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE, related_name='weight')
    weight = models.DecimalField(max_digits=3, decimal_places=2,
                                 validators=[MinValueValidator(0.1), MaxValueValidator(5)])
    date_weighed = models.DateField(default=timezone.now)
    date_recorded = models.DateTimeField(auto_now_add=True)


class EggSales(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='egg_sales', null=True)
    no_of_crates = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    date_sold = models.DateField(default=timezone.now)
    date_recorded = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True)


class Finance(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='finance', null=True)
    category = models.CharField(max_length=10, choices=FinanceCategoryChoices.choices)
    finance_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date_occurred = models.DateField(default=timezone.now)
    date_recorded = models.DateTimeField(auto_now_add=True)
    beneficiary = models.CharField(max_length=250)
    description = models.TextField(null=True)
