<template>
  <div class="album py-5 bg-light">
    <navbar></navbar>
    <div class="container" id="main_container">
      
      <div class="album py-5 bg-light">
        <div class="container">
          <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">
            <div v-for="datSer in APIData" :key="datSer.id" class="col">
              <div class="card mb-4 shadow-sm" v-bind:style=" datSer.driftDetected ? 'box-shadow: 0 0 30px #911414 !important;' : 'box-shadow: none;' ">
                <div class="card-header">
                  <h4 class="my-0 fw-normal">{{ datSer.name }}</h4>
                </div>
                <div class="card-body">
                  <img v-if="datSer.thumbnail !== null" v-bind:src="datSer.thumbnail" width="200">
                  <div class="btn-group">
                    <a
                      v-bind:href="'/' + datSer.id"
                      class="btn btn-sm btn-outline-primary"
                      role="button"
                      aria-pressed="true"
                      >View
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <foot></foot>
  </div>
</template>

<script>
import { getAPI } from "../axios-api";
import Navbar from "../components/Navbar.vue";
import foot from "../components/Footer.vue";
export default {
  name: "DataSeries",
  data() {
    return {
      APIData: [],
    };
  },
  components: {
    Navbar,
    foot,
  },
  created() {
    getAPI
      .get("")
      .then((response) => {
        console.log("Data Series API has recieved data");
        this.APIData = response.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.my-0{
  text-align: center;
} 
.py-5{
  padding: 0 !important;
}
#main_container{
  padding: 2em;
}
.btn-group{
  padding-top: 2%;
  width: 100%;
  align-items: center;
  min-height: 60px;
}
.container{
  max-width: 100% !important;
}
.bg-light{
  background-color :darkgrey!important;
}
</style>
