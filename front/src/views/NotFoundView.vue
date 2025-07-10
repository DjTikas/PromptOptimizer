<template>
  <div class="not-found-view">
    <div class="container">
      <h1>404</h1>
      <p>抱歉，您访问的页面不存在</p>
      <router-link to="/" class="home-link">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
</script>


<style scoped>
.not-found-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  text-align: center;
  background-color: #f9fafb;
}

.container {
  max-width: 400px;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 3rem;
  margin: 0 0 1rem;
  color: #ef4444;
}

p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  color: #6b7280;
}

.home-link {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #4f46e5;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.2s;
}

.home-link:hover {
  background-color: #4338ca;
}
</style>

