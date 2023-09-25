<script setup>
import { getButtonColor } from "@/colors.js";
import BaseIcon from "@/components/BaseIcon.vue";
import { useStyleStore } from "@/stores/style.js";
import { mdiMinus, mdiPlus } from "@mdi/js";
import { computed, ref } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["menu-click"]);
const styleStore = useStyleStore();

const hasColor = computed(() => props.item && props.item.color);
const asideMenuItemActiveStyle = computed(() =>
  hasColor.value ? "" : styleStore.asideMenuItemActiveStyle
);
const isDropdownActive = ref(false);
const componentClass = computed(() => [
  "py-3",
  hasColor.value
    ? getButtonColor(props.item.color, false, true)
    : `${styleStore.asideMenuItemStyle} dark:text-slate-300 dark:hover:text-white`,
]);
const hasDropdown = computed(() => !!props.item.menu);
const menuClick = (event) => {
  emit("menu-click", event, props.item);

  if (hasDropdown.value) {
    isDropdownActive.value = !isDropdownActive.value;
  }
};
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

      <BaseIcon
        v-if="item.icon"
        :path="item.icon"
        class="flex-none"
        :class="[vSlot && vSlot.isExactActive ? asideMenuItemActiveStyle : '']"
        w="w-16"
        :size="14" />

      <span
        class="grow text-ellipsis line-clamp-1"
        :class="[
          { 'pr-12': !hasDropdown },
          vSlot && vSlot.isExactActive ? asideMenuItemActiveStyle : '',
        ]">{{ item.label }}
      </span>

      <BaseIcon
        v-if="hasDropdown"
        :path="isDropdownActive ? mdiMinus : mdiPlus"
        class="flex-none"
        :class="[vSlot && vSlot.isExactActive ? asideMenuItemActiveStyle : '']"
        w="w-12" />
    </component>

  </li>
</template>
