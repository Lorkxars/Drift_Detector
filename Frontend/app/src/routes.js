import Vue from 'vue'
import VueRouter from 'vue-router'
import DataSeries from './views/DataSeries'
import DataSeriesDetail from './views/DataSeriesDetail'

//Add to middleware
Vue.use(VueRouter)

export default new VueRouter({
    //The default mode for Vue Router is hash mode. 
    //It uses a URL hash to simulate a full URL so that the page won’t be reloaded when the URL changes.  
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
        path: '/',
        name: 'DataSeries',
        component: DataSeries,
        },
        {
        path: '/:id',
        name: 'DataSeriesDetail',
        component: DataSeriesDetail,
        },
    ]
})