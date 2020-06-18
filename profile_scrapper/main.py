from filmmakers import get_profiles as get_filmmakers_profile
from megaphone import get_profiles as get_megaphone_profile
from save import save_to_file

filmmakers_profiles = get_filmmakers_profile()
megaphone_profiles = get_megaphone_profile()
profiles = filmmakers_profiles + megaphone_profiles

save_to_file(profiles)
