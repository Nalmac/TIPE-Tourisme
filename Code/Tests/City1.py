# Durées en secondes, prix en euros
SITES = [
    {"duree" : 7200, "prix" : 10},
    {"duree" : 3600, "prix" : 13},
    {"duree" : 10800, "prix" : 12.50},
    {"duree" : 5400, "prix" : 11.80}
]

#On part du principe que tous les lieux sont connectés : "tous les chemins mènent à Rome", il reste donc simplement à modéliser les distances
#On compte ici en temps de trajet en secondes : TRAJETS[0][1] donne le temps de trajet entre le lieu 0 et le lieu 1
ADJACENCE = [
    [1, 2, 3],
    [0, 2, 3],
    [0, 1, 3],
    [0, 1, 2]
]

TRAJETS = [
    [0, 300, 600, 420],
    [300, 0, 720, 660],
    [600, 720, 0, 480],
    [420, 660, 480, 0]
]

