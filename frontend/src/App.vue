<script setup>
import { RouterView } from 'vue-router';
import { useRootHistogramStore } from './stores/RootHistogramStore';

const store = useRootHistogramStore();
store.getHistograms();


</script>
<template>
  <h1 v-if="store.loading">Please Wait</h1>
  <RouterView v-else></RouterView>
 
</template>
