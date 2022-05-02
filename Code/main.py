from Utils.FileUtils import load_city
from random import randint
import neat
import os
import datetime

SITES,ADJACENCE,TRAJETS = load_city("Tests/City2.json")

DUREE = 28800 #8h en secondes
BUDGET = 40 #40 euros la journée

#On va tout d'abord chercher à créer une fonction d'évaluation
#Le test : En 4h, faire visiter un ensemble de sites touristiques donné.
#On évalue ensuite les candidats via le ratio prix/nombre de sites visités

def eval_guide(genomes, config):
    for genome_id,genome in genomes:
        cout = 0
        temps = DUREE
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
                cout += destination["prix"]
                temps -= destination["duree"] + TRAJETS[lieu_actuel][dest_id]
                lieu_actuel = dest_id
                visites.append(lieu_actuel)
            else :
                temps -= 300
        if cout > BUDGET or len(visites) <= 2:
            genome.fitness = 0
        else :
            genome.fitness = (DUREE - temps)/cout
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
    popu.add_reporter(neat.Checkpointer(300))

    #300 générations pour commencer
    top = popu.run(eval_guide, 100)

    #Affichage du meilleur après les 300 générations

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

def cleanup():
    path = "Code/neat_checkpoints/checkpoint{}".format(datetime.datetime.now())
    os.mkdir(path)
    for target in os.listdir():
        if target[:15] == "neat-checkpoint":
            os.rename(target, "Code/neat_checkpoints/{}".format(path + "/" + target))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'City2.conf')
    run(config_path)
    cleanup()