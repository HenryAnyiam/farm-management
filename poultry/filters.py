from django_filters import rest_framework as filters

from poultry.models import *


class CaseInsensitiveBooleanFilter(filters.BooleanFilter):
    def filter(self, qs, value):
        if value in ["true", "T", "t", "1"]:
            value = True
        elif value in ["false", "F", "f", "0"]:
            value = False
        return super().filter(qs, value)


class FlockSourceFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = FlockSource
        fields = ["name"]


class FlockBreedFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = FlockBreed
        fields = ["name"]


class HousingStructureFilterSet(filters.FilterSet):
    housing_type = filters.CharFilter(lookup_expr="icontains")
    category = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = HousingStructure
        fields = ["housing_type", "category"]


class FlockFilterSet(filters.FilterSet):
    source = filters.CharFilter(lookup_expr="icontains")
    breed = filters.CharFilter(lookup_expr="icontains")
    chicken_type = filters.CharFilter(lookup_expr="icontains")
    is_present = CaseInsensitiveBooleanFilter(field_name="is_present")
    date_established = filters.DateFilter(
        field_name="date_established", lookup_expr="exact"
    )
    year_established = filters.NumberFilter(
        field_name="date_established__year", lookup_expr="exact"
    )
    month_established = filters.NumberFilter(
        field_name="date_established__month", lookup_expr="exact"
    )
    week_established = filters.NumberFilter(
        field_name="date_established__week", lookup_expr="exact"
    )
    day_established = filters.NumberFilter(
        field_name="date_established__day", lookup_expr="exact"
    )

    class Meta:
        model = Flock
        fields = [
            "source",
            "breed",
            "chicken_type",
            "date_established",
            "is_present",
            "year_established",
            "month_established",
            "week_established",
            "day_established",
        ]


class FeedPurchaseFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    variety = filters.CharFilter(lookup_expr="icontains")
    form = filters.CharFilter(lookup_expr="icontains")
    chicken_type = filters.CharFilter(lookup_expr="icontains")
    growth_stage = filters.CharFilter(lookup_expr="icontains")
    purchase_date = filters.DateFilter(
        field_name="purchase_date", lookup_expr="exact"
    )
    year_purchased = filters.NumberFilter(
        field_name="purchase_date__year", lookup_expr="exact"
    )
    month_purchased = filters.NumberFilter(
        field_name="purchase_date__month", lookup_expr="exact"
    )
    week_purchased = filters.NumberFilter(
        field_name="purchase_date__week", lookup_expr="exact"
    )
    day_purchased = filters.NumberFilter(
        field_name="purchase_date__day", lookup_expr="exact"
    )

    class Meta:
        model = FeedPurchase
        fields = [
            "name",
            "variety",
            "form",
            "chicken_type",
            "growth_stage",
            "purchase_date",
            "year_purchased",
            "month_purchased",
            "week_purchased",
            "day_purchased",
        ]

class FeedingFilterSet(filters.FilterSet):
    feed = filters.CharFilter(lookup_expr="icontains")
    flock = filters.CharFilter(lookup_expr="icontains")
    feed_date = filters.DateFilter(
        field_name="feed_date", lookup_expr="exact"
    )
    year_fed = filters.NumberFilter(
        field_name="feed_date__year", lookup_expr="exact"
    )
    month_fed = filters.NumberFilter(
        field_name="feed_date__month", lookup_expr="exact"
    )
    week_fed = filters.NumberFilter(
        field_name="feed_date__week", lookup_expr="exact"
    )
    day_fed = filters.NumberFilter(
        field_name="feed_date__day", lookup_expr="exact"
    )

    class Meta:
        model = Feeding
        fields = [
            "feed",
            "flock",
            "feed_date",
            "year_fed",
            "month_fed",
            "week_fed",
            "day_fed",
        ]


class TreatmentFilterSet(filters.FilterSet):
    flock = filters.CharFilter(lookup_expr="icontains")
    treatment_type = filters.CharFilter(lookup_expr="icontains")
    treatment_method = filters.CharFilter(lookup_expr="icontains")
    veterinarian = filters.CharFilter(lookup_expr="icontains")
    date_administered = filters.DateFilter(
        field_name="date_administered", lookup_expr="exact"
    )
    year_administered = filters.NumberFilter(
        field_name="date_administered__year", lookup_expr="exact"
    )
    month_administered = filters.NumberFilter(
        field_name="date_administered__month", lookup_expr="exact"
    )
    week_administered = filters.NumberFilter(
        field_name="date_administered__week", lookup_expr="exact"
    )
    day_administered = filters.NumberFilter(
        field_name="date_administered__day", lookup_expr="exact"
    )

    class Meta:
        model = Treatment
        fields = [
            "flock",
            "treatment_type",
            "treatment_method",
            "veterinarian",
            "date_administered",
            "year_administered",
            "month_administered",
            "week_administered",
            "day_administered",
        ]


