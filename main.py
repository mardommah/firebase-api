from handlers import add_data, read_all_data, update_data, get_data_by_id

# enable firestore api di google cloud console

data = {
    "nama": "Budi Gunawan",
    "umur": 20,
    "tempat_lahir": "Makassar"
}

# add_data("users", data)
read_all_data("users")

data_update = {
    "nama": "Budi Coy"
}

update_data("users", "mN6s1Vk47kwnygnEJr3m", data_update)

get_data_by_id("users", "mN6s1Vk47kwnygnEJr3m")