const express = require('express');
const morgan = require('morgan');
const path = require('path');
const Filesaver = require('file-saver');
const fetch = require('node-fetch');
const bodyParser = require('body-parser');
const { response } = require('express');
// var fs = require('fs');
// var stream = fs.createWriteStream("my_file.txt");

const DEFAULT_PORT = process.env.PORT || 3144;

// initialize express.
const app = express();

// Initialize variables.
let port = DEFAULT_PORT;
app.use(bodyParser.json())
// Configure morgan module to log all requests.
app.use(morgan('dev'));

// Setup app folders.
app.use(express.static('app'));
app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT,DELETE");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");
    next();
});
// Set up a route for index.html
app.get('/plantID/', (req, res) => {
    // console.log('hey')
    // let url1 = "https://data.mongodb-api.com/app/data-vzfvl/endpoint/data/v1/action/find"
    
    // console.log("hey")
    // let sendBody1 ={
    //         dataSource:"Cluster0",
    //         database:"test",
    //         collection:"picins",
    //         filter: { "finder": { "$lt" : 2} },
    //         sort: { "finder": 1 } }
    
    // //console.log(sendBody)
    // fetch(url1, {
    //     method: "POST",
    //     headers:{
    //         "Content-Type": "application/json",
    //         "api-key": "___",
    //         "Access-Control-Allow-Origin": "*",
    //         'Access-Control-Request-Headers': '*'
    //     }, body: JSON.stringify(sendBody1)
    // }).then(response =>
    //         response.json()
    // )
    // .then((data) => {
    //     console.log(data.documents)
    //     dbSize = Object.keys(data.documents).length
    //     console.log(dbSize + 77)
    // })
    // .then(()=>{
        res.sendFile(path.join(__dirname + '/app/index.html'))
 
    // })
    // .catch(()=>{
    //     console.log("error")
    // })
    


    
    
   
});

app.get('/plantID/sizeDB', (req, res) => {
    let url1 = "https://data.mongodb-api.com/app/data-vzfvl/endpoint/data/v1/action/find"
    
    console.log("hey")
    let sendBody1 ={
            dataSource:"Cluster0",
            database:"test",
            collection:"picins",
            filter: { "finder": { "$lt" : 2} },
            sort: { "finder": 1 } 
    }
    
    //console.log(sendBody1)
    fetch(url1, {
        method: "POST",
        headers:{
            "Content-Type": "application/json",
            "api-key": "____",
            "Access-Control-Allow-Origin": "*",
            'Access-Control-Request-Headers': '*'
        }, body: JSON.stringify(sendBody1)
    }).then(response => 
        response.json()
    )
    .then((data) => {
        //console.log(data)
        dbSize = Object.keys(data.documents).length + 77
        //console.log(dbSize + 77)
        return dbSize
    })    
    .then((dbSize)=>{
        res.json({"dbCount" :dbSize})
    })
    .catch((error)=>{
        console.log(error)
    })

    
    
   
});

app.post('/plantID/sizeUserDB', (req, res) => {
    let url2 = "https://data.mongodb-api.com/app/data-vzfvl/endpoint/data/v1/action/find"
    console.log(req.body.user)
    console.log("hey")
    let sendBody2 ={
            dataSource:"Cluster0",
            database:"test",
            collection:"picins",
            filter: { "user": req.body.user },
            sort: { "user": 1 } 
    }
    
    console.log(sendBody2)
    fetch(url2, {
        method: "POST",
        headers:{
            "Content-Type": "application/json",
            "api-key": "____",
            "Access-Control-Allow-Origin": "*",
            'Access-Control-Request-Headers': '*'
        }, body: JSON.stringify(sendBody2)
    }).then(response => 
        response.json()
    )
    .then((data) => {
        console.log(data)
        userDbSize = Object.keys(data.documents).length
        //console.log(dbSize + 77)
        return userDbSize
    })    
    .then((userDbSize)=>{
        res.json({"userDbCount" : userDbSize})
    })
    .catch((error)=>{
        console.log(error)
    })

    
    
   
});

app.post('/plantID/picPost', (req, res) => {
    let url = "https://data.mongodb-api.com/app/data-vzfvl/endpoint/data/v1/action/insertOne"
    
    reqBody= req.body
    let picIDStr = reqBody.document.picID
    let picFileNameStr = reqBody.document.picFileName
    let timeNowStr = reqBody.document.timeNow

    let sendBody ={
        picID: picIDStr,
        picFileName: picFileNameStr,
        timeNow: timeNowStr 
    }
    console.log(req.body)
    //console.log(sendBody)
    fetch(url, {
        method: "POST",
        headers:{
            "Content-Type": "application/json",
            "api-key": "____",
            "Access-Control-Allow-Origin": "*",
            'Access-Control-Request-Headers': '*'
        }, body: JSON.stringify(reqBody)
        }).then(response =>{
        console.log(response)
    })

    
    res.json({
        reqBody
    })
    
    
    //res.sendFile(path.join(__dirname + '/app/index.html'));
});
// Start the server.
app.listen(port);
console.log(`Listening on port ${port}...`);

// stream.once('open', function(fd) {
//     stream.write("My first row\n");
//     stream.write("My second row\n");
//     stream.end();
//   });