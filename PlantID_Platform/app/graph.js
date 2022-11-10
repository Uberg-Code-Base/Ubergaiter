// /** 
//  * Helper function to call MS Graph API endpoint
//  * using the authorization bearer token scheme
// */
// function callMSGraph(endpoint, token, callback) {
//     const headers = new Headers();
//     const bearer = `Bearer ${token}`;

//     headers.append("Authorization", bearer);

//     const options = {
//         method: "GET",
//         headers: headers
//     };

//     console.log('request made to Graph API at: ' + new Date().toString());


//     if( endpoint.includes('items')) {
//         let data;
//         let objectURL
//         fetch(endpoint, options)
//         .then(response => {
//             response.blob()
//             .then((blobresponse) => {
//                 data = blobresponse
//                 console.log(blobresponse)
//                 objectURL = URL.createObjectURL(data);
//                 console.log(objectURL)
//                 const image = document.getElementById('image')
//                 image.src = objectURL
//             })}
            
//         )
//         .catch(error => {
//             console.log('this is the error')
//             console.log(error)
//         });
//     }
//     // else if( endpoint.includes('root:')) {
//     //     let data;
//     //     let objectURL = []
//     //     fetch(endpoint, options)
//     //     .then(response => //{
//     //         {response.json()
//     //         console.log(response)})
//     //     .then(response => callback(response, endpoint))
//     //         // .then((blobresponse) => {
//     //         //     data = blobresponse
//     //         //     console.log(blobresponse)
//     //         //     objectURL = URL.createObjectURL(data);
//     //         //     console.log(objectURL)
//     //         //     const image = document.getElementById('image')
//     //         //     image.src = objectURL
//     //        // })}
            
        
//     //     .catch(error => {
//     //         console.log('this is the error')
//     //         console.log(error)
//     //     });
//     // }
//     else {
//         fetch(endpoint, options)
//             .then(response => {
//                 response.json()
//                 .then(jsonData => callback(jsonData,endpoint))
//             })
//             .then(response => callback(response, endpoint))
//             .catch(error => {
//                 console.log('this is the error')
//                 console.log(error)
//             });
//         }
// }
