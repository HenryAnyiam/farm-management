from rest_framework import serializers
from poultry.models import *


class FlockSourceSerializer(serializers.ModelSerializer):

    total_registered = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FlockSource
        fields = "__all__"
    
    def get_total_registered(self, obj):
        """get total flocks registered to house"""

        return obj.flocks.count()


class FlockBreedSerializer(serializers.ModelSerializer):

    total_registered = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FlockBreed
        fields = "__all__"
    
    def get_total_registered(self, obj):
        """get total flocks registered to house"""

        return obj.flocks.count()


class HousingStructureSerializer(serializers.ModelSerializer):

    total_registered = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HousingStructure
        fields = "__all__"

    def get_total_registered(self, obj):
        """get total flocks registered to house"""

        return obj.flocks.count()


class FlockSerializer(serializers.ModelSerializer):
    age_in_months = serializers.ReadOnlyField()
    age_in_weeks_in_farm = serializers.ReadOnlyField()
    age_in_months_in_farm = serializers.ReadOnlyField()
    current_housing_structure = serializers.PrimaryKeyRelatedField(
        queryset=HousingStructure.objects.all()
    )
    source = FlockSourceSerializer()
    breed = FlockBreedSerializer()

    class Meta:
        model = Flock
        fields = "__all__"

    def create(self, validated_data):
        flock_source_data = validated_data.pop("source")
        flock_breed_data = validated_data.pop("breed")
        organization = validated_data.get("organization")
        flock_source_data['organization'] = organization
        flock_breed_data['organization'] = organization
        source, _ = FlockSource.objects.get_or_create(**flock_source_data)
        breed, _ = FlockBreed.objects.get_or_create(**flock_breed_data)
        flock = Flock.objects.create(breed=breed, source=source, **validated_data)
        return flock

    def update(self, instance, validated_data):
        fields_to_exclude = [
            "source",
            "breed",
            "chicken_type",
            "initial_number_of_birds",
            "current_housing_structure",
            "date_established",
            "is_present",
        ]

        for field in fields_to_exclude:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)


class FlockHistorySerializer(serializers.ModelSerializer):

    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())
    current_housing_structure = serializers.PrimaryKeyRelatedField(queryset=HousingStructure.objects.all())

    flock_name = serializers.SerializerMethodField(read_only=True)
    housing_structure_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FlockHistory
        fields = "__all__"
    
    def get_flock_name(self, obj):
        return obj.flock.name if obj.flock else None

    def get_housing_structure_name(self, obj):
        return obj.current_housing_structure.name if obj.current_housing_structure else None

class FeedPurchaseSerializer(serializers.ModelSerializer):

    total_feed_weight = serializers.SerializerMethodField(read_only=True)
    total_feed_left = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FeedPurchase
        fields = "__all__"
    
    def get_total_feed_weight(self, obj):
        return obj.total_feed_weight

    def get_total_feed_left(self, obj):
        return obj.total_feed_left


class EggSalesSerializer(serializers.ModelSerializer):

    class Meta:
        model = EggSales
        fields = "__all__"


class FinanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Finance
        fields = "__all__"


class FeedingSerializer(serializers.ModelSerializer):

    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())
    flock_name = serializers.SerializerMethodField(read_only=True)
    feed_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Feeding
        fields = "__all__"
    
    def get_flock_name(self, obj):
        return obj.flock.name if obj.flock else None

    def get_feed_name(self, obj):
        return obj.feed.name if obj.feed else None


class TreatmentSerializer(serializers.ModelSerializer):

    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())
    flock_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Treatment
        fields = "__all__"
    
    def get_flock_name(self, obj):
        return obj.flock.name if obj.flock else None


class FlockWeightSerializer(serializers.ModelSerializer):

    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())
    flock_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FlockWeight
        fields = "__all__"
    
    def get_flock_name(self, obj):
        return obj.flock.name if obj.flock else None


class FlockMovementSerializer(serializers.ModelSerializer):
    """
    Serializer for the FlockMovement model.

    Serializes the following fields:
    - `flock`: The associated flock for the movement.
    - `from_structure`: The housing structure from which the flock is moved.
    - `to_structure`: The housing structure to which the flock is moved.

    """

    # Use PrimaryKeyRelatedField for accepting IDs during creation
    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())
    from_structure = serializers.PrimaryKeyRelatedField(queryset=HousingStructure.objects.all())
    to_structure = serializers.PrimaryKeyRelatedField(queryset=HousingStructure.objects.all())

    # Use SerializerMethodField for returning names during serialization
    flock_name = serializers.SerializerMethodField()
    from_structure_name = serializers.SerializerMethodField()
    to_structure_name = serializers.SerializerMethodField()

    

    class Meta:
        model = FlockMovement
        fields = "__all__"
        extra_kwargs = {
            'flock': {'write_only': True},
            'from_structure': {'write_only': True},
            'to_structure': {'write_only': True},
            'flock_name': {'read_only': True},
            'from_structure_name': {'read_only': True},
            'to_structure_name': {'read_only': True},
        }
    
    def get_flock_name(self, obj):
        return obj.flock.name if obj.flock else None

    def get_from_structure_name(self, obj):
        return obj.from_structure.name if obj.from_structure else None

    def get_to_structure_name(self, obj):
        return obj.to_structure.name if obj.to_structure else None


class FlockInspectionRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the FlockInspectionRecord model.

    Serializes the following fields:
    - `flock`: The associated flock for the inspection record.
    - `date`: The date and time of the inspection.
    - `number_of_dead_birds`: The number of dead birds recorded in the inspection.

    """

    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())
    flock_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FlockInspectionRecord
        fields = "__all__"
    
    def get_flock_name(self, obj):
        return obj.flock.name if obj.flock else None


class FlockBreedInformationSerializer(serializers.ModelSerializer):
    """
    Serializer for the FlockBreedInformation model.

    Serializes the following fields:
    - `breed`: The associated flock breed.
    - `chicken_type`: The type of chicken.
    - `date_added`: The date when the breed information was added.
    - `average_mature_weight_in_kgs`: The average mature weight of the breed in kilograms.
    - `average_egg_production`: The average egg production of the breed.
    - `maturity_age_in_weeks`: The maturity age of the breed in weeks.

    """

    breed = serializers.PrimaryKeyRelatedField(queryset=FlockBreed.objects.all())
    breed_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FlockBreedInformation
        fields = "__all__"
    
    def get_breed_name(self, obj):
        return obj.breed.name if obj.breed else None


class EggCollectionSerializer(serializers.ModelSerializer):
    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())
    flock_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EggCollection
        fields = "__all__"
    
    def get_flock_name(self, obj):
        return obj.flock.name if obj.flock else None
