<script setup>
// TODO can be usable inside hist list
import { toRefs } from 'vue';
import axios from "axios";
import { useRootHistogramStore } from '../stores/RootHistogramStore';
import { httpRequest, draw,  } from 'jsroot';

const store = useRootHistogramStore()

const { details } = toRefs(props);
console.log("------");
console.log("${histImg}");
console.log("$histImg");
console.log("histImg");
console.log("`${histImg}`");
console.log("------");

// let obj = await httpRequest("histImg", 'object');
let obj = axios.get("${histImg}");

console.log('Read object of type', obj._typename);
draw("rootJsonDrawing", details.histImg, "hist");

</script>
<template>
    <div>
        <div id="rootJsonDrawing"></div>
        
    </div>
</template>
<style>
.disabled-link {pointer-events: none; text-decoration: none; cursor: not-allowed;}
</style>