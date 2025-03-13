import axios from '../utils/axios'

export function getAdminInfo() {
    return axios.get('/admin/profile',
        {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
          }
    );
}

export function adminLogout() {  
    return axios.post('/admin/logout',{},
        {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }
    );
}

// userAcount
export function getUser() {
    return axios.get('/admin/users',
        {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
    );
}

// export function addUser(params) {
//     return axios.put('/admin/addUser', params);
// }

export function updateUser(params) {
    return axios.put('/admin/updateUser', params,
        {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
    );
}

export function banUser(userId) {
    return axios.patch(
        `/admin/users/${userId}/forbid`,
        {}, // No body, so an empty object
        {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }
    );
}

export function unbanUser(userId) {
    return axios.patch(
        `/admin/users/${userId}/unforbid`,
        {}, // No body, so an empty object
        {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }
    );
}


export function deleteUser(userId) {
    return axios.delete(`/admin/users/${userId}/delete`,
        {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
    );
}

// restaurantAcount
export function getRestaurant() {
    return axios.get('/admin/getRestaurant');
}

export function addRestaurant(params) {
    return axios.post('/admin/addRestaurant', params,);
}

export function updateRestaurant(params) {
    return axios.put('/admin/updateRestaurant', params);
}

export function banRestaurant(params) {
    return axios.put('/admin/banRestaurant', params);
}

export function deleteRestaurant(params) {
    return axios.delete('/admin/deleteRestaurant', params);
}

// reportHandling
export function getReport() {
    return axios.get('/admin/getReport');
}

export function commitReply(params) {
    return axios.put('/admin/commitReply', params);
}

export function deleteReport(params) {
    return axios.delete('/admin/deleteReport', params);
}

// realNameAuthentication
export function getRealNameAuthentication() {
    return axios.get('/admin/getRealNameAuthentication');
}

export function updateAuthentication(params) {
    return axios.put('/admin/updateAuthentication', params);
}

export function deleteAuthentication(params) {
    return axios.delete('/admin/deleteAuthentication', params);
}




