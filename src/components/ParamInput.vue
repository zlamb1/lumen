<template>
    <q-input v-if="param.type == 'number'" 
        :label="name" :model-value="value" :min="param?.min" :max="param?.max" @change="onValueChange" type="number" filled />
    <q-toggle v-else-if="param.type == 'bool'" :label="name" :model-value="value" @update:model-value="onValueChange" />
    <q-input
        v-else-if="param.type == 'color'"
        :label="name"
        :model-value="value"
        @change="onValueChange"
        filled
      >
        <template v-slot:append>
            <div :style="`width: 16px; height: 16px; border-radius: 50%; background: ${value};`" />
            <q-icon name="colorize" class="cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-color :model-value="value" @change="onValueChange" />
                </q-popup-proxy>
            </q-icon>
        </template>
    </q-input>
</template>

<script setup lang="ts">
import { useAnimationStore } from '../stores/animation';
import { computed } from 'vue';

const props = defineProps(['param'])
const param = computed(() => props.param);

const name = computed(() => param.value.name.charAt(0).toUpperCase() + param.value.name.slice(1));
const value = computed(() => param.value.value);

const animationStore = useAnimationStore();

async function onValueChange(value: boolean | number) {
    if (param.value.type == 'number') {
        if (param.value.min)
            value = Math.max(value as number, param.value.min);
        if (param.value.max)
            value = Math.min(value as number, param.value.max);
    }
    await animationStore.setParam(param.value.name, value);
}
</script>