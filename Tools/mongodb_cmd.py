
## Update all documents to set a new value for the "status" key
# MongoDB Compass (Desktop Version)
# Need to call using which Database
Use Night_Database   
db.Night_Database.updateMany({}, { $set: { "status": "new_value" } })


## Update all documents to set a new value for the "status" key
# Pymongo (Python Version)
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Night_Database"]
collection = db["Night_Database"]

update_result = collection.update_many({"name": "John"}, {"$set": {"status": "new_value"}})
update_result.modified_count

######################################################################################################

# Pymongo (Python Version)
# Search
# Findone and update
db.Night_Database.findOne(
   { "Ven_Machine": { "$regex": /ven29/i } })


# Delete one 
db.Night_Database.deleteOne({Ven_Machine: {"$regex": /ven239/i}})

#Find and Modify
db.Night_Database.findAndModify({
query: {"Ven_Machine": { "$regex": /ven290/i}},
update: {"$set": {"Credit": "940102"}},
new: true  
});


# findOne
db.Night_Database.findOne({Ven_Machine: {"$regex": /ven239/i}})

# updateOne
db.Night_Database.updateOne({"Ven_Machine":{"$regex": /ven356/i}}, { $set: { "Credit": "28174.92" } })