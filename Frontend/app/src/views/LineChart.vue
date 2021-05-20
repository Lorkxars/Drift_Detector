<script>
import { Line, mixins } from "vue-chartjs";

const { reactiveProp } = mixins;
export default {
  extends: Line,
  mixins: [reactiveProp],
  props: ["options"],
  data() {
    return {
      polling: null,
    };
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },

  methods: {
    pollData() {
      this.polling = setInterval(() => {
        this.$data._chart.update();
      }, 3000);
    },
  },

  created() {
    this.pollData();
  },

  beforeDestroy() {
    clearInterval(this.polling);
  },
};
</script>

<style scoped>
</style>
