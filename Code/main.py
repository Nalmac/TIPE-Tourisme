from Utils.FileUtils import load_city
from random import randint
from interval import interval
import neat
import os
import datetime

SITES,ADJACENCE,TRAJETS = load_city("Tests/City2.json")

DUREE = 28800 #8h en secondes
BUDGET = 80 #40 euros la journée
HEURE_DEBUT = 30600 #La visite débute à 8h30 ; Evidemment changeable
PROBAS_REFUS = [0.1, 0.3, 0.5, 0.9] #Probabilité de se voir refuser l'entrée suivant l'affluence

#On va tout d'abord chercher à créer une fonction d'évaluation
#Le test : En 4h, faire visiter un ensemble de sites touristiques donné.
#On évalue ensuite les candidats via le ratio prix/nombre de sites visités

#Dans l'évaluation, on prend désormais en compte la fréquentation du lieu
def entree(freq : int) -> bool :
    p = PROBAS_REFUS[freq]
    indic = randint(0, 1)
    return (indic > p)

#Retourne l'indice de fréquentation d'un site à une heure donnée
def get_freq(site : list, clock : float) -> int:
    for i in range(len(site["freq"])):
        if clock in interval(site["freq"][i]):
            return i

#Evaluation globale de la population
def eval_guide(genomes, config):
    for genome_id,genome in genomes:
        cout = 0
        temps = DUREE
        montre = HEURE_DEBUT
        duree_visite = 0
        visites = []
        lieu_actuel = randint(0, 3)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        while temps > 0:
            input = (cout, temps)
            for i in ADJACENCE[lieu_actuel]:
                input = input + (SITES[i]["duree"], SITES[i]["prix"])
            output = net.activate(input)
            dest_id = ADJACENCE[lieu_actuel][output.index(max(output))]
            if not dest_id in visites :
                destination = SITES[dest_id]
                freq = get_freq(destination, montre)
                if entree(freq):
                    cout += destination["prix"]
                    temps_visite = destination["duree"] + TRAJETS[lieu_actuel][dest_id]
                    duree_visite += TRAJETS[lieu_actuel][dest_id]
                else:
                    temps_visite = TRAJETS[lieu_actuel][dest_id] + 300
                temps -= temps_visite
                montre += temps_visite
                lieu_actuel = dest_id
                visites.append(lieu_actuel)
            else :
                temps -= 300
                montre += 300
        if cout > BUDGET or len(visites) <= 2:
            genome.fitness = 0
        else :
            genome.fitness = duree_visite/cout
        temps = DUREE
        cout = 0
            

# On lance l'entraînement

def run(config_file):
    #Initialisation de la configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)    

    #Création de la population
    popu = neat.Population(config)

    #Génération de rapports
    popu.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    popu.add_reporter(stats)
    #100 générations pour commencer
    top = popu.run(eval_guide, 100)

    #Affichage du meilleur après les 100 générations, ou bien si le seuil de fitness a été atteint

    print('\nRésultat:')
    guide = neat.nn.FeedForwardNetwork.create(top, config)
    cout = 0
    temps = DUREE
    visites = []
    lieu_actuel = randint(0, 3)
    while temps > 0:
        input = (cout, temps)
        for i in ADJACENCE[lieu_actuel]:
            input = input + (SITES[i]["duree"], SITES[i]["prix"])
        output = guide.activate(input)
        dest_id = ADJACENCE[lieu_actuel][output.index(max(output))]
        if not dest_id in visites :
            destination = SITES[dest_id]
            cout += destination["prix"]
            temps -= destination["duree"] + TRAJETS[lieu_actuel][dest_id]
            lieu_actuel = dest_id
            visites.append(lieu_actuel)
        else :
            temps -= 300
    print(visites)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'Conf/City2.conf')
    run(config_path)
