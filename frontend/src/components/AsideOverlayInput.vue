<script setup>
import { computed, ref } from "vue";
import { useOverlayRunsStore } from "@/stores/overlayRuns.js";
import { useStyleStore } from "@/stores/style.js";
import { getButtonColor } from "@/colors.js";
import BaseIcon from "@/components/BaseIcon.vue";
import { mdiPlusThick, mdiMinus } from '@mdi/js';


/* TODO: validation https://vuejs.org/guide/components/props.html#prop-validation*/
const props = defineProps({
  icon: {
    type: String,
    required: true,
  },
  item: {
    type: Object,
    required: true,
  },
});

const overlayRunsStore = useOverlayRunsStore();
const styleStore = useStyleStore();

const emit = defineEmits(["menu-click"]);
const hasColor = computed(() => props.item && props.item.color);
const componentClass = computed(() => [
  props.isDropdownList ? "py-3 px-0 text-sm" : "py-3",
  hasColor.value
    ? getButtonColor(props.item.color, false, true)
    : `${styleStore.asideMenuItemStyle} dark:text-slate-300 dark:hover:text-white`,
]);
const menuClick = (event) => {
  emit("menu-click", event, props.item);
};

/* Input values with default mainRun store input run number */
const inputRuns = ref(overlayRunsStore.inputRunNumbers)

/* Initial get of histograms */
// mainRunStore.updateRunNumber(parseInt(inputRun.value));

/* On input hit enter */
function submit() {
  mainRunStore.updateRunNumber(parseInt(inputRun.value));
}

const newRunNumber = ref()

function addRun() {
  if (!inputRuns.value.includes(parseInt(newRunNumber.value))) {
    inputRuns.value.push(parseInt(newRunNumber.value))
  }
  overlayRunsStore.updateOverlayRunNumbers(inputRuns.value)
  newRunNumber.value = ''
}

function removeRun(run) {
  inputRuns.value = inputRuns.value.filter((num) => num !== run)
  overlayRunsStore.updateOverlayRunNumbers(inputRuns.value)
}



</script>

<style>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}
</style>
<template>
  <li>
    <component
      :is="item.to ? RouterLink : 'a'"
      v-slot="vSlot"
      :to="item.to ?? null"
      :href="item.href ?? null"
      :target="item.target ?? null"
      class="flex cursor-pointer h-60 px-8"
      :class="componentClass"
      @click="menuClick">


      <div class="grow text-ellipsis"
        :class="[vSlot && vSlot.isExactActive ? asideMenuItemActiveStyle : '',]">

        <span for="input-run-numbers" class="block text-xs py-2 font-small text-white">Give Run Numbers (>1)</span>

        <form @submit.prevent="addRun">
          <input v-model.number.lazy="newRunNumber" maxLength="9" type="number"
            oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"
            class="w-28 py-0 text-sm rounded-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            required>
          <button>
            <BaseIcon :path="mdiPlusThick" class="flex-none" w="w-6" :size="18"
              :class="[vSlot && vSlot.isExactActive ? asideMenuItemActiveStyle : '']" />
          </button>
        </form>
        <ul v-if="inputRuns.length > 0">
          <li v-for="run, index in inputRuns" :key="index" class="grid grid-cols-2 border border-slate-300 rounded-md">
            <span class="text-xs mb-0 w-24 focus:ring-blue-500 focus:border-blue-500 text-white ">
              <span class="text-xs">{{ index }}.</span> {{ run }}
            </span>
            <button @click="removeRun(run)">
              <BaseIcon :path="mdiMinus" class="flex-none" w="w-6" h="h-5" :size="18"
                :class="[vSlot && vSlot.isExactActive ? asideMenuItemActiveStyle : '']" />
            </button>
          </li>
        </ul>

      </div>
    </component>
  </li>
</template>
