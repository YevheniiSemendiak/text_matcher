const express = require("express");
const mongoDB = require("mongodb");

const router = express.Router();

// Commands to fetch data from MongoDB
router.get("/texts", async ( req, res ) => {
    const tc = await getTextsCollection();
    const skip = req.query.skip;
    const nrToReturn = req.query.nrToReturn;
    res.send(await tc.find({}).toArray());
})

router.get("/text/:id", async ( req, res ) => {
    const tc = await getTextsCollection();
    const resp = await tc.findOne({_id: req.params.id});
    if (!resp) res.status(404)
    res.send(resp);
})

router.get("/textSentences/:textID", async ( req, res ) => {
    const sc = await getSentenceCollection();
    const resp = await sc.find(
        {
            $expr: {
                $eq: ["$textUUID", req.params.textID]
            }
        },
        {
            projection: {"embedding": 0}
        }).toArray();
    res.send(resp)
})

router.get("/sentence/:id", async ( req, res ) => {
    const sc = await getSentenceCollection();
    const resp = await sc.findOne({_id: req.params.id}, {
        projection: {"embedding": 0}
    });
    if (!resp) res.status(404)
    res.send(resp);
})

// Mongo DB interaction functions
let client;

async function getMongoClient() {
    if (!client) {
        client = await mongoDB.MongoClient.connect(
            "mongodb://admin:securePasswd!@tm_mongo_db_server/?retryWrites=true&w=majority", {
                useUnifiedTopology: true
            }
        );
        console.log("Client was connected to DB.");
    };
    return client;
};

async function getTextsCollection() {
    const cl = await getMongoClient();
    return cl.db("text_matcher").collection("Text");
}

async function getSentenceCollection() {
    const cl = await getMongoClient();
    return cl.db("text_matcher").collection("Sentence");
}


module.exports = router;
