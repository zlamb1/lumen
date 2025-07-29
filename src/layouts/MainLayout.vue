<template>
  <q-layout view="hhh lpr FFF">
    <q-header elevated>
      <q-toolbar>
        <q-icon name="sym_o_lightbulb" color="yellow" size="sm" />
        <q-toolbar-title class="text-bold non-selectable">Lumen</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer class="row justify-center q-py-md">
      <q-btn color="secondary" :icon="animation && animation?.paused == false ? 'pause' : 'play_arrow'" size="md" round />
    </q-footer>
  </q-layout>
</template>

<script setup lang="ts">
import { useAnimationStore } from '../stores/animation';
import { computed } from 'vue';

const animationStore = useAnimationStore();
const animation = computed(() => animationStore.animation);
</script>