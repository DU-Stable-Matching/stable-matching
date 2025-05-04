from api.utlils import get_preferences
from api.logic import get_matching



# get all applicants
applicant_pref, building_pref = get_preferences()


print("Building Preferences:")
print(building_pref)
print("Applicant Preference:")
print(applicant_pref)

matching = get_matching(applicant_pref, building_pref)
print("Matching:")
print(matching)