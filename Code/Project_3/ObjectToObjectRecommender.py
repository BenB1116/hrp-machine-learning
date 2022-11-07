class ObjectToObjectRecommender:
    import pandas as pd

    def __init__(self, df, actor_col, object_col):
        self.df = df
        self.actor_col = actor_col
        self.object_col = object_col

        # Create a list of object ids and patron ids
        self.object_ids = df[object_col].unique().tolist()
        self.actor_ids = df[actor_col].unique().tolist()

        # Create the actors by object and objects by actor dictionary
        self.objects_by_actor = {actor: df[df[actor_col] == actor][object_col].unique().tolist() for actor in self.actor_ids}
        self.actors_by_object = {object: df[df[object_col] == object][actor_col].unique().tolist() for object in self.object_ids}


    def union(self, list1, list2):
        return set.union(set(list1), set(list2))


    def intersect(self, list1, list2):
        return set.intersection(set(list1), set(list2))


    def jaccard(self, object1, object2):
        list1 = self.actors_by_object[object1]
        list2 = self.actors_by_object[object2]

        return len(self.intersect(list1, list2)) / len(self.union(list1, list2))

    def get_objects(self, actor_id):
        return self.objects_by_actor[actor_id]

    def get_actors(self, object_id):
        return self.actors_by_object[object_id]

    def get_canidates(self, object_id):
        # Create a list of all actors that have checked out that object
        common_actors = self.df[self.df[self.object_col] == object_id][self.actor_col].unique().tolist()
        
        # For each actor append its object list to common objects
        common_objects = []
        for actor in common_actors:
            common_objects.extend(self.objects_by_actor[actor])
        
        return list(set(common_objects))


    def get_sims(self, object_id):
        can_list = self.get_canidates(object_id)
        can_list.remove(object_id)
    
        if isinstance(can_list, type(None)):
            return {}
        
        return {can_id: self.jaccard(object_id, can_id) for can_id in can_list}


    def sort_sims(self, sims):
        return {object: sim for object, sim in sorted(sims.objects(), key = lambda object: object[1], reverse = True)}


    def get_top(self, object_id):
        sim_scores = self.get_sims(object_id)

        top = list(sim_scores.keys())[1]
        top_sim = sim_scores[top]

        return top, top_sim