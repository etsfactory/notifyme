<template>
  <div v-show="visible" class="modal" id="modal" :class="{hide: !visible}">
    <div class="modal-bg" @click="close"></div>
    <div class="modal-inner">
      <a class="modal-close" @click="close">X</a>
      <h2 class="modal-title">{{ title }}</h2>
      <h3 class="modal-subtitle">{{ subtitle }}</h3>
      <div class="modal-buttons-container">
        <button class="modal-button modal-accept" @click="accept">YES</button>
        <button class="modal-button modal-exit" @click="close">NO</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConfirmModal",
  props: {
    visible: Boolean,
    title: {
      type: String,
      default: "Are you sure?"
    },
    subtitle: {
      type: String,
      default: "This action can not be undone"
    }
  },
  methods: {
    close() {
      this.$emit("update:visible", false);
    },
    accept() {
      this.$emit("accept");
    }
  }
};
</script>

<style lang="scss" scoped>

</style>
