import axios from 'axios'

const getAPI = axios.create({
    baseURL: 'http://192.168.1.70:8000/api',
    timeout: 1000,
})

export {getAPI}