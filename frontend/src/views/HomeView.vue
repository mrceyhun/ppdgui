<script setup>
import AsideMenu from "@/components/AsideMenu.vue";
import FooterBar from "@/components/FooterBar.vue";
import NavBar from "@/components/NavBar.vue";
import PlotsLayout from "@/layouts/PlotsLayout.vue";
import menuNavBar from "@/menuNavBar.js";
import { useStyleStore } from "@/stores/style.js";
import { ref } from "vue";
import { useRouter } from "vue-router";

const layoutAsidePadding = "xl:pl-60";
const styleStore = useStyleStore();
const router = useRouter();
const isAsideMobileExpanded = ref(false);
const isAsideLgActive = ref(false);

router.beforeEach(() => {
  isAsideMobileExpanded.value = false;
  isAsideLgActive.value = false;
});

const menuClick = (event, item) => {
  if (item.isToggleLightDark) {
    styleStore.setDarkMode();
  }
};
</script>

<template>
  <div :class="{ dark: styleStore.darkMode, 'overflow-hidden lg:overflow-visible': isAsideMobileExpanded, }">
    <div :class="[layoutAsidePadding, { 'ml-60 lg:ml-0': isAsideMobileExpanded }]"
      class="pt-14 min-h-screen w-screen transition-position lg:w-auto bg-gray-50 dark:bg-slate-800 dark:text-slate-100">

      <NavBar :menu="menuNavBar" :class="[layoutAsidePadding, { 'ml-60 lg:ml-0': isAsideMobileExpanded },]"
        @menu-click="menuClick" />

      <AsideMenu
        :is-aside-mobile-expanded="isAsideMobileExpanded"
        :is-aside-lg-active="isAsideLgActive"
        @menu-click="menuClick"
        @aside-lg-close-click="isAsideLgActive = false" />

      <!-- Plots -->
      <PlotsLayout />

      <FooterBar>
        Get more with
      </FooterBar>
    </div>
  </div>
</template>
