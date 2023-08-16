<script setup>
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import { useRootHistogramStore } from '../stores/RootHistogramStore';

let mobileMenu = ref(false)

</script>

<template>
  <!-- component -->
  <!-- Header -->
  <div class="sticky top-0 z-10">
    <div class="bg-gray-900">
      <nav class="
          container
          px-6
          py-8
          mx-auto
          md:flex md:justify-between md:items-center
          text-white
        ">
        <div class="flex items-center justify-between">
          <router-link to="/" class="
              text-xl
              font-bold
              text-white
              md:text-2xl
              hover:text-blue-400
            ">PPD GUI
          </router-link>
          <!-- Mobile menu button -->
          <div @click="mobileMenu = !mobileMenu" class="flex md:hidden">
            <button type="button" class="
                text-white
                hover:text-gray-400
                focus:outline-none focus:text-gray-400
              ">
              <svg viewBox="0 0 24 24" class="w-6 h-6 fill-current">
                <path fill-rule="evenodd"
                  d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z">
                </path>
              </svg>
            </button>
          </div>
        </div>


        <!-- Mobile Menu open: "block", Menu closed: "hidden" -->
        <ul :class="mobileMenu ? 'flex' : 'hidden'" class="
            flex-col
            mt-8
            space-y-4
            md:flex
            md:space-y-0
            md:flex-row
            md:items-center
            md:space-x-10
            md:mt-0
            
          ">
          <li class="text-sm font-bold text-white hover:text-blue-400">
            <RouterLink to="/">Home</RouterLink>
          </li>

          <li class="text-sm font-bold text-white hover:text-blue-400">
            <a href="#">Contact Us</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>