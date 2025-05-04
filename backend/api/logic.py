class Dorm:
    def __init__(self, building_id, ranks):
        self.building_id = building_id
        # self.name = name
        self.ra_ranks = ranks
        self.count = 0

    def __str__(self):
        return f"Dorm: {self.building_id}"

class Buildings:    
    def __init__(self,data):
        self.buildings = {}
        for d in data: 
            dorm = Dorm(d[0],d[1])
            self.buildings[dorm.building_id] = dorm 
        
    def get(self, id):
        return self.buildings[id]
    
    def __str__(self):
        str_to_return = ""
        for building in self.buildings.values():
            str_to_return += str(building) + "\n"
        return str_to_return
    
    def free_buildings(self): 
        return sorted(self.buildings.keys())


class RA: 
    def __init__(self, id, ranks): 
        self.applicant_id = id
        self.building_ranks = ranks
        self.free = True
        self.matched_with = None
        self.inverse = self.invert_ranks()

    def set_matched(self, matched):
        # Method to set the matched building
        self.matched_with = matched.building_id
        self.free = False


    def invert_ranks(self):
        # Method to invert the ranks and return as an array
        inverted = [0] * len(self.building_ranks)
        for index, rank in enumerate(self.building_ranks):
            inverted[rank - 1] = index + 1
        return inverted

    def preferred_building(self, other_building):
        # Method to check if the applicant prefers the other building
        return self.inverse[(other_building.building_id)-1] < self.inverse[(self.matched_with)-1]
    
    def __str__(self):
        return f"RA: {self.applicant_id}" 



class Applicants:
    def __init__(self, data):
        self.applicants = {}
        for d in data: 
            ra = RA(d[0],d[1])
            self.applicants[ra.applicant_id] = ra

    def get(self, id):
        return self.applicants[id]
    
    def matchings(self):
        matching = []
        for applicant in self.applicants.values():
            matching.append((applicant.applicant_id, applicant.matched_with))
        return matching
    
    def __str__(self):
        str_to_return = ""
        for app in self.applicants.values():
            str_to_return += str(app) + "\n"
        return str_to_return

def get_matching(a, b): 
    buildings = Buildings(b) 
    
    applicants = Applicants(a) 
    free_buildings = buildings.free_buildings()
    
    while len(free_buildings) > 0:
        proposing_dorm = buildings.get(free_buildings.pop(0))
        # print(proposing_dorm, end=" ")
        possible_ra = applicants.get(proposing_dorm.ra_ranks[proposing_dorm.count])
        # print(possible_ra)
        
        if possible_ra.free:
            proposing_dorm.count +=1 
            possible_ra.set_matched(proposing_dorm)
        else:
            #if the ra is matched check if they prefer the proposing building more
            if possible_ra.preferred_building(proposing_dorm):
                dumped_building = possible_ra.matched_with 
                possible_ra.set_matched(proposing_dorm)
                free_buildings.append(dumped_building)
                #print(f"RA {possible_ra.applicant_id} dumped Building {dumped_building} for Building {proposing_building.building_id}")
            else: 
                proposing_dorm.count += 1
                free_buildings.append(proposing_dorm.building_id)
                #print(f"RA {possible_ra.applicant_id} rejected Building {proposing_building.building_id} and is still matched with Building {possible_ra.matched_with}")
    # #print the matchings 
    return applicants.matchings()
    for applicant in matching:
        print(f"Applicant {applicant[0]} is matched with Building {applicant[1]}")