<script setup>
import BaseDivider from "@/components/BaseDivider.vue";
import RootHistogramWidget from "@/components/RootHistogramWidget.vue";
import { ref } from "vue";
import { useRouter } from "vue-router";

defineProps({
  plots: {
    type: Array, required: true
  },
  groupName: {
    type: String
  },
  dataset: {
    type: String
  },
  rootFile: {
    type: String
  },
});

const router = useRouter();
const isAsideMobileExpanded = ref(false);
const isAsideLgActive = ref(false);

router.beforeEach(() => {
  isAsideMobileExpanded.value = false;
  isAsideLgActive.value = false;
});
</script>

<template>
  <BaseDivider nav-bar></BaseDivider>
  <div class="group w-full block h-6">
    <span class="dark:dark:border-slate-700 text-xs lg:text-sm">
      <span
        class="border border-solid text-xs lg:text-sm bg-pink-300 dark:bg-pink-500 via-pink-900 font-bold leading-none tracking-tight px-2 py-1">
        {{ groupName }}
      </span>
      : {{ dataset }}
    </span>
    <span class="opacity-0 group-hover:opacity-100 text-sky-500 w-1/3 text-xs break-all">
      {{ rootFile }}
    </span>
  </div>
  <div class="grid lg:grid-cols-5 grid-cols-1 border-solid border-2 gap-1">
    <RootHistogramWidget
      v-for="(plot, index) in plots"
      :key="plot.id"
      :id="plot.id"
      :name="plot.conf_name"
      :type="plot.type"
      :data="plot.data" />
  </div>
</template>
