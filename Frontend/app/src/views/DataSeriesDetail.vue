<template>
  <div class="album py-5 bg-light">
    <navbar></navbar>
    <div class="container">
      
      <h1 id="Title">{{ APIData.name }}</h1>
      
      <div id="filters" class="row">
        <div class="col-9">
          <div class="row">
            <div class="col-2">
            <label> Algoritmos:</label><br>
            </div>
            <div class="col-2">
              <input type="checkbox" id="CUSUM" v-model="CUSUM">
              <label for="CUSUM"> CUSUM</label><br>
            </div>
            <div class="col-3">
              <input type="checkbox" id="PH" v-model="PH">
              <label for="PH"> Page-Hinkley</label><br>
            </div>
            <div class="col-2">
              <input type="checkbox" id="SPC" v-model="SPC">
              <label for="SPC"> SPC</label><br>
            </div>
            <div class="col-2">
              <input type="checkbox" id="SPRT" v-model="SPRT">
              <label for="SPRT"> SPRT</label><br>
            </div>
          </div>
        </div>
        <div class="col-3">
          <div class="row">
            <div class="col-3">
              <label> Values: </label><br>
            </div>
            <div class="col-9">
              <select v-model="numberOfPoints">
                <option value= 25>25</option>
                <option value= 50>50</option>
                <option value= 100>100</option>
                <option value= 250>250</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div>
            <line-chart :chart-data="datacollection" :options="options" />
          </div>
        </div>
      </div>
    </div>
    <foot></foot>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { getAPI } from "../axios-api";
import VueRouter from "../routes";
import LineChart from "./LineChart";
import foot from "../components/Footer.vue";

export default {
  name: "DataSeriesDetail",
  data() {
    return {
      APIData: [],
      CUSUM: true,
      PH: true,
      SPC: true,
      SPRT: true,
      numberOfPoints: 50,
      Points: [],
      datacollection: {
        labels: [],
        datasets: [
          {
            label: "Error",
            data: [],
            pointBackgroundColor: [],
            fill: false,
            borderColor: "#2554FF",
            backgroundColor: "#2554FF",
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: false,
              },
              gridLines: {
                display: true,
              },
            },
          ],
          xAxes: [
            {
              gridLines: {
                display: false,
              },
            },
          ],
        },
        legend: {
          display: false,
        },
        responsive: true,
        maintainAspectRatio: false,
      },
    };
  },
  components: {
    Navbar,
    LineChart,
    foot,
  },
  async created() {
    getAPI
      .get("/" + VueRouter.history.current.params.id)
      .then((response) => {
        console.log("Data Series API has recieved data");
        this.APIData = response.data;
        var point;
        for (point in response.data.data_points) {
          getAPI
            .get("/datapoints/" + response.data.data_points[point])
            .then((response) => {
              if (response.data.timestampUpdated != null) {
                this.Points.push(response.data);
                this.datacollection.labels.push(
                  response.data.timestampUpdated.toString()
                );
                this.datacollection.datasets[0].data.push(
                  response.data.absError
                );
                if (
                  (response.data.cusum && this.CUSUM) ||
                  (response.data.ph && this.PH)||
                  (response.data.spc && this.SPC) ||
                  (response.data.sprt && this.SPRT)
                ) {
                  this.datacollection.datasets[0].pointBackgroundColor.push(
                    "red"
                  );
                } else {
                  this.datacollection.datasets[0].pointBackgroundColor.push(
                    "green"
                  );
                }
              }
            })
            .catch((err) => {
              console.log(err);
            });
        }
      })
      .catch((err) => {
        console.log(err);
      });
  },
  mounted() {
    this.pollData();
  },
  methods: {
    reArrange() {
      this.Points.sort(function (a, b) {
        if (a.timestampUpdated > b.timestampUpdated) {
          return 1;
        } else if (a.timestampUpdated < b.timestampUpdated) {
          return -1;
        } else {
          return 0;
        }
      });
      var i;
      this.datacollection.labels = [];
      this.datacollection.datasets[0].data = [];
      this.datacollection.datasets[0].pointBackgroundColor = [];
      var start = 0;
      if(this.Points.length>this.numberOfPoints){
        start = (this.Points.length - this.numberOfPoints)-1;
      }
      for (i = start; i < this.Points.length; i++) {
        this.datacollection.labels.push(
          this.Points[i].timestampUpdated.toString()
        );
        this.datacollection.datasets[0].data.push(this.Points[i].absError);
        if (
          (this.Points[i].cusum && this.CUSUM) ||
          (this.Points[i].ph && this.PH)||
          (this.Points[i].spc && this.SPC) ||
          (this.Points[i].sprt && this.SPRT)
        ) {
          this.datacollection.datasets[0].pointBackgroundColor.push("red");
        } else {
          this.datacollection.datasets[0].pointBackgroundColor.push("green");
        }
      }
      this.getUpdatedData();
    },
    getUpdatedData() {
      var time;
      var parts = this.Points[this.Points.length - 1].timestampUpdated.match(
        /(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})/
      );
      time =
        Date.UTC(
          +parts[1],
          parts[2] - 1,
          +parts[3],
          +parts[4],
          +parts[5],
          +parts[6]
        ) / 1000;
      getAPI
        .get("/" + VueRouter.history.current.params.id + "/" + time)
        .then((response) => {
          if (response.data.length == 0) {
            console.log("No new data");
          } else {
            var i;
            for (i = 0; i < response.data.length; i++) {
              this.Points.push(response.data[i]);
            }
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    pollData() {
      this.polling = setInterval(() => {
        this.reArrange();
      }, 500);
    },
  },

  beforeDestroy() {
    clearInterval(this.polling);
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped >
.container >>> #Title {
  text-align: center;
}
.container >>> .col-12{
  padding-right: 15px; 
    padding-left: 15px;
}

.container >>> .bg-light{
  background-color: #8e8d89!important;
}
.container >>> body{
  background-color: #8e8d89!important;
}
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
