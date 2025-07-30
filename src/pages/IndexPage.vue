<template>
  <q-page class="row justify-center items-center">
    <div class="row justify-center q-gutter-sm">
      <q-card class="col-5 column justify-center q-pa-sm">
        <p class="text-h6 text-bold non-selectable">Animations</p>
        <q-separator />
        <div class="col row q-col-gutter-sm q-pa-md">
          <template v-for="n in pageSize" :key="page + '-' + n">
            <div class="col-3 text-bold">
              <q-btn v-if="animations[getIndex(n)]" :color="getColor(animations[getIndex(n)]!.name)" class="full-width" 
                icon="question_mark" :label="animations[getIndex(n)]!.name" 
                @click="() => setAnimation(animations[getIndex(n)]!.name)" rounded no-wrap />
              <q-btn v-else text-color="yellow-7" icon="lightbulb" class="full-width" rounded disable />
            </div>
          </template>
        </div>
        <div class="row justify-end">
          <q-pagination v-model="page" :max="maxPage" direction-links />
        </div>
      </q-card>
      <q-card class="col-5 column q-pa-sm">
        <p class="text-h6 text-bold non-selectable">Animation State</p>
        <q-separator />
        <div class="column q-col-gutter-y-md q-pa-md">
          <template v-for="param in animation?.params" :key="param.name">
            <ParamInput :param="param" />
          </template>
        </div>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
  import ParamInput from '../components/ParamInput.vue';
  import { useAnimationStore } from '../stores/animation';
  import { computed, ref } from 'vue';

  const animationStore = useAnimationStore();
  const animation = computed(() => animationStore.animation);
  const animations = computed(() => animationStore.animations);

  const getIndex = (n: number) => (n - 1) + (page.value - 1) * pageSize;

  const pageSize = 16;
  const page = ref<number>(1);
  const maxPage = computed(() => Math.ceil(animations.value.length / pageSize));

  function getColor(name: string) {
    return name == animation.value?.name ? 'accent' : 'secondary';
  }

  async function setAnimation(name: string) {
    await animationStore.setAnimation(name);
  }
</script>
