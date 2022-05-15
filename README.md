<strong><center>NFT-Uploading-Bot</center></strong>

* This program created for uploading and listing NFTs on OpenSea.

* Before using this program you need to change following variables:
```py
self.image_folder_name = "Your image folder name"
self.metadata_folder_name = "Your meta data folder name"
self.collection_url = "Your collection url"
self.secret_phrase = "Your metamask secret phrase"
self.metamask_password = "Your metamask password"
self.price = "Price"
# Starts from this number to upload
self.start_number = 0
# This is your folder number, Your project folder should contain a folder named this number
self.dictionary_number = 1
```

* You should also change loop in add_properties function according to your metadata file.
````py
# Define character and prob_name for every single property
        ###
        for i in self.data[n]:
            if i != "tokenId":
                character = i
                prop_name = self.data[n][i]
            else:
                break
            ###
````

* After these you can run this program.