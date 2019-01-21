<template>
  <div class="home">
    <h1><i class="fas fa-cog"></i> Control panel</h1>
    <div class="menu">
      <div class="item">
        <router-link class="link" to="/users">
          <div class="item-container">
            <div class="icon">
              <i class="fas fa-users"></i>
            </div>
            <div class="title">
              <h2>Users</h2>
            </div>
          </div>
        </router-link>
      </div>

      <div class="item">
        <router-link class="link" to="/bus_filters">
          <div class="item-container">
            <div class="icon">
              <i class="fas fa-filter"></i>
            </div>
            <div class="title">
              <h2>Bus filters</h2>
            </div>
          </div>
        </router-link>
      </div>

      <div class="item">
        <router-link class="link" to="/templates">
          <div class="item-container">
            <div class="icon">
              <i class="fas fa-envelope"></i>
            </div>
            <div class="title">
              <h2>Templates</h2>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home"
};
</script>

<style lang="scss" scoped>
.menu {
  display: grid;
  grid-template-columns: repeat(3, 150px);
  grid-template-rows: repeat(1, 150px);
  grid-gap: 30px 30px;
  margin-top: 2rem;
}
.item {
  width: 100%;
  height: 100%;
  border-radius: 7px;
  border: 3px solid $color-main;
}
.item-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  text-align: center;
  align-content: center;
  justify-content: center;
  &:hover {
    background-color: $color-main-light;
  }
}
.icon {
  font-size: 2.5rem;
}
.title {
  font-size: 1rem;
  & h2 {
    margin-top: 1rem;
    margin-bottom: 0;
  }
}
.link {
  color: black;
  text-decoration: none;
}
</style>
