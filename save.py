import csv
import requests


def save_to_csv(profiles):
    file = open("프로필.csv", mode="w", encoding="utf-8", newline="")
    writer = csv.writer(file)
    writer.writerow(["name", "age", "image_src"])
    for profile in profiles:
        writer.writerow(list(profile.values()))
    return


def save_image(profiles):
    for profile in profiles:
        name = profile.get("name")
        img_data = requests.get(profile.get("image_src")).content
        print(f"GET]{name}: {img_data}")
        if img_data:
            with open(f"./남자/{name}.jpg", 'wb') as handler:
                handler.write(img_data)


def save_to_file(profiles):
    save_to_csv(profiles)
    save_image(profiles)
    print("Save complete!")
