<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { containerMaxW } from "@/config.js";
import RootHistogramGroupRow from "@/components/RootHistogramGroupRow.vue";
import { useMainRunStore } from "@/stores/mainRun.js";

const router = useRouter();
const isAsideMobileExpanded = ref(false);
const isAsideLgActive = ref(false);

router.beforeEach(() => {
  isAsideMobileExpanded.value = false;
  isAsideLgActive.value = false;
});

const mainRunStore = useMainRunStore();

</script>

<template>
  <!-- <span>{{ mainRunStore.runYear }} - {{ mainRunStore.runNumber }}</span> -->
  <section class="p-0 px-0" :class="containerMaxW">

    <RootHistogramGroupRow
      v-for="(detectorGroup, index) in mainRunStore.detectorHistograms"
      :key="index"
      :histograms="detectorGroup.histograms"
      :group-name="detectorGroup.gname"
      :dataset="detectorGroup.dataset"
      :root-file="detectorGroup.root_file"
      :run-year="mainRunStore.runYear"
      :run-number="mainRunStore.runNumber" />

  </section>
</template>
