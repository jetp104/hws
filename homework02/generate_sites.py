import random
import json

# Generate five random sites
sites = []
for i in range(5):
    lat = round(random.uniform(16.0, 18.0), 1)
    lon = round(random.uniform(82.0, 84.0), 1)
    comp = random.choice(["stony", "iron", "stony-iron"])
    sites.append({"site_id ": i+1, "latitude": lat, "longitude": lon, "composition": comp})


# Save the data to a JSON file
data = {"sites": sites}
with open("sites.json", "w") as f:
    json.dump(data, f)
