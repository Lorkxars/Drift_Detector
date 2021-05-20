<template>
  <footer>
    <div class="container-fluid">
      <div class="col-md-12">
        <p>
            Drift Detector |  David de la Fuente &copy; 2021 
        </p>
      </div>
    </div>
  </footer>
</template>

<script>
  export default {
    name: 'foot',
  }
</script>

<style scoped>
    a {
      color:#000;
  }
  footer {
  width:100%;
  height: 80px;
  background-color: #313131;
  bottom:0;
  left:0;
  display: block;
}
footer p {
  text-align: center;
  color: #fff;
  font-weight: 200;
  text-transform: uppercase;
  padding-top: 33px;
  letter-spacing: 0.5px;
}
</style>