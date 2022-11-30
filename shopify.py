import requests, json, random, sys, math
def loadConfig():
    with open('config.json', 'r') as configfile:
        return json.loads(configfile.read())
antiblock = {}
if loadConfig()['use-random-ua'] == True:
    antiblock = {
        "User-Agent": random.choice(loadConfig()['user-agents']),
        "Referer":"https://google.com/",
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
    }
else:
    antiblock = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Referer":"https://google.com/",
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
    }
args = sys.argv

if(len(sys.argv) > 3):
    print("Usage:\npy shopify.py [website url] --option\nValid options are listed in the README.")
    exit()
else:
    url = args[1]
    opt = args[2]


if(opt.split("=")[0] == "--coltofile"):
    ofname = opt.split("=")[1]
    col_obj = json.loads(requests.get(url + "collections.json", headers=antiblock, proxies=dict(http=loadConfig()['proxy'], https=loadConfig()['proxy'])).text)["collections"]
    col_array = []
    for i in col_obj:
        col_array.append(i["title"])
    with open(ofname, 'w') as outfile:          
        json.dump((col_array), outfile, indent= 2, sort_keys=True)
    print("Finished scraping.")
elif(opt.split("=")[0] == "--prodtofile"):
    ofname = opt.split("=")[1]
    col_obj = json.loads(requests.get(url + "collections.json", headers=antiblock, proxies=dict(http=loadConfig()['proxy'], https=loadConfig()['proxy'])).text)["collections"]
    product_count = 0
    for i in col_obj:
        product_count += i["products_count"]

    big_object = {}
    pages_count = math.ceil(product_count/30)
    fails = 0
    print("{} pages, {} products".format(pages_count, product_count))
    for i in range(pages_count):
        page_obj = json.loads(requests.get(url+"collections/all/products.json?page={}".format(i), headers=antiblock, proxies=dict(http=loadConfig()['proxy'], https=loadConfig()['proxy'])).text)["products"]
        for product in page_obj:
            updateObj = {product["title"]:{"id":product["id"],"tags":[],"prices":{}}}
            for tag in product["tags"]:
                updateObj[product["title"]]["tags"].append(tag)
            for variant in product["variants"]:
                if(variant['title'] == "Default Title"):
                    updateObj[product["title"]]['prices'].update({"Standard":float(variant['price'])})
                else:
                    updateObj[product["title"]]['prices'].update({variant['title']:float(variant['price'])})


            big_object.update(updateObj)
        if not page_obj == []:
            print("finished page {}/{} | {} on this page".format(i, pages_count, len(page_obj)))
        else:
            print("finished page {}/{} | [Products Empty]".format(i, pages_count))
            fails+= 1
        if(fails == 5):
            print("Finished scraping.")
            break
    with open(ofname, 'w') as outfile:          
        json.dump((big_object), outfile, indent= 2, sort_keys=True)

elif (opt == "--printcol"):
    col_obj = json.loads(requests.get(url + "collections.json", headers=antiblock, proxies=dict(http=loadConfig()['proxy'], https=loadConfig()['proxy'])).text)["collections"]
    col_array = []
    for i in col_obj:
        col_array.append(i["title"])
    print(json.dumps(col_array, indent=2, sort_keys=True))

