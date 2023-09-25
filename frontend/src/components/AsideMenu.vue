<script setup>
import AsideMenuInputs from "@/components/AsideMenuInputs.vue";
import BaseIcon from "@/components/BaseIcon.vue";
import { useStyleStore } from "@/stores/style.js";
import { mdiClose, mdiHome, mdiTagSearchOutline } from "@mdi/js";

defineProps({
  isAsideMobileExpanded: Boolean,
  isAsideLgActive: Boolean,
});

const emit = defineEmits(["menu-click", "aside-lg-close-click"]);
const styleStore = useStyleStore();

const menuClick = (event, item) => {
  emit("menu-click", event, item);
};

const asideLgCloseClick = (event) => {
  emit("aside-lg-close-click", event);
};
</script>

<template>
  <aside id="aside" class="lg:py-2 lg:pl-2 w-60 fixed flex z-30 top-0 h-screen transition-position overflow-hidden"
    :class="[
      isAsideMobileExpanded ? 'left-0' : '-left-60 lg:left-0',
      { 'lg:hidden xl:flex': !isAsideLgActive },
    ]">
    <div :class="styleStore.asideStyle" class="lg:rounded-2xl flex-1 flex flex-col overflow-hidden dark:bg-slate-900">
      <div :class="styleStore.asideBrandStyle"
        class="flex flex-row h-14 items-center justify-between dark:bg-slate-900">
        <div class="text-center flex-1 lg:text-center lg:pl-6 xl:text-center xl:pl-0">
          <a href="/"> PPD
            <BaseIcon
              :path="mdiHome"
              class="flex-none"
              w="w-16"
              :size="18" /> Dashboard
          </a>
        </div>
        <button class=" lg:inline-block xl:hidden p-3" @click.prevent="asideLgCloseClick">
          <BaseIcon :path="mdiClose" />
        </button>
      </div>
      <div
        :class="styleStore.darkMode ? 'aside-scrollbars-[slate]' : styleStore.asideScrollbarsStyle"
        class="flex-1 overflow-y-auto overflow-x-hidden">
        <!-- ADDITIONAL ITEMS CAN BE ADDED HERE -->
        <!-- <ul>
        </ul> -->

        <AsideMenuInputs
          :icon="mdiTagSearchOutline"
          :item={} />
      </div>
    </div>
  </aside>
</template>
