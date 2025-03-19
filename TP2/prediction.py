import numpy as np

STOP = set('l le la les au aux un une du des c ça ce cette cet ces celle celui celles ceux je j tu il elle on nous vous ils elles me m te t se s y à de pour sans par mais ou et donc car ni or ne n pas dans que qui qu de d mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs lui en quel quelle quelles lequel laquelle lesquels lesquelles dont quoi quand où comment pourquoi sur dessus tout tous toutes avec comme avec'.split())

def least_squares(u, v):
    return np.sum((u - v)**2)

def city_block(u, v):
    return np.sum(np.abs(u - v))

class Prediction():
    @staticmethod
    def predire(cerveau, mot, nb_syn, methode) -> list[str, float]:
        if mot not in cerveau.lexique:
            raise Exception(f'Le mot "{mot}" n\'est pas dans le lexique.')
        
        index = cerveau.lexique[mot]
        v = cerveau.matrice[index]
        
        f = [np.dot, least_squares, city_block][methode]
        candidats = []
        for _mot, _index in cerveau.lexique.items():
            if _index != index and _mot not in STOP:
                candidats.append( ( _mot, f(v, cerveau.matrice[_index]) ) )
        
        return sorted(candidats, key=lambda t:t[1], reverse= f == np.dot)[:nb_syn]