/**
 * Configuration object to be passed to MSAL instance on creation. 
 * For a full list of MSAL.js configuration parameters, visit:
 * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/configuration.md 
 */
 const msalConfig = {
    auth: {
        clientId: "2d696b14-a0e6-49fa-83d2-5e474b5eb1e7",       // apply your changes here
//        authority: "https://login.microsoftonline.com/60409c15-dd37-4640-975b-9eaa707437b7",
        authority: "https://login.microsoftonline.com/common",

        redirectUri: "https://uberg.ca/plantID/",       // apply your changes here
        //GET https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=2d696b14-a0e6-49fa-83d2-5e474b5eb1e7&scope=Files.ReadWrite.All
    //&response_type=token&redirect_uri=http://localhost:3000/
        //85167297639a01ac (driveID Ubergaiter Data)
        //e7ed823328da1811  (driveID)
        // Ubergaiter Folder ID 85167297639A01AC!108      E7ED823328DA1811!120822
        // aHR0cHM6Ly8xZHJ2Lm1zL3UvcyFBaEVZMmlnemd1M25oNjkyWU1IU3BDTUZZb3ZXYmc_ZT05eVk3a1Y url encoded

    },
    cache: {
        cacheLocation: "sessionStorage", // This configures where your cache will be stored
        storeAuthStateInCookie: true, // Set this to "true" if you are having issues on IE11 or Edge
    },
    system: {	
        loggerOptions: {	
            loggerCallback: (level, message, containsPii) => {	
                if (containsPii) {		
                    return;		
                }		
                switch (level) {		
                    case msal.LogLevel.Error:		
                        console.error(message);		
                        return;		
                    case msal.LogLevel.Info:		
                        console.info(message);		
                        return;		
                    case msal.LogLevel.Verbose:		
                        console.debug(message);		
                        return;		
                    case msal.LogLevel.Warning:		
                        console.warn(message);		
                        return;		
                }	
            }	
        }	
    }
};

/**
 * Scopes you add here will be prompted for user consent during sign-in.
 * By default, MSAL.js will add OIDC scopes (openid, profile, email) to any login request.
 * For more information about OIDC scopes, visit: 
 * https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-permissions-and-consent#openid-connect-scopes
 */
const loginRequest = {
    scopes: ["User.Read",  "Files.ReadWrite.All"],
    forceRefresh: true
};

/**
 * Add here the scopes to request when obtaining an access token for MS Graph API. For more information, see:
 * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/resources-and-scopes.md
 */
const tokenRequest = {
    scopes: ["User.Read", "Mail.Read", "Files.ReadWrite.All"],
    forceRefresh: true // Set this to "true" to skip a cached token and go to the server to get a new token
};