class EggSalesFilterSet(filters.FilterSet):
    date_sold = filters.DateFilter(
        field_name="date_sold", lookup_expr="exact"
    )
    year_sold = filters.NumberFilter(
        field_name="date_sold__year", lookup_expr="exact"
    )
    month_sold = filters.NumberFilter(
        field_name="date_sold__month", lookup_expr="exact"
    )
    week_sold = filters.NumberFilter(
        field_name="date_sold__week", lookup_expr="exact"
    )
    day_sold = filters.NumberFilter(
        field_name="date_sold__day", lookup_expr="exact"
    )

    class Meta:
        model = EggSales
        fields = [
            "date_sold",
            "year_sold",
            "month_sold",
            "week_sold",
            "day_sold",
        ]


class FinanceFilterSet(filters.FilterSet):
    category = filters.CharFilter(lookup_expr="icontains")
    finance_type = filters.CharFilter(lookup_expr="icontains")
    beneficiary = filters.CharFilter(lookup_expr="icontains")
    date_occurred = filters.DateFilter(
        field_name="date_occurred", lookup_expr="exact"
    )
    year_occurred = filters.NumberFilter(
        field_name="date_occurred__year", lookup_expr="exact"
    )
    month_occurred = filters.NumberFilter(
        field_name="date_occurred__month", lookup_expr="exact"
    )
    week_occurred = filters.NumberFilter(
        field_name="date_occurred__week", lookup_expr="exact"
    )
    day_occurred = filters.NumberFilter(
        field_name="date_occurred__day", lookup_expr="exact"
    )

    class Meta:
        model = Finance
        fields = [
            "category",
            "finance_type",
            "beneficiary",
            "date_occurred",
            "year_occurred",
            "month_occurred",
            "week_occurred",
            "day_occurred",
        ]


class FlockHistoryFilterSet(filters.FilterSet):
    flock = filters.CharFilter(lookup_expr="icontains")
    rearing_method = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = FlockHistory
        fields = ["flock", "rearing_method"]


class FlockMovementFilterSet(filters.FilterSet):
    flock = filters.CharFilter(lookup_expr="icontains")
    from_structure = filters.CharFilter(lookup_expr="icontains")
    to_structure = filters.CharFilter(lookup_expr="icontains")
    year_of_movement = filters.NumberFilter(
        field_name="movement_date__year", lookup_expr="exact"
    )
    month_of_movement = filters.NumberFilter(
        field_name="movement_date__month", lookup_expr="exact"
    )
    week_of_movement = filters.NumberFilter(
        field_name="movement_date__week", lookup_expr="exact"
    )
    day_of_movement = filters.NumberFilter(
        field_name="movement_date__day", lookup_expr="exact"
    )

    class Meta:
        model = FlockMovement
        fields = [
            "flock",
            "from_structure",
            "to_structure",
            "year_of_movement",
            "month_of_movement",
            "week_of_movement",
            "day_of_movement",
        ]


class FlockInspectionRecordFilterSet(filters.FilterSet):
    flock = filters.CharFilter(lookup_expr="icontains")
    month_of_inspection = filters.NumberFilter(
        field_name="date_of_inspection__month", lookup_expr="exact"
    )
    week_of_inspection = filters.NumberFilter(
        field_name="date_of_inspection__week", lookup_expr="exact"
    )
    day_of_inspection = filters.NumberFilter(
        field_name="date_of_inspection__day", lookup_expr="exact"
    )

    class Meta:
        model = FlockInspectionRecord
        fields = [
            "flock",
            "month_of_inspection",
            "week_of_inspection",
            "day_of_inspection",
        ]


class EggCollectionFilterSet(filters.FilterSet):
    flock = filters.CharFilter(lookup_expr="icontains")
    month_of_collection = filters.NumberFilter(
        field_name="date_of_collection__month", lookup_expr="exact"
    )
    week_of_collection = filters.NumberFilter(
        field_name="date_of_collection__week", lookup_expr="exact"
    )
    day_of_collection = filters.NumberFilter(
        field_name="date_of_collection__day", lookup_expr="exact"
    )
    time_of_collection = filters.NumberFilter(
        field_name="time_of_collection__day", lookup_expr="exact"
    )

    class Meta:
        model = EggCollection
        fields = [
            "flock",
            "month_of_collection",
            "week_of_collection",
            "day_of_collection",
            "time_of_collection",
        ]
