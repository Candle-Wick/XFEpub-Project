<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import mainBody from './components/main.vue'


</script>

<template>
  <div>
    <div class="container-xxl-fluid rounded" style="background: rgba(150,100,0,0.2); max-width: 90%; margin: auto;">
    <mainBody class=""/>
    </div>
  </div>


  <!-- <header>

    

  
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div> 
  </header>

  <RouterView /> -->
</template>
