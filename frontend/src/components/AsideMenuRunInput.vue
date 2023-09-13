<script setup>
import { computed, ref } from "vue";
import { useMainRunStore } from "@/stores/mainRun.js";
import { useStyleStore } from "@/stores/style.js";
import { getButtonColor } from "@/colors.js";
import BaseIcon from "@/components/BaseIcon.vue";


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

const mainRunStore = useMainRunStore();
const styleStore = useStyleStore();

const emit = defineEmits(["menu-click"]);
const hasColor = computed(() => props.item && props.item.color);
const componentClass = computed(() => [
  props.isDropdownList ? "py-3 px-6 text-sm" : "py-3",
  hasColor.value
    ? getButtonColor(props.item.color, false, true)
    : `${styleStore.asideMenuItemStyle} dark:text-slate-300 dark:hover:text-white`,
]);
const menuClick = (event) => {
  emit("menu-click", event, props.item);
};

const inputRun = ref(mainRunStore.inputRunNumber)

/* Initial get of histograms */
mainRunStore.updateRunNumber(2023, parseInt(inputRun.value));

/* On input hit enter */
async function submit() {
  await mainRunStore.updateRunNumber(2023, parseInt(inputRun.value));
}

</script>

<template>
  <li>
    <component
      :is="item.to ? RouterLink : 'a'"
      v-slot="vSlot"
      :to="item.to ?? null"
      :href="item.href ?? null"
      :target="item.target ?? null"
      class="flex cursor-pointer"
      :class="componentClass"
      @click="menuClick">

      <BaseIcon v-if="icon" :path="icon" class="flex-none" w="w-16" :size="18"
        :class="[vSlot && vSlot.isExactActive ? asideMenuItemActiveStyle : '']" />

      <div class="grow text-ellipsis line-clamp-1"
        :class="[vSlot && vSlot.isExactActive ? asideMenuItemActiveStyle : '',]">

        <span for="input-run-number" class="block text-xs font-medium text-white">Search Run</span>

        <input
          @keyup.enter="submit" id="input-run-number"
          v-model.lazy.number="inputRun" maxLength="9" type="number"
          oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"
          class="block w-full px-2 py-0 text-sm rounded-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          required>

      </div>
    </component>
  </li>
</template>
