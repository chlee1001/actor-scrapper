from filmmakers import get_profiles as get_filmmakers_profile
from save import save_to_file

filmmakers_profiles = get_filmmakers_profile()
profiles = filmmakers_profiles

save_to_file(profiles)
