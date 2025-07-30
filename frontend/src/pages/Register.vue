<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <p>Current path: {{ route.path }}</p>
  <nav class="flex flex-col gap-2">
    <router-link to="/">Welcome</router-link>
    <router-link to="/login">Login</router-link>
    <router-link to="/register">Register</router-link>
    <router-link to="/forgot-password">Forgot Password</router-link>
    <router-link to="/catalog">Catalog</router-link>
  </nav>
</template>