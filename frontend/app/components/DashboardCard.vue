<template>
  <div class="bg-white rounded-xl shadow p-5 flex flex-col">
    
    <span class="text-gray-500 text-sm">
      {{ title }}
    </span>

    <span class="text-2xl font-bold mt-2">
      {{ displayValue }}
    </span>

    <span class="text-sm mt-1" :class="color">
      {{ subtitle }}
    </span>

  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  title: String,
  value: [String, Number],
  subtitle: String,
  color: String,
  format: {
    type: String,
    default: "plain" // plain | currency
  }
})

const displayValue = computed(() => {
  const v = props.value ?? 0

  if (props.format === "currency") {
    const num = typeof v === "number" ? v : Number(v)
    const safe = Number.isFinite(num) ? num : 0
    return new Intl.NumberFormat("pt-PT", { style: "currency", currency: "EUR" }).format(safe)
  }

  return v
})

</script>