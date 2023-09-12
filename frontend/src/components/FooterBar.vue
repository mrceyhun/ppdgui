<script setup>
import { containerMaxW } from "@/config.js";
import BaseLevel from "@/components/BaseLevel.vue";
import CernLogo from "./CernLogo.vue";

const year = new Date().getFullYear();
</script>

<template>
  <footer
    class="py-10 px-6"
    :class="containerMaxW">
    <BaseLevel>
      <div class="text-center md:text-left">
        <b>
          &copy;{{ year }},
          <a href="https://cern.ch/home" target="_blank">CERN</a>
          .
        </b>

        <slot />

      </div>
      <div class="md:py-2">
        <a href="https://cern.ch/home">
          <CernLogo class="w-auto h-8 md:h-6" />
        </a>
      </div>
    </BaseLevel>
  </footer>
</template>
