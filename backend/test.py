from api.utlils import get_preferences


# get all applicants
admin_pref, applicant_pref = get_preferences()


print("Admin Preferences:")
print(admin_pref)
print("Applicant Preference:")
print(applicant_pref)
