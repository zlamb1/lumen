import { defineStore, acceptHMRUpdate } from 'pinia';
import type { Animation } from '../model/animation'
import { ref } from 'vue';

const url = window.location.protocol + '//' + window.location.hostname + ':5000';

export const useAnimationStore = defineStore('animations', () => {
    const animation = ref<Animation | null>(null);
    const animations = ref<Animation[]>([]);

    async function getAnimation() {
        try {
            const res = await fetch(`${url}/animation`);
            animation.value = await res.json();
        } catch {
            animation.value = null;
        }
    }

    async function getAnimations() {
        try {
            const res = await fetch(`${url}/animations`);
            // TODO: validate server-side data
            animations.value = await res.json();
            return true;
        } catch {
            animations.value = [];
            return false;
        }
    }

    async function setAnimation(name: string) {
        try {
            const res = await fetch(`${url}/animation/${name}`, { method: 'POST' });
            animation.value = await res.json();
            return true;
        } catch {
            return false;
        }
    }

    async function setParam(name: string, value: string | number | boolean) {
        if (animation.value == null)
            return false;
        const param = animation.value.params.find(el => el.name == name);
        if (!param)
            return false;
        try {
            const params = new URLSearchParams();
            if (typeof value == 'string')
                params.append('value', value);
            else
                params.append('value', JSON.stringify(value));
            const res = await fetch(`${url}/animation/param/${name}`, {
                method: 'POST',
                body: params
            });
            const json = await res.json();
            if (param.type == 'color')
                param.value = json.value;
            else
                param.value = JSON.parse(json.value);
            return true;
        } catch (exc) {
            console.log('fail', exc);
            return false;
        }
    }

    void getAnimation();
    void getAnimations();

    return { animation, animations, getAnimation, getAnimations, setAnimation, setParam };
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useAnimationStore, import.meta.hot));
}
