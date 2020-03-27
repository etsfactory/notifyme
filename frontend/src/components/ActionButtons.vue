<template>
  <div class="actions">
    <button class="button edit" @click="$emit('edit')">
      <img svg-inline class="icon" src="../assets/icons/pencil.svg">
    </button>
    <button class="button delete" @click="$emit('remove')">
      <img svg-inline class="icon" src="../assets/icons/trash.svg">
    </button>
  </div>
</template>

<script>
export default {
  name: "ActionButtons"
};
</script>

<style lang="scss" scoped>
.actions {
  display: flex;
  width: 100%;
  align-items: center;
  margin-top: 1rem;
}
.button {
  border: none;
  font-weight: bold;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.1rem;
}
.edit {
  background-color: rgba(0, 145, 255, 0.2);
  color: #0091ff;
  &:hover {
    background-color: rgba(0, 145, 255, 0.5);
  }
}
.delete {
  margin-left: 0.7rem;
  background-color: rgba(235, 87, 87, 0.2);
  color: #eb5757;
  &:hover {
    background-color: rgba(235, 87, 87, 0.5);
  }
}
</style>
