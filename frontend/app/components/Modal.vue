<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/40 flex justify-center items-center p-4 z-50"
    @click.self="$emit('update:show', false)"
  >
    <div class="bg-white p-6 rounded-xl shadow-xl w-full max-w-2xl">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-bold">{{ title }}</h2>
        <button
          class="w-9 h-9 rounded-lg hover:bg-slate-100 transition flex items-center justify-center"
          @click="$emit('update:show', false)"
          type="button"
        >
          ✕
        </button>
      </div>
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue"

const props = defineProps({
  title: String,
  show: Boolean
})

const emit = defineEmits(["update:show"])

const onKeyDown = (e) => {
  if (e.key === "Escape" && props.show) emit("update:show", false)
}

onMounted(() => document.addEventListener("keydown", onKeyDown))
onUnmounted(() => document.removeEventListener("keydown", onKeyDown))
</script>