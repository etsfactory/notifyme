<template>
  <div>
    <button class="button edit" @click="$emit('edit')">
      <i class="fas fa-edit"></i> Edit
    </button>
    <button class="button delete" @click="$emit('remove')">
      <i class="far fa-trash-alt"></i> Delete
    </button>
  </div>
</template>

<script>
export default {
  name: "ActionButtons"
};
</script>

<style lang="scss" scoped>
.button {
  border: none;
  margin: 0px auto;
  padding: 0.7rem 1.5rem;
  font-weight: bold;
  color: white;
  margin-bottom: 1rem;
  display: block;
  width: 300px;
  border-radius: 5px;
  cursor: pointer;
  & i {
    margin-right: 0.5rem;
  }
}
.edit {
  background-color: $color-main-dark;
}
.delete {
  background-color: #994c63;
}
</style>
