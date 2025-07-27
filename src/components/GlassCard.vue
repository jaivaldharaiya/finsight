<template>
  <div 
    :class="cardClasses" 
    @click="handleClick"
    :style="{ cursor: onClick ? 'pointer' : 'default' }"
    class="transition-transform duration-300"
    :data-hoverable="hoverable"
  >
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps, defineEmits } from 'vue';

const props = defineProps({
  className: {
    type: String,
    default: ''
  },
  hoverable: {
    type: Boolean,
    default: false
  },
  neonBorder: {
    type: Boolean,
    default: false
  },
  onClick: {
    type: Function,
    default: null
  }
});

const emit = defineEmits(['click']);

const cardClasses = computed(() => {
  return [
    'glass-card',
    props.className,
    { 'neon-border': props.neonBorder }
  ];
});

const handleClick = (event: MouseEvent) => {
  if (props.onClick) {
    props.onClick();
  }
  emit('click', event);
};
</script>

<style scoped>
/* Apply hover effects only when the hoverable prop is true */
div[data-hoverable="true"]:hover {
  transform: scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}
</style>