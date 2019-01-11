<template>
  <div v-show="visible" class="modal" id="modal" :class="{hide: !visible}">
    <div class="bg" @click="close"></div>
    <div class="modal-inner">
      <a class="close" @click="close">X</a>
      <h2 class="title">{{ title }}</h2>
      <h3>{{ subtitle }}</h3>
      <div class="buttons-container">
        <button class="button accept" @click="accept">YES</button>
        <button class="button exit" @click="close">NO</button>
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
      default: 'Are you sure?',
    },
    subtitle: {
      default: 'This action can not be undone'
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
.bg {
  width: 100vw;
  min-height: 100vh;
  height: 100%;
  position: absolute;
  bottom: 0;
  right: 0;
  top: 0;
  background-color: rgba(26, 48, 54, 0.85);
  z-index: 1;
}
.modal {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  width: 100vw;
  min-height: 100vh;
  height: 100%;
  bottom: 0;
  right: 0;
  top: 0;
  z-index: 2;
  visibility: hidden;
  opacity: 0;
  overflow: hiden;
  transition: 0.4s ease-in-out;
  visibility: visible;
  opacity: 1;

  &-inner {
    position: relative;
    bottom: 0;
    right: 0;
    transform: rotate(0);
    display: flex;
    align-items: center;
    flex-direction: column;
    max-width: 800px;
    max-height: 600px;
    width: 28%;
    height: 30%;
    background-color: #fff;
    border-radius: 6px;
    transition: 0.64s ease-in-out;
    z-index: 3;
    padding: 4rem;
  }
}
.title {
  font-size: 3rem;
  font-weight: bold;
}
.close {
  position: absolute;
  right: 1rem;
  top: 1rem;
  width: 3rem;
  height: 3rem;
  font-size: 2rem;
  font-weight: 300;
  border-radius: 100%;
  z-index: 4;
  color: black;
  line-height: 3rem;
  text-align: center;
  cursor: pointer;
  text-decoration: none;
}
.hide {
  visibility: hidden !important;
  opacity: 0 !important;
}
.buttons-container {
  position: absolute;
  bottom: 0;
  left: 0;
  display: flex;
  width: 100%;
}
.button {
  width: 50%;
  padding: 1.4rem 0;
  border: none;
  cursor: pointer;
  font-weight: bold;
}
.accept {
  background: #fc7169;
  color: white;
  &:hover {
    background: #e7645d;
  }
}
.exit {
  background: #b6bece;
  color: white;
  &:hover {
    background: #a0aabe;
  }
}
</style>
