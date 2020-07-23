<template>
    <v-app>
        <app-navigation></app-navigation>
        <v-main>
            <router-view />
            <alert-notifier />
        </v-main>
        <v-footer></v-footer>
    </v-app>
</template>

<script>
import AppNavigation from "@/components/AppNavigation";
import AlertNotifier from "@/components/AlertNotifier";

export default {
    name: "App",
    components: {
        AppNavigation,
        AlertNotifier
    },
    watch: {
        $route(to, from) {
            document.title = "TextMacher | " + to.meta.title;
        }
    }
};
</script>
<style></style>
