// Add here the endpoints for MS Graph API services you would like to use.
const graphConfig = {
    //getBatchEndpoint: "https://graph.microsoft.com/v1.0/me/drive/root:/UbergaiterAcquisitions:/children",
    //getBatchEndpoint: "https://graph.microsoft.com/v1.0/me/drive/root:/AquisitionFolder:/children",
    getBatchEndpoint: "https://graph.microsoft.com/v1.0/drives/E7ED823328DA1811/items/E7ED823328DA1811!120822/children",       // apply your changes here
    
    //graphSharedEndpoint: "https://graph.microsoft.com/v1.0/me/drive/sharedwithme?allowexternal=true",
    
    //getPicdEndpoint: "https://graph.microsoft.com/v1.0/me/drive/items/",//015ZCCUZFAB2GX5E5E7BAKKFBDFINHCE4E/content",
    getPicdEndpoint: "https://graph.microsoft.com/v1.0/drives/E7ED823328DA1811/items/",//015ZCCUZFAB2GX5E5E7BAKKFBDFINHCE4E/content",       // apply your changes here
    
    //GOOD ONE!!!!!graphSharedEndpoint: "https://graph.microsoft.com/v1.0/me/drive/root:/UbergaiterAcquisitions:/children",
    
    
    //graphSharedEndpoint: "https://graph.microsoft.com/v1.0/shares/u!aHR0cHM6Ly8xZHJ2Lm1zL2YvcyFBaEVZMmlnemd1M25oNjkyWU1IU3BDTUZZb3ZXYmc",
    //graphSharedEndpoint: "https://graph.microsoft.com/v1.0/shares/u!aHR0cHM6Ly9vbmVkcml2ZS5saXZlLmNvbS9lbWJlZD9jaWQ9RTdFRDgyMzMyOERBMTgxMSZyZXNpZD1FN0VEODIzMzI4REExODExJTIxMTIwODIyJmF1dGhrZXk9QUM1NV9XQVB2cm5yNEtz",

    assignPlantEndpoint: "https://graph.microsoft.com/v1.0/me/messages"
};
//E7ED823328DA1811%21120822&cid=E7ED823328DA1811
//E7ED823328DA1811 (CID)

// string sharingUrl = "https://onedrive.live.com/redir?resid=1231244193912!12&authKey=1201919!12921!1";
// string base64Value = System.Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(sharingUrl));
// string encodedUrl = "u!" + base64Value.TrimEnd('=').Replace('/','_').Replace('+','-');

// https://1drv.ms/f/s!AhEY2igzgu3nh5EGnAWtBtZkglkFKw
//aHR0cHM6Ly8xZHJ2Lm1zL2YvcyFBaEVZMmlnemd1M25oNjkyRXpGVWsyQkNEUFhFRVE=
//u!aHR0cHMmIzU4Oy8vb25lZHJpdmUubGl2ZS5jb20vcmVkaXImIzYzO3Jlc2lkJiM2MTtFN0VEODIzMzI4REExODExJiMzMzsxMjA4MjImIzM4O2F1dGhrZXkmIzYxOyYjMzM7QUdEQjBxUWpCV0tMMW00JiMzODtpdGhpbnQmIzYxO2ZvbGRlcg


//015ZCCUZFAB2GX5E5E7BAKKFBDFINHCE4E