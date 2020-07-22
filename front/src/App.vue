<template>
    <v-app>
        <app-navigation></app-navigation>
        <v-main><home></home></v-main>
    </v-app>
</template>

<script>
import AppNavigation from "@/components/AppNavigation";
import Home from "@/components/Home";

export default {
    name: "App",
    components: {
        AppNavigation,
        Home
    }
};
</script>
<style></style>
