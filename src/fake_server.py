from flask import Flask
import json
import random
import ipaddress
import copy
import iptools
from datetime import datetime

## Randomizer Code

ip_positions = [
    "alert_type_details.detail.srcipv4",
    "alert_type_details.detail.dstipv4"
]
domain_positions = [
    "alert_type_details.detail.cnchost"
]

isp_positions = [
    "alert_type_details.detail.dstisp"
]

user_positions = [
    "updated_by"
]

type_id_positions = [
    "alert_type.type_id"
]


def ip_type(ip):
    ip = ipaddress.ip_address(ip)
    if ip.is_private:
        return "private"
    elif ip.is_global:
        return "public" 
    else:
        return False

def get_random_ip(ip_type="private"):

    if ip_type == "private":
        private_class = random.randint(1, 3)
        if private_class == 1:
            return  "10.{}.{}.{}".format(
                str(random.randint(0, 255)),
                str(random.randint(0, 255)),
                str(random.randint(1, 254)),
            )
        elif private_class == 2:
            return  "172.{}.{}.{}".format(
                str(random.randint(16, 32)),
                str(random.randint(0, 255)),
                str(random.randint(1, 254)),
            )
        elif private_class == 3:
            return  "192.168.{}.{}".format(
                str(random.randint(0, 255)),
                str(random.randint(1, 254)),
            )
    elif ip_type == "public":
        random_ip = "{}.{}.{}.{}".format(
                str(random.randint(1, 223)),
                str(random.randint(0, 255)),
                str(random.randint(0, 255)),
                str(random.randint(1, 254)),
            )
        random_ip = ipaddress.ip_address(random_ip)
        while not random_ip.is_global:
            random_ip = "{}.{}.{}.{}".format(
                str(random.randint(1, 223)),
                str(random.randint(0, 255)),
                str(random.randint(0, 255)),
                str(random.randint(1, 254)),
            )
            random_ip = ipaddress.ip_address(random_ip)
        return str(random_ip)

def get_random_domain():
    levels = random.randint(1, 3)
    tlds = ["com", "net", "ph", "bit", "org"]
    with open("words.txt") as f:
        words = f.read().splitlines()
        domain = ''
        for level in range(0, levels):
            index = random.randint(0, len(words)-1)
            domain += words[index].replace("'s", "").lower() + "."
        tld_rand = random.randint(0, len(tlds)-1)
        domain += tlds[tld_rand]
        return domain

def get_random_isp():
    
    no_of_words = random.randint(1, 3)
    endings = ["inc.", "llc.", "co.", "telecom"]
    with open("words.txt") as f:
        words = f.read().splitlines()
        isp = ''
        for word_no in range(0, no_of_words):
            index = random.randint(0, len(words)-1)
            isp += words[index].replace("'s", "").lower() + " "
        end_rand = random.randint(0, len(endings)-1)
        isp += endings[end_rand]
        return isp

def get_random_type_id():
    strings = "abcdefghi-jklm-nopq-rstu-vwxyz123456".split("-")
    type_id = []
    for string in strings:
        new_string = ''
        for letter in string:
            letter_or_number = random.randint(0, 1)
            if letter_or_number == 1:
                new_string += chr(random.randint(48,57))
            else:
                new_string += chr(random.randint(97,122))

        type_id.append(new_string)
    type_id = "-".join(type_id)

    return type_id

def get_random_user():
    with open("users.json") as f:
        users = json.load(f)
        user_rand = random.randint(0, len(users)-1)
        user = users[user_rand]
        return user

def get_random_country():
    with open("countries.txt") as f:
        countries = f.read().splitlines()
        country_rand = random.randint(0, len(countries)-1)
        country = countries[country_rand]
        return country.lower()

def replace_in_dict(dict_object, string_from, string_to):
    object_as_string = json.dumps(dict_object)
    object_as_string = object_as_string.replace(string_from, string_to)
    dict_object = json.loads(object_as_string)
    return dict_object

def randomize_ip(dict_object):
    original_dict = copy.deepcopy(dict_object)
    for ip_position in ip_positions:
        ip_position = ip_position.split(".")
        try:
            for key in ip_position:
                dict_object = dict_object[key]
        except Exception as e:
            dict_object = copy.deepcopy(original_dict)
            break
        ip = dict_object
        extracted_ip_type = ip_type(ip)
        if extracted_ip_type == False:
            raise Exception()
        else:
            randomized_ip = get_random_ip(ip_type=extracted_ip_type)
            dict_object = replace_in_dict(original_dict, ip, randomized_ip)
            original_dict = copy.deepcopy(dict_object)
    return original_dict

