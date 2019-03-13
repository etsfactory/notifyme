<template>
  <div class="actions">
    <button class="button edit" @click="$emit('edit')"><i class="fas fa-edit"></i>
    </button>
    <button class="button delete" @click="$emit('remove')"><i class="far fa-trash-alt"></i>
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
  margin-top: 2rem;
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
}
.delete {
  margin-left: 0.7rem;
  background-color: rgba(235, 87, 87, 0.2);
  color: #eb5757;
}
</style>
