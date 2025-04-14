import numpy as np

# Keep the STOP set as before
STOP = set('l le la les au aux un une du des c ça ce cette cet ces celle celui celles ceux je j tu il elle on nous vous ils elles me m te t se s y à de pour sans par mais ou et donc car ni or ne n pas dans que qui qu de d mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs lui en quel quelle quelles lequel laquelle lesquels lesquelles dont quoi quand où comment pourquoi sur dessus tout tous toutes avec comme avec'.split())

from similarite import DotProduct, LeastSquares, CityBlock

class Prediction:
    @staticmethod
    def predire(cerveau, mot, nb_syn, methode) -> list:
        """
        Calculez le nombre de mots nb_syn les plus similaires (et leurs scores de similarité) à « mot » 
        en utilisant la méthode de similarité indiquée par « methode » :
            0 : DotProduct
            1 : LeastSquares
            2 : CityBlock
        """

        if not hasattr(cerveau, 'matrice'):
            cerveau.charger_donnees()
            
        if mot not in cerveau.lexique:
            raise Exception(f'Le mot "{mot}" n\'est pas dans le lexique.')
        
        index = cerveau.lexique[mot]
        v = cerveau.matrice[index]
        
        similarity_calculators = {
            0: DotProduct(),
            1: LeastSquares(),
            2: CityBlock()
        }
        sim = similarity_calculators[methode]
        
        candidats = []
        for _mot, _index in cerveau.lexique.items():
            if _index != index and _mot not in STOP:
                score = sim.compute(v, cerveau.matrice[_index])
                candidats.append((_mot, score))
        
        if isinstance(sim, DotProduct):
            candidats = sorted(candidats, key=lambda t: t[1], reverse=True)
        else:
            candidats = sorted(candidats, key=lambda t: t[1])
            
        return candidats[:nb_syn]
