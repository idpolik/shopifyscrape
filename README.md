# shopifyscrape
config.json:

"proxy" : This should be some form of webproxy you intend to use to bypass bot-blocking. I recommend a rotating proxy network, such as ones provided by https://brightdata.com/

"use-random-ua" : This option toggles whether to use a single, default user agent, or to choose a random one from "user-agents".

"user-agents" : This should contain multiple valid User-Agents. If "use-random-ua" is enabled, a random one will be selected from this list.

# Options
--coltofile=file.json (outputs collections to file.json)

--prodtofile=file.json (outputs products and their important data to file.json)

--printcol (prints collections)

--printtags (prints all product tags)

--tagstofile=file.json (outputs all product tags to file.json)

More will be added.
# Usage
py shopify.py [website url] --option

for example:
```
py shopify.py https://shop.glassaqua.com/ --printcol
```
```
py shopify.py https://aqualabaquaria.com/ --coltofile=collections.json
```
```
py shopify.py https://buceplant.com/ --prodtofile=products.json
```
```
py shopify.py https://aquaforestaquarium.com/ --printtags
```
```
py shopify.py https://aquascapesupply.co/ --tagstofile=tags.json
```
