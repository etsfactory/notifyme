<template>
  <label class="switch">
    <input type="checkbox" :checked="toggled" @click="toggle">
    <span class="slider round"></span>
  </label>
</template>

<script>
export default {
  name: "Toggler",
  props: {
    toggled: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    toggle() {
      this.$emit("click", !this.toggled);
    }
  }
};
</script>

<style lang="scss" scoped>
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 26px;
  margin: 0px auto;
}
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: transparent;
  transition: 0.4s;
  border: 2px solid #bdbdbd;
}

.slider:before {
  position: absolute;
  content: "";
  height: 14px;
  width: 14px;
  top: 2px;
  left: 3px;
  bottom: 4px;
  transition: 0.4s;
}

input:checked + .slider {
  border: 2px solid $color-main;
}

input:checked + .slider:before {
  border: 2px solid $color-main;
}

input:focus + .slider {
  box-shadow: 0 0 1px $color-secundary;
}

input:checked + .slider:before {
  transform: translateX(33px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
  border: 2px solid #bdbdbd;
}
</style>
