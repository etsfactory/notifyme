<template>
  <transition name="bounce">
    <div class="http-error">{{error.statusText}} - {{error.status}}</div>
  </transition>
</template>

<script>
export default {
  name: "Error",
  props: {
    error: Error
  }
};
</script>

<style>
.http-error {
  padding: 1rem 1rem;
  background-color: #bb747e;
  color: white;
  border-radius: 7px;
  font-size: 1.2rem;
  margin-top: 2rem;
  font-weight: bold;
}
.bounce-enter-active {
  animation: bounce-in .1s ease-in-out;
}
.bounce-leave-active {
  animation: bounce-in .1s ease-in-out;
}
@keyframes bounce-in {
  0% {
    transform: translateX(-20px);
  }
  33% {
    transform: translateX(0px);
  }
  66% {
    transform: translateX(20px);
  }
  100% {
    transform: translateX(0px);
  }
}
</style>
