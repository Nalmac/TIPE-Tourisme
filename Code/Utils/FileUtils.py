def export_city(CITY, path = "Tests/") -> None :
    import json
    SITES, ADJACENCE, TRAJETS = CITY.SITES, CITY.ADJACENCE, CITY.TRAJETS
    data = {
        "SITES" : SITES,
        "ADJACENCE" : ADJACENCE,
        "TRAJETS" : TRAJETS
    }
    with open("cities.env") as index :
        cities = index.read().split()
        new_city = str(int(cities[-1]) + 1)
        with open(path + "City" + new_city + ".json", "a") as city_file:
            json.dump(data, city_file)
        index.write(new_city)

def load_city(path : str) -> tuple :
    import json
    with open(path) as city_file:
        data = json.load(city_file)
    return data["SITES"], data["ADJACENCE"], data["TRAJETS"]

def gen_conf(city_path) -> None:
    import configparser
    n = len(load_city(city_path)[0])
    config = configparser.ConfigParser()
    template_conf = config.read()
    with open("cities.env") as index :
        cities = index.read().split()
        latest_city = str(int(cities[-1]))
        config.read("Conf/City" + latest_city)
        config["DefaultGenome"]["num_inputs"] = 2*n
        config["DefaultGenome"]["num_outputs"] = n-1
        with open("Conf/City" + str(int(latest_city) + 1), "w") as configfile:
            config.write(configfile)
            