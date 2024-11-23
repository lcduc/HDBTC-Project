<script>
</script>

<template>
  <div id="app container-fluid">
    <router-view />
  </div>
</template>

<style>
.pagination {
  display: flex;
  justify-content: center;
  text-align: center;
}

.pagination a {
  color: black;
  border: 1px solid #ddd;
  float: left;
  padding: 8px 16px;
  text-decoration: none;
  cursor: pointer;
}

.currentPage a {
  background-color: lightblue;
}

h1 {
  font-weight: bold;
}
</style>
