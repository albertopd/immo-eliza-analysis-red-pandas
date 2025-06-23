# How many rows and columns?

- Number of rows = 76370
- Number of columns = 36

# What is the correlation between the variables and the price? (Why might that be?)

- Positive correlations (e.g., bedroomCount, kitchenTypeNormalize, terraceSurface, landSurface) suggest that larger or more equipped properties tend to have higher prices — which aligns with real estate market expectations.

- Negative correlations (e.g., epcScoreNormalize, heatingTypeNormalize) could indicate that poorer energy performance or certain heating types might lower the value.

# How are variables correlated to each other? (Why?)

While the plot doesn’t directly show inter-variable correlations, we can infer that:

- Variables like bedroomCount, roomCount, habitableSurface, landSurface, and bathroomCount are likely positively correlated among themselves — all relate to property size or livability.

- Boolean features such as hasGarden, hasLift, or hasAirConditioning likely correlate with landSurface or property type (e.g., houses vs. apartments).

These correlations happen because:

- Larger properties tend to have more rooms, land, and additional features.

- Energy efficiency (epcScoreNormalize) and building condition might inversely correlate with price due to renovation needs or regulatory impact.

# Which variables have the greatest influence on the price?

The most influential variables (strongest positive correlation with price) are:

- bedroomCount (~0.38)
- kitchenTypeNormalize
- terraceSurface
- landSurface
- facadeCount

These make sense — more bedrooms, better kitchen types, terraces, and land all add value.

# Which variables have the least influence on the price?

The least influential variables are those with correlation coefficients close to 0:

- hasThermicsPanels
- hasPhotovoltaicPanels
- hasFireplace
- hasOffice
- hasVisiophone

These have very weak or near-zero correlation with price — possibly because:

- They’re niche or present in both low- and high-priced homes.
- Buyers may not value them as highly in pricing, or they’re inconsistently recorded


# How many qualitative and quantitative variables are there? 

- Qualitative: 17
- Quantitative: 19

# How would you transform these values into numerical values?

We normalized => see code 

# Percentage of missing values per column?

Data                        type    Non-null count  Missing count  Missing %  Unique values
hasAirConditioning          object            1124          79244  98.601433              1
hasSwimmingPool             object            1816          78552  97.740394              1
hasDressingRoom             object            2628          77740  96.730042              1
hasFireplace                object            3044          77324  96.212423              1
hasThermicPanels            object            3112          77256  96.127812              1
hasArmoredDoor              object            3698          76670  95.398666              1
gardenOrientation           object            5601          74767  93.030808              8
diningRoomSurface          float64            6901          73467  91.413249             89
hasHeatPump                 object            7473          72895  90.701523              1
hasPhotovoltaicPanels       object            8048          72320  89.986064              1
hasOffice                   object           10387          69981  87.075702              1
terraceOrientation          object           11262          69106  85.986960              8
hasAttic                    object           12516          67852  84.426637              1
hasDiningRoom               object           14141          66227  82.404688              1
streetFacadeWidth          float64           15510          64858  80.701274            746
hasGarden                   object           15958          64410  80.143838              1
gardenSurface              float64           15958          64410  80.143838           1735
hasVisiophone               object           15991          64377  80.102777              1
parkingCountOutdoor        float64           18326          62042  77.197392             46
hasLift                     object           19044          61324  76.304002              1
roomCount                  float64           21948          58420  72.690623             48
kitchenSurface             float64           24263          56105  69.810123            119
parkingCountIndoor         float64           28239          52129  64.862881             86
terraceSurface             float64           28599          51769  64.414941            236
livingRoomSurface          float64           28950          51418  63.978200            194
hasBasement                 object           29315          51053  63.524039              1
floorCount                 float64           37546          42822  53.282401             40
landSurface                float64           39541          40827  50.800070           4374
kitchenType                 object           41916          38452  47.844913              8
hasLivingRoom               object           42876          37492  46.650408              1
floodZoneType               object           44466          35902  44.672009              9
heatingType                 object           47153          33215  41.328638              7
hasTerrace                  object           47429          32939  40.985218              1
buildingConstructionYear   float64           49106          31262  38.898567            229
facedeCount                float64           53239          27129  33.755973             12
toiletCount                float64           55094          25274  31.447840             26
buildingCondition           object           57992          22376  27.841927              6
epcScore                    object           65391          14977  18.635527             20
bathroomCount              float64           66672          13696  17.041609             30
habitableSurface           float64           67783          12585  15.659218           1015
bedroomCount               float64           73558           6810   8.473522             42
price                      float64           76370           3998   4.974617           5921
subtype                     object           80368              0   0.000000             26
postCode                     int64           80368              0   0.000000           1100
province                    object           80368              0   0.000000             11
locality                    object           80368              0   0.000000           5470
type                        object           80368              0   0.000000              4