<script setup>
import HelloWorld from './components/LogIn.vue'
</script>

<template>
  <!-- <div>
    <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div> -->
  <HelloWorld msg="Vite + Vue" />
</template>

<style>
.pagination {
  /* style for the whole pagination  */
  display: flex;
  justify-content: center;
  text-align: center;
}

.pagination a {
  /* style for the anchor */
  color: black;
  border: 1px solid #ddd;
  float: left;
  padding: 8px 16px;
  text-decoration: none;
  cursor: pointer;
}

.currentPage a {
  /* style to indicate the current page  */
  background-color: lightblue;
}

h1 {
  font-weight: bold;
}
</style>
