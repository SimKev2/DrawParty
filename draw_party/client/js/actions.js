import store from './store'

export function changePassword(userID, password, callback){
    let credentials = {
        'userID': userID,
        'password': password
    };

    // request({method:'POST', url:'/api/user/profile?userID=' + userID, body:credentials, json: true}, function(err, response){
    //     callback(response.statusCode === 200);
    // });
}
