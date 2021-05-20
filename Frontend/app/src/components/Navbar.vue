<template>
  <div class="nav-bar">
    <nav class="navbar navbar-expand-lg navbar-light bg-white nav-1">
      <div class="container mw-0 px-3">

        <a class="navbar-brand" href="/">
        <img src="../assets/logo.png" width="" height="27" class="d-inline-block align-top" alt="" loading="lazy">
        </a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <a v-bind:href="'/'"> HOME </a>
            </li>
          </ul>
        </div>

      </div>
    </nav>
  </div>
</template>

<script>
  export default {
    name: 'Navbar',
  }
</script>

<style scoped>
    a {
      color:rgb(226, 226, 226);
  }
.bg-white {
    background-color: #313131 !important;
}
</style>