def randomize_domain(dict_object):
    original_dict = copy.deepcopy(dict_object)
    for domain_position in domain_positions:
        domain_position = domain_position.split(".")
        try:
            for key in domain_position:
                dict_object = dict_object[key]
        except Exception as e:
            dict_object = copy.deepcopy(original_dict)
            break
        domain = dict_object
        if iptools.ipv4.validate_ip(domain):
            break
        else:
            randomized_domain = get_random_domain()
            dict_object = replace_in_dict(original_dict, domain, randomized_domain)
            original_dict = copy.deepcopy(dict_object)
    return original_dict

def randomize_isp(dict_object):
    original_dict = copy.deepcopy(dict_object)
    for isp_position in isp_positions:
        isp_position = isp_position.split(".")
        try:
            for key in isp_position:
                dict_object = dict_object[key]
        except Exception as e:
            dict_object = copy.deepcopy(original_dict)
            break
        isp = dict_object
        randomized_isp = get_random_isp()
        dict_object = replace_in_dict(original_dict, isp, randomized_isp)
        original_dict = copy.deepcopy(dict_object)
    return original_dict

def randomize_user(dict_object):
    original_dict = copy.deepcopy(dict_object)
    for user_position in user_positions:
        user_position = user_position.split(".")
        try:
            for key in user_position:
                dict_object = dict_object[key]
        except Exception as e:
            dict_object = copy.deepcopy(original_dict)
            break
        user = dict_object
        randomized_user = get_random_user()
        dict_object = replace_in_dict(original_dict, json.dumps(user), json.dumps(randomized_user))
        original_dict = copy.deepcopy(dict_object)

        for key in user:
            dict_object = replace_in_dict(original_dict, user[key], randomized_user[key])
            original_dict = copy.deepcopy(dict_object)
    return original_dict

def randomize_type_id(dict_object):
    original_dict = copy.deepcopy(dict_object)
    for type_id_position in type_id_positions:
        type_id_position = type_id_position.split(".")
        try:
            for key in type_id_position:
                dict_object = dict_object[key]
        except Exception as e:
            dict_object = copy.deepcopy(original_dict)
            break
        type_id = dict_object
        if type_id in type_ids:
            randomized_type_id = type_ids[type_id]

        else:
            randomized_type_id = get_random_type_id()
            type_ids[type_id] = randomized_type_id
        dict_object = replace_in_dict(original_dict, type_id, randomized_type_id)
        original_dict = copy.deepcopy(dict_object)
    return original_dict


def randomize_srcport(dict_object):
    if "srcport" in dict_object["alert_type_details"]["detail"]:
        dict_object["alert_type_details"]["detail"]["srcport"] = random.randint(50001, 65000)
    return dict_object

def randomize_dstport(dict_object):
    if "dstport" in dict_object["alert_type_details"]["detail"]:
        dstports = [80, 443, 22, 21, 53, 873, 25, 465, 587]
        dict_object["alert_type_details"]["detail"]["dstport"] = dstports[random.randint(0, len(dstports)-1)]
    return dict_object

def randomize_primary_id(dict_object):
    dict_object["primary_id"] = random.randint(1, 1000)
    return dict_object

def randomize_country(dict_object):
    if "dstcountry" in dict_object["alert_type_details"]["detail"]:
        dstcountry = get_random_country()
        dict_object["alert_type_details"]["detail"]["dstcountry"] = dstcountry
    return dict_object

def randomize_timestamps(dict_object):
    updated_ms = int(datetime.now().timestamp())
    updated_ms -= 180
    created_ms = updated_ms - random.randint(0, 600)
    dict_object["updated_at"] = datetime.fromtimestamp(updated_ms).strftime('%Y-%m-%d %H:%M:%S')
    dict_object["created_at"] = datetime.fromtimestamp(created_ms).strftime('%Y-%m-%d %H:%M:%S')

    return dict_object
## End of Randomizer Code            
app = Flask(__name__)


# Auth endpoint
@app.route("/auth/api/m0ckhelix",  methods=['POST'])
def authenticate():
    api_key = request.args.get("api_key")
    return "OK"


# Alerts endpoint
@app.route("/get_alerts", methods=['GET'])
def get_alerts():
    with open("alerts.json") as f:
        mock_alerts = json.load(f)
        new_results = []
        for result in mock_alerts["results"]:
            result = randomize_ip(result)
            result = randomize_domain(result)
            result = randomize_isp(result)
            result = randomize_user(result)
            result = randomize_country(result)
            result = randomize_srcport(result)
            result = randomize_dstport(result)
            result = randomize_primary_id(result)
            result = randomize_timestamps(result)
            new_results.append(result)

        mock_alerts["results"] = new_results
    return mock_alerts
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